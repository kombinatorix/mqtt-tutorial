import paho.mqtt.client as mqtt


# Ist ein Callback, der ausgeführt wird, wenn sich mit dem Broker verbunden wird
def on_connect(client, userdata, flags, rc):
    print("Hat sich mit Result code " + str(rc) + " mit dem Broker verbunden.")

    client.subscribe("allgemein/spezieller")

# Ist ein Callback, der ausgeführt wird, wenn eine Nachricht empfangen wird
def on_message(client, userdata, msg):
    print("Topic: \t\t"+msg.topic)
    print("Payload: \t"+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()
