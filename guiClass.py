from tkinter import  *
from explosmClass import *
from PIL import Image, ImageTk

class Window(Frame):
    global current_comic
    global img
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        Window.current_comic = starting_comic
    def init_window(self):
        self.master.title("C & H")
        self.pack(fill = BOTH, expand = 1)

        prevButton = Button(self, text="PREVIOUS", command = self.prev_comic, width=10)
        prevButton.place(x=50, y=0)

        nextButton = Button(self, text="NEXT", command = self.next_comic, width=10)
        nextButton.place(x=350, y=0)

        dbgButton = Button(self, text = "INFO", command = self.dbg, width = 10)
        dbgButton.place(x=150, y=0)

        menu = Menu(self.master)
        self.master.config(menu = menu)

        file = Menu(menu)
        file.add_command(label='Exit', command=self.client_exit)
        menu.add_cascade(label='File', menu=file)
        self.show_img(starting_comic.title)
    def dbg(self):
        print(Window.current_comic)

    def show_img(self, path):
        scale = 1/2

        load = Image.open(path) #ovde samo menjam putanju za nove slike
        [loadSizeWidth, loadSizeHeight] = load.size
        ratio = loadSizeWidth/loadSizeHeight
        print(loadSizeWidth, loadSizeHeight)
        print('W x H, ratio', ratio)

        if loadSizeWidth>loadSizeHeight:
            newLoadSizeWidth = 650
            newLoadSizeHeight = int(loadSizeHeight* 1/ratio)
        elif loadSizeWidth<= loadSizeHeight:
            newLoadSizeHeight = 650
            newLoadSizeWidth =  int(newLoadSizeHeight * ratio)

        load = load.resize((newLoadSizeWidth, newLoadSizeHeight), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        Window.img = Label(self, image=render)
        Window.img.image = render
        Window.img.place(x=10, y=30)

    def show_text(self):
        text = Label(self, text = 'THIS IS LAST COMIC')
        text.place(x=150, y=0)

    def prev_comic(self):
        Window.img.destroy()
        prevNumb = Window.current_comic.previous
        new_comic = Comic(prevNumb)
        new_comic.get_all_data()
        new_comic.download_img()
        self.show_img(new_comic.title)
        Window.current_comic = new_comic

    def next_comic(self):
        Window.img.destroy()
        nextNumb = Window.current_comic.next
        new_comic = Comic(nextNumb)
        new_comic.get_all_data()
        new_comic.download_img()

        self.show_img(new_comic.title)
        Window.current_comic = new_comic

        if(latest_id == Window.current_comic.comic_id):
            self.show_text()

    def client_exit(self):
        exit()
root = Tk()
root.geometry("700x700")
app = Window(root);
root.mainloop()