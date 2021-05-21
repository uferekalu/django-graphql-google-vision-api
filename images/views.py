from django.shortcuts import render
from google.cloud import vision
# Create your views here.

def test_api(request):
    # image_url = 'gs://cloud-samples-data/vision/using_curl/shanghai.jpg'
    image_url = 'https://raw.githubusercontent.com/googleapis/python-vision/master/samples/snippets/quickstart/resources/wakeupcat.jpg'
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = image_url

    response = client.label_detection(image=image)

    print('Labels (and confidence score):')
    print('=' * 30)
    for label in response.label_annotations:
        print(label.description, '(%.2f%%)' % (label.score*100.))

    img_labels = ""
    for label in response.label_annotations:
        img_labels += ('%s - (%.2f%%)\n' % (label.description, label.score*100))

    context = {
        "image_labels": img_labels
    }
    return render(request, "index.html", context)

def index(request):
    context = {
    }
    return render(request, "index.html", context)

