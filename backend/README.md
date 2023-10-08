# Penguin Classification API

![api-penguin.jpeg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3292052/57c5c334-d909-e34b-b66f-26f79317fdd0.jpeg)

## Overview

This API is a penguin classification API built with FastAPI.

### Features

- Health check
- Image classification

### Health check

A `GET` request to the `/` endpoint will return the following JSON:

```json
{
  "message": "Welcome to Penguin-classification API!"
}
```

### Image classification

A `POST` request to the `/classify/` endpoint with the image to classify in the `file` parameter will return the following JSON:

```json
{
  "id": pred,
  "name": dst
}
```

`pred` is the ID of the classified penguin species. `name` is the name of the classified penguin species.

### Development environment

- In development, the API uses efficientnet_v2_s for classification.
- The API specification can be viewed in Swagger UI.
- Run `python3 main.py` to start the API.
- Swagger UI will be launched at `/docs`.

### Production environment

- In production, the API uses a fine-tuned mobilenet_v3_small model for classification.

## License

This API is licensed under the MIT License.
