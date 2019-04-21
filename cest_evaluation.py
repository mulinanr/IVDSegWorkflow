import os

import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

from cest import cest_corrector
from cest import mtr_asym_calculator
from utils import common_functions
from utils import draw_image
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
    imgMask =  ImageTk.PhotoImage(image = Image.fromarray(common_functions.interval_mapping(Mask, 0.0, 1.0, 0, 255)), master = rootMask)
    canvas = tk.Canvas(rootMask, width = 230, height = 230)
    canvas.pack()
    canvas.create_image(20, 20, anchor = "nw", image = imgMask)

    #   3.2. Save to SName if needed


    # 4. Make WASSR calculation
    algoritm = mscf_algorithm.MscfAlgorithm(wassrProperties.hStep, wassrProperties.maxOffset, wassrProperties.maxOffset)
    wassrCorrector = wassr_corrector.WassrCorrector(wassrProperties.sSlide, 
                wassrProperties.hStep, wassrProperties.maxOffset, wassrProperties.alternating, wassrProperties.nDynamics, 
                wassrProperties.lmo, wassrProperties.gauss, wassrProperties.zFilter, algoritm)
    #(Offsets, R) = wassrCorrector.calculateWassrAmlCorrection(wassrPath, sName, filename, Mask)
    #   4.1. Display if needed
    Offsets = np.ones((192, 192)) * 0.7
    rootWassr = tk.Tk()
    rootWassr.title("Offset")
    imgWassr =  ImageTk.PhotoImage(image = Image.fromarray(common_functions.interval_mapping(Offsets, 0.0, 1.0, 0, 255)), master = rootWassr)
    canvas = tk.Canvas(rootWassr, width = 230, height = 230)
    canvas.pack()
    canvas.create_image(20, 20, anchor = "nw", image = imgWassr)

    #   4.2. Save to SName if needed


    # 5. Make CEST cortrection
    cestCorrector = cest_corrector.CestCorrector(cestProperties.sSlide, cestProperties.hStep, cestProperties.maxOffset, 
                cestProperties.abreite, cestProperties.fshift, cestProperties.dfreq, cestProperties.alternating, 
                cestProperties.nDynamics, cestProperties.gauss, cestProperties.S0yn, cestProperties.zFilter)
    (CestCurveS, x_calcentries) = cestCorrector.calculateCestAmlEvaluation(cestPath, OF, sName, filename, Mask)
    #   5.1. Dispalay if needed
    #   5.2. Save if


    # 6. Calculate MTR Async
    mtrAsymCalculator = mtr_asym_calculator.MtrAsymCalculator(cestProperties.fshift, cestProperties.dfreq)
    mtrAsymCalculator.calculateMtrAsymCurves(CestCurveS, x_calcentries, Mask)
    #   6.1. Display if needed
    #   6.2. Save if needed

    pass
