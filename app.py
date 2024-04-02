import roslibpy
import socketio
import numpy as np


# Take the R from the pose, transpose it before sending to rotmat2qvec
# This function returns quaternions as WXYZ so make sure to swap to XYZW
def rotmat2qvec(R):
    Rxx, Ryx, Rzx, Rxy, Ryy, Rzy, Rxz, Ryz, Rzz = R.flat
    K = (
            np.array(
                [
                    [Rxx - Ryy - Rzz, 0, 0, 0],
                    [Ryx + Rxy, Ryy - Rxx - Rzz, 0, 0],
                    [Rzx + Rxz, Rzy + Ryz, Rzz - Rxx - Ryy, 0],
                    [Ryz - Rzy, Rzx - Rxz, Rxy - Ryx, Rxx + Ryy + Rzz],
                ]
            )
            / 3.0
    )
    eigvals, eigvecs = np.linalg.eigh(K)
    qvec = eigvecs[[3, 0, 1, 2], np.argmax(eigvals)]
    if qvec[0] < 0:
        qvec *= -1
    return qvec


client = roslibpy.Ros(host='localhost', port=9090)

topic_name = "/webinspector_pose"
message_type = "geometry_msgs/Pose"
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


@sio.on('pose')
def on_pose(data):
    pose = np.array(data)
    R = pose[:3, :3]
    t = pose[:3, 3]
    # idk what to do here :P
    # it either t = t or t = -R depending on if you want C2W or W2C
    #t = -R @ t * (1 / 1.2736)  # Scaling factor for cviss_lab
    t = t * (1 / 1.2736)  # Scaling factor for cviss_lab

    R = R.T

    # qvec is in WXYZ format
    qvec = rotmat2qvec(R)

    pose_msg = roslibpy.Message({
        "position": {
            "x": t[0],
            "y": t[1],
            "z": t[2]
        },
        "orientation": {
            "x": qvec[1],
            "y": qvec[2],
            "z": qvec[3],
            "w": qvec[0]
        }
    })
    print('Pose Update Recieved...')
    talker.publish(pose_msg)

sio.connect('http://localhost:5000')
print('my sid is', sio.sid)
sio.wait()
