import tkinter as tk
import praw
import requests
from PIL import Image, ImageTk
from prawcore import NotFound

# Todo: add gif support
# Todo: quit main for loop when you enter a new subreddit


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

    def display_nopicture(self):
        image = Image.open("reddit_logo.jpg").resize((338, 388), Image.ANTIALIAS)
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
        self.click = tk.IntVar()
        self.sub_entry_label = tk.Label(self.frame, text="Enter subreddit:", font="Arial 16")
        self.sub_entry_label.grid(row=0, column=0, padx=(10, 0), pady=(0, 20))
        self.sub_entry = tk.Entry(self.frame, font="Arial 14")
        self.sub_entry.grid(row=0, column=1, columnspan=4, padx=(0, 20), pady=(0, 20), sticky=tk.E + tk.W)
        self.go_to_sub_button = tk.Button(self.frame, text="GO", command=self.go_to_sub)
        self.go_to_sub_button.config(font="Arial 20", bg="#61f9ad")
        self.go_to_sub_button.grid(row=2, column=0, columnspan=10, padx=(10, 10), pady=(10, 20), sticky=tk.E + tk.W)
        self.post_title = tk.Label(self.frame, text="", relief="sunken", width=60, height=4, wraplength=400)
        self.post_title.grid(row=3, column=0, columnspan=5, padx=(10, 10))
        self.back_button = tk.Button(self.frame, text="Back", command=self.last_post)
        self.back_button.config(font="Arial 20")
        self.back_button.grid(row=9, column=0, columnspan=2, pady=(20, 0), padx=(10, 70), sticky=tk.E + tk.W)
        self.next_button = tk.Button(self.frame, text="Next", command=self.next_post)
        self.next_button.config(font="Arial 20")
        self.next_button.grid(row=9, column=2, columnspan=3, pady=(20, 0), padx=(0, 10), sticky=tk.E + tk.W)

    def go_to_sub(self):
        if not self.sub_entry.get() or not self.sub_exists(self.sub_entry.get()):
            return
        for submission in self.reddit.subreddit(self.sub_entry.get()).hot(limit=50):
            try:
                self.post_title.config(text=submission.title)
            except tk.TclError:  # emojis in the title...
                continue
            file_name = "picture.jpg"
            r = requests.get(submission.url)
            with open(file_name, "wb") as f:
                f.write(r.content)
            try:
                self.gui.display_window.display_picture()
            except OSError:
                self.gui.display_window.display_nopicture()
                print("no picture found")

            self.click.set(0)
            self.frame.wait_variable(self.click)

    def sub_exists(self, sub):
        exists = True
        try:
            self.reddit.subreddits.search_by_name(sub, exact=True)
        except NotFound:
            exists = False
            print("Subreddit does not exist")
        return exists

    def next_post(self):
        self.click.set(1)

    def last_post(self):
        # Todo: Add stuff to this
        print("Last post")
        pass

    # Todo: Why does this work? Whats better syntax?
    def right_arrow(self, _):
        self.next_post()

    def left_arrow(self, _):
        self.last_post()

    def enter_key(self, __):
        self.go_to_sub()


class GUI(object):
    def __init__(self):
        self.master_frame = tk.Tk()
        self.master_frame.title("Reddit Window")
        self.master_frame.geometry("800x400")
        self.main = Main(self)
        self.display_window = DisplayWindow(self)
        self.master_frame.bind("<Right>", self.main.right_arrow)
        self.master_frame.bind("<Left>", self.main.left_arrow)
        self.master_frame.bind("<Return>", self.main.enter_key)
        self.master_frame.bind("<Escape>", self.exit_gui)

        self.master_frame.mainloop()

    def exit_gui(self, _):
        self.master_frame.destroy()


my_gui = GUI()
