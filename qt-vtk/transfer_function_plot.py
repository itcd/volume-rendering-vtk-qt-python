"""
http://matplotlib.org/examples/shapes_and_collections/scatter_demo.html
http://nbviewer.ipython.org/github/dpsanders/matplotlib-examples/blob/master/colorline.ipynb
http://stackoverflow.com/questions/20130227/matplotlib-connect-scatterplot-points-with-line-python
"""

import sys
import vtk
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtk.util.misc import vtkGetDataRoot
import xml.etree.ElementTree as ET
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QApplication, QMessageBox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_transfer_function():
    filename = str(QtGui.QFileDialog.getOpenFileName(QtGui.QWidget(), 'Select a transfer function', '../transfer_function', "Voreen transfer functions (*.tfi);; All Files (*)"))
    if len(filename ) < 1:
        filename = "../transferfuncs/nucleon.tfi"
        
    tree = ET.parse(filename)
    root = tree.getroot()
    
    TransFuncIntensity = root.find("TransFuncIntensity")
    domain = TransFuncIntensity.find("domain")
    domain_x = domain.get("x")
    domain_y = domain.get("y")
    threshold = TransFuncIntensity.find("threshold")
    threshold_x = threshold.get("x")
    threshold_y = threshold.get("y")
    
    list_intensity = []
    list_split = []
    list_r = []
    list_g = []
    list_b = []
    list_a = []
    
    for key in root.iter('key'):
        colour = key.find("colorL")
        list_intensity.append(key.find("intensity").get("value"))
        list_split.append(key.find("split").get("value"))
        list_r.append(colour.get("r"))
        list_g.append(colour.get("g"))
        list_b.append(colour.get("b"))
        list_a.append(colour.get("a"))

    # Create transfer mapping scalar value to opacity
    opacityTransferFunction = vtk.vtkPiecewiseFunction()
     
    # Create transfer mapping scalar value to color
    colorTransferFunction = vtk.vtkColorTransferFunction()
    
    max_intensity = 255
    for i in range(len(list_intensity)):
        intensity = float(list_intensity[i]) * max_intensity
        r = float(list_r[i]) / max_intensity
        g = float(list_g[i]) / max_intensity
        b = float(list_b[i]) / max_intensity
        a = float(list_a[i]) / max_intensity
        opacityTransferFunction.AddPoint(intensity, a)
        colorTransferFunction.AddRGBPoint(intensity, r, g, b)

    return opacityTransferFunction, colorTransferFunction

def plot_tf(opacityTransferFunction, colorTransferFunction):
    v4 = [0] * 4
    v6 = [0] * 6
    color_list = []
    opacity_list = []
    intensity_list = []
    N = colorTransferFunction.GetSize()
    for i in range(N):
        colorTransferFunction.GetNodeValue(i, v6)
        opacityTransferFunction.GetNodeValue(i, v4)
        intensity_list.append(v4[0])
        opacity_list.append(v4[1])
        color_list.append([v6[1], v6[2], v6[3]])
    
    x = intensity_list
    y = opacity_list
    colors = color_list
    area = [15**2] * N
    plt.title("Transfer Function")
    plt.xlabel("Intensity")
    plt.ylabel("Opacity")
    plt.scatter(x, y, s=area, color=colors, alpha=0.5)
    plt.plot(x, y, '-o', color=[.6,.6,.6])
    plt.show()

if __name__ == "__main__":
    print sys.argv[0]
    print __file__
    app = QtGui.QApplication(sys.argv)
    opacityTransferFunction, colorTransferFunction = load_transfer_function()
    plot_tf(opacityTransferFunction, colorTransferFunction)
    sys.exit(app.exec_())
