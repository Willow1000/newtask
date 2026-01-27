import pyautogui
import keyboard
import threading
import os
import io
import time
from datetime import datetime
import fire
import tkinter as tk
from PIL import Image, ImageTk


'''
this script requires you to take pictures of the runescape game in fullscreen mode
This script takes a screenshot when the 'print screen' 
 key is pressed and logs the coordinates of the screenshot's borders.
'''

user_input = None


class ScreenSelection:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.5)
        self.root.configure(bg='black')
        # starts on top (together with bring_to_front keeps the window on top)
        self.root.attributes('-topmost', True)
        self.bring_to_front() 

    def bring_to_front(self):
        # Ensures the window is in focus and on top
        self.root.update()
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def is_selection_success(self):
        return self.selection_success

    def on_click(self, event):
        self.start_x = self.root.winfo_pointerx()
        self.start_y = self.root.winfo_pointery()

        if self.selection_rectangle:
            self.canvas.delete(self.selection_rectangle)
        self.selection_rectangle = None

        self.canvas = tk.Canvas(self.root, cursor="cross", bg="black", bd=0, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)
        self.canvas.configure(bg='gray')

    def on_drag(self, event):
        self.end_x = self.root.winfo_pointerx()
        self.end_y = self.root.winfo_pointery()

        if self.selection_rectangle:
            self.canvas.delete(self.selection_rectangle)
        self.selection_rectangle = \
            self.canvas.create_rectangle(
                self.start_x, self.start_y, self.end_x, self.end_y, outline='red', width=5
            )

    def on_release(self, event):
        self.end_x = self.root.winfo_pointerx()
        self.end_y = self.root.winfo_pointery()

        self.set_screen_coords()
        if self.selection_success:
            self.root.destroy()

    def set_screen_coords(self):
        x1 = min(self.start_x, self.end_x)
        y1 = min(self.start_y, self.end_y)
        x2 = max(self.start_x, self.end_x)
        y2 = max(self.start_y, self.end_y)
        width = x2 - x1
        height = y2 - y1
        if width < 1 or height < 1:
            print("Selection too small")
            self.selection_success= False
            self.root.destroy()
            return
        self.selection_success = True
        self.top_left = (x1, y1)
        self.bottom_right = (x2, y2)

    def get_screenshot_coords(self):
        # Ensure correct coordinate range
        return self.top_left, self.bottom_right
    

class ScreenshotInfo():
    def __init__(self, borders, screenshot):
        self.borders = borders
        self.screenshot = screenshot

    def get_borders(self): 
        return self.borders
     
    def get_screenshot(self):
        return self.screenshot
         
    def add_screenshot_path(self, screenshot_path):
        self.screenshot_path = screenshot_path

    def show_screenshot(self):
        # Step 1: Create a Tkinter window
        root = tk.Tk()
        root.title("Image Display")
        root.geometry("300x450")  # Set window size to 300x300

        # widgets 
        # Create a Label widget for user instructions
        instruction_label = tk.Label(root, text="Enter your input below:")
        instruction_label.pack(pady=10)
        # Create an Entry widget for user input
        self.input_entry = tk.Entry(root, width=50)
        self.input_entry.pack(pady=5)
        self.input_entry.bind('<Return>', lambda event: self.close_window_and_capture_input())

        # Step 2: Load image using PIL
        screenshot_image = Image.frombytes('RGB', self.screenshot.size, self.screenshot.tobytes())
        # Step 3: Resize the image to fit within the window
        screenshot_image = screenshot_image.resize((300, 300), Image.LANCZOS)
        # Step 4: Convert the image to a Tkinter-compatible format
        photo = ImageTk.PhotoImage(screenshot_image)
        # Step 5: Create a Label widget to display the image
        label = tk.Label(root, image=photo)
        label.pack()
        # Step 6: Run the Tkinter event loop
        # root.after(4000, self.close_show_screenshot)
        self.root = root
        root.mainloop()

    def close_window_and_capture_input(self, event=None):
        global user_input
        user_input = self.input_entry.get()  # Get the user input from the entry widget
        self.root.destroy()  # Destroy the Tkinter window

    def close_show_screenshot(self):
        self.root.destroy()

    def __str__(self):
        try:
            return f"Screenshot Path: {self.screenshot_path}, Borders: {self.borders}"
        except Exception as e:
            return f"Borders: {self.borders}"


class ScreenshotTool(object):
    def __init__(self, app_id, action_id, action_repo_path, is_full_path=False):
        self.app_id = app_id
        self.action_id = action_id
        self.action_repo_path = action_repo_path
        app_action_dir_name = os.path.basename(self.action_repo_path.rstrip('/')) 
        self.app_action_dir_name = app_action_dir_name
        if is_full_path:
            self.screenshots_dir = f"{action_repo_path}/{self.action_id}/all_action_files/screenshots/" 
        else:
            self.screenshots_dir = f"{action_repo_path}/{app_action_dir_name}/{self.action_id}/all_action_files/screenshots/" 
        self.all_taken_screenshot_info = []

    def log_coordinates(self, borders, log_file, screenshot_file_path):
        ending_of_screenshot_file_path = screenshot_file_path.split(f'{self.app_action_dir_name}/')[-1]
        ending_of_screenshot_file_path = f'{ self.app_action_dir_name }/{self.action_id}/all_action_files/screenshots/{ending_of_screenshot_file_path}'
        with open(log_file, 'a') as f:
            log_entry = f"{ending_of_screenshot_file_path} : Point(x={borders[0][0]}, y={borders[0][1]}) : Point(x={borders[1][0]}, y={borders[1][1]})\n"
            f.write(log_entry)

    def take_screenshot_wrapper(self, is_full_screen):
        # try:
        self.take_screenshot(is_full_screen)
        # except Exception as e:
            # print(f"Error while taking screenshot: {e}")
            # self.take_screenshot(is_full_screen)
             
    def take_screenshot(self, is_full_screen):
        # Get the current screen size
        screen_width, screen_height = pyautogui.size()
        if is_full_screen:
            top_left_x1, top_left_y1 = 0, 0
            bottom_right_x2, bottom_right_y2 = screen_width, screen_height
            top_left = (top_left_x1, top_left_y1)
            bottom_right = (bottom_right_x2, bottom_right_y2)
        else:
            root = tk.Tk()
            screen_selection = ScreenSelection(root)
            root.mainloop()
            if not screen_selection.is_selection_success():
                return
            top_left, bottom_right = screen_selection.get_screenshot_coords()

        borders = (top_left, bottom_right)

        # Take screenshot
        width = bottom_right[0] - top_left[0]
        height = bottom_right[1] - top_left[1]
        screenshot = pyautogui.screenshot(region=(top_left[0], top_left[1], width, height))
        screenshot_image = Image.frombytes('RGB', screenshot.size, screenshot.tobytes())
        # (Optional) Resize the screenshot if needed
        screenshot_image = screenshot_image.resize((300, 300), Image.LANCZOS)

        screenshot_info = ScreenshotInfo(borders, screenshot)
        self.all_taken_screenshot_info.append(screenshot_info)

        
    
    def save_screenshot_from_screenshot_info(self, screenshot_info: ScreenshotInfo, screenshot_file_path):
        screenshot = screenshot_info.get_screenshot()
        screenshot_bytes = io.BytesIO()
        screenshot.save(screenshot_bytes, format='PNG')
        screenshot_bytes.seek(0)
        screenshot_file_path += ".png"
        with open(screenshot_file_path, 'wb') as f:
            f.write(screenshot_bytes.getvalue())

    def log_all_screenshots(self):
        global user_input
        screenshot_info: ScreenshotInfo
        for screenshot_info in list(self.all_taken_screenshot_info):  # Create a copy of the list to iterate over
            print(screenshot_info)
            screenshot_info.show_screenshot()
            while user_input is None:
                time.sleep(0.1)
            screenshot_name = user_input
            user_input = None
            screenshot_name = screenshot_name.strip()
            screenshot_path = self.screenshots_dir + screenshot_name
            print(f'screenshot named, screenshot_path: {screenshot_path}')
            screenshot_info.add_screenshot_path(screenshot_path)
            self.save_screenshot_from_screenshot_info(screenshot_info, screenshot_path)
        
            # logs
            borders = screenshot_info.get_borders()
            log_file_path = '/'.join(screenshot_path.split('/')[:-2]) + "/coord_logs.txt"
            self.log_coordinates(borders, log_file_path, screenshot_path)
            
            # Remove the processed element
            self.all_taken_screenshot_info.remove(screenshot_info)
    
    def on_exit(self):
        self.log_all_screenshots()

    def run_pre(self):
        '''
        this is just so other scripts can call this, without calling the specific run method, 
         meant to be used only when iteratively running the script
        '''
        print("Press alt+v to take a fullscreen picture")
        print("Press 'left ctrl+e' key to take a screenshot")
        print("Press 'esc' to quit and name all the screenshots you took") 
        while True:
            # Wait for print screen key
            if keyboard.is_pressed('alt+v'):
                self.take_screenshot_wrapper(is_full_screen=True)
                time.sleep(0.2)

            if keyboard.is_pressed('left ctrl+e'):
                self.take_screenshot_wrapper(is_full_screen=False)
                time.sleep(0.2)

            # Exit on pressing 'esc'
            if keyboard.is_pressed('esc'):
                self.on_exit()
                print("Exiting...")
                break

            # Sleep to reduce CPU usage
            time.sleep(0.1)

    def run(self):
        self.run_pre()


if __name__ == "__main__":
    fire.Fire(ScreenshotTool)

