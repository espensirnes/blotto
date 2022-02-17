import tkinter as tk
import time
from tkinter.constants import S
from PIL import ImageTk, Image
import numpy as np
WIDTH = 800
HEIGHT = 500
BALLWITH=90

N_FIELDS=6




def create_image(imgfile,alpha=1,size=1.0):
    opacity_level=int(alpha*255)
    img=Image.open(imgfile)
    if size<1.0:
        s=img.size
        img=img.resize((int(s[0]*size), int(s[1]*size)), Image.ANTIALIAS)

    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[3] < opacity_level:
            newData.append(item)
        else:
            item=(item[0],item[1],item[2],opacity_level)
            newData.append(item)

    img.putdata(newData)
    img=ImageTk.PhotoImage(img)
    return img


class tanks:
    def __init__(self,master,imgfile,x=20,y=20):
        self.x=x
        self.y=y
        self.speedx = 5
        self.speedy = 5
        self.master=master
        self.img=create_image(imgfile,size=0.5)
        self.shape = master.create_image(self.x,self.y,anchor=tk.NW, image=self.img)


    def ball_update(self):
        self.x+=self.speedx
        self.y+=self.speedy
        self.master.moveto(self.shape, self.x, self.y)

        if self.x >= WIDTH-BALLWITH or self.x <= 0:
            self.speedx *= -1
        if self.y >= HEIGHT-BALLWITH or self.y <= 0:
            self.speedy *= -1

    def delete(self):
        self.master.delete(self.shape)

class battle_field(tk.Canvas):
    def __init__(self,master,n_battalions, win):
        tk.Canvas.__init__(self,master,bg='pink')
        self.master=master
        self.n_battalions=n_battalions
        self.battalion_objects_player=[]
        self.battalion_objects_computer=[]
        self.win=win


        #Adding fields:
        self.battalion_stand_computer=tk.Canvas(self,bg='grey', height=180)
        self.playing_field=tk.Canvas(self,bg='orange')
        self.battalion_stand_player=tk.Canvas(self,bg='grey', height=180)

        #Adding buttons
        self.button_pluss=tk.Button(self,text='+',font="Courier 20 bold",
            command=self.pluss_player
            )
        self.button_minus=tk.Button(self,text='-',font="Courier 20 bold",
            command=self.minus_player
            )

        #Information about number of battalions for player:
        self.info_txt_player=tk.StringVar(self)
        self.info_player=tk.Label(self,textvariable=self.info_txt_player,font="Courier 20 bold",justify=tk.LEFT,anchor=tk.W)
        self.info_txt_player.set(0)

        #Information about number of battalions for computer:
        self.info_txt_computer=tk.StringVar(self)
        self.info_computer=tk.Label(self,textvariable=self.info_txt_computer,font="Courier 20 bold",justify=tk.LEFT,anchor=tk.W)
        self.info_txt_computer.set(0)

        self.columnconfigure(0,weight=1)
        for i,w in [(0,1),(1,1), (2,8), (3,1), (4,1), (5,1),(6,1)]:
            self.rowconfigure(i,weight=w)

        self.info_computer.grid(column=0,               row=0,sticky=tk.NSEW)
        self.battalion_stand_computer.grid(column=0,    row=1,sticky=tk.NSEW)
        self.playing_field.grid(column=0,               row=2,sticky=tk.NSEW)
        self.battalion_stand_player.grid(column=0,      row=3,sticky=tk.NSEW)
        self.button_pluss.grid(column=0,                row=4,sticky=tk.NSEW)
        self.button_minus.grid(column=0,                row=5,sticky=tk.NSEW)
        self.info_player.grid(column=0,                 row=6,sticky=tk.NSEW)
        
    def pluss_player(self):
        if self.win.get_battalions_left()==0:
            self.win.message('You have no more battalions to deploy')
            return
        self.win.message('')
        self.pluss(self.battalion_objects_player, self.battalion_stand_player,self.info_txt_player)
        self.win.computer_reaction()

    def minus_player(self):
        self.win.message('')
        self.minus(self.battalion_objects_player,self.info_txt_player)
        self.win.computer_reaction()

    def set_player(self,n_battalions):
        self.set(n_battalions, self.battalion_objects_player, self.battalion_stand_player,self.info_txt_player)

    def pluss_computer(self):
        if self.win.get_battalions_left(False)==0:
            return
        self.pluss(self.battalion_objects_computer, self.battalion_stand_computer,self.info_txt_computer)

    def minus_computer(self):
        self.minus(self.battalion_objects_computer,self.info_txt_computer)

    def set_computer(self,n_battalions):
        self.set(n_battalions, self.battalion_objects_computer, self.battalion_stand_computer,self.info_txt_computer)

    def set(self,n_battalions,battalions,battalion_stand, info):
        while n_battalions>len(battalions) and self.win.get_battalions_left(False)>0:
            self.pluss(battalions,battalion_stand,info)
        while n_battalions<len(battalions):
            self.minus(battalions,info)



    def pluss(self,battalions,battalion_stand,info):
        CDIST=40
        RDIST=40
        NCOLS=6

        row=int(len(battalions)/NCOLS)
        x=(len(battalions)-row*NCOLS)*CDIST
        y=10+row*RDIST
        battalions.append(tanks(battalion_stand,'tanks.png',x,y))
        info.set(len(battalions))
        self.win.battalions_left.set(f'Remaining Battalions: {self.win.get_battalions_left()}')


    def minus(self,battalions,info):
        if len(battalions)==0:
            return
        battalions.pop().delete()
        self.info_txt_player.set(len(battalions))
        self.win.battalions_left.set(f'Remaining Battalions: {self.win.get_battalions_left()}')





class window(tk.Tk):
    def __init__(self,n_fields,n_battalions, computer_strategy=None):
        tk.Tk.__init__(self)
        self.title("Blotto")
        self.geometry('%sx%s+%s+%s' %(self.winfo_screenwidth(),self.winfo_screenheight()-75,-5,0))
        self.n_fields=n_fields
        self.n_battalions=n_battalions
        self.mean_battalions=int(self.n_battalions/n_fields)
        self.battlefields=[]
        if computer_strategy is None:
            self.computer_strategy=default_computer_strategy
        else:
            self.computer_strategy=computer_strategy

        
        #Defining main areas:
        self.battlefields_canvas=tk.Canvas(self,bg="yellow")
        self.controls=tk.Canvas(self,bg="red")

        #Defining attack button:
        self.button_attack=tk.Button(self.controls,command=self.attack, text="Attack",font="Courier 20 bold")

        #Defining information text containers:
        self.output=tk.Canvas(self.controls,bg="blue")
        self.output_text=tk.StringVar(self)
        self.output_label=tk.Label(self.output,textvariable=self.output_text,font="Courier 20 bold",justify=tk.LEFT,anchor=tk.W,width=30)
        self.battalions_left=tk.StringVar(self)
        self.battalions_left_label=tk.Label(self.output,textvariable=self.battalions_left,font="Courier 20 bold",justify=tk.LEFT,anchor=tk.W,width=30)
        self.battalions_left.set(f'Remaining Battalions: {n_battalions}')
        self.message('')

        #Defining battlefileds:
        for i in range(n_fields):
            bf=battle_field(self.battlefields_canvas,n_battalions,self)
            self.battlefields.append(bf)

        self.configure_layout()
        self.grid_all()
        self.initiate_game()


    def initiate_game(self):
        for i in self.battlefields:
            i.set_player(self.mean_battalions)
            i.set_computer(self.mean_battalions)
        rest=self.n_battalions-self.mean_battalions*self.n_fields
        for i in range(rest):
            b=self.battlefields[i]
            b.pluss_player()
            b.pluss_computer()

    def configure_layout(self):
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1)
        self.columnconfigure(0,weight=1)
        self.battlefields_canvas.rowconfigure(0,weight=1)
        for i in range(self.n_fields):
            self.battlefields_canvas.columnconfigure(i,weight=1)
        self.controls.rowconfigure(0,weight=1)
        self.controls.rowconfigure(1,weight=1)
        self.controls.columnconfigure(0,weight=1)
        self.output.rowconfigure(0,weight=1)
        self.output.columnconfigure(0,weight=1)
        self.output.columnconfigure(1,weight=1)


    def grid_all(self):
        for i in range(self.n_fields):
            self.battlefields[i].grid(column=i,row=0,sticky=tk.NSEW)
        self.battlefields_canvas.grid(row=0,sticky=tk.NSEW)
        self.controls.grid(row=1,column=0,sticky=tk.EW)
        self.button_attack.grid(row=1,column=0,sticky=tk.EW)
        self.output.grid(row=2,column=0,sticky=tk.EW)
        self.output_label.grid(row=0,column=1,sticky=tk.EW)
        self.battalions_left_label.grid(row=0,column=0,sticky=tk.EW)


    def attack(self):
        player_battalions, computer_battalions=self.get_battalion_count()
        diff=(player_battalions-computer_battalions)
        points=np.sum(diff>0)-np.sum(diff<0)
        if points>0:
            self.message('You won')
        elif points==0:
            self.message('It was a draw')
        else:
            self.message('YOU LOST!!!!')
        


    def get_battalions_left(self,player=True):
        b=0
        for i in self.battlefields:
            if player:
                b+=len(i.battalion_objects_player)
            else:
                b+=len(i.battalion_objects_computer)
        return self.n_battalions-b

    def message(self,message):
        self.output_text.set(f'Message: {message}')

    def get_battalion_count(self):
        battalions_player=[]
        battalions_computer=[]
        for i in self.battlefields:
            battalions_player.append(len(i.battalion_objects_player))
            battalions_computer.append(len(i.battalion_objects_computer))
        return np.array(battalions_player, dtype=int), np.array(battalions_computer, dtype=int)

    def computer_reaction(self):
        player_battalions, computer_battalions=self.get_battalion_count()
        computer_battalions=self.computer_strategy(player_battalions,computer_battalions, self.n_battalions, self.n_fields)
        for i in range(len(self.battlefields)):
            b=self.battlefields[i]
            b.set_computer(computer_battalions[i])
            diff=len(b.battalion_objects_player)-len(b.battalion_objects_computer)
            if diff>0:
                b.playing_field['bg']='green'
            elif diff==0:
                b.playing_field['bg']='orange'
            else:
                b.playing_field['bg']='red'





    

def default_computer_strategy(player_battalions, computer_battalions,n_battalions,n_fields):
    #you have to make shure yourself that the sum of computer battalions do not 
    #exceed n_battalions

    for i in range(100):
        diff=(computer_battalions-player_battalions)
        won=np.sum(diff>0)-np.sum(diff<0)
        if won>0:
            return computer_battalions
        #obtains the diff ranking
        s=diff.argsort()
        #adds battalion where the computer is weakest
        computer_battalions[s[0]]+=1
        #reduces battalion by chekcing for positive deployments in reverse order:
        for i in s[::-1]:
            #if there are battalions to take and the change is inconsequential, then remove a battalion
            if (computer_battalions[i]>0 
                    and 
                    (computer_battalions[i]<player_battalions[i] or
                    computer_battalions[i]>player_battalions[i]+1 )
                    ):
                computer_battalions[i]-=1
                break
    return computer_battalions
        
        




w=window(6,21)

w.mainloop()