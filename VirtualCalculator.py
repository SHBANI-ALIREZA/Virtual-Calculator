# Importing the necessary libraries
import cv2
from cvzone.HandTrackingModule import HandDetector

# Creating a class for buttons of the calculator
class Button:
    """" Initializing the properties of the buttons """
    def __init__(self, position, width, height, value):
        self.position = position
        self.width = width
        self.height = height
        self.value = value

    # Drawing the buttons on the frame
    def draw(self, frame):
        # Drawing a filled rectangle for button
        cv2.rectangle(frame, self.position,
                      (self.position[0]+ self.width, self.position[1]+self.height),
                      (200, 200, 200), cv2.FILLED)
        # Drawing a margin for the button
        cv2.rectangle(frame, self.position,
                      (self.position[0] + self.width, self.position[1] + self.height),
                      (50, 50, 50), 3)
        # Putting a number or operator in the button
        cv2.putText(frame, self.value,
                    (self.position[0] + 25, self.position[1] + 65),
                    cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 5)

    # Checking if the button is clicked using the coordinates of the button
    def checkClick(self, x, y):
        if self.position[0] < x < (self.position[0] + self.width) and \
           self.position[1] < y < (self.position[1] + self.height):
            """ Highlighting the clicked button to show it is selected """
            cv2.rectangle(frame, self.position,
                          (self.position[0] + self.width, self.position[1] + self.height),
                          (255, 255, 255), cv2.FILLED)
            cv2.rectangle(frame, self.position,
                          (self.position[0] + self.width, self.position[1] + self.height),
                          (0, 0, 0), 3)
            cv2.putText(frame, self.value,
                       (self.position[0] + 30, self.position[1] + 65),
                        cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)
            # Returning True if the button is clicked to get processed later
            return True
        else:
            # Returning False if the button is NOT clicked
            return False

# Capturing WebCam stream live and creating a VideoCaptureObject
cap = cv2.VideoCapture(0)
# Resizing the WebCam width
cap.set(3, 1280)
# Resizing the WebCam height
cap.set(4, 720)

# Creating a HandDetectorObject
hand_detector = HandDetector(detectionCon=0.8, maxHands=1)

# Creating a list of the Values of each button
buttonListValues = [["7", "8", "9", "*"],
                    ["4", "5", "6", "-"],
                    ["1", "2", "3", "+"],
                    ["0", "/", ".", "="],]

# Creating a list for buttons
button_list = []

# Looping through X and Y in order to get the Position and Value of each button
for x in range(4):
    for y in range(4):
        x_position = x * 100 + 800
        y_position = y * 100 + 150
        button_list.append(Button((x_position, y_position), 100, 100, buttonListValues[y][x]))

# Creating a variable to calculate the Equation
myEquation = ""

# Creating a variable to avoid Clicking Duplication
delayCounter = 0

# Creating a Loop to capture the Video from the WebCam Frame-by-Frame
while True:
    #Getting each frame from the VideoCaptureObject and a flag to check whether it is capturing the frame sucessfully or not
    success, frame = cap.read()

    # Flipping the frame (make sure your Left-Hand is Left_Hand not Right!
    frame = cv2.flip(frame, 1)

    # Finging the the Hand in the frame
    hands, frame = hand_detector.findHands(frame, flipType=False)

    # Drawing the result rectangle for Calculator
    cv2.rectangle(frame, (800, 50), (800+ 400, 70+ 100), (255, 255, 255), cv2.FILLED)
    cv2.rectangle(frame, (800, 50), (800 + 400, 70 + 100), (0, 0, 0), 3)

    # Drawing the buttons using a for-loop and the method draw of the class button to instantiate each button
    for button in button_list:
        button.draw(frame)

    # Finding the distance between the index and middle finger to check whether it is clicked or not
    if hands:
        lmList = hands[0]["lmList"]
        length, info, frame = hand_detector.findDistance(lmList[8][:2], lmList[12][:2], frame)
        x, y = lmList[8][:2]
        if length < 45:
            for i, button in enumerate(button_list):
                if button.checkClick(x, y) and delayCounter == 0:
                    myValue = (buttonListValues[int(i%4)][int(i/4)])
                    if myValue == "=":
                        myEquation = str(eval(myEquation))
                    else:
                        myEquation += myValue
                    delayCounter = 1

    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0

    # Drawing the Calculated Equation in the result rectangle
    cv2.putText(frame, myEquation,(810, 110),
                cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

    # Displaying the frames with 1 milisecond delay
    cv2.imshow("WebCam", frame)
    key = cv2.waitKey(1)

    # Enter "c" to erase the result rectangle
    if key == ord("c"):
        myEquation = ""

    # Enter "q" to exit
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()