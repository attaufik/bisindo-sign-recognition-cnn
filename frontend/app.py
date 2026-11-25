import base64
import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

app = Flask(__name__)

model = load_model('model_bisindo_cnn.h5')

class_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict_snapshot', methods=['POST'])
def predict_snapshot():
    try:
        data = request.json['image']
        encoded_data = data.split(',')[1]
        
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Gambar dari frontend sudah HANYA berisi kotak hijau, langsung resize
        # 224x224 sesuai dengan model CNN Transfer Learning (MobileNetV2)
        img_resized = cv2.resize(img, (224, 224))
        img_float = img_resized.astype(np.float32)
        img_preprocessed = preprocess_input(img_float)
        img_input = np.expand_dims(img_preprocessed, axis=0)

        prediksi = model.predict(img_input, verbose=0)
        index_kelas = np.argmax(prediksi)
        akurasi = np.max(prediksi) * 100

        return jsonify({
            'huruf': class_names[index_kelas],
            'akurasi': f"{akurasi:.2f}"
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)