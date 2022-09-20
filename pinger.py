from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit
from PyQt6.QtGui import QIcon, QFont 
from PyQt6.QtCore import QObject, QThread, pyqtSignal
import sys, urllib.request, socket 
from notifypy import Notify
from time import sleep

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    def run(self):
        """Long-running task."""
        while True:
            mwindow.message = mwindow.client.recv(16).decode('ascii')
            try :
                if mwindow.message[:6] == "PINGED" or mwindow.message == "Why?" or mwindow.message == "404" :
                    mwindow.lable3.setText(mwindow.message)

                elif mwindow.message[:5] == "PING ":
                    mwindow.lable3.setText(mwindow.message)
                    mwindow.notif(mwindow.message)

            except Exception as e :
                mwindow.lable3.setText("There is a problem please Reconnect")
                mwindow.notif(e)
                    


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("pinger")
        self.setWindowIcon(QIcon("icon.png"))
        self.setFixedHeight(300)
        self.setFixedWidth(500)
        self.setWindowOpacity(0.98)
        self.wdg()

        self.host = '132.145.109.138'
        self.port = 8002
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)




    def wdg(self):
        btn1 = QPushButton("connect", self)
        btn1.setIcon(QIcon("connect.png"))
        btn1.setGeometry(200, 85, 100, 25)
        btn1.clicked.connect(self.connect_user)


        btn2 = QPushButton("ping", self)
        btn2.setIcon(QIcon("ping.png"))
        btn2.setGeometry(200, 160, 100, 25)
        btn2.clicked.connect(self.ping_user)

        btn3= QPushButton("Exit", self)
        btn3.setGeometry(0, 0, 50, 25)
        btn3.setIcon(QIcon("powerbtn.png"))
        btn3.clicked.connect(self.powerbtn)

        btn4= QPushButton("", self)
        btn4.setGeometry(380, 0, 30, 30)
        btn4.setIcon(QIcon("refresh.png"))
        btn4.clicked.connect(self.checknet)        


        self.textbox1 = QLineEdit(self)
        self.textbox1.setGeometry(150, 30, 200,50)
        self.textbox1.setFont(QFont("Cambria", 15))

        self.textbox2 = QLineEdit(self)
        self.textbox2.setGeometry(150, 110, 200,50)
        self.textbox2.setFont(QFont("Cambria", 15))

        self.lable1 = QLabel("stat..", self)
        self.lable1.setGeometry(430, 0, 70, 30)
        self.lable1.setFont(QFont("Segoe Print", 15))

        self.lable2 = QLabel("status :", self)
        self.lable2.setGeometry(120, 195, 75, 70)
        self.lable2.setFont(QFont("Segoe Print", 15))

        self.lable3 = QLabel("", self)
        self.lable3.setGeometry(200, 195, 300, 70)
        self.lable3.setFont(QFont("Segoe Print", 15))

        self.lable4 = QLabel("connected as : not connected", self)
        self.lable4.setGeometry(150, 0, 200, 30)
        self.lable4.setFont(QFont("Cambria", 12))
        
    def powerbtn(self):
        exit()

    def checknet(self):
        "check internet connection"
        try:
            urllib.request.urlopen("http://google.com")
            self.lable1.setText("Online")
            self.lable1.setStyleSheet("color:green")
        except:
            self.lable1.setText("Offline")
            self.lable1.setStyleSheet("color:red")

    def notif(self , msg):
        "notofication fnc"
        notification = Notify()
        notification.title = "pinger"
        notification.message = msg
        notification.audio = "notif.wav"
        notification.icon = "icon.png"
        notification.send()

    def connect_user(self):
        "connect user to server by username"
        self.username = self.textbox1.text()
        try:
            self.client.connect((self.host, self.port))
            self.message = self.client.recv(16).decode('ascii')
            if self.message == 'NICK':
                self.client.send(self.username.encode('utf8'))

            self.message = self.client.recv(16).decode('ascii')
            if self.message == "OK":
                self.lable4.setText(f"Connected as : {self.username}")
                self.notif(f"Connected as {self.username}")
                self.is_pinged()

        except Exception as e :
                self.lable4.setText(f"{e}")
        
    def ping_user(self):
        "ping friend with friendname"
        self.friendname = self.textbox2.text()
        self.client.send(self.friendname.encode('utf8'))


    def is_pinged(self):
        "check if you got pinged by your friend"
        self.thread = QThread()  # type: ignore
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.thread.start()






m_app =QApplication(sys.argv)
mwindow = Window()
mwindow.show()

sys.exit(m_app.exec())