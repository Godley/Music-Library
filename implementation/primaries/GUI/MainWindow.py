from tkinter import *
from tkinter import filedialog, dialog

class MainWindow(object):
    def __init__(self, root):
        self.root = root
        Search = CloseableFrame(self, background="#333", name="Search",height=80)
        Search.place(relx=0.0)
        ScoreBook = CloseableFrame(self, background="#333", name="Scorebook",height=300)
        ScoreBook.place(relx=0.0,rely=0.103)
        MyPlaylists = CloseableFrame(self, background="#333", name="My Playlists", height=300)
        MyPlaylists.place(relx=0.0,rely=0.485)
class CloseableFrame(Frame):
    def __init__(self, root, **kwargs):
        self.width=350
        self.height=350
        self.background="white"
        self.name="frame"
        if "background" in kwargs:
            self.background = kwargs["background"]
        if "name" in kwargs:
            self.name = kwargs["name"]
        if "width" in kwargs:
            self.width = kwargs["width"]
        if "height" in kwargs:
            self.height = kwargs["height"]
        Frame.__init__(self, width=self.width, height=self.height, bg=self.background, bd=5)
        title_label = Label(self, text=self.name, bg=self.background, fg="#222", font=("Purisa",15))
        title_label.place(relx=0.4, rely=0.0)
        xButton = Label(self, text="x", bg=self.background, fg="#222")
        xButton.place(relx=0.0,rely=0.0)
        xButton.bind("<Button-1>", self.quit)


    def quit(self, event):
        self.destroy()



def main():
    root = Tk()
    root.configure(background="#444")
    root.wm_title("MuseLib")
    root.grid_columnconfigure(index=0, minsize=100)
    root.grid_columnconfigure(index=0, minsize=400)
    root.grid_propagate(True)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = screen_width
    window_height = screen_height-110
    left_offset = 0
    top_offset = 0
    root.geometry(str(window_width)+"x"+str(window_height)+"+"+str(int(left_offset))+"+"+str(int(top_offset)))
    app = MainWindow(root)
    root.mainloop()



if __name__ == '__main__':
    main()
