import json
from pymongo import MongoClient
from datetime import datetime
import paho.mqtt.client as mqtt

# Kết nối đến MongoDB
client_db = MongoClient(
    "mongodb+srv://admin:Ua3rWeU0S3SUd214@temhum.ve2zq.mongodb.net/?retryWrites=true&w=majority&appName=temhum"
)
db = client_db['dht11']
collection = db['sensor']

def on_message(client, userdata, message):
    print(f"Received message: {message.payload.decode()}")

    try:
        data = json.loads(message.payload.decode())

        temperature = data.get('temperature')
        humidity = data.get('humidity')

        if temperature is not None and humidity is not None:
            timestamp = datetime.now()
            collection.insert_one({
                'temperature': temperature,
                'humidity': humidity,
                'timestamp': timestamp
            })
            print("Data stored in MongoDB")
        else:
            print("Invalid data format")
    except json.JSONDecodeError:
        print("Error decoding JSON")

mqtt_client = mqtt.Client("python_mqtt_client")
mqtt_client.connect("broker.emqx.io", 1883, 60)
mqtt_client.on_message = on_message
mqtt_client.subscribe("sensor/temperature_humidity")
mqtt_client.loop_forever()
