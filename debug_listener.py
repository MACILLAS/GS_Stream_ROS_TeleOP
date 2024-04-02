import roslibpy

client = roslibpy.Ros(host='localhost', port=9090)
client.run()

topic_name = "/webinspector_pose"
message_type = "geometry_msgs/Pose"

listener = roslibpy.Topic(client, topic_name, message_type, queue_size=1)
listener.subscribe(lambda msg: print(msg["position"]))

try:
    while True:
        pass
except KeyboardInterrupt:
    client.terminate()