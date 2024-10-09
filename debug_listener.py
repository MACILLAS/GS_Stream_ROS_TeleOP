import roslibpy

client = roslibpy.Ros(host='localhost', port=9090)
client.run()

topic_name = "/towereye_wp"
message_type = "gps_msgs/GPSFix"

listener = roslibpy.Topic(client, topic_name, message_type, queue_size=1)
listener.subscribe(lambda msg: print(msg["altitude"], msg["track"]))

try:
    while True:
        pass
except KeyboardInterrupt:
    client.terminate()