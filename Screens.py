import os
import sys
import ctypes
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication
from qt_material import apply_stylesheet

class SplashScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(SplashScreen, self).__init__()
        loadUi("./Screens/SplashScreen.ui", self)
        self.getStartedButton.clicked.connect(self.goToLoginScreen)

    def goToLoginScreen(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

class LoginScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("./Screens/LoginScreen.ui", self)
        self.loginButton.clicked.connect(self.goToAcctOptsScreen)
        self.joinButton.clicked.connect(self.goToNewMemScreen)



    def goToAcctOptsScreen(self):
        acctOptsScreen = AccountOptionsScreen()
        widget.addWidget(acctOptsScreen)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def goToNewMemScreen(self):
        newMemScreen = NewMemberScreen()
        widget.addWidget(newMemScreen)
        widget.setCurrentIndex(widget.currentIndex()+1)

class NewMemberScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(NewMemberScreen, self).__init__()
        loadUi("./Screens/NewMemberScreen.ui", self)
        self.newMemJoinButton.clicked.connect(self.goToAcctOptScreen)
        self.newMemCancelButton.clicked.connect(self.goToLoginScreen)

    def goToAcctOptScreen(self):
        self.newMemAcctNum.setText("12345")

    def goToLoginScreen(self):
        self.newMemAcctNum.setText("Canceled")

class AccountOptionsScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(AccountOptionsScreen, self).__init__()
        loadUi("./Screens/AccountOptionsScreen.ui", self)

# class AddAccountTypeScreen(QtWidgets.QMainWindow):
#     def __init__(self):
#         super(AddAccountTypeScreen, self).__init__()
#         loadUi("./Screens/AddAccountTypeScreen.ui", self)
#
# class AccountDetailsScreen(QtWidgets.QMainWindow):
#     def __init__(self):
#         super(AccountDetailsScreen, self).__init__()
#         loadUi("./Screens/AccountDetailsScreen.ui", self)
#
# class TransferScreen(QtWidgets.QMainWindow):
#     def __init__(self):
#         super(TransferScreen, self).__init__()
#         loadUi("./Screens/TransferScreen.ui", self)

# class ExitScreen(QtWidgets.QMainWindow):
#     def __init__(self):
#         super(ExitScreen, self).__init__()
#         loadUi("./Screens/ExitScreen.ui", self)
#
#     def goToSplashScreen(self):
#         splash = SplashScreen()
#         widget.addWidget(splash)
#         widget.setCurrentIndex(widget.currentIndex()+1)

# def main():
    # Create taskbar icon
myappid = u'mycompany.myproduct.subproduct.version'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

app = QApplication(sys.argv)
app.setApplicationName("CB Portal")
app.setWindowIcon(QtGui.QIcon("Icons/CBP_Icon(50x50).png"))
splashScreen = SplashScreen()
apply_stylesheet(app, theme='dark_teal.xml')
stylesheet = app.styleSheet()
with open('custom.css') as file:
    app.setStyleSheet(stylesheet + file.read().format(**os.environ))
widget = QtWidgets.QStackedWidget()
widget.addWidget(splashScreen)
widget.setFixedHeight(400)
widget.setFixedWidth(500)
widget.show()

sys.exit(app.exec_())
