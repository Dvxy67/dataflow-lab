import json, os, random, time
from datetime import datetime
import pika

HOTE = os.getenv("RABBITMQ_HOST", "localhost")
UTILISATEUR = os.getenv("RABBITMQ_USER", "lab")
MOT_DE_PASSE = os.getenv("RABBITMQ_PASS", "lab")
INTERVALLE = float(os.getenv("INTERVALLE", "1"))
FILE = "flux"
TYPES = ["log", "mesure", "fichier", "alerte"]

def connecter():
    identifiants = pika.PlainCredentials(UTILISATEUR, MOT_DE_PASSE)
    parametres = pika.ConnectionParameters(host=HOTE, credentials=identifiants)
    while True:
        try:
            return pika.BlockingConnection(parametres)
        except pika.exceptions.AMQPConnectionError:
            print("RabbitMQ pas encore disponible, nouvel essai dans 3 s...")
            time.sleep(3)

def main():
    connexion = connecter()
    canal = connexion.channel()
    canal.queue_declare(queue=FILE, durable=True)
    print(f"Connecté à RabbitMQ, envoi dans la file '{FILE}'")
    while True:
        message = {
            "type": random.choice(TYPES),
            "source": f"serveur-{random.randint(1, 5):02d}",
            "valeur": random.randint(0, 100),
            "date": datetime.now().isoformat(timespec="seconds"),
        }
        canal.basic_publish(exchange="", routing_key=FILE, body=json.dumps(message),
                            properties=pika.BasicProperties(delivery_mode=2))
        print("Envoyé :", message)
        time.sleep(INTERVALLE)

if __name__ == "__main__":
    main()
