# signals.py
from PyQt5.QtCore import QObject, pyqtSignal

class BackendSignals(QObject):
    # Define a signal that will emit a message (str)
    new_message = pyqtSignal(str)

# Create a global instance of BackendSignals
signals = BackendSignals()