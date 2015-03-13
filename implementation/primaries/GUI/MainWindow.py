from tkinter import *



class StartupWidget(object):

    def __init__(self, root, title="My App"):
        self.root = root
        self.root.title = title
        self.left_frame = LeftFrame()
        self.left_frame.grid(row=0,column=0)
        self.right_frame = RightFrame()
        self.right_frame.grid(row=0,column=1, pady=100)

class LeftFrame(Frame):
    def __init__(self):
        Frame.__init__(self, bg="#EEE", bd=10, width=300, height=400)


class RightFrame(Frame):
    def __init__(self):
        Frame.__init__(self,width=450, height=400, bg="#DDD")
        frameText = Label(self, bg="#DDD", text="Welcome to MuseLib", font=("Purisa",20,"bold"))
        frameTwo = Label(self, bg="#DDD", text="Please select a folder to store your collection in, \nor open one of your previous collections from the list on the left", font=("Purisa",15))
        frameText.grid(row=0,column=0, padx=0)
        frameTwo.grid(row=1,column=0)
        #file = tkFileDialog.askopenfile(parent=self,mode='rb',title='Choose a file')


def main():

    root = Tk()
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