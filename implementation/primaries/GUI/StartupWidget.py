from tkinter import *
from tkinter import filedialog, dialog

class StartupWidget(object):

    def __init__(self, root, title="My App"):
        self.root = root
        self.left_frame = LeftFrame()
        self.left_frame.place(relx=0.4, rely=.5, anchor="e")
        self.right_frame = RightFrame()
        self.right_frame.place(relx=0.4, rely=.5, anchor="w")

class LeftFrame(Frame):
    def __init__(self):
        Frame.__init__(self, bg="#EEE", bd=10, width=300, height=400)
        frameText = Label(self, bg="#EEE", text="Previous Collections",font=("Calibri",20))
        frameText.place(relx=0.4, rely=0.1, anchor="n")
        box = Listbox(self, bg="#EEE", width=30)
        box.insert(0, "hello world")
        box.place(relx=0.5, rely=0.6, anchor="c")

class RightFrame(Frame):
    def __init__(self):
        Frame.__init__(self,bg="#DDD",width=450, height=400)
        frameText = Label(self, bg="#DDD", text="Welcome to MuseLib", font=("Calibri",20,"bold"))
        frameText.place(relx=0.4, rely=0.1, anchor="n")
        frameTwo = Label(self, bg="#DDD", text="Please select a folder to store your collection in, \nor open one of your previous collections from the list on the left", font=("Purisa",15))
        frameTwo.place(relx=0.5, rely=0.3, anchor="c")
        btn = Button(self, text='Select Folder...', command=self.askopenfile)
        btn.place(relx=0.5, rely=0.4, anchor="c")


    def askopenfile(self):
        folder = filedialog.askdirectory()
        return folder

def main():

    root = Tk()
    root.wm_resizable(0,0)
    root.wm_title("MuseLib | Landing")
    root.grid_columnconfigure(index=0, minsize=100)
    root.grid_columnconfigure(index=0, minsize=400)
    root.grid_propagate(True)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 750
    window_height = 400
    left_offset = screen_width/2-(window_width/2)
    top_offset = screen_height/2-(window_height/2)+20
    root.geometry(str(window_width)+"x"+str(window_height)+"+"+str(int(left_offset))+"+"+str(int(top_offset)))
    app = StartupWidget(root)
    root.mainloop()



if __name__ == '__main__':
    main()