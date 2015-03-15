from tkinter import *
from PIL import Image, ImageTk



class DarkFrame(Frame):
    def __init__(self, root, **kwargs):
        self.width=350
        self.height=350
        self.background="white"
        self.name="frame"
        self.textcolor = "#666"
        self.textHighlight = "#888"
        if "background" in kwargs:
            self.background = kwargs["background"]
        if "name" in kwargs:
            self.name = kwargs["name"]
        if "width" in kwargs:
            self.width = kwargs["width"]
        if "height" in kwargs:
            self.height = kwargs["height"]
        Frame.__init__(self, width=self.width, height=self.height, bg=self.background, bd=5)
        title_label = Label(self, text=self.name, bg=self.background, fg=self.textcolor, font=("Purisa",15))
        title_label.bind("<Enter>", lambda e: e.widget.config(fg=self.textHighlight))
        title_label.bind("<Leave>", lambda e: e.widget.config(fg=self.textcolor))
        title_label.place(relx=0.4, rely=0.0)

class CloseableFrame(DarkFrame):
    def __init__(self, root, **kwargs):
        DarkFrame.__init__(self, root, **kwargs)
        xButton = Label(self, text="x", bg=self.background, fg="#222")
        xButton.place(relx=0.0,rely=0.0)
        xButton.bind("<Button-1>", self.quit)


    def quit(self, event):
        self.destroy()

class GenPlaylist(CloseableFrame):
    def __init__(self, root, **kwargs):
        CloseableFrame.__init__(self, root, **kwargs)
        piece_list = Listbox(self, bg=self.background, height=8,width=37)
        piece_list.place(relx=0.05,rely=0.15)
        self.refresh = Image.open("images/glyphicons-82-refresh.png")
        self.tkpi = ImageTk.PhotoImage(self.refresh)
        refresh_label = Label(self, width=self.refresh.size[0], height=self.refresh.size[1], image=self.tkpi)
        refresh_label.place(relx=0.9, rely=0.0)
        refresh_label.bind("<Button-1>",self.refresh_playlists)

    def refresh_playlists(self, event):
        print("refresh")
        pass


class ScoreBook(GenPlaylist):
    pass

class MainWindow(object):
    def __init__(self, root):
        self.root = root
        Search = DarkFrame(self, background="#333", name="Search",height=80, width=300)
        Search.place(relx=0.0)
        ScoreBook = GenPlaylist(self, background="#333", name="Scorebook",height=300, width=300)
        ScoreBook.place(relx=0.0,rely=0.103)
        MyPlaylists = CloseableFrame(self, background="#333", name="My Playlists", height=200,width=300)
        MyPlaylists.place(relx=0.0,rely=0.485)
        GenPlaylists = GenPlaylist(self, background="#333", name="Auto-Playlists", height=200,width=300)
        GenPlaylists.place(relx=0.0,rely=0.741)
        PieceInfo = CloseableFrame(self, background="#333", name="Piece Information", height=450, width=300)
        PieceInfo.place(relx=0.79, rely=0.0)
        PlaylistFeature = CloseableFrame(self, background="#333", name="Features in...", height=200, width=300)
        PlaylistFeature.place(relx=0.79, rely=0.573)

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
