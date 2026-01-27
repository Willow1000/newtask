import fire
import os

from take_screenshots import ScreenshotTool


class ScreenshotUIRunescape(object):
    def __init__(self):
        self.app_id = "runescape"
        self.action_id = "temp"
        self.action_repo_name = './'
        # self.action_repo_name = os.path.basename(self.action_repo_name) 

    def run(self):
        st = ScreenshotTool(self.app_id, self.action_id, self.action_repo_name, is_full_path=True)
        st.run_pre()


if __name__ == "__main__":
    ScreenshotUIRunescape().run()


