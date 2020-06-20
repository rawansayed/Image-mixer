import logging

from PyQt5 import QtWidgets, QtCore, uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QMessageBox, QLabel)
from PyQt5.QtGui import QIcon, QPixmap
from pyqtgraph import ImageView
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
import sys
import cv2 as cv
import numpy as np
from ImageViewer import Ui_ImageViewer
from imageModel import ImageModel
from modesEnum import Modes

logging.basicConfig(filename="logging",level=logging.INFO)
log_file = logging.getLogger()
class ApplicationWindow(QtWidgets.QMainWindow):
    imageclass: ImageModel

    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_ImageViewer()
        self.ui.setupUi(self)
        # choose where you want input image to appear
        self.images = [self.ui.Image_1, self.ui.Image_2]
        self.images[0].triggered.connect(lambda: self.menubar_Control(0))
        self.images[1].triggered.connect(lambda: self.menubar_Control(1))
        self.flag = 0
        # choose where you want output image to appear
        self.outwidgets = [self.ui.Output1, self.ui.Output2]
        # choose type from input-FT-combobox
        self.inputcombos = [self.ui.choose1, self.ui.choose2]
        self.inputcombos[0].currentTextChanged.connect(lambda: self.inputcombobox(0))
        self.inputcombos[1].currentTextChanged.connect(lambda: self.inputcombobox(1))
        # choose which widget i want to show ft
        self.edits = [self.ui.EditImage1, self.ui.EditImage2]
        # Calling Mixer
        self.sliders = [self.ui.Slider1, self.ui.Slider2]
        for i in range(len(self.sliders)):
            self.sliders[i].setMaximum(100)
            self.sliders[i].setMinimum(0)
            self.sliders[i].setValue(50)
            self.sliders[i].setSingleStep(1)
            self.sliders[i].valueChanged.connect(self.checks)
        # Calling checks
        self.ui.Fchoose2.clear()
        self.ui.Fchoose1.currentIndexChanged.connect(self.change_combo)
        self.ui.Fchoose1.setCurrentIndex(1)
        self.ui.Fchoose2.currentIndexChanged.connect(self.checks)
        #list for images from imagemodel class
        self.imageclass = [0 for i in range(2)]
        # Hide Buttons that appeared in ImageView widgets
        self.hidebuttons = [self.ui.Image1, self.ui.EditImage1, self.ui.Image2, self.ui.EditImage2, self.ui.Output1,
                            self.ui.Output2]
        for j in range(len(self.hidebuttons)):
            self.hidebuttons[j].ui.histogram.hide()
            self.hidebuttons[j].ui.roiBtn.hide()
            self.hidebuttons[j].ui.menuBtn.hide()
            self.hidebuttons[j].ui.roiPlot.hide()

    def menubar_Control(self, i):
        self.images[i].triggered.connect(lambda: self.uploadimage(i))

    def uploadimage(self, i):
        self.image = QtWidgets.QFileDialog.getOpenFileName(None, 'open File',
                                                           'D:/BIOMEDICAL ENGINEERING/3rd/2nd semester/dsp/tasks/sbe309-2020-task3-rawansayed',
                                                           "images(*.jpg *.png)")
        self.img = cv.imread(self.image[0])
        # self.grayscale = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        if self.flag == 0:
            self.size = self.img.shape
            if i == 0:
                log_file.info("upload image 1")
                self.image1 = ImageModel(imgPath=self.image[0])
                self.imageclass[0] = self.image1
                self.ui.Image1.show()
                self.ui.Image1.setImage(self.image1.imgByte.T)
                self.flag = 1
            elif i == 1:
                log_file.info("upload image 2")
                self.image2 = ImageModel(imgPath=self.image[0])
                self.imageclass[1] = self.image2
                self.ui.Image2.show()
                self.ui.Image2.setImage(self.image2.imgByte.T)
                self.flag = 0
        elif self.flag == 1:
            if (self.size == self.img.shape):
                if i == 1:
                    log_file.info("upload image 2")
                    self.image2 = ImageModel(self.image[0])
                    self.imageclass[1] = self.image2
                    self.ui.Image2.show()
                    self.ui.Image2.setImage(self.image2.imgByte.T)
                    self.flag = 0
            else:
                log_file.info("Size Error")
                self.errormsg = QMessageBox()
                self.errormsg.setWindowTitle("ERROR404")
                self.errormsg.setText("The 2 Images have Different Size and This isn't Allowable")
                self.errormsg.setStandardButtons(QMessageBox.Ok)
                self.errormsg.setIcon(QMessageBox.Critical)
                self.x = self.errormsg.exec_()

    def inputcombobox(self, i):
        self.edits[i].clear()
        self.edits[i].show()
        if (str(self.inputcombos[i].currentText())) == 'Phase':
            log_file.info("Show FT-Phase")
            self.edits[i].setImage(self.imageclass[i].phase.T)
        elif (str(self.inputcombos[i].currentText())) == 'Magnitude':
            log_file.info("Show FT-Magnitude")
            self.edits[i].setImage(20*np.log(np.fft.fftshift(self.imageclass[i].magnitude)+1).T)
        elif (str(self.inputcombos[i].currentText())) == 'Real':
            log_file.info("Show FT-Real")
            self.edits[i].setImage(20 * np.log(self.imageclass[i].real + 1).T)
        elif (str(self.inputcombos[i].currentText())) == 'Imaginary':
            log_file.info("Show FT-Imaginary")
            self.edits[i].setImage(20 * np.log(self.imageclass[i].imaginary + 1).T)

    
    def change_combo(self):
        text1 = str(self.ui.Fchoose1.currentText())
        if text1 == "Magnitude":
            log_file.info("Combo 1 option is Magnitude so combo 2 will have Phase,Uniform Phase Items ")
            self.ui.Fchoose2.clear()
            self.ui.Fchoose2.addItems(['Phase','Uniform Phase'])
        elif text1 == "Phase":
            log_file.info("Combo 1 option is Phase so combo 2 will have Magnitude,Uniform Magnitude Items ")
            self.ui.Fchoose2.clear()
            self.ui.Fchoose2.addItems(['Magnitude','Uniform Magnitude'])
        elif text1 == "Real":
            log_file.info("Combo 1 option is Real so combo 2 will have Imaginary Item ")
            self.ui.Fchoose2.clear()
            self.ui.Fchoose2.addItems(['Imaginary'])
        elif text1 == "Imaginary":
            log_file.info("Combo 1 option is Imaginary so combo 2 will have Real Item ")
            self.ui.Fchoose2.clear()
            self.ui.Fchoose2.addItems(['Real'])
        elif text1 == "Uniform Magnitude":
            log_file.info("Combo 1 option is Uniform Magnitude so combo 2 will have Phase,Uniform Phase Items ")
            self.ui.Fchoose2.clear()
            self.ui.Fchoose2.addItems(['Phase','Uniform Phase'])   
        elif text1 == "Uniform Phase":
            log_file.info("Combo 1 option is Uniform Phase so combo 2 will have Magnitude,Uniform Magnitude Items ")
            self.ui.Fchoose2.clear()
            self.ui.Fchoose2.addItems(['Magnitude','Uniform Magnitude'])     


    def checks(self):
        ratio1 = float(float(self.ui.Slider1.value())/100.0)
        log_file.info("Get Ratio 1 from Slider 1")
        ratio2 = float(float(self.ui.Slider2.value())/100.0)
        log_file.info("Get Ratio 2 from Slider 2")
        # Component indecies(image 1 or 2)
        index1 = self.ui.Mchoose1.currentIndex()
        log_file.info("What you choose from Component 1 (image 1 or 2)")
        index2 = self.ui.Mchoose2.currentIndex()
        log_file.info("What you choose from Component 2 (image 1 or 2)")
        text1 = str(self.ui.Fchoose1.currentText())
        text2 = str(self.ui.Fchoose2.currentText())
        print(ratio1,ratio2,text1,text2,index1,index2)
        if text1 == "Magnitude":
            print("Magnitude")
            if (text2) == "Phase":
                log_file.info("You are now in Mode=magnitudeAndPhase")
                self.draw = self.imageclass[index1].mix(self.imageclass[index2],
                                                             ratio1,
                                                             ratio2, Modes.magnitudeAndPhase)
            elif (text2) == "You are now in Mode=Uniform Phase":
                log_file.info("Modes.uniformPhase")
                self.draw = self.imageclass[index1].mix(self.imageclass[index2],
                                                             ratio1,
                                                             ratio2, Modes.uniformPhase)
        elif (text1) == "Phase":
            if (text2) == "Magnitude":
                log_file.info("You are now in Mode=magnitudeAndPhase")
                self.draw = self.imageclass[index2].mix(self.imageclass[index1], ratio2,
                                                      ratio1, Modes.magnitudeAndPhase)
            elif (text2) == "Uniform Magnitude":
                log_file.info("You are now in Mode=uniformMagnitude")
                self.draw = self.imageclass[index2].mix(self.imageclass[index1],
                                                             ratio2,
                                                             ratio1, Modes.uniformMagnitude)
        elif (text1) == "Uniform Magnitude":
            if (text2)  == "Phase":
                log_file.info("You are now in Mode=uniformMagnitude")
                self.draw = self.imageclass[index1].mix(self.imageclass[index2],
                                                             ratio1,
                                                            ratio2, Modes.uniformMagnitude)
            elif (text2)  == "Uniform Phase":
                log_file.info("You are now in Mode=uniformMagnitudeAndPhase")
                self.draw = self.imageclass[index1].mix(self.imageclass[index2],
                                                             ratio1,
                                                             ratio2,
                                                             Modes.uniformMagnitudeAndPhase)
        elif (text1) == "Uniform Phase":
            if (text2)  == "Magnitude":
                log_file.info("You are now in Mode=uniformPhase")
                self.draw = self.imageclass[index2].mix(self.imageclass[index1],
                                                             ratio2,
                                                             ratio1, Modes.uniformPhase)
            elif (text2)  == "Uniform Magnitude":
                log_file.info("You are now in Mode=uniformMagnitudeAndPhase")
                self.draw = self.imageclass[index2].mix(self.imageclass[index1],
                                                             ratio2,
                                                             ratio1,
                                                             Modes.uniformMagnitudeAndPhase)
        elif (text1) == "Real":
            if (text2) == "Imaginary":
                log_file.info("You are now in Mode=realAndImaginary")
                self.draw = self.imageclass[index1].mix(self.imageclass[index2],
                                                             ratio1,
                                                             ratio2, Modes.realAndImaginary)
        elif (text1) == "Imaginary":
            print("Imaginary")
            if (text2) == "Real":
                log_file.info("You are now in Mode=realAndImaginary")
                self.draw = self.imageclass[index2].mix(self.imageclass[index1],
                                                             ratio2,
                                                             ratio1, Modes.realAndImaginary)

        self.outindex = self.ui.choosemixeroutput.currentIndex()
        self.outwidgets[self.outindex].clear()
        self.outwidgets[self.outindex].show()
        self.outwidgets[self.outindex].setImage(self.draw.T)

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    # Now use a palette to switch to dark colors:
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()
