import cv2
from datetime import datetime
from os import getcwd
from os.path import join
execution_path = getcwd()

if 'projet_sudoku' in execution_path:
    execution_path = execution_path.split('projet_sudoku')[0]
if 'PROJETS' not in execution_path:
    execution_path = join(execution_path, "PROJETS")
if 'projet_sudoku' not in execution_path:
    execution_path = join(execution_path, "projet_sudoku")
print(f"[sudoku_capture] execution path= {execution_path}")
import sys
sys.path.append(execution_path)
from sudoku_util import PATH_SUDOKU_DIR

cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        dt=datetime.today().strftime('%Y-%m-%d-%H%M%S')
        # SPACE pressed
        img_name = join(PATH_SUDOKU_DIR, f"opencv_frame_{dt}-{img_counter}.png")
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()