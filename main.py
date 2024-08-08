import tkinter as tk
from ui.splash_screen import SplashScreen
from ui.main_window import MainWindow
from data.data_manager import DataManager
from utils.logger import setup_logger
import queue
import threading

def main():
    logger = setup_logger()
    try:
        root = tk.Tk()
        root.withdraw()

        data_manager = DataManager()
        task_queue = queue.Queue()

        splash = SplashScreen(root)
        main_window = MainWindow(root, data_manager)

        root.bind("<<InitComplete>>", lambda e: on_init_complete(root, splash, main_window))

        init_thread = threading.Thread(target=initialize_app, args=(task_queue, data_manager))
        init_thread.start()

        root.after(100, update_splash, root, splash, task_queue)

        root.mainloop()
    except Exception as e:
        logger.error(f"An unexpected error occurred in main: {e}")
    finally:
        if 'root' in locals():
            root.destroy()

def initialize_app(queue, data_manager):
    tasks = [
        ("Connecting to Google...", 20, lambda: None),
        ("Loading GUI...", 40, lambda: None),
        ("Fetching Data...", 60, data_manager.get_data),
        ("Starting...", 80, lambda: None),
        ("Complete", 100, lambda: None)
    ]

    for message, progress, task_func in tasks:
        queue.put((message, progress))
        task_func()

    queue.put(("DONE", None))

def update_splash(root, splash, task_queue):
    try:
        message, progress = task_queue.get(block=False)
        if message == "DONE":
            root.event_generate("<<InitComplete>>")
        else:
            splash.update_status(message, progress)
            root.after(100, update_splash, root, splash, task_queue)
    except queue.Empty:
        root.after(100, update_splash, root, splash, task_queue)

def on_init_complete(root, splash, main_window):
    splash.destroy()
    root.deiconify()
    main_window.setup()

if __name__ == "__main__":
    main()
