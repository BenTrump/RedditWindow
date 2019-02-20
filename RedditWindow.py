import tkinter as tk
import praw
import requests
from PIL import Image, ImageTk


class DisplayWindow(tk.Frame):
    def __init__(self, gui, *args, **kw):
        tk.Frame.__init__(self, master=gui.master_frame, *args, **kw)
        self.gui = gui
        self.grid(row=0, column=1)
        self.frame = tk.Frame(self)
        self.frame.grid()
        self.frame.config(relief="sunken", height=400, width=350, bd=6)

    def display_picture(self):
        image = Image.open("picture.jpg").resize((338, 388), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        display = tk.Label(self.frame, image=image)
        display.image = image
        display.grid(row=0, column=0)


class Main(tk.Frame):
    def __init__(self, gui, *args, **kwargs):
        tk.Frame.__init__(self, master=gui.master_frame, *args, **kwargs)
        self.gui = gui
        self.grid(row=0, column=0)
        self.frame = tk.Frame(self, height=400, width=400)
        self.frame.grid(row=0, column=0)
        self.reddit = praw.Reddit(client_id="Sij4UW8Tg03-Lg",
                                  client_secret="5U6SrhqxA2jfIL2OolP65G26YFI", user_agent="agent")
        self.subreddit = self.reddit.subreddit("aww")
        self.click = tk.IntVar()
        self.sub_entry_label = tk.Label(self.frame, text="Enter subreddit:", font="Arial 16")
        self.sub_entry_label.grid(row=1, column=0, padx=(10, 0), pady=(10, 0))
        self.sub_entry = tk.Entry(self.frame)
        self.sub_entry.grid(row=1, column=1, padx=(10, 0), pady=(10, 0))
        self.go_to_sub_button = tk.Button(self.frame, text="go", command=self.go_to_sub)
        self.go_to_sub_button.grid(row=1, column=2, padx=(10, 0), pady=(10, 0))
        self.post_title = tk.Label(self.frame, text="", relief="sunken", width=60)
        self.post_title.grid(row=3, column=0, columnspan=5, padx=(10, 0))
        self.back_button = tk.Button(self.frame, text="back")
        self.back_button.grid(row=9, column=1)
        self.next_button = tk.Button(self.frame, text="next", command=self.next_post)
        self.next_button.grid(row=9, column=2)

    def go_to_sub(self):
        self.subreddit = self.reddit.subreddit(self.sub_entry.get())
        for submission in self.subreddit.hot(limit=100):
            self.post_title.config(text=submission.title)
            file_name = "picture.jpg"
            r = requests.get(submission.url)
            with open(file_name, "wb") as f:
                f.write(r.content)

            try:
                self.gui.display_window.display_picture()
            except:
                print("didnt work")
                continue

            self.click.set(0)
            self.frame.wait_variable(self.click)

    def next_post(self):
        self.click.set(1)


class GUI(object):
    def __init__(self):
        self.master_frame = tk.Tk()
        self.master_frame.title("Reddit Window")
        self.master_frame.geometry("800x400")
        self.main = Main(self)
        self.display_window = DisplayWindow(self)

        self.master_frame.mainloop()


my_gui = GUI()
