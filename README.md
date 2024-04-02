# GS_Stream SocketIO Client and ROSBridge Server: Docker

This short program creates a ROSBridge container, which allows us to interface with the GS_Stream application
and Robotics through ROSBridge.

```
docker build -t noetic-rosbridge .
docker run -i --network="host" -t noetic-rosbridge /bin/bash
```

Run this to setup a rosbridge server for testing connection to ROS
```
roslaunch rosbridge_server rosbridge_websocket.launch
```

Open a new terminal and connect to the running docker container then run stuff
```
docker exec -it container-name /bash/bash

python3 app.py
```

If you want to check if everything is working you can open another terminal
and run...
```
python3 debug_listener.py
```