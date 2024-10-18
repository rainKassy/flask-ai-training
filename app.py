from flask import Flask, render_template, jsonify, request, Response
import cv2
import time
import threading
import tensorflow as tf
from tensorflow.keras import layers, models

app = Flask(__name__)

# Переменные для управления тренировкой и статусом
training_status = "Waiting"
stop_training = False

# Главная страница с интерфейсом
@app.route('/')
def index():
    return render_template('index.html')

# API для запуска тренировки модели
@app.route('/train', methods=['POST'])
def train_model():
    global training_status, stop_training
    # Получаем параметры из запроса
    epochs = request.json.get('epochs', 10)
    batch_size = request.json.get('batch_size', 32)

    training_status = "Training started"
    stop_training = False

    def train():
        global training_status

        # Загрузка данных MNIST
        (train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()
        train_images, test_images = train_images / 255.0, test_images / 255.0

        # Создание модели
        model = models.Sequential([
            layers.Flatten(input_shape=(28, 28)),
            layers.Dense(128, activation='relu'),
            layers.Dense(10)
        ])

        model.compile(optimizer='adam',
                      loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                      metrics=['accuracy'])

        # Логирование начала тренировки
        with open('train_log.txt', 'a') as f:
            f.write(f"Training started with {epochs} epochs and {batch_size} batch size\n")

        # Тренировка модели с параметрами
        for epoch in range(epochs):
            if stop_training:
                training_status = "Training stopped"
                with open('train_log.txt', 'a') as f:
                    f.write("Training was stopped by user\n")
                break

            training_status = f"Training in progress: {int((epoch / epochs) * 100)}%"
            model.fit(train_images, train_labels, epochs=1, batch_size=batch_size, verbose=0)

        if not stop_training:
            training_status = "Training completed"
            model.save('trained_model.h5')
            with open('train_log.txt', 'a') as f:
                f.write(f"Training completed successfully\n")

    thread = threading.Thread(target=train)
    thread.start()

    return jsonify({"status": "Training started"})

# API для остановки тренировки
@app.route('/stop', methods=['POST'])
def stop_training_route():
    global stop_training
    stop_training = True
    return jsonify({"status": "Stopping training..."})

# API для получения статуса тренировки
@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": training_status})

# Видеопоток с камеры Raspberry Pi
@app.route('/video_feed')
def video_feed():
    def generate():
        cap = cv2.VideoCapture(0)  # Камера Raspberry Pi
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        cap.release()

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
