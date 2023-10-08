# Penguin-classification API

## Overview

This API is for classifying penguin images.

## Endpoints

| Endpoint   | Method | Description       |
| ---------- | ------ | ----------------- |
| /          | GET    | Health check      |
| /classify/ | POST   | Classify an image |

## Parameters

| Endpoint   | Parameter | Description           |
| ---------- | --------- | --------------------- |
| /          | -         | -                     |
| /classify/ | file      | The image to classify |

## Responses

| Endpoint   | Response                                              | Description           |
| ---------- | ----------------------------------------------------- | --------------------- |
| /          | {"message": "Welcome to Penguin-classification API!"} | Health check          |
| /classify/ | {"id": pred, "name": dst}                             | Classification result |

## Health check

A `GET` request to the `/` endpoint will return the following JSON:

```json
{
  "message": "Welcome to Penguin-classification API!"
}
```

## Classify an image

A `POST` request to the `/classify/` endpoint with the image to classify in the `file` parameter will return the following JSON:

```json
{
  "id": pred,
  "name": dst
}
```

`pred` is the ID of the classified penguin species. `name` is the name of the classified penguin species.

## Params

The `file` parameter specifies the image to classify. The image format must be JPEG or PNG.

## Errors

In case of an error, the following JSON will be returned:

```json
{
    "error": str(e)
}
```
