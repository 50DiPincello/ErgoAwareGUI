#### 
# Everytime I change interface.py by editing qtdesigner, have to import:
# from PySide2.QtCore import *
# from PySide2.QtGui import *
# from PySide2.QtWidgets import *
# Comment this import: from PyQt5 import QtCore, QtGui, QtWidgets
# And clear 3 wrong packages behind QWidget, etc. with ctrl+F2 to "change all occurrences"


import sys
import os
from PySide2 import *

from interface import *

import webbrowser

#MAIN WINDOW CLASS
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Remove window title bar
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
        #Set main background to transparent
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        #Shadow effect style
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(50)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 92, 157, 550))

        #Apply shadow to central widget -> WHAT COMES NEXT TO UI IS ALWAYS AN OBJECT FROM MY QT DESIGNER
        self.ui.centralwidget.setGraphicsEffect(self.shadow)

        #Set window icon -> this would not appear on the app main window because I removed the title bar
        #self.setWindowIcon(QtGui.QIcon(":/icons/icons/anchor.svg"))
        self.setWindowIcon(QtGui.QIcon("/home/gui/Desktop/Tese/Treinos/Training3/ea.ico"))

        #Set window title
        self.setWindowTitle("MODERN UI")

        #Window Size grip to resize window -> WHAT COMES NEXT TO UI IS ALWAYS AN OBJECT FROM MY QT DESIGNER
        QSizeGrip(self.ui.size_grip)

        #Minimize Window
        self.ui.minimize_window_button.clicked.connect(lambda: self.showMinimized())

        #Close window
        self.ui.close_window_button.clicked.connect(lambda: self.close())
        self.ui.exit_button.clicked.connect(lambda: self.close())

        #Restore/Maximize window
        self.ui.restore_window_button.clicked.connect(lambda: self.restore_or_maximize_window())

        #Funciton to move window on mouse drag event on the tittle bar
        def moveWindow(e):
            #detect if the window is normal size
            if self.isMaximized() == False:
                #move window only when window is normal size
                #if left mouse is clicked (only accept left mouse button clicks)
                if e.buttons() == Qt.LeftButton:
                    #move window
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()
        
        #Add click event/mouse move event/drag event to the top header to move the window
        self.ui.header_frame.mouseMoveEvent = moveWindow

        #Left menu toggle button
        self.ui.open_close_side_bar_btn.clicked.connect(lambda: self.slideLeftMenu())

        #Button to ergoaware site
        self.ui.site_button.clicked.connect(lambda: self.goToSite())

        self.show()
    
    #Site Ergoaware
    def goToSite(self):
        webbrowser.open('http://birdlab.dei.uminho.pt/ergoaware/')

    #Slide left menu function
    def slideLeftMenu(self):
        #get current left menu width
        width = self.ui.side_menu_container.width()

        #if minimized
        if width == 0:
            #expand menu
            newWidth = 200
            self.ui.open_close_side_bar_btn.setIcon(QtGui.QIcon(":/icons/icons/chevron-left.svg"))
        #if maximized
        else:
            #restore menu
            newWidth = 0
            self.ui.open_close_side_bar_btn.setIcon(QtGui.QIcon(":/icons/icons/align-left.svg"))
        
        #animate the transition
        self.animation = QPropertyAnimation(self.ui.side_menu_container, b"maximumWidth") #Animate minimumWidth
        self.animation.setDuration(250)
        self.animation.setStartValue(width) #start value is the current menu width
        self.animation.setEndValue(newWidth) #end value is the new menu width
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    #Add mouse events to the window
    def mousePressEvent(self, event):
        #get the current position of the mouse
        self.clickPosition = event.globalPos()
        #we will use this value to move the window

    #Update restore button icon on maximizing or minimizing window
    def restore_or_maximize_window(self):
        #If window is maximized
        if self.isMaximized():
            self.showNormal()
            #change icon
            self.ui.restore_window_button.setIcon(QtGui.QIcon(":/icons/icons/maximize-2.svg"))
        else:
            self.showMaximized()
            #change icon
            self.ui.restore_window_button.setIcon(QtGui.QIcon(":/icons/icons/minimize-2.svg"))



#EXECUTE APP
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())