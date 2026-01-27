import time
import pyautogui
import keyboard
def get_coords():
    ''' function to determin the mouse coordinates'''

    print('press "Tab" key to lock position...')

    while True:
        # Check if tab key is pressed
        time.sleep(0.1)

        if keyboard.is_pressed('Tab'):
            break

    # Get the current mouse position
    x, y = pyautogui.position()
    return x, y

def caculate_offset(x1, y1 , x2, y2):
    x = x2-x1
    y = y2-y1
    return x, y


while True:
    x1, y1 = get_coords()
    print("first coords")
    print(x1,y1)
    x2, y2 = get_coords()
    print("second coords")
    print(x2,y2)
    print("offset:")
    print(caculate_offset(x1, y1, x2, y2))