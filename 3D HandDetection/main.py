from HandTrackingModule import handDetector
from handAnimation import hand_animation
from handTracking import hand_tracking
import socket
 

def main(mode='camera'):
    # parameters
    window_w = 800
    window_h = 600
    # initialize handDetector
    detector = handDetector(maxHands=2,detectionCon=0.4, trackCon=0.4)
    # initialize port between python and unity
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverAddressPort = ("127.0.0.1", 8055)
    # choose type of detection
    if mode=='camera':
        hand_tracking(detector,sock,serverAddressPort,window_w,window_h)
    else:
        hand_animation(detector,'video3.mp4',window_w,window_h)


if __name__ == "__main__":
    main()