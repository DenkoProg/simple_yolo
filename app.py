from flask import Flask, request, jsonify
from auth import auth
import base64
import cv2
import numpy as np
from ultralytics import YOLO

app = Flask(__name__)

model = YOLO('yolov9m.pt')


@app.route('/tag-image', methods=['POST'])
@auth.login_required
def tag_image():
    data = request.get_json()

    if not data or 'Image' not in data:
        return jsonify({'error': 'No image data provided'}), 400

    try:
        image_data = base64.b64decode(data['Image'])
        np_arr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({'error': 'Invalid image data'}), 400

        results = model(img)
        tags = []

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = float(box.conf.cpu().numpy())
                cls = int(box.cls.cpu().numpy())
                label = model.names[cls]

                cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(
                    img,
                    f'{label} {conf:.2f}',
                    (int(x1), int(y1) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 255, 0),
                    2
                )

                tag = {
                    'label': label,
                    'probability': conf,
                    'bounding_box': {
                        'x_min': int(x1),
                        'y_min': int(y1),
                        'x_max': int(x2),
                        'y_max': int(y2)
                    }
                }
                tags.append(tag)

        _, buffer = cv2.imencode('.jpg', img)
        output_base64 = base64.b64encode(buffer).decode('utf-8')

        return jsonify({
            'OutputBase64': output_base64,
            'Tags': tags
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
