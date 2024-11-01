## Image Tagging REST API with YOLOv9

This project provides a REST API that accepts base64-encoded images, detects objects in the image using YOLOv9, and returns an annotated image and detection tags. It includes basic authentication for secure access.

### Features
- Accepts images in base64 format and processes them with YOLOv9.
- Returns annotated images with bounding boxes, labels, and probabilities.
- Basic authentication is implemented to restrict access.

### Project Structure
```plaintext
.
├── app.py               # Main Flask application
├── auth.py              # Basic authentication setup
├── requirements.txt     # Dependencies list
├── README.md            # Project documentation
└── yolov9.pt            # YOLOv9 model file (download separately)
```

### Requirements
- Python 3.x
- Required packages listed in `requirements.txt`

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download YOLOv9 model file**:
   - Place `yolov9.pt` in the project directory.
   - If YOLOv9 is not available, use YOLOv8 and modify code references to match.

### Running the App
Start the Flask server by running:
```bash
python app.py
```

The app will be available at `http://127.0.0.1:5000`.

### Using the API

1. **Endpoint**: `POST /tag-image`
2. **Authentication**:
   - **Username**: `admin`
   - **Password**: `secret`
3. **Request Format**:
   - JSON payload with a `Image` field containing the base64-encoded image.
   
   Example:
   ```json
   {
     "Image": "your_base64_encoded_image_here"
   }
   ```

4. **Response**:
   - JSON response with:
     - `OutputBase64`: base64-encoded annotated image.
     - `Tags`: Array of detected objects, each with `label`, `probability`, and `bounding_box` coordinates.

### Testing the API

#### Using Postman
1. Create a `POST` request to `http://127.0.0.1:5000/tag-image`.
2. Set up Basic Auth with `admin` / `secret`.
3. Set `Content-Type` to `application/json`.
4. Paste your base64-encoded image in the `Image` field of the JSON body.
5. Send the request and verify the response format and annotations.

#### Using CURL
```bash
curl -X POST http://127.0.0.1:5000/tag-image \
-u admin:secret \
-H "Content-Type: application/json" \
-d '{"Image": "your_base64_encoded_image_here"}'
```

### Troubleshooting
- Ensure all dependencies are installed, and the YOLO model file is accessible.
- If using a different YOLO model, adjust model loading code accordingly.
