from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64
from reconhecer_letra import prever_letra
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({'error': 'Nenhuma imagem enviada'}), 400

    try:
        # Decodificar a imagem base64
        img_data = base64.b64decode(data['image'].split(',')[1])
        np_arr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        letra = prever_letra(frame)
        return jsonify({'letra': letra})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Porta padrão para rodar localmente
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
