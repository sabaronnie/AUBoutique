from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from pyqttoast import Toast, ToastPreset, ToastPosition
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor

# BOTTOM_LEFT, BOTTOM_MIDDLE, BOTTOM_RIGHT, TOP_LEFT, TOP_MIDDLE, TOP_RIGHT, CENTER

def getErrorNotification(title, text, somewidget):
    toast = Toast()
    toast.setDuration(5000)  # Hide after 5 seconds
    toast.setTitle(title)
    toast.setText(text)
    toast.setBorderRadius(8)
    
    # Apply style preset
    toast.applyPreset(ToastPreset.ERROR)    
    
    toast.setPositionRelativeToWidget(somewidget) 
    toast.setPosition(ToastPosition.TOP_RIGHT)  
    toast.show()
    
def getSuccessNotification(title, text, somewidget):
    toast = Toast()
    toast.setDuration(5000)  # Hide after 5 seconds
    toast.setTitle(title)
    toast.setText(text)
    toast.setBorderRadius(8)
    
    # Apply style preset
    toast.applyPreset(ToastPreset.SUCCESS)    
    
    toast.setPositionRelativeToWidget(somewidget) 
    toast.setPosition(ToastPosition.TOP_RIGHT)  
    toast.show()
    
def getInfoNotification(title, text, somewidget):
    toast = Toast()
    toast.setDuration(5000)  # Hide after 5 seconds
    toast.setTitle(title)
    toast.setText(text)
    toast.setBorderRadius(8)
    
    # Apply style preset
    toast.applyPreset(ToastPreset.INFORMATION)    
    
    toast.setPositionRelativeToWidget(somewidget) 
    toast.setPosition(ToastPosition.TOP_RIGHT)  
    toast.show()
    
def getWarningNotification(title, text, somewidget):
    toast = Toast()
    toast.setDuration(5000)  # Hide after 5 seconds
    toast.setTitle(title)
    toast.setText(text)
    toast.setBorderRadius(8)
    
    # Apply style preset
    toast.applyPreset(ToastPreset.WARNING)    
    
    toast.setPositionRelativeToWidget(somewidget) 
    toast.setPosition(ToastPosition.TOP_RIGHT)  
    toast.show()