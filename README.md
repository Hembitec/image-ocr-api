# Image OCR API

A specialized API for extracting text from images using OCR (Optical Character Recognition).

## Features

- Extract text from images using Tesseract OCR
- Optimized for text extraction with image preprocessing
- CORS properly configured for cross-origin requests
- Supports multiple image formats (JPG, PNG, BMP, TIFF)

## Deployment to Render

1. Create a new Web Service on Render
2. Connect to your repository
3. Configure the service:
   - **Name**: image-ocr-api
   - **Environment**: Docker
   - **Root Directory**: image-ocr-api (if in a subdirectory)
   - **Region**: Choose closest to your users
   - **Plan**: Free (or higher tier for better performance)

## API Usage

### Extract Text from Image

**Endpoint**: `POST /extract-text`

**Request Body**:
```json
{
  "image": "base64EncodedImageContentHere",
  "lang": "eng"
}
```

**Response**:
```json
{
  "text": "Extracted text content from the image",
  "characters": 1234
}
```

**Error Response**:
```json
{
  "error": "Error message describing what went wrong"
}
```

## Local Development

1. Build the Docker image:
```bash
docker build -t image-ocr-api .
```

2. Run the container:
```bash
docker run -p 10000:10000 image-ocr-api
```

3. The API will be available at `http://localhost:10000`

## Testing

Test the API with curl:

```bash
curl -X POST http://localhost:10000/extract-text \
  -H "Content-Type: application/json" \
  -d '{"image":"base64EncodedImageContentHere"}'
``` 