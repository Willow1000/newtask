import os
from scraper import App


if __name__ == "__main__":
    app = App(action_id='temp', actions_repo=os.getcwd(), is_full_path=True)
    app.run_pre()
     


