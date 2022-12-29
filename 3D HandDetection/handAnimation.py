import cv2
from HandTrackingModule import handDetector
import time

def hand_animation(detector,video,window_w=600,window_h=600):
    # set window params
    cap = cv2.VideoCapture(video)
    cap.set(3, window_w)
    cap.set(4, window_h)

    pTime = 0
    cTime = 0
    # lamdmarks lists
    posList1 = []
    posList2 = []
    while True:
        success, img = cap.read()
        if success:
            # Find the hands and their landmarks
            img = detector.drawHands(img)
            hands = detector.findPosition(img)
            
            if hands:
                for hand in hands:
                    lmList = hand["lmList"]  # List of 21 Landmark points
                    points = []
                    for lm in lmList:
                        points.append(f'{lm[0]},{img.shape[0] - lm[1]},{lm[2]}')

                    if hand["side"] == "Right":
                        posList1.append(','.join(points))
                    else:
                        posList2.append(','.join(points))
            
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

    # write landmarks to .txt files
    with open("Animation1.txt", 'w') as f:
        f.writelines(["%s\n" % item for item in posList1])
    with open("Animation2.txt", 'w') as f:
        f.writelines(["%s\n" % item for item in posList2])
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # initialize handDetector
    detector = handDetector(maxHands=2)
    hand_animation(detector,'video.mp4')