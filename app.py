import roslibpy
import socketio
import numpy as np
from pyproj import Proj

"""
Hardcoded transformation parameters from MatLab and UTM to LLA transform
For Ford_Tower_20240529 
What the center of 
"""
ps = 4.041857840563472
pR = np.array([
            [0.649713360622769, -0.447261133664891, 0.614678800139605],
            [-0.753435867982405, -0.271411832965926, 0.598890649253832],
            [-0.101029410895386, -0.852228311685826, -0.513322474566679]])
pT = np.array([536853.955540370, 4814155.48301584, 338.052789287157]).T

ZoneNo = "17"
# Peterborough to Windsor (Ontario) if you decide to use UTM coordinates please change.
myProj = Proj("+proj=utm +zone="+ZoneNo+" +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs") # Northern Hemisphere

tower_center_lla = []

client = roslibpy.Ros(host='localhost', port=9090)

topic_name = "/towereye_wp"
message_type = "gps_msgs/GPSFix"
talker = roslibpy.Topic(client, topic_name, message_type, queue_size=1)

sio = socketio.Client(logger=True, engineio_logger=True)


@sio.event
def connect():
    client.run()
    print('Is Ros connected?', client.is_connected)


@sio.event
def disconnect():
    sio.disconnect()
    talker.unadvertise()
    client.terminate()
    print('Ros disconnected.')


# @sio.on('pose')
# def on_pose(data):
#     pose = np.array(data)
#     R = pose[:3, :3]
#     t = pose[:3, 3]
#     # idk what to do here :P
#     # it either t = t or t = -R depending on if you want C2W or W2C
#     t = -R @ t * (1 / 1.2736)  # Scaling factor for cviss_lab
#     #t = t * (1 / 1.2736)  # Scaling factor for cviss_lab
#
#     #R = R.T
#
#     # qvec is in WXYZ format
#     qvec = rotmat2qvec(R)
#
#     pose_msg = roslibpy.Message({
#         "position": {
#             "x": t[0],
#             "y": t[1],
#             "z": t[2]
#         },
#         "orientation": {
#             "x": qvec[1],
#             "y": qvec[2],
#             "z": qvec[3],
#             "w": qvec[0]
#         }
#     })
#     print('Pose Update Recieved...')
#     talker.publish(pose_msg)

@sio.on('pose_and_heading')
def on_pose_and_heading(data):
    R = np.array(data['R'])
    T = np.array(data['T'])
    heading = int(data['heading'])
    if heading > 180:
        heading = heading - 360

    cam_center = -R.T @ T
    UTM = ps * pR @ cam_center + pT
    #print(UTM)
    Lon, Lat = myProj(UTM[0], UTM[1], inverse=True)
    #print(Lon, Lat, UTM[2])
    gps_msg = roslibpy.Message({
        "latitude": Lat,
        "longitude": Lon,
        "altitude": UTM[2],
        "track": heading
    })
    print('Pose Update Recieved...')
    talker.publish(gps_msg)

sio.connect('http://localhost:5000')
print('my sid is', sio.sid)
sio.wait()
