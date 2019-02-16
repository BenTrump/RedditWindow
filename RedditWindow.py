import tkinter as tk
import praw
import requests


class DisplayWindow(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.config(relief="sunken", bd=6, width=50, height=50)
        self.frame = tk.Frame(self)
        self.frame.grid(row=10, column=10)


class Main(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0)
        self.reddit = praw.Reddit(client_id="Sij4UW8Tg03-Lg",
                                  client_secret="5U6SrhqxA2jfIL2OolP65G26YFI", user_agent="agent")
        self.subreddit = self.reddit.subreddit("aww")
        self.click = tk.IntVar()
        self.sub_entry_label = tk.Label(root, text="Enter subreddit:", font="Arial 16")
        self.sub_entry_label.grid(row=1, column=0, padx=(10, 0), pady=(10, 0))
        self.sub_entry = tk.Entry(root)
        self.sub_entry.grid(row=1, column=1, padx=(10, 0), pady=(10, 0))
        self.go_to_sub_button = tk.Button(root, text="go", command=self.go_to_sub)
        self.go_to_sub_button.grid(row=1, column=2, padx=(10, 0), pady=(10, 0))
        self.post_title = tk.Label(root, text="", relief="sunken", width=60)
        self.post_title.grid(row=3, column=0, columnspan=5, padx=(10, 0))
        self.back_button = tk.Button(root, text="back")
        self.back_button.grid(row=9, column=1)
        self.next_button = tk.Button(root, text="next", command=self.next_post)
        self.next_button.grid(row=9, column=2)

    def go_to_sub(self):
        self.subreddit = self.reddit.subreddit(self.sub_entry.get())
        for submission in self.subreddit.hot(limit=10):
            self.post_title.config(text=submission.title)
            file_name = "images/picture.jpg"
            r = requests.get(submission.url)
            with open(file_name, "wb") as f:
                f.write(r.content)

            self.click.set(0)
            root.wait_variable(self.click)

    def next_post(self):
        self.click.set(1)


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.main = Main(self)
        #  self.main.grid(row=0, column=0)
        self.display_window = DisplayWindow(self)
        #  self.display_window.grid(row=10, column=10)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x400")
    root.title("Reddit Window")
    MainApplication(root).grid(row=0, column=0)
    root.mainloop()
