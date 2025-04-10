from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import logging
import tempfile
import os
from PIL import Image
import pytesseract

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure CORS properly - allow all origins
CORS(app, resources={r"/*": {"origins": "*"}}, 
     supports_credentials=True,
     methods=["GET", "POST", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"])

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "online",
        "message": "Image OCR API is running",
        "usage": "Send a POST request to /extract-text with a base64-encoded image",
        "supported_formats": ["JPG", "JPEG", "PNG", "BMP", "TIFF"],
        "version": "1.0.0"
    })

@app.route('/extract-text', methods=['POST', 'OPTIONS'])
def extract_text():
    # Handle preflight OPTIONS request for CORS
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        # Check if request has JSON data
        if not request.is_json:
            logger.error("Request is not JSON")
            return jsonify({"error": "Request must be JSON with a base64-encoded image"}), 400
        
        # Get base64 encoded image from request
        image_base64 = request.json.get('image')
        if not image_base64:
            logger.error("No image data found in request")
            return jsonify({"error": "No image data found in request"}), 400
        
        # Get the language for OCR (default to English)
        lang = request.json.get('lang', 'eng')
        
        logger.info(f"Received image OCR request. Processing...")
        
        try:
            # Decode the base64 string
            image_bytes = base64.b64decode(image_base64)
        except Exception as e:
            logger.error(f"Failed to decode base64: {e}")
            return jsonify({"error": "Invalid base64 encoding"}), 400
        
        # Process the image with OCR
        try:
            # Save image to temporary file
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_img:
                temp_img.write(image_bytes)
                temp_path = temp_img.name
            
            try:
                # Open the image and extract text
                image = Image.open(temp_path)
                
                # Add preprocessing for better OCR results
                # Convert to grayscale
                if image.mode != 'L':
                    image = image.convert('L')
                
                # Apply thresholding for cleaner text
                # Experiment with these values for best results
                # threshold_value = 150
                # image = image.point(lambda p: p > threshold_value and 255)
                
                # Use pytesseract to extract text
                text = pytesseract.image_to_string(image, lang=lang)
                
                if not text.strip():
                    logger.warning(f"No text extracted from image with OCR")
                    return jsonify({
                        "text": "",
                        "warning": "No text could be extracted from the image",
                    })
                
                logger.info(f"Successfully extracted {len(text)} characters from image")
                
                return jsonify({
                    "text": text,
                    "characters": len(text)
                })
            finally:
                # Clean up temp file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    
        except Exception as e:
            logger.error(f"Error processing image with OCR: {e}")
            return jsonify({"error": f"Failed to extract text from image: {str(e)}"}), 500
        
    except Exception as e:
        logger.error(f"OCR extraction error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False) 