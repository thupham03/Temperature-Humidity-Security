import paho.mqtt.client as mqtt
from pymongo import MongoClient
import json

# Kết nối tới MongoDB bằng URI của bạn
client_db = MongoClient(
    "mongodb+srv://admin:Ua3rWeU0S3SUd214@temhum.ve2zq.mongodb.net/?retryWrites=true&w=majority&appName=temhum")
db = client_db['dht11']
collection = db['sensor']


# Hàm xử lý khi nhận được tin nhắn từ MQTT
def on_message(client, userdata, message):
    print(f"Received message: {message.payload.decode()}")
    data = json.loads(message.payload.decode())

    temperature = data['temperature']
    humidity = data['humidity']

    # Lưu dữ liệu vào MongoDB
    collection.insert_one({
        'temperature': temperature,
        'humidity': humidity
    })
    print("Data stored in MongoDB")


# Thiết lập kết nối MQTT
mqtt_client = mqtt.Client("python_mqtt_client")
mqtt_client.connect("broker.emqx.io", 1883, 60)
mqtt_client.on_message = on_message
mqtt_client.subscribe("sensor/temperature_humidity")
mqtt_client.loop_forever()
