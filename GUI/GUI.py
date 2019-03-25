from guizero import App, PushButton, Slider, Text, Window, TextBox, Picture, Box
from tkinter.filedialog import askdirectory

def open_browse_FF():
    filename = askdirectory() # show an "Open" dialog box and return the path to the selected file
    FF_path.value = filename

def open_browse_FFC():
    filename = askdirectory() # show an "Open" dialog box and return the path to the selected file
    FFC_path.value = filename

def open_cest_settings():
    cest_settings_window.show()

def close_cest_settings():
    cest_settings_window.hide()

def open_wassr_settings():
    wassr_settings_window.show()

def close_wassr_settings():
    wassr_settings_window.hide()


#
# app = App(title="Hello world", layout='grid')
# text = Text(app, text='Ola World', grid=[0,1])
# #button = PushButton(app, command=say_hello)
#
# text_box = TextBox(app, text='Enter some Text', align='left', grid=[0,2])
#
#
#
# open_button = PushButton(app, text='Open', command=open_window)
# close_button = PushButton(window, text='Close', command=close_window)




app = App(title='CEST Auswertung', width=550, height=700, bg='white')



logo_box = Box(app, width='fill')
hhu_logo = Picture(logo_box, image='hhu_logo.jpg', width=215, height=124, align='right')


#Choose CEST and WASSR MRIs folders from the filesystem. Gives back their path as a String
chooseFF_box = Box(app, align='left', layout='grid')
FF_path = Text(chooseFF_box, grid=[1,0])
FFC_path = Text(chooseFF_box, grid=[1,1])
chooseFF_button = PushButton(chooseFF_box, text='Suche FF', command=open_browse_FF, grid=[0,0])
chooseFFC_button = PushButton(chooseFF_box, text='Suchen FFC', command=open_browse_FFC, grid=[0,1])


#Define CEST parameters
cest_box = Box(app, align='left', layout='grid')
cest_settings_button = PushButton(cest_box, text='WASSR Settings', command=open_cest_settings, grid=[0,0])
cest_settings_window = Window(app, title='CEST Settings')
close_cest_button = PushButton(cest_settings_window, text='Speichern', command=close_cest_settings, grid=[0,0])
cest_settings_window.hide()

#Define WASSR parameters
wassr_box = Box(app, align='left', layout='grid')
open_wassr_button = PushButton(wassr_box, text='Speichern', command=open_wassr_settings, grid=[0,0])
wassr_settings_window = Window(app, title='WASSR Settings')
close_wassr_button = PushButton(wassr_settings_window, text='Speichern', command=close_wassr_settings, grid=[0,0])
wassr_settings_window.hide()




app.display()