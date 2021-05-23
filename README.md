# Image Objects Identifier Built with Django and GraphQL using Google Vision API

[![Open in Browser][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://django-graphql-imageid.ew.r.appspot.com

https://django-graphql-imageid.ew.r.appspot.com/graphql/#operationName=getImages&query=query%20getImages%20%7B%0A%20images%20%7B%0A%20%20id%0A%20image%0A%20%09url%0A%20%20imgObjects%0A%20%7D%0A%7D%0A%0A

Object identifier on images using [Django](https://www.djangoproject.com/) 
and [GraphQL](https://graphql.org/) as the API


## How to Use

GET IMAGES

Make get request to with [https://django-graphql-imageid.ew.r.appspot.com/graphql/]https://django-graphql-imageid.ew.r.appspot.com/graphql/
use query:

```json
getImages&query=query%20getImages%20%7B%0A%20images%20%7B%0A%20%20id%0A%20image%0A%20%09url%0A%20%20imgObjects%0A%20%7D%0A%7D%0A%0A
```

UPLOAD IMAGE

Post request with headers:
 - Content-Type: application/graphql
 - Content-Transfer-Encoding: multipart/form-data

 Post Body with fields:
  - image: <your image file>
  - query: ```mutation createImage {
    createImage(
        image: ""
    ) {
        ok
        id 
    }
}```


DELETE IMAGE

Post request with query field:
- query: ```mutation deleteImage {
    deleteImage(
        id: "14"
) {
        ok
    }
}```