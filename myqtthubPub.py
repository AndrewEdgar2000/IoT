#install paho by the command:  pip install paho-mqtt
import paho.mqtt.client as mqtt
import time
import ssl
import temp_hum

host          = "node02.myqtthub.com"
port          = 1883
clean_session = True
client_id     = "tempHum"
user_name     = "tempHum"
password      = "London97"

def on_connect (client, userdata, flags, rc):
    """ Callback called when connection/reconnection is detected """
    print ("Connect %s result is: %s" % (host, rc))
    
    # With Paho, always subscribe at on_connect (if you want to
    # subscribe) to ensure you resubscribe if connection is
    # lost.
    # client.subscribe("some/topic")

    if rc == 0:
        client.connected_flag = True
        print ("connected OK")
        return
    
    print ("Failed to connect to %s, error was, rc=%s" % rc)
    # handle error here
    sys.exit (-1)


def on_message(client, userdata, msg):
    """ Callback called for every PUBLISH received """
    print ("%s => %s" % (msg.topi, str(msg.payload)))

# Define clientId, host, user and password
client = mqtt.Client (client_id = client_id, clean_session = clean_session)
client.username_pw_set (user_name, password)

client.on_connect = on_connect
client.on_message = on_message

# configure TLS connection
# client.tls_set (cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2)
# client.tls_insecure_set (False)
# port = 8883

# connect using standard unsecure MQTT with keepalive to 60
client.connect (host, port, keepalive = 60)
client.connected_flag = False
while not client.connected_flag:           #wait in loop
    client.loop()
    time.sleep (1)

# publish message (optionally configuring qos=1, qos=2 and retain=True/False)
temp = temp_hum.temperature()
hum = temp_hum.humidity()
pressure = temp_hum.pressure()
client.publish("temperature",temp)
client.publish("humidity",hum)
client.publish("pressure",pressure)
print ("The room temperature is:  temp=%s" % temp + "the humidity is: hum=%s" % hum + "and the pressure is: pressure=%s" % pressure)

# close connection
client.disconnect ()
