import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, maxHands=1, modelComplexity=0, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplexity=modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon
 
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.modelComplexity,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
 
    def drawHands(self, img, draw=True):
        img = cv2.flip(img,1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img.flags.writeable = False
        self.results = self.hands.process(imgRGB)
        img.flags.writeable = True

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,self.mpHands.HAND_CONNECTIONS)              
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    if draw:
                        cv2.circle(img, (cx, cy), 5, (36, 122, 243), cv2.FILLED)

        return img
 
    def findPosition(self, img, flipType=True):
        img = cv2.flip(img,1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img.flags.writeable = False
        self.results = self.hands.process(imgRGB)
        img.flags.writeable = True
        hands = []
        h, w, c = img.shape
 
        if self.results.multi_hand_landmarks:
            for handType, handLms in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                hand = {"lmList":[],"side":""}
                # lmList
                for id, lm in enumerate(handLms.landmark):
                    px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                    hand["lmList"].append([px, py, pz])

                if flipType:
                    if handType.classification[0].label == "Right":
                        hand["side"] = "Left"
                    else:
                        hand["side"] = "Right"
                else:
                    hand["side"] = handType.classification[0].label

                hands.append(hand)

        return hands
 
if __name__ == "__main__":
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector(maxHands=2)
    while True:
        success, img = cap.read()
        img = detector.drawHands(img)
        lmList = detector.findPosition(img)
 
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
 
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)
 
        cv2.imshow("Image", img)
        cv2.waitKey(1)
 
