from PyQt5.QtCore import QObject, pyqtSignal

class MSGNotification(QObject):
    new_message = pyqtSignal(str)  # Emitting sender and message content
notif = MSGNotification()