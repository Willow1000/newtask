import fire 
import os
import customtkinter
from PIL import Image, ImageTk
from scraper_libs.sprite_scraper_view import SpriteScraperView

class App():
    WIDTH = 680
    HEIGHT = 480
    DEFAULT_GRAY = ("gray50", "gray30")
    def __init__(self, action_id, actions_repo, is_full_path: bool = False):
        super().__init__()
        self.action_id = action_id
        self.data_path = actions_repo
        app_action_dir_name = os.path.basename(self.data_path.rstrip('/'))
        if is_full_path:
            self.data_path = f"{self.data_path}/{self.action_id}" 
        else:
            self.data_path = f"{self.data_path}/{app_action_dir_name}/{self.action_id}" 

    def start_scraper(self):
        # window = customtkinter.CTkToplevel(master=self)
        window = customtkinter.CTk()
        window.title('item finder')
        window.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        window.update()
        view = SpriteScraperView(self.action_id, self.data_path, parent=window)
        view.pack(side="top", fill="both", expand=True, padx=20, pady=20)
        window.after(100, window.lift)  # Workaround for bug where main window takes focus
        window.mainloop()

    def run_pre(self):
        self.start_scraper()
     
    def run(self):
        self.run_pre()

if __name__ == "__main__":
    fire.Fire(App)


