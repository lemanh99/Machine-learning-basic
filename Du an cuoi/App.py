from lib import *

width = 500
height = 500
center = height//2
black = (0, 0, 0)
green = (0,128,0)

class main:
    def __init__(self,master):
        self.master = master
        self.color_fg = 'black'
        self.color_bg = 'white'
        self.old_x = None
        self.old_y = None
        self.penwidth = 5
        self.button_fr = None
        self.writter = None
        self.model = self.load_model()
        self.drawWidgets()
        self.c.bind('<B1-Motion>',self.paint)#drwaing the line 
        self.c.bind('<ButtonRelease-1>',self.reset)
        self.image = Image.new("RGB", (width, height), black)
        self.draw = ImageDraw.Draw(self.image)


    def load_model(self, model_path = './model/model.pkl'):
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        return model

    def img_preprocessing(self, image):
        image = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(image, (28,28))
        image= image.reshape(1, -1)
        return image

    def predict(self):
        self.save()
        image = self.img_preprocessing('image.png')
        y_pred = self.model.predict(image)
        self.writter = Label(self.control, text='This number is '+y_pred[0],font=('arial 14'), fg = 'red').grid(row=0,column=0)
        

    def save(self):
        filename = "image.png"
        newsize = (28, 28) 
        self.image = self.image.resize(newsize)
        self.image.save(filename)

    def paint(self,e):

        if self.old_x and self.old_y:
            self.c.create_line(self.old_x,self.old_y,e.x,e.y,width=self.penwidth,fill=self.color_fg,capstyle=ROUND,smooth=True)
            self.draw.line([self.old_x,self.old_y,e.x,e.y], fill='white',width=50)
        self.old_x = e.x
        self.old_y = e.y

    def reset(self,e):    #reseting or cleaning the canvas
        self.old_x = None
        self.old_y = None      

    def clear(self):
        self.writter = Label(self.control, text='', width =50).grid(row=0,column=0)
        self.image = Image.new("RGB", (width, height), black)
        self.draw = ImageDraw.Draw(self.image)
        self.c.delete(ALL)

    def change_fg(self):  #changing the pen color
        self.color_fg=colorchooser.askcolor(color=self.color_fg)[1]

    def change_bg(self):  #changing the background color canvas
        self.color_bg=colorchooser.askcolor(color=self.color_bg)[1]
        self.c['bg'] = self.color_bg

    def drawWidgets(self):


        self.control = Frame(self.master,padx = 5,pady = 5)
        self.writter = Label(self.control, text='',font=('arial 18'), width=5).grid(row=0,column=0)
        self.control.pack(side=TOP)

        self.controls = Frame(self.master,padx = 5,pady = 5)
        self.button = ttk.Button(self.controls, text = 'Predict', command= self.predict)
        self.button.grid(row=0,column=1,ipadx=30)

        self.btn_clear = ttk.Button(self.controls, text = 'Clear', command=self.clear)
        self.btn_clear.grid(row=0,column=2,ipadx=30)
        self.controls.pack(side=BOTTOM)
        
        self.c = Canvas(self.master,width=500,height=500,bg=self.color_bg,)
        self.c.pack(fill=BOTH,expand=True)


        menu = Menu(self.master)
        self.master.config(menu=menu)
        filemenu = Menu(menu)
        colormenu = Menu(menu)
        menu.add_cascade(label='Colors',menu=colormenu)
        colormenu.add_command(label='Brush Color',command=self.change_fg)
        colormenu.add_command(label='Background Color',command=self.change_bg)
        optionmenu = Menu(menu)
        menu.add_cascade(label='Options',menu=optionmenu)
        optionmenu.add_command(label='Clear Canvas',command=self.clear)
        optionmenu.add_command(label='Exit',command=self.master.destroy)

        
        

        

if __name__ == '__main__':
    root = Tk()
    main(root)
    root.title('Application')
    root.mainloop()