import os

import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

from cest import cest_corrector
from cest import mtr_asym_calculator
from utils import common_functions
from wassr import algorithm
from wassr import mscf_algorithm
from wassr import wassr_corrector


def processMri(wassrPath, cestPath, wassrProperties, cestProperties):

    # 1. Load Files

    # 2. Create SName and filename pattern
    (sName, filename) = common_functions.defineSName(wassrPath, wassrProperties.sSlide)


    # 3. Get Mask, temporary use test Mask
    Mask = common_functions.createTestMask(192, 192, 5)

    #   3.1. Display if needed
    rootMask = tk.Tk()
    rootMask.title("Makse")
    imageMask = Image.fromarray(common_functions.interval_mapping(Mask, 0.0, 1.0, 0, 255))
    imageMask = imageMask.resize((576, 576))
    imgMask =  ImageTk.PhotoImage(image = imageMask, master = rootMask)
    canvas = tk.Canvas(rootMask, width = 620, height = 620)
    canvas.pack()
    canvas.create_image(20, 20, anchor = "nw", image = imgMask)

    #   3.2. Save to SName if needed


    # 4. Make WASSR calculation
    algoritm = mscf_algorithm.MscfAlgorithm(wassrProperties.hStep, wassrProperties.maxOffset, wassrProperties.maxOffset)
    wassrCorrector = wassr_corrector.WassrCorrector(wassrProperties.sSlide, 
                wassrProperties.hStep, wassrProperties.maxOffset, wassrProperties.alternating, wassrProperties.nDynamics, 
                wassrProperties.lmo, wassrProperties.gauss, wassrProperties.zFilter, algoritm)
    (Offsets, R) = wassrCorrector.calculateWassrAmlCorrection(wassrPath, sName, filename, Mask)
 
    #   4.1. Display if needed
    #Offsets = np.ones((192, 192)) * 0.7
    rootWassr = tk.Tk()
    rootWassr.title("Offset")
    imageWassr = Image.fromarray(common_functions.interval_mapping(Offsets, 0.0, 1.0, 0, 255))
    imageWassr = imageWassr.resize((576, 576))
    imgWassr =  ImageTk.PhotoImage(image = imageWassr, master = rootWassr)
    canvas = tk.Canvas(rootWassr, width = 620, height = 620)
    canvas.pack()
    canvas.create_image(20, 20, anchor = "nw", image = imgWassr)

    #   4.2. Save to SName if needed


    # 5. Make CEST cortrection
    filename = common_functions.defineFilename(cestPath, cestProperties.sSlide)
    cestCorrector = cest_corrector.CestCorrector(cestProperties.sSlide, cestProperties.hStep, cestProperties.maxOffset, 
                cestProperties.abreite, cestProperties.fshift, cestProperties.dfreq, cestProperties.alternating, 
                cestProperties.nDynamics, cestProperties.gauss, cestProperties.S0yn, cestProperties.zFilter)
    (CestCurveS, x_calcentries) = cestCorrector.calculateCestAmlEvaluation(cestPath, Offsets, sName, filename, Mask)
 
    #   5.1. Save to SName if needed


    # 6. Calculate MTR Async
    mtrAsymCalculator = mtr_asym_calculator.MtrAsymCalculator(cestProperties.fshift, cestProperties.dfreq)
    (MTRasymCurves, MTRasym_Bild) = mtrAsymCalculator.calculateMtrAsymCurves(CestCurveS, x_calcentries, Mask)

    #   6.1. Display if needed
    #MTRasym_Bild = np.ones((192, 192)) * 0.7
    rootMtr = tk.Tk()
    rootMtr.title("MTRasym")
    imageMtr = Image.fromarray(common_functions.interval_mapping(MTRasym_Bild, 0.0, 1.0, 0, 255))
    imageMtr = imageMtr.resize((576, 576))
    imgMtr =  ImageTk.PhotoImage(image = imageMtr, master = rootMtr)
    canvas = tk.Canvas(rootMtr, width = 620, height = 620)
    canvas.pack()
    canvas.create_image(20, 20, anchor = "nw", image = imgMtr)
    rootMtr.mainloop()

    #   6.2. Save if needed

    pass
