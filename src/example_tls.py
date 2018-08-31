import paho.mqtt.client as mqtt
import json
import ssl

# Ist ein Callback, der ausgeführt wird, wenn sich mit dem Broker verbunden wird
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Verbindung akzeptiert")
        client.subscribe("allgemein/spezieller")
    elif rc == 1:
        print("Falsche Protokollversion")
    elif rc == 2:
        print("Identifizierung fehlgeschlagen")
    elif rc == 3:
        print("Server nicht erreichbar")
    elif rc == 4:
        print("Falscher benutzername oder Passwort")
    elif rc == 5:
        print("Nicht autorisiert")
    else:
        print("Ungültiger Returncode")


# Ist ein Callback, der ausgeführt wird, wenn eine Nachricht empfangen wird
def on_message(client, userdata, msg):
    print("Topic: \t\t" + msg.topic)
    print("Payload: \t" + str(msg.payload))


client = mqtt.Client()

mqtt_username = ""
mqtt_password = "mqttversuch"
#client.username_pw_set(mqtt_username, password=mqtt_password)
client.tls_set(ca_certs="./tls/ca.crt", certfile=None,
               keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
               tls_version=ssl.PROTOCOL_TLSv1_1, ciphers=None)
client.tls_insecure_set(False)
client.on_connect = on_connect
client.on_message = on_message


client.connect("127.0.0.1", 8883, 60)
for _ in range(2):
    client.loop(.1)
_dict = {"Hallo": "MQTT"}
_payload = json.dumps(_dict)
client.publish("allgemein/spezieller",_payload)

client.loop_forever()
