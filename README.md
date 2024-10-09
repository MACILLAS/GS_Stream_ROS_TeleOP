# GS_Stream SocketIO Client and ROSBridge Server: Docker

This short program creates a ROSBridge container, which allows us to interface with the GS_Stream application
and Robotics through ROSBridge.

Changes 10-09-2024 updated to ROS Humble (ROS2)

```
docker build -t humble-rosbridge .
docker run -i --network="host" -t humble-rosbridge /bin/bash
```

Run this to setup a rosbridge server for testing connection to ROS
```
# roslaunch rosbridge_server rosbridge_websocket.launch 
ros2 launch rosbridge_server rosbridge_websocket_launch.xml 
```

Open a new terminal and connect to the running docker container then run stuff
```
docker exec -it container-name /bin/bash

python3 app.py
```

If you want to check if everything is working you can open another terminal
and run...
```
python3 debug_listener.py
```