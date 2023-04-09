import random
import threading
import time
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['bancoiot']
teste = db['sensores']

def simula_temperatura():
    while True:
        temperatura = random.randint(30, 40)  #temperatura aleatoria

        nome_sensor = threading.current_thread().name  #nome do sensor

        #criando documento
        documento = {
            "nomeSensor" : nome_sensor,
            "valorSensor" : temperatura,
            "unidadeMedida" : "C°",
            "sensorAlarmado" : False
        }

        #inserindo
        teste.replace_one({"nomeSensor": nome_sensor}, documento, upsert=True)

        print(f"Sensor {nome_sensor}: {temperatura} Cº")

        if temperatura > 38:
            documento["sensorAlarmado"] = True

            teste.replace_one({"nomeSensor": nome_sensor}, documento)

            print(f"Atenção! Temperatura  muito  alta! Verificar Sensor {nome_sensor}!")

            break

        time.sleep(random.randint(1,5))


sensor1 = threading.Thread(target= simula_temperatura, name='Sensor 01')
sensor2 = threading.Thread(target= simula_temperatura, name='Sensor 02')
sensor3 = threading.Thread(target= simula_temperatura, name='Sensor 03')

sensor1.start()
sensor2.start()
sensor3.start()

sensor1.join()
sensor2.join()
sensor3.join()

