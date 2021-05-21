from django.db import models
from google.cloud import vision
from django.db.models.signals import post_save
from uuid import uuid4

# function for image upload
def image_upload(instance, filename):
    basename, file_extension = filename.split(".")
    return f"IMGIDPROJ-{uuid4().hex}.{file_extension}"


class Image(models.Model):
    uuid = models.CharField(max_length=120)
    image = models.ImageField(upload_to=image_upload)
    labels = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.uuid
    

    class Meta:
        ordering = ('uuid',)

def image_label_post_save_receiver(sender, instance, created, *args, **kwargs):
    client = vision.ImageAnnotatorClient()

    with io.open(instance.image, 'rb') as image_file:
        content = image_file.read()
    
    image = vision.Image(content=content)

    response = client.label_detection(image=image)

    img_labels = ""
    for label in response.label_annotations:
        img_labels.append('%s - (%.2f%%)\n' % (label.description, label.score*100))
    
    instance.labels = img_labels
    instance.save()

post_save.connect(image_label_post_save_receiver, sender=Image)
