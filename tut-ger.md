# Was ist MQTT?
*MQTT* steht für **Message Queuing Telemetry Transport** und ist ein
Protokoll, um zwischen Maschinen zu kommunizieren.

MQTT basiert auf dem Publisher-Subscriber-Modell. D.h. man kann ein
bestimmtes Thema, **Topic** genannt, abbonieren. Das bedeutet, dass man
sich bei dem sogenannten **Broker** für dieses Thema registriert. Wenn
eine Nachricht zu diesem Thema veröffentlich (**gepublished**) wird,
dann wird diese Nachricht an alle Abbonenten weiterverteilt.

MQTT sendet standarmäßig alles unverschlüsselt auf Port 1883. Ansonsten
ist der Standardport für die mit TLS verschlüsselten Nachrichten 8883.

Alle technischen Details können auch [hier][http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html]
nachgelesen werden.

## Topics
Topics sind hierarchisch aufgebaut. Die allgemeinste Spezifizierung
kommt als erstes und dann die nächst spezifischere usw.; immer mit einem
"/" abgetrennt:

``` allgemein/spezifischer/noch_spezifischer ```

Man kann auch leere Subtopics haben:

``` vor_leerem_Subtopic//nach_leerem_Subtopic ```


Topics dürfen UTF-8 Zeichen enthalten, außer Leerzeichen.
Zudem muss mindestens ein ichen ngegeben werden. Außerdem dürfen nicht
mehr als 65535 Bytes zur Kodierung genutzt werden.
Das heißt, einem stehen mindestens 16383 Zeichen zur Verfügung, was mehr
als genug ist.

### Wildcards
Es gibt zwei Arten von Wildcards: *Single level wildcard* **+** und
*Multi level wildcard* **#**

Mit + kann man auf einem Level alle Subtopics matchen. Damit würde
``` Zuhause/Wohnzimmer/+/Temperatur ``` z.B. auf

| Topic |
| --- |
| Zuhause/Wohnzimmer/Sensor1/Temperatur |
| Zuhause/Wohnzimmer/Sensor_XA432/Temperatur |
| Zuhause/Wohnzimmer//Temperatur |
| Zuhause/Wohnzimmer/WasAuchImmer/Temperatur |
matchen und man würde von allen diesen Topics Nachrichten bekommen.

Die Wildcard # match auf alle Subtopics der gleichen und weiteren
Ebenen. Deshalb muss  # immer in der Topicbeschreibung zuletzt stehen.
``` Zuhause/# ``` match z.B. auf:


| Topic |
| --- |
| Zuhause/Wohnzimmer/Sensor_XA432/Temperatur |
| Zuhause/Schlafzimmer/Energieverbruch |
| Zuhause/Toilette/Sensor_YZ51/Luftfeuchtigkeit |


## Nachrichtentypen
| Nachrichtentyp | Beschreibung |
| --- | --- |
| CONNECT  | Das erste Packet, dass bei einer Connection vom Client an den Server gesendet wird |
| CONNACK | Wird vom Server als Antwort auf ein CONNECT-Paket gesendet. |
| PUBLISH | Packet von einem Client zum Server oder Server zum Client im eine Nachricht zu übertragen |
| PUBACK | Antwort auf ein PUBLISH-Paket *QoS level 1* |
| PUBREC | Antwort auf ein PUBLISH-Paket *QoS level 2* (Publish received) |
| PUBREL | Antwort auf ein PUBREC-Paket *QoS level 2* (Publish release) |
| PUBCOMP | Antwort auf ein PUBREL-Paket *QoS level 2* (Publish complete) |
| SUBSCRIBE | Paket, mit dem der Client sendet welche Topics er auf welchem QoS vom Server abboniert |
| SUBACK | Antwort des Servers auf das SUBSCRIBE-Paket |
| UNSUBSCRIBE | Paket, mit dem der Client sagt, dass er auf das Paket nicht mehr hören möchte|
| UNSUBACK | Antwort des Servers auf das UNSUBSCRIBE-Paket |
| PINGREQ | Paket vom Client zum Server. 1. Client ist am Leben. 2. Server soll Lebenszeichen geben. 3. Netzwerkverbindung aktiv |
| PINGRESP | Paket vom Server zum Client. Zeigt, dass der Server am Leben ist. |
| DISCONNECT | Paket zeigt an, dass der Client sich sauber vom Server trennt. |


### CONNECT
CONNECT sendet folgende Informationen (*kursiv* ist optional) mit:

clientID (string), cleanSession (boolean), *username* (string),
*password* (string), *lastWillTopic* (string),
*lastWillQos* (0,1 oder 2), *lastWillMessage* (string),
*lastWillRetain* (boolean), keepAlive (natürliche Zahl)
### CONNACK
CONACK sendet folgende Informationen (*kursiv* ist optional) mit:

sessionPresent (boolean), returnCode

| Returncode | Bedeutung |
| --- | --- |
| 0 | Verbindung akzeptiert |
| 1 | Falsche Protokollversion |
| 2 | Identifizierung fehlgeschlagen |
| 3 | Server nicht erreichbar |
| 4 | Falscher Benutzername oder Passwort |
| 5 | Nicht autorisiert |


### PUBLISH
PUBLISH sendet folgende Informationen (*kursiv* ist optional) mit:

packetID (natrüliche Zahl und 0, wenn QoS gleich 0), topicName (string),
qos (0,1 oder 2), retainFlag (boolean), payload (string), dupFlag
(boolean)

### PUBACK
### PUBREC
### PUBREL
### PUBCOMP
### SUBSCRIBE
SUBSCRIBE sendet folgende Informationen (*kursiv* ist optional) mit:

packetId (natürliche Zahl), qos1 (0,1 oder 2), topic1 (string),
qos2 (0,1 oder 2), topic2 (string), qos3 (0,1 oder 2), topic3 (string),
...
### SUBACK
SUBSCRIBE sendet folgende Informationen (*kursiv* ist optional) mit:

packetID, returnCode1, returnCode2, returnCode3, ...

| Returncode | Bedeutung |
| --- | --- |
| 0 | Erfolgreich - Maximales QoS-Level 0 |
| 1 | Erfolgreich - Maximales QoS-Level 1 |
| 2 | Erfolgreich - Maximales QoS-Level 2 |
| 128 | Fehlgeschlagen |



### UNSUBSCRIBE
UNSUBSCRIBE sendet folgende Informationen (*kursiv* ist optional) mit:

packetId (natürliche Zahl), topic1 (string), topic2 (string),
topic3 (string), ...
### UNSUBACK
UNSUBSCRIBE sendet folgende Informationen mit:

packetId (ntürliche Zahl)

### PINGREQ
### PINGRESP
### DISCONNECT

# Get things running
Um MQTT zu nutzen, braucht man als erstes einen MQTT-Broker. Einer der
bekanntesten Broker ist **Mosquitto**.
Man kann sich den broker [hier][https://mosquitto.org/download/]
herunterladen.
Für Ubuntu geht das ganze aber am einfachsten mit:

```bash
sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
sudo apt update
sudo apt install mosquitto
```

Damit hat man schon alles, was man braucht.

Man kann jetzt subscriben und publishen:

<table align="center">
<tr>
<td>
	Tab 1
</td>
<td>
	Tab 2
</td>
</tr>
<tr>
<td valign="top">
    <pre lang = "bash">
    $ mosquitto_sub -h localhost -t meinTopic
    meineNachricht
    </pre>

</td>
<td valign="top">
    <pre lang = "bash">
    $ mosquitto_pub -h localhost -m meineNachricht -t meinTopic
    </pre>
</td>
</tr>
</table>

Was ist hier passiert? Mit ``` mosquitto_sub ``` haben wir uns beim
Broker unter der der Adresse **localhost** für das Topic **meinTopic**
registriert und bekommen dadurch alle Nachrichten, die unter diesem
Topic publisht werden.

Mit ``` mosquitto_pub ``` haben wir die Nachricht **meineNachricht**
über unter dem Topic **meinTopic** publisht. Dies wurde dann im Tab 1
für uns sichtbar.

```python
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
```

# QoS und Co.

| Quality of Service-Level | Bedeutung |
| --- | --- |
| 0 | Höchstens eine Nachricht kommt an |
| 1 | Mindestens eine Nachricht kommt an |
| 2 | Genau eine Nachricht kommt an |


# MQTT in Verbindung mit JSON und Protobuf

# Best practices

# Netzwerk profiling
