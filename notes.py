import tkinter as tk
from tkinter import ttk as ttk
from tkinter import scrolledtext
from tkinter import filedialog as fd
from tkinter import messagebox
from PIL import ImageTk, Image
from win32api import GetSystemMetrics
import cv2 as cv
import dill as dill
import os
from pathlib import Path
import tkinter.font as font
from shutil import copyfile



# serialize
maps_list = []
map_path = ''
map_dict = {}
# /serialise
screenSize = (GetSystemMetrics(0), GetSystemMetrics(1))
cwd = Path(__file__).parents[0]
if(os.path.isdir(cwd/"map_images")):
    pass
else:
    Path.mkdir(cwd/"map_images")
    Path.mkdir(cwd/'saved_maps')

images_path = cwd/"map_images"
saves_path = cwd/'saved_maps'
open_notes = ''
map_name = ''
room_name = ''
map_image = None
pop_up_frame = None
pop_up_win = None

print(Path.cwd())

def display_map():
    global canvas, map_dict, map_path, map_image
    cv_img = cv.cvtColor(cv.imread(filename=map_path), cv.COLOR_BGR2RGB)
    map_image = ImageTk.PhotoImage(image=Image.fromarray(cv_img))
    canvas.create_image((0, 0), image=map_image, anchor='nw')
    canvas.configure(scrollregion=canvas.bbox("all"))
    note.select(map_tab)
    for x in map_dict.keys():
        load_rect(x, map_dict[x][0][0], map_dict[x][0]
                  [1], map_dict[x][0][2], map_dict[x][0][3])


def new_map():
    global canvas, map_path, map_image
    map_path = fd.askopenfilename(
        title="Choose a file",
        filetypes=[('image files', ('.png', '.jpg'))
                   ])
    create_popup_window('map')
    copyfile(map_path, str(images_path)+'/'+map_name+'.png')
    map_path = str(images_path)+'/'+map_name+'.png'
    cv_img = cv.cvtColor(cv.imread(filename=map_path), cv.COLOR_BGR2RGB)
    map_image = ImageTk.PhotoImage(image=Image.fromarray(cv_img))
    canvas.create_image((0, 0), image=map_image, anchor='nw')
    canvas.configure(scrollregion=canvas.bbox("all"))
    note.select(map_tab)


def name_map(*args):
    global text_box, map_name
    map_name = text_box.get()
    pop_up_win.destroy()


def select_room(event, _name):
    global open_notes
    open_notes = _name
    create_popup_window('note')


def delete_room(event, _name):
    global map_dict, canvas
    MsgBox = messagebox.askquestion(
        'Delete Room', 'You will lose all notes attached to '+str(_name), icon='warning')
    if MsgBox == 'yes':
        canvas.delete(map_dict[str(_name)][2])
        map_dict.pop(str(_name), None)


def start_rect(event):
    global x, y
    x = event.x
    y = event.y


def create_rect(event):
    global x, y, canvas, map_dict, root, room_name
    x = canvas.canvasx(x)
    y = canvas.canvasy(y)
    _x2 = canvas.canvasx(event.x)
    _y2 = canvas.canvasy(event.y)
    if(abs(x-_x2) < 20):
        return
    create_popup_window('room')
    rect = canvas.create_rectangle(
        x, y, _x2, _y2, stipple='gray50', fill='black')
    canvas.tag_bind(rect, "<Button-3>", lambda event,
                    n=room_name: select_room(event, n))
    canvas.tag_bind(rect, "<Shift-ButtonRelease-1>",
                    lambda event, n=room_name: delete_room(event, n))
    map_dict[room_name] = [(x, y, _x2, _y2), '', rect]
    centre = ((x + _x2)/2, (y + _y2)/2)
    canvas.create_text(centre, anchor=tk.CENTER, text=room_name, fill='white')


def create_popup_window(_name):
    global pop_up_frame, text_box, notes_box, pop_up_win, root, map_dict
    pop_up_win = tk.Tk()
    pop_up_frame = ttk.Frame(pop_up_win)
    pop_up_frame.pack()
    print(map_dict)
    print(open_notes)
    name_str = 'Name the ' + str(_name)
    if(_name != 'note'):
        ttk.Label(pop_up_frame, text=name_str, font=(18)).pack()
        text_box = ttk.Entry(pop_up_frame, font=(18))
        text_box.pack(side='top')
    else:
        notes_box = tk.scrolledtext.ScrolledText(
            pop_up_frame, wrap=tk.WORD, font=(18))
        #notes_box.delete(1.0, 'end')
        notes_box.insert('end', map_dict[open_notes][1])
        notes_box.pack(side='top')

    def save_text(*args):
        global room_name, map_name
        nonlocal _name
        if(_name == 'note'):
            map_dict[open_notes][1] = notes_box.get(index1='1.0', index2='end')
        elif(_name == "map"):
            map_name = text_box.get()
        elif(_name == 'room'):
            room_name = text_box.get()
        pop_up_win.destroy()

    pop_up_win.bind("<Escape>", save_text)
    pop_up_win.bind("<Return>", save_text)
    pop_up_win.protocol("WM_DELETE_WINDOW", save_text)
    pop_up_win.wait_window(pop_up_win)


def load_rect(name, x, y, _x2, _y2):
    global canvas
    rect = canvas.create_rectangle(
        x, y, _x2, _y2, stipple='gray50', fill='black')
    canvas.tag_bind(rect, "<Button-3>", lambda event,
                    n=name: select_room(event, n))
    canvas.tag_bind(rect, "<Shift-ButtonRelease-1>",
                    lambda event, n=name: delete_room(event, n))
    centre = ((x + _x2)/2, (y + _y2)/2)
    canvas.create_text(centre, anchor=tk.CENTER, text=name, fill='white')


def load_map():
    global map_name, maps_list, map_path, map_dict
    save_file = fd.askopenfilename(
        title="Choose a file",
        filetypes=[('Save Files', ('.dill'))],
        initialdir=map_path)
    with open(save_file, 'rb') as l:
        pickle_list = [x for x in dill.load(l)]
        map_name = pickle_list[0]
        maps_list = pickle_list[1]
        map_path = pickle_list[2]
        map_dict = pickle_list[3]
    display_map()


def on_close_main():
    global map_name
    if (messagebox.askokcancel("Quit", "Do you really wish to quit? \n(everything will be saved)")):
        if(map_name != ''):
            save_and_close()
        root.destroy()


def save_and_close():
    global map_name,  maps_list, map_path, map_dict
    maps_list.append(map_dict)
    pickle_list = [map_name, maps_list, map_path, map_dict]
    with open(str(saves_path) + '/' + map_name + ".dill", 'wb') as s:
        dill.dump(pickle_list, s)


root = tk.Tk()
text_box = tk.Entry()
notes_box = tk.scrolledtext.ScrolledText()
font.nametofont('TkDefaultFont').configure(family='console', size=12)
root.protocol("WM_DELETE_WINDOW", on_close_main)
note = ttk.Notebook(root, width=screenSize[0], height=screenSize[1])
menu_tab = tk.Frame(note, width=screenSize[0], height=screenSize[1])
map_tab = tk.Frame(note, width=screenSize[0], height=screenSize[1])
note.add(menu_tab, text="Menu")
note.add(map_tab, text="Map")
note.pack()
vbar = ttk.Scrollbar(map_tab, orient='vertical')
hbar = ttk.Scrollbar(map_tab, orient='horizontal')
canvas = tk.Canvas(map_tab, width=screenSize[0]-100, height=screenSize[1]-100)
vbar.config(command=canvas.yview)
hbar.config(command=canvas.xview)
vbar.pack(side='right', fill='y')
hbar.pack(side='bottom', fill='x')
canvas.pack(side='top', fill='both')
canvas.config(yscrollcommand=vbar.set)
canvas.config(xscrollcommand=hbar.set)
canvas.configure(scrollregion=canvas.bbox("all"))
canvas.bind("<Button-1>", start_rect)
canvas.bind("<ButtonRelease-1>", create_rect)
new_map_button = ttk.Button(
    menu_tab, text='      New Map      ', command=new_map)
new_map_button.pack(padx=100, pady=10)
load_map_button = ttk.Button(
    menu_tab, text='      Load Map      ', command=load_map).pack(padx=100, pady=10)
root.mainloop()
