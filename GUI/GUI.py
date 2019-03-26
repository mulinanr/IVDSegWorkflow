from guizero import App, PushButton, Slider, Text, Window, TextBox, Picture, Box, Combo
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


app = App(title='CEST Auswertung', width=550, height=700, bg='white')



logo_box = Box(app, width='fill')
hhu_logo = Picture(logo_box, image='hhu_logo.jpg', width=215, height=124, align='right')
ukd_logo = Picture(logo_box, image='ukd_logo.jpg', width=323, height=73, align='left')


#Choose CEST and WASSR MRIs folders from the filesystem. Gives back their path as a String
main_page_box = Box(app, align='left', layout='grid')
FF_path = Text(main_page_box, grid=[1, 0])
FFC_path = Text(main_page_box, grid=[1, 1])
chooseFF_button = PushButton(main_page_box, text='Suche FF', command=open_browse_FF, grid=[0, 0])
chooseFFC_button = PushButton(main_page_box, text='Suchen FFC', command=open_browse_FFC, grid=[0, 1])


#CEST Settings
cest_settings_button = PushButton(main_page_box, text='CEST Settings', command=open_cest_settings, grid=[0, 2])
cest_settings_window = Window(app, title='CEST Settings', layout='grid')

#Define CEST Parameters
text_abreite = Text(cest_settings_window, align='left', text='Abreite', grid=[0, 1])
text_hstep_cest = Text(cest_settings_window, align='left', text='Schritt Weite', grid=[0, 2])
text_fshift = Text(cest_settings_window, align='left',  text='Frequenz Shift', grid=[0, 3])
text_alternating_cest = Text(cest_settings_window, align='left',  text='Alternating', grid=[0, 4])
text_ndyn_cest = Text(cest_settings_window, align='left',  text='Dynamiken', grid=[0, 5])
text_dfreq = Text(cest_settings_window, align='left',  text='Delta Frequenz', grid=[0, 6])
text_mtrasym = Text(cest_settings_window, align='left',  text='MTRasym', grid=[0, 7])
text_maxoffset = Text(cest_settings_window, align='left',  text='Max Offset', grid=[0, 8])

cest_abreite = TextBox(cest_settings_window, text='3.0', align='left', grid=[1,1])
cest_hstep = TextBox(cest_settings_window, text='0.01', align='left', grid=[1,2])
cest_fshift = TextBox(cest_settings_window, text='1.4', align='left', grid=[1,3])
cest_alternating = TextBox(cest_settings_window, text='0', align='left', grid=[1,4])
combo_alternating = Combo(cest_settings_window, align='left', width=15, options=["True", "False"], grid=[2,4])
cest_ndyn = TextBox(cest_settings_window, text='32', align='left', grid=[1,5])
cest_dfreq = TextBox(cest_settings_window, text='1.0', align='left', grid=[1,6])
cest_mtrasym = TextBox(cest_settings_window, text='[-10, 10]', align='left', grid=[1,7])
cest_max_offset = TextBox(cest_settings_window, text='4.0', align='left', grid=[1,8])

close_cest_button = PushButton(cest_settings_window, text='Speichern', command=close_cest_settings, grid=[1,20])
cest_settings_window.hide()
#CEST
#ndyn = 32;  h_step = 0.01; max_offset = 4.0; Abreite = 3.0;fshift = 1.4;dfreq = 1.0;clims_MTRasym_Bild = [-10 10]; altern = 0;


#WASSR Settings
open_wassr_button = PushButton(main_page_box, text='WASSR Settings', command=open_wassr_settings, grid=[0, 3])
wassr_settings_window = Window(app, title='WASSR Settings', layout='grid')

#Define WASSR Parameters
text_selsl = Text(wassr_settings_window, align='left', text='Selektierte Schicht', grid=[0, 1])
text_hstep  = Text(wassr_settings_window, align='left', text='Schrittweite für WASSR Interpolation', grid=[0, 2])
text_maxoffset = Text(wassr_settings_window, align='left',  text='Max Offset', grid=[0, 3])
text_alternating = Text(wassr_settings_window, align='left',  text='Alternating', grid=[0, 4])
text_ndyn = Text(wassr_settings_window, align='left',  text='Dynamiken', grid=[0, 5])
text_LMO = Text(wassr_settings_window, align='left',  text='LMO', grid=[0, 6])
text_gauss = Text(wassr_settings_window, align='left',  text='Gauss', grid=[0, 7])

wassr_selsl = TextBox(wassr_settings_window, align='right',  text='1', grid=[1,1])
wassr_hstep = TextBox(wassr_settings_window, align='right',   text='0.01', grid=[1,2])
wassr_max_offeset = TextBox(wassr_settings_window, align='right',   text='1.0', grid=[1,3])
wassr_alternating = TextBox(wassr_settings_window, align='right',   text='0', grid=[1,4])
combo_alternating = Combo(wassr_settings_window, align='right',   width=15, options=["True", "False"], grid=[2,4])
wassr_ndyn = TextBox(wassr_settings_window, align='right',   text='22', grid=[1,5])
wassr_LMO = TextBox(wassr_settings_window, align='right',   text='B', grid=[1,6])
combo_LMO = Combo(wassr_settings_window, align='right',   width=15, options=["L", "M", 'MS', "O", "I", 'B', 'BSpline', 'BSplineG'], grid=[2,6])
wassr_gauss = TextBox(wassr_settings_window, align='right',   text='3.0', grid=[1,7])


close_wassr_button = PushButton(wassr_settings_window, text='Speichern', command=close_wassr_settings, grid=[1,20])
wassr_settings_window.hide()


#WASSR
#selsl = 1; hstep = 0.01; max_offset = 1.0; alternating = 0; ndyn = 22; LMO = 'B';gauss = 3.0;



app.display()