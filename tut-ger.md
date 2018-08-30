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

Alle technischen Details können auch [hier](http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html)
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
PUBLISH sendet folgende Informationen mit:

packetID (natrüliche Zahl und 0, wenn QoS gleich 0), topicName (string),
qos (0,1 oder 2), retainFlag (boolean), payload (string), dupFlag
(boolean)

### PUBACK
### PUBREC
### PUBREL
### PUBCOMP
### SUBSCRIBE
SUBSCRIBE sendet folgende Informationen mit:

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
Man kann sich den broker [hier](https://mosquitto.org/download/)
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

Um tiefer einzusteigen, nutzen wir Python 3 und das Paket **paho-mqtt***[]:

```bash
$ pip install paho-mqtt
```

Jetzt können wir mit unserem ersten [Beispiel](src/example1.py) anfangen.

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

Nehmen wir das Programm Schritt für Schritt auseinander:

```python
import paho.mqtt.client as mqtt
```
Mit dem import wird der Code aus dem eben installierten paho-mqtt-Paket
in das aktuelle Programm geladen.

```python
def on_connect(client, userdata, flags, rc):
    print("Hat sich mit Result code " + str(rc) + " mit dem Broker verbunden.")

    client.subscribe("allgemein/spezieller")
```
Dies ist eine Funktion, die als Callback fungiert. Sie wird aufgerufen,
wenn der Client versucht sich mit dem Server zu verbinden.
Als Parameter hat die Funktion *client*, *userdata*, *flags* und *rc*.
Wofür man *userdata* und *flags* nutzt, wird später erläutert.

Wichtig ist der Returncode *rc*. An ihm kann geschaut werden, ob die
Verbindung geklappt hat.

*client* wird genutzt, um ein Topic zu subscriben. Es ist "best practice"
dies direkt beim Verbindungsaufbau zu tun, da dies dann auch immer
automatisch bei jedem reconnect geschieht.

```python
def on_message(client, userdata, msg):
    print("Topic: \t\t"+msg.topic)
    print("Payload: \t"+str(msg.payload))
```

Die Funktion *on_message* wird als Callback immer dann aufgerufen, wenn
eine Nachricht auf einem abbonierten Topic ankommt.
Da das Topic immer als String übermittelt wird, kann dies sofort
ausgegeben werden. Die Payload ist ein Bytestream und muss erst in einen
String übersetzt werden.

Mit der folgenden Zeile wird ein client-Objekt erzeugt
```python
client = mqtt.Client()
```
und mit
```python
client.on_connect = on_connect
client.on_message = on_message
```
werden dem client-Objekt die Callbackfunktionen (von oben) zugewiesen.

Mit
```python
client.connect("localhost", 1883, 60)
```
verbindet versucht der Client sich mit dem Broker zu verbinden, der
auf diesem System läuft. *localhost* ist ein Synonym für die IP-Adresse
127.0.0.1 und 1883 ist der Standardport für unverschlüsselte
MQTT-Nachrichten. Die 60 steht für das keep-alive-Intervall in Sekunden.

Als letztes haben wir:
```python
client.loop_forever()
```
Dies ist die Eventschleife, die auf neue Nachrichten und dergleichen
wartet. Ohne Sie würde sich das Programm sofort beenden.

## Returncode nutzen
Im zweiten [Beispiel](src/example2.py) wird gezeigt, wie man den Returncode von CONACK
nutzen kann:

```python
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
```

Mit einer Abfrage des Returncodes kann auf Verbindungsfehlschläge reagiert
werden. In unserem Beispiel wird allerdings erstmal nur die Information
an den Benutzer weitergereicht.

## Loops
Wir haben eben ``` loop_forever()``` kennengelernt. paho-mqtt gibt uns
allerdings drei verschiedene Arten eine Loop zu nutzen:

+ loop_forever()
+ loop_start()
+ loop()

### loop\_forever()
```loop_forever()``` erzeugt eine blockendierende Eventschleife. Es kann
nichts mehr neben der Eventloop laufen. Für die meisten Anwendungszwecke
ist dies auch mehr als ausreichend.


### loop\_start()
```loop_start()``` erstellt einen Thread, der eine Eventloop enthält.
Dies blockiert den Haupthread nicht. Man muss jedoch beachten, dass der
Thread automatisch beendet wird, sofern das Hauptprogramm ein Ende
findet.

### loop()
```loop()``` muss mit einem Zahlenwert, z.B. ```client.loop(.2)``` 
aufgerufen.
Die Schleife blockiert dann den Haupthread für 200ms. Hier muss man
selbständig ```loop()``` in regelmäßigen abständen aufrufen.

### Stoppen einer Schleife
Mit ```client.loop_stop()``` kann eine Schleife automatisch gestoppt
werden. Z.B. kann das in einem *Disconnect*-Callback geschehen.
Jedoch sollte man sich sicher sein, dass es das Verhalten ist, dass
man sich wünscht.

### Mehrere clients
Hat man mehrere Clients, die zum gleichen oder verschieden Brokern
verbunden wird, kann man nicht mehr auf ```loop_forever()```
zurückgreifen, da diese Schleife blockierend ist. 
Es bleiben einem also nur ```loop_start()``` und ```loop()```.
Da ```loop_start()``` jedesmal einen neuen Thread erstellt ist
diese Möglichkeit nur für wenige clients geeignet. Wächst die
Zahl der Clients, sollte man auf ```loop()``` zurückgreifen.
Ein Beispiel, wie man dies realisieren kann, ist wie folgt:

```python
number_of_clients=7
clients=[]
mqtt.Client.connected_flag=False

for i in range(number_of_clients):
    clientid = "id-"+str(i)
    clients.append(mqtt.Client(clientid))
for client in clients:
    client.connect(...)
while True:
    for client in clients:
        client.loop(0.01)
        if not client.connected_flag:
            client.connect()
```

Oder bei einer kleinen Anzahl von Clients:


```python
number_of_clients=7
clients=[]
mqtt.Client.connected_flag=False

for i in range(number_of_clients):
    clientid = "id-"+str(i)
    clients.append(mqtt.Client(clientid))
for client in clients:
    client.connect_async()
    client.loop_start()
```



# QoS und Co.
Alles was in diesem Abschnitt erklärt wir kann [hier](https://pypi.org/project/paho-mqtt/)
noch einmal nachgelesen werden. Dort stehen natürlich noch viel mehr Optionen und Funktionen,
die man nutzen kann.

## Quality of Service
| Quality of Service-Level | Bedeutung |
| --- | --- |
| 0 | Höchstens eine Nachricht kommt an |
| 1 | Mindestens eine Nachricht kommt an |
| 2 | Genau eine Nachricht kommt an |


## Subscriben mehrerer Topics

```python
client.subscribe([("erstes_Topic",0),("zweites_topic",2)])
```


## Retained Messages 
Eine Nachricht für die das retained flag und ggf. das QoS-level
gesetzt wurde, wird sich vom broker gemerkt. Und wenn ein Client
für das entsprechende Topic subscribed, wird ihm die Nachricht
mit dem entsprechenden QoS gesendet.

Ein Beispiel wäre:

```python
client.publish("meinTopic", "Meine Nachricht/Payload", qos=1, retain=True)
```

**Wichtig!** Jede neue Nachricht mit dem retained flag überschreibt die
letzte, dem Broker bekannte, retained message.

## Last Will and Testament (LWT)
Der letzte Wille wird veröffentlicht, wenn sich der client die Verbindung
nicht sauber über ```disconnect()``` trennt.

```python
client.will_set(topic, payload=None, qos=0, retain=False)
```


# MQTT in Verbindung mit JSON und Protobuf
Bisher haben wir die Payload von MQTT nur genutzt, um Strings zu übertragen.
Dieses Konzept kann, zweistufig erweitert werden. So kann ein JSON-String
über das Netzwerk gesendet werden, das von Python direkt in ein Dictionary
übersetzt wird. Damit fällt das eigene Parsen des Strings weg. Hat aber auch
den Nachteil, dass eventuell mehr Zeichen als Payload verschickt werden müssen.
Nutzt man Googles protobuf, kann mit ein paar einbußen in der Flexibilität
die Größe der Payload drastisch reduziert werden. Außerdem kann sofort auf
die entsprechenden Datentypen - ohne eigenes Parsing - zugegriffen werden.

## JSON
JSON steht für **Javascript Object Notation**. Wie diese Notation genau aufgebaut
ist steht auf [https://json-schema.org/](https://json-schema.org/).

Uns interessieren in Python im Moment genau zwei Funktionen und ein import.
```python
import json

json.loads(...)

json.dumps(...)
```
 
Der Import stellt uns die Konvertierungsfunktionen von Python zur Verfügung.

Die *dumps(...)*-Funktion führt ein Python Dictionary in einen JSON-String über.
Die *loads(...)*-Funktion führt einen JSON-String in ein Python Dictionary über.

Ein einfach Program wäre:

```python
import paho.mqtt.client as mqtt
import json


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
    payload = json.loads(str(msg.payload))
    keys = payload.keys()
    print("Keys: " + str(keys))
    _dict = {'keys': str(keys)}
    _payload = json.dumps(_dict)
    client.publish("keys", _payload)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()
```

## Protobuf
Zuerst müssen wir erstmal Protobuf installieren. Dazu folgen wir der [Anleitung](https://developers.google.com/protocol-buffers/docs/downloads)

Als nächstes müssen wir unsere Protobufnachricht definieren. Dies tun wir in der [payload.proto](src/payload.proto):
```
syntax = "proto2";

package tutorial;

message payload {
  required string payload = 1;
  required int32 id = 2;
}
```

Als nächstes müssen wir die entsprechende Python-Datei erstellen. Die allgemeine
Syntax dafür lautet:
```bash
protoc -I=$SRC_DIR --python_out=$DST_DIR $SRC_DIR/addressbook.proto
```

In unserem Fall ist der Befehl (wir befinden uns im src-Ordner):
```bash
protoc -I=./ --python_out=./ ./payload.proto 
```

Jetzt finden wir eine *payload_pb2.py*-Datei im src-Ordner, die wir einbinden können:

```python
import paho.mqtt.client as mqtt
import payload_pb2

# Ist ein Callback, der ausgeführt wird, wenn sich mit dem Broker verbunden wird
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Verbindung akzeptiert")
        client.subscribe("protobuf")
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
    _payload = payload_pb2.payload()
    _payload.ParseFromString(msg.payload)
    print("Payload: \t"+_payload.payload)
    print("id: \t\t"+str(_payload.id))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


client.connect("localhost", 1883, 60)

_payload = payload_pb2.payload()
_payload.payload = "Meine Payload"
_payload.id = 1
client.loop(.1)
client.publish("protobuf", _payload.SerializeToString())

client.loop_forever()
```

# Best practices

## Topics
Topics sollten sehr kleinschrittig in verschiedene Subtopics unterteilt sein.
Es sollte möglichst kein Parsing im Client stattfinden. Vor allem weil das
Erstellen eines Topics sehr wenig Overhead erzeugt.
### Kein vorangestelten Slash

### Das Topic soll kurz und bündig sein

### Man sollte sich auf ASCII-Zeichen beschränken

### Man sollte einen unique identifier oder eine ClientID im Topic haben

### Topics sollen spezifisch und nicht allgemein sein

## Payload
Wenn die Payload als lesbarer String übertragen wird, sollte die Payload "gereinigt"
werden. Es kann sein, dass der String ein nullterminierter String ist.
D.h.:
```python
msg.payload.replace("\x00","")
```
# Netzwerk profiling

# Literatur
[Correlation Analysis of MQTT Loss and Delay 
According to QoS Level](http://cgweb1.northumbria.ac.uk/SubjectAreaResources/KF7046/papers/review/iot/lkh13.pdf)
