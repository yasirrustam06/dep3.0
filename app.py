# app.py
from flask import Flask, request, render_template, jsonify
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

# Load the pre-trained face detection model from OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-frame', methods=['POST'])
def process_frame():
    data = request.get_json()
    frame_data = data.get('frame')

    # Convert base64-encoded frame to NumPy array
    decoded_frame = base64.b64decode(frame_data.split(',')[1])
    np_frame = np.frombuffer(decoded_frame, dtype=np.uint8)
    frame = cv2.imdecode(np_frame, cv2.IMREAD_COLOR)

    # Convert the frame to grayscale for face detection
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform face detection
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Convert the processed frame back to base64 for sending to the frontend
    _, encoded_frame = cv2.imencode('.jpg', frame)
    base64_frame = base64.b64encode(encoded_frame.tobytes()).decode('utf-8')

    return jsonify({'processed_frame': base64_frame})

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)
