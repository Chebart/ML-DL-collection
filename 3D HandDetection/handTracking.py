import cv2
from HandTrackingModule import handDetector
import socket
import time

def hand_tracking(detector,sock,address,window_w=800,window_h=600):
    # set the camera and window params
    cap = cv2.VideoCapture(0)
    cap.set(3, window_w)
    cap.set(4, window_h)

    pTime = 0
    cTime = 0
    
    while True:
        # Get image frame
        success, img = cap.read()
        if success:
            # Find the hand and its landmarks
            img = detector.drawHands(img)
            hands = detector.findPosition(img)

            # lamdmarks list
            data = []
            
            if hands:
                for hand in hands:
                    lmList = hand["lmList"]  # List of 21 Landmark points
                    for lm in lmList:
                        data.extend([lm[0], window_h - lm[1], lm[2]])

                sock.sendto(str.encode(str(data)), address)

            # calculate FPS
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

            # show FPS
            cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                        (255, 0, 255), 3)
        
            # show image
            img = cv2.resize(img, (0,0), None, 0.75, 0.75)
            cv2.imshow("Image", img)
            cv2.waitKey(1)
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # initialize handDetector
    detector = handDetector(maxHands=2)
    # initialize port between python and unity
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverAddressPort = ("127.0.0.1", 8055)
    hand_tracking(detector,sock,serverAddressPort)