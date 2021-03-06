import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from .models import Image
from graphene_file_upload.scalars import Upload
from google.cloud import vision

import io

class ImageType(DjangoObjectType):
    class Meta:
        model = Image

class Query(ObjectType):
    image = graphene.Field(ImageType, id=graphene.Int())
    images = graphene.List(ImageType)

    def resolve_image(self, info, **kwargs):
        id = kwargs.get('id')

        # Google Vision API
        client = vision.ImageAnnotatorClient()

        if id is not None:
            this_image = Image.objects.get(pk=id)
            if this_image.url == None:
                this_image.url = this_image.image.url

            if this_image.img_objects == None or len(this_image.img_objects) == 0:
                image = vision.Image()
                image.source.image_uri = this_image.image.url

                objects = client.object_localization(image=image).localized_object_annotations
                img_objects = ""
                for object_ in objects:
                    img_objects += ('%s (%.2f%%),' % (object_.name, object_.score*100))
                
                this_image.img_objects = img_objects
            return this_image
        return None
    
    def resolve_images(self, info, **kwargs):
        # Google Vision API
        client = vision.ImageAnnotatorClient()
        images = Image.objects.all()
        for this_image in images:
            if this_image.url == None:
                this_image.url = this_image.image.url

            if this_image.img_objects == None or len(this_image.img_objects) == 0:
                image = vision.Image()
                image.source.image_uri = this_image.image.url

                objects = client.object_localization(image=image).localized_object_annotations
                img_objects = ""
                for object_ in objects:
                    img_objects += ('%s (%.2f%%),' % (object_.name, object_.score*100))

                this_image.img_objects = img_objects
        return images
    
# Create Input Object Types
class ImageInput(graphene.InputObjectType):
    id = graphene.ID()
    labels = graphene.String()
    image = Upload()


class UploadImage(graphene.Mutation):
    image = Upload()
    ok = graphene.Boolean()
    id = graphene.ID()

    class Arguments:
        image = Upload()

    def mutate(self, info, image):
        if info.context.FILES and info.context.method == 'POST':
            the_file = info.context.FILES['image']
            """Detects faces in an image."""
            client = vision.ImageAnnotatorClient()

            image = vision.Image(content=the_file.read())
            response = client.face_detection(image=image)
            faces = response.face_annotations

            if len(faces) == 0:
                # No Face detected, Ask to retry
                ok = False
                raise Exception(
                    'No Face Detected. Upload Another Image: ')
                return
            # Face detected, Proceed to save Image
            ok = True
            image_instance = Image.objects.create(image=the_file)
            return UploadImage(ok=ok, id=image_instance.id)


class DeleteImage(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    def mutate(cls, info, **kwargs):
        image_instance = Image.objects.get(pk=kwargs["id"])
        image_instance.delete()
        return DeleteImage(ok=True)


class ImageMutation(graphene.ObjectType):
    create_image = UploadImage.Field()
    delete_image = DeleteImage.Field()

schema = graphene.Schema(query=Query, mutation=ImageMutation, types=[Upload])