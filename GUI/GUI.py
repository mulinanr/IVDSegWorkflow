from guizero import App, PushButton, Slider, Text, Window, TextBox, Picture, Box, Combo
from tkinter.filedialog import askdirectory
import os

from gui import cest_properties
from gui import wassr_properties

import cest_evaluation


def calculate():
    cestProperties = cest_properties.CestProperties(cest_sslide.value, cest_hstep.value, 
                    cest_maxoffset.value, cest_abreite.value, cest_fshift.value, 
                    cest_dfreq.value, cest_alternating.value, cest_ndynamic.value, 
                    cest_gauss.value, cest_s0yn.value, cest_zfilter.value)
    wassrProperties = wassr_properties.WassrProperties(wassr_selsl.value, wassr_hstep.value, 
                    wassr_maxoffset.value, wassr_alternating.value, wassr_ndynamic.value, 
                    wassr_lmo.value, wassr_gauss.value, wassr_zfilter.value)
    cest_evaluation.processMri(FF_path.value, FFC_path.value, wassrProperties, cestProperties)


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

cestProperties = cest_properties.CestProperties()
wassrProperties = wassr_properties.WassrProperties()

logo_box = Box(app, width='fill')
hhu_logo = Picture(logo_box, image='gui/hhu_logo.jpg', width=215, height=124, align='right')
ukd_logo = Picture(logo_box, image='gui/ukd_logo.jpg', width=323, height=73, align='left')


#Choose CEST and WASSR MRIs folders from the filesystem. Gives back their path as a String
main_page_box = Box(app, align='left', layout='grid')
FF_path = Text(main_page_box, grid=[1, 0])
FFC_path = Text(main_page_box, grid=[1, 1])
chooseFF_button = PushButton(main_page_box, text='Suche FF', command=open_browse_FF, grid=[0, 0])
chooseFFC_button = PushButton(main_page_box, text='Suchen FFC', command=open_browse_FFC, grid=[0, 1])

button = PushButton(main_page_box, command = calculate, text = "Calculate", grid = [0,5])


#CEST Settings
cest_settings_button = PushButton(main_page_box, text='CEST Settings', command=open_cest_settings, grid=[0, 2])
cest_settings_window = Window(app, title='CEST Settings', layout='grid')

#Define CEST Parameters
cest_sslide_label = Text(cest_settings_window, align='left', text='sSlide', grid=[0, 1])
cest_sslide = TextBox(cest_settings_window, text=cestProperties.sSlide, align='left', grid=[1, 1])

cest_hstep_label = Text(cest_settings_window, align='left', text='hStep', grid=[0, 2])
cest_hstep = TextBox(cest_settings_window, text=cestProperties.hStep, align='left', grid=[1, 2])

cest_maxoffset_label = Text(cest_settings_window, align='left',  text='Max Offset', grid=[0, 3])
cest_maxoffset = TextBox(cest_settings_window, text=cestProperties.maxOffset, align='left', grid=[1, 3])

cest_abreite_label = Text(cest_settings_window, align='left', text='Abreite', grid=[0, 4])
cest_abreite = TextBox(cest_settings_window, text=cestProperties.abreite, align='left', grid=[1, 4])

cest_fshift_label = Text(cest_settings_window, align='left',  text='Frequenz Shift', grid=[0, 5])
cest_fshift = TextBox(cest_settings_window, text=cestProperties.fshift, align='left', grid=[1, 5])

cest_dfreq_label = Text(cest_settings_window, align='left',  text='Delta Frequenz', grid=[0, 6])
cest_dfreq = TextBox(cest_settings_window, text=cestProperties.dfreq, align='left', grid=[1, 6])

cest_alternating_label = Text(cest_settings_window, align='left',  text='Alternating', grid=[0, 7])
cest_alternating = Combo(cest_settings_window, selected = cestProperties.alternating, align='left', options=["True", "False"], grid=[1, 7])

cest_ndynamic_label = Text(cest_settings_window, align='left',  text='Dynamiken', grid=[0, 8])
cest_ndynamic = TextBox(cest_settings_window, text=cestProperties.nDynamics, align='left', grid=[1, 8])

cest_gauss_label = Text(cest_settings_window, align='left',  text='Gauss', grid=[0, 9])
cest_gauss = TextBox(cest_settings_window, text=cestProperties.gauss, align='left', grid=[1, 9])

cest_s0yn_label = Text(cest_settings_window, align='left',  text='S0yn', grid=[0, 10])
cest_s0yn = TextBox(cest_settings_window, text=cestProperties.S0yn, align='left', grid=[1, 10])

cest_zfilter_label = Text(cest_settings_window, align='left',  text='zFilter', grid=[0, 11])
cest_zfilter = Combo(cest_settings_window, selected = cestProperties.zFilter, align='left', options=["True", "False"], grid=[1, 11])

close_cest_button = PushButton(cest_settings_window, text='Speichern', command=close_cest_settings, grid=[1,20])
cest_settings_window.hide()


#WASSR Settings
open_wassr_button = PushButton(main_page_box, text='WASSR Settings', command=open_wassr_settings, grid=[0, 3])
wassr_settings_window = Window(app, title='WASSR Settings', layout='grid')

#Define WASSR Parameters
wassr_selsl_label = Text(wassr_settings_window, align='left', text = 'sSlide', grid=[0, 1])
wassr_selsl = TextBox(wassr_settings_window, align='left',  text = wassrProperties.sSlide, grid=[1, 1])

wassr_hstep_label = Text(wassr_settings_window, align='left', text = 'hStep', grid=[0, 2])
wassr_hstep = TextBox(wassr_settings_window, align='left',  text = wassrProperties.hStep, grid=[1, 2])

wassr_maxoffset_label = Text(wassr_settings_window, align='left', text = 'Max Offset', grid=[0, 3])
wassr_maxoffset = TextBox(wassr_settings_window, align='left',  text = wassrProperties.maxOffset, grid=[1, 3])

wassr_alternating_label = Text(wassr_settings_window, align='left', text = 'Alternating', grid=[0, 4])
wassr_alternating = Combo(wassr_settings_window, selected = wassrProperties.alternating, align='left', options=["True", "False"], grid=[1, 4])

wassr_ndynamic_label = Text(wassr_settings_window, align='left', text = 'Dynamiken', grid=[0, 5])
wassr_ndynamic = TextBox(wassr_settings_window, align='left',  text = wassrProperties.nDynamics, grid=[1, 5])

wassr_lmo_label = Text(wassr_settings_window, align='left', text = 'LMO', grid=[0, 6])
wassr_lmo = Combo(wassr_settings_window, selected = wassrProperties.lmo, align='left', options = wassr_properties.algorithmList, grid=[1, 6])

wassr_gauss_label = Text(wassr_settings_window, align='left', text = 'Gauss', grid=[0, 7])
wassr_gauss = TextBox(wassr_settings_window, align='left',  text = wassrProperties.gauss, grid=[1, 7])

wassr_zfilter_label = Text(wassr_settings_window, align='left', text = 'zFilter', grid=[0, 8])
wassr_zfilter = Combo(wassr_settings_window, selected = wassrProperties.zFilter, align='left', options=["True", "False"], grid=[1, 8])

close_wassr_button = PushButton(wassr_settings_window, text='Speichern', command=close_wassr_settings, grid=[1, 10])
wassr_settings_window.hide()


app.display()
