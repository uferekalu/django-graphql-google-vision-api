from django.db import models
from google.cloud import vision
from django.db.models.signals import post_save
from uuid import uuid4

import io
import os

# function for image upload
def image_upload(instance, filename):
    file_extension = filename.split(".")[-1]
    return f"IMGIDPROJ-{uuid4().hex}.{file_extension}"


class Image(models.Model):
    image = models.ImageField(upload_to=image_upload)
    img_objects = models.CharField(max_length=1000, null=True, blank=True)
    url = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.id
    
    class Meta:
        ordering = ('id',)


def image_url_post_save_receiver(sender, instance, created, *args, **kwargs):
    if created:
        instance.url = instance.image.url

        # Google Vision API
        client = vision.ImageAnnotatorClient()
        image = vision.Image()
        image.source.image_uri = instance.image.url

        objects = client.object_localization(image=image).localized_object_annotations
        img_objects = ""
        for object_ in objects:
            img_objects += ('%s (%.2f%%),' % (object_.name, object_.score*100))
        
        instance.img_objects = img_objects

        instance.save()

post_save.connect(image_url_post_save_receiver, sender=Image)