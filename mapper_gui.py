from coils import *
from movement import *
from collection import *
from mapping import *
from data import *
import tkinter as tk
import config
from functools import partial


#########################tk nonsense ###############################################
"""some nasty stuff where parameters arent passed but works just some global
scoping is used. maybe fix later. not really best practice but its the easiest
way to setup tkinter and it works"""

def start_gui():
    def goToClick(relative_pos,abs_pos):
        """takes the values in the goto bozes on the interface and sends those to
        goTo. This uses relative coordinates"""
        x = int(xmove.get())#make this more elegant for restriction to ints
        y = int(ymove.get())
        if goTo(x,y,relative_pos,abs_pos,abs_Label,relative_Label):return -1

    def initialize_Click():
        """call for tkinter to make initializing funtion portable"""
        initialize_sensors(mode.get())

    def scan_Click():
        """funtion only needed for tkinter so that the 'core function' can be portable
        as pulling data from entries is vile"""
        scan(int(step_size.get()),int(xstart.get()),int(ystart.get()),
        int(xend.get()),int(yend.get()),config.relative_pos, config.abs_pos, mode.get(),
        save.get(),save_dir.get(),abs_Label,relative_Label)

    def Field_Window(relative_pos):
        """opens a new window displaying the field at the current point"""
        Field = tk.Toplevel(win)
        Field.geometry("300x300")

        if(mode.get() == "Keithly"):
            Cur_Field = Keithly_Point(relative_pos)
        if(mode.get() == "Sypris"):
            Cur_Field = Sypris_Point(relative_pos)
        elif(mode.get() == "labjack"):
            Cur_Field = U6_Point(relative_pos)

        tk.Label(Field, text = "Bx:%.7g" %(Cur_Field[2])).grid(column=1,row=1)
        tk.Label(Field, text = "By:%.7g" %(Cur_Field[3])).grid(column=1,row=2)
        tk.Label(Field, text = "Bz:%.7g" %(Cur_Field[4])).grid(column=1,row=3)

    def Two_D_map_Click():
        """helper code to make 2d mapping funtion portable"""
        Two_D_map(int(step_size.get()),int(xstart.get()),int(ystart.get()),
                  int(xend.get()),int(yend.get()),config.relative_pos, config.abs_pos, mode.get(),
                  save.get(),save_dir.get(),dom_dir.get(),abs_Label,relative_Label)

    def advancedNewWindow():
        """opens window with advanced settings"""
        advanced = tk.Toplevel(win)
        advanced.title("advanced settings")
        advanced.geometry("300x300")
        tk.Button(advanced, text="set absolute 0",
                 command=partial(set_absolute_zero,config.abs_pos,
                 config.abs_steps, config.relative_pos,abs_Label)).grid(column=1, row=3)

        step_Label = tk.Label(advanced, text = "%s , %s" %(config.abs_steps[0],config.abs_steps[1]))
        step_Label.grid(column=1,row=1)

    win = tk.Tk()
    win.title("3D Mapper")
    win.geometry("2200x700")

    tk.Label(win, text="absolute position").grid(row=1,column=1)
    abs_Label = tk.Label(win, text = "%s , %s" %(config.abs_pos[0],config.abs_pos[1]))
    abs_Label.grid(column=1, row=2)


    tk.Label(win, text="relative position").grid(row=1,column=2)
    relative_Label = tk.Label(win, text = "%s , %s" %(config.relative_pos[0],config.relative_pos[1]))
    relative_Label.grid(column=2, row=2)


    tk.Button(win, text="set relative 0",
              command=partial(set_relative_zero,config.relative_pos,
              config.relative_offset,config.abs_pos,relative_Label)).grid(column=2, row=3)
    tk.Button(win, text="home to absolute 0",
              command=partial(abs_home,config.abs_pos,abs_Label,
                              relative_Label)).grid(column=1, row=4)
    tk.Button(win, text="home to relative 0",
              command=partial(relative_home,config.relative_pos,
                              config.abs_pos,abs_Label,
                              relative_Label)).grid(column=2, row=4)

    tk.Button(win, text="up 1",command=partial(move,'u', 1,abs_Label, relative_Label)).grid(column=6, row=4)
    tk.Button(win, text="up 10",command=partial(move,'u', 10,abs_Label, relative_Label)).grid(column=6, row=3)
    tk.Button(win, text="up 100",command=partial(move,'u', 100,abs_Label, relative_Label)).grid(column=6, row=2)

    tk.Button(win, text="down 1",command=partial(move,'d', 1,abs_Label, relative_Label)).grid(column=6, row=6)
    tk.Button(win, text="down 10",command=partial(move,'d', 10,abs_Label, relative_Label)).grid(column=6, row=7)
    tk.Button(win, text="down 100",command=partial(move,'d', 100,abs_Label, relative_Label)).grid(column=6, row=8)

    tk.Button(win, text="back 1",command=partial(move,'b', 1,abs_Label, relative_Label)).grid(column=5, row=5)
    tk.Button(win, text="back 10",command=partial(move,'b', 10,abs_Label, relative_Label)).grid(column=4, row=5)
    tk.Button(win, text="back 100",command=partial(move,'b', 100,abs_Label, relative_Label)).grid(column=3, row=5)

    tk.Button(win, text="forward 1",command=partial(move,'f', 1,abs_Label, relative_Label)).grid(column=7, row=5)
    tk.Button(win, text="forward 10",command=partial(move,'f', 10,abs_Label, relative_Label)).grid(column=8, row=5)
    tk.Button(win, text="forward 100",command=partial(move,'f', 100,abs_Label, relative_Label)).grid(column=9, row=5)

    tk.Label(win, text="go to:").grid(column=10,row=1)
    tk.Label(win, text="z:").grid(column=10,row=2)
    xmove = tk.Entry(win,width=3)
    xmove.grid(column=11,row=2)
    tk.Label(win, text="y:").grid(column=12,row=2)
    ymove = tk.Entry(win,width=3)
    ymove.grid(column=13,row=2)
    tk.Button(win, text="GO!",command=partial(goToClick,config.relative_pos,config.abs_pos)).grid(column=14, row=2)

    tk.Label(win, text="scan from:").grid(column=10,row=4)
    tk.Label(win, text="z:").grid(column=10,row=5)
    xstart = tk.Entry(win,width=3)
    xstart.grid(column=11,row=5)
    tk.Label(win, text="y:").grid(column=12,row=5)
    ystart = tk.Entry(win,width=3)
    ystart.grid(column=13,row=5)

    tk.Label(win, text="stepsize:").grid(column=14,row=5)
    step_size = tk.Entry(win,width=3)
    step_size.grid(column=15,row=5)

    tk.Label(win, text="scan to:").grid(column=10,row=6)
    tk.Label(win, text="z:").grid(column=10,row=7)
    xend = tk.Entry(win,width=3)
    xend.grid(column=11,row=7)
    tk.Label(win, text="y:").grid(column=12,row=7)
    yend = tk.Entry(win,width=3)
    yend.grid(column=13,row=7)
    tk.Button(win, text="GO!",command=partial(scan_Click)).grid(column=14, row=7)
    tk.Button(win, text="2D GO!",command=partial(Two_D_map_Click)).grid(column=15, row=7)

    dom_dir = tk.StringVar(win)
    doms = {"z","y"}
    dom_dir.set("z")
    dom_select = tk.OptionMenu(win,dom_dir,*doms)
    dom_select.grid(column=15,row=8)

    save = tk.IntVar()
    tk.Checkbutton(win, text="Save Data?", variable=save).grid(column = 16, row=7)

    tk.Label(win, text="save directory").grid(row=16,column=8)
    save_dir = tk.Entry(win,width=10)
    save_dir.grid(column = 16, row=9)


    tk.Button(win, text="Get current field",command= partial(Field_Window,config.relative_pos)).grid(column=10,row=9)


    tk.Button(win, text="Advanced Settings",command=advancedNewWindow).grid(column=16, row=26)

    Ax1 = tk.Entry(win,width=3)
    Ax1.grid(column=1,row=21)
    tk.Button(win, text="set z Helmholtz current",command=partial(setCurrent,0,5000,Ax1.get)).grid(column=1, row=22)

    Ax2 = tk.Entry(win,width=3)
    Ax2.grid(column=2,row=21)
    tk.Button(win, text="set z Newton current",command=partial(setCurrent,1,5002,Ax2.get)).grid(column=2, row=22)

    Ay1 = tk.Entry(win,width=3)
    Ay1.grid(column=1,row=23)
    tk.Button(win, text="set y Helmholtz current",command=partial(setCurrent,2,5000,Ay1.get)).grid(column=1, row=24)

    Ay2 = tk.Entry(win,width=3)
    Ay2.grid(column=2,row=23)
    tk.Button(win, text="set y Newton current",command=partial(setCurrent,3,5002,Ay2.get)).grid(column=2, row=24)

    Az1 = tk.Entry(win,width=3)
    Az1.grid(column=1,row=25)
    tk.Button(win, text="set x Helmholtz current").grid(column=1, row=26)

    Az2 = tk.Entry(win,width=3)
    Az2.grid(column=2,row=25)
    tk.Button(win, text="set x Newton current").grid(column=2, row=26)

    tk.Button(win, text="auto zero z",command=partial(auto_zero,(5000,0),4,U6_Point)).grid(column=4, row=21)

    tk.Button(win, text="auto zero y",command=partial(auto_zero,(5000,3),3,U6_Point)).grid(column=4, row=22)

    tk.Button(win, text="auto zero x",command=partial(auto_zero,(5000,0),2,U6_Point)).grid(column=4, row=23)

    mode = tk.StringVar(win)
    modes = {"labjack", "Keithley", "Sypris"}
    mode.set("labjack")
    mode_select = tk.OptionMenu(win,mode,*modes)
    mode_select.grid(column=1,row=7)
    tk.Button(win, text="Initiliaze",command=initialize_Click).grid(column=2, row=7)
    win.mainloop()