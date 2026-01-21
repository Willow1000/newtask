import json
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from typing import Dict, Any, List, Union
 
class JSONEditorApp:
    def __init__(self, root, load_json_file_path:str, save_json_file_path:str):
        self.root = root
        self.root.title("JSON Editor")
        self.root.geometry("900x700")
        
        self.json_data = {}
        self.input_widgets = {}

        # Add a message label at the top
        self.message_frame = ttk.Frame(root)
        self.message_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.message_label = ttk.Label(
            self.message_frame, 
            text=f"Welcome to JSON Editor.\nyou are editing {load_json_file_path} \nany int values you set with -1 will be ignored, and not changed",
            font=("Helvetica", 10, "bold"),
            foreground="red"
        )
        self.message_label.pack(fill=tk.X)
        
        # Create main frame with scrollbar
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Add scrollbar
        self.canvas = tk.Canvas(self.main_frame)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Control buttons
        self.button_frame = ttk.Frame(root)
        self.button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.save_json_file_path = save_json_file_path
        self.load_json(load_json_file_path)
         
        self.save_button = ttk.Button(self.button_frame, text="Save JSON", command=self.save_json)
        self.save_button.pack(side=tk.LEFT, padx=5)
    
    def load_json(self, file_path):
        if not file_path:
            return
        self.file_path = file_path
        try:
            with open(file_path, "r") as file:
                self.json_data = json.load(file)

            # Clear previous widgets
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            
            self.input_widgets = {}
            
            # Create UI elements based on JSON structure
            self.create_ui_for_json(self.json_data, "", self.scrollable_frame)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load JSON file: {str(e)}")
    
    def create_ui_for_json(self, data, path_prefix, parent_frame):
        if isinstance(data, dict):
            for key, value in data.items():
                current_path = f"{path_prefix}.{key}" if path_prefix else key
                
                # Create a labeled frame for each dictionary
                frame = ttk.LabelFrame(parent_frame, text=key)
                frame.pack(fill=tk.X, padx=10, pady=5, anchor=tk.W)
                
                if isinstance(value, (dict, list)):
                    self.create_ui_for_json(value, current_path, frame)
                else:
                    self.create_input_for_value(current_path, value, frame)
                    
        elif isinstance(data, list):
            for i, item in enumerate(data):
                current_path = f"{path_prefix}[{i}]"
                
                # Create a labeled frame for each list item
                frame = ttk.LabelFrame(parent_frame, text=f"Item {i}")
                frame.pack(fill=tk.X, padx=10, pady=5, anchor=tk.W)
                
                if isinstance(item, (dict, list)):
                    self.create_ui_for_json(item, current_path, frame)
                else:
                    self.create_input_for_value(current_path, item, frame)
    
    def create_input_for_value(self, path, value, parent_frame):
        frame = ttk.Frame(parent_frame)
        frame.pack(fill=tk.X, padx=5, pady=2)
        
        # Extract the key name from the path
        key_name = path.split(".")[-1]
        if "[" in key_name:
            key_name = "Index " + key_name.split("[")[1].replace("]", "")
        
        # Create label
        label = ttk.Label(frame, text=f"{key_name}:", width=20, anchor=tk.W)
        label.pack(side=tk.LEFT, padx=5)
        
        # Create appropriate input widget based on value type
        if isinstance(value, bool):
            var = tk.BooleanVar(value=value)
            input_widget = ttk.Checkbutton(frame, variable=var, onvalue=True, offvalue=False)
            self.input_widgets[path] = var
        elif isinstance(value, int):
            var = tk.StringVar(value=str(value))
            input_widget = ttk.Spinbox(frame, from_=-10000, to=10000, textvariable=var)
            self.input_widgets[path] = var
        elif isinstance(value, float):
            var = tk.StringVar(value=str(value))
            input_widget = ttk.Spinbox(frame, from_=-10000.0, to=10000.0, increment=0.1, textvariable=var)
            self.input_widgets[path] = var
        else:
            var = tk.StringVar(value=str(value))
            input_widget = ttk.Entry(frame, textvariable=var)
            self.input_widgets[path] = var
        
        input_widget.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Add type indicator
        type_label = ttk.Label(frame, text=f"({type(value).__name__})", width=10)
        type_label.pack(side=tk.LEFT, padx=5)
    
    def save_json(self):
        if not self.json_data:
            messagebox.showwarning("Warning", "No JSON data to save")
            return
        
        try:
            # Update JSON data with UI values
            for path, widget_var in self.input_widgets.items():
                value = widget_var.get()
                self.update_json_value(path, value)
            
            with open(self.save_json_file_path, "w") as file:
                json.dump(self.json_data, file, indent=4)
            
            messagebox.showinfo("Success", f"JSON saved successfully to {self.save_json_file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save JSON: {str(e)}")
    
    def update_json_value(self, path, value):
        # Convert the path string into a series of keys/indices
        parts = []
        current = ""
        in_bracket = False
        
        for char in path:
            if char == "." and not in_bracket:
                if current:
                    parts.append(current)
                    current = ""
            elif char == "[":
                if current:
                    parts.append(current)
                    current = ""
                in_bracket = True
            elif char == "]":
                if current:
                    parts.append(int(current))
                    current = ""
                in_bracket = False
            else:
                current += char
        
        if current:
            parts.append(current if not in_bracket else int(current))
        
        # Navigate to the correct position in the JSON structure
        target = self.json_data
        for i, part in enumerate(parts[:-1]):
            if isinstance(target, dict):
                if part not in target:
                    target[part] = {} if isinstance(parts[i+1], str) else []
                target = target[part]
            elif isinstance(target, list):
                while len(target) <= part:
                    target.append({} if isinstance(parts[i+1], str) else [])
                target = target[part]
        
        # Convert value to appropriate type
        last_part = parts[-1]
        if last_part in target or (isinstance(target, list) and isinstance(last_part, int)):
            # Get the current value to determine its type
            if isinstance(target, dict):
                current_value = target.get(last_part)
            else:
                current_value = target[last_part] if last_part < len(target) else None
            
            # Convert the new value to the same type as the current value
            if isinstance(current_value, bool):
                if isinstance(value, bool):
                    converted_value = value
                else:
                    converted_value = value.lower() in ('true', 'yes', '1', 'y')
            elif isinstance(current_value, int):
                try:
                    converted_value = int(value)
                except ValueError:
                    converted_value = 0
            elif isinstance(current_value, float):
                try:
                    converted_value = float(value)
                except ValueError:
                    converted_value = 0.0
            else:
                converted_value = value
            
            # Update the value
            if isinstance(target, dict):
                target[last_part] = converted_value
            else:
                while len(target) <= last_part:
                    target.append(None)
                target[last_part] = converted_value
                 
                 
if __name__ == "__main__":
    root = tk.Tk()
    json_load_file_path = sys.argv[1]
    json_save_file_path = sys.argv[2]
    app = JSONEditorApp(root, json_load_file_path, json_save_file_path)
    root.mainloop()

