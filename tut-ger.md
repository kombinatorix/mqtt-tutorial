# Was ist MQTT?

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

Damit hat man schon alles, was man braucht. Man kann jetzt subscriben
und publishen:

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


# QoS und Co.

# MQTT in Verbindung mit JSON und Protobuf

# Best practices

# Netzwerk profiling
