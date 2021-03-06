import paho.mqtt.client as mqtt


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
    print("Topic: \t\t"+msg.topic)
    print("Payload: \t"+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()
