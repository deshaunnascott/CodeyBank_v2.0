# =============================================================================
# Created By  : ShaunCodes
# Created Date: July 03, 2021
# =============================================================================
"""
This file contains the code to create the CodeyBank GUI Screens
"""
# =============================================================================
# Imports
# =============================================================================
import os
import sys
import ctypes
import random

import AccountClass
import MemDatabase
import config

from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from qt_material import apply_stylesheet

# =============================================================================
# Class Definitions for GUI Screens
# =============================================================================
class SplashScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(SplashScreen, self).__init__()
        loadUi("./Screens/SplashScreen.ui", self)
        self.getStartedButton.clicked.connect(goToLoginScreen)

class LoginScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("./Screens/LoginScreen.ui", self)
        self.loginButton.clicked.connect(self.verifyAcct)
        self.joinButton.clicked.connect(goToNewMemScreen)

    def verifyAcct(self):
        acctNum = self.usernameEdit.text().strip()
        acctPin = self.passwordEdit.text().strip()

        if len(acctNum) == 0 or len(acctPin) == 0:
            # clear the line edit widget
            self.usernameEdit.clear()
            self.passwordEdit.clear()

            return

        if not acctNum.isnumeric() or not acctPin.isnumeric():
            # clear the line edit widget
            self.usernameEdit.clear()
            self.passwordEdit.clear()

            return

        # check for account in the database
        exists = config.DB.member_exists(config.DB.table, int(acctNum), int(acctPin))

        if exists:
            # clear the line edit widget
            self.usernameEdit.clear()
            self.passwordEdit.clear()

            acct_info = config.DB.get_acct_info(config.DB.table, 'acctNum', int(acctNum))
            config.ACCT = AccountClass.Account(acct_info[0], acct_info[1], acct_info[2],
                                               acct_info[3], acct_info[4], acct_info[5])

            goToAcctOptsScreen()
        else:
            # clear the line edit widget
            self.usernameEdit.clear()
            self.passwordEdit.clear()

            showPopUp("Invalid Entry. Try Again.")

class NewMemberScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(NewMemberScreen, self).__init__()
        loadUi("./Screens/NewMemberScreen.ui", self)
        self.newMemJoinButton.clicked.connect(self.addNewMember)
        self.newMemCancelButton.clicked.connect(goToLoginScreen)

    def addNewMember(self):
        acctNum = self.newMemAcctNum.text().strip()
        pin = self.newAcctPinEdit.text().strip()
        fName = self.newMemFNameEdit.text().strip()
        lName = self.newMemLNameEdit.text().strip()
        config.ACCT = AccountClass.Account(acctNum, pin, fName, lName)

        config.DB.add_new_acct(config.DB.table, config.ACCT)

        goToAcctOptsScreen()

class AccountOptionsScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(AccountOptionsScreen, self).__init__()
        loadUi("./Screens/AccountOptionsScreen.ui", self)
        self.acctDtlsButton.clicked.connect(goToAccDtlsScreen)
        self.transferButton.clicked.connect(goToTransferScreen)
        self.checkDepositButton.clicked.connect(goToCheckDepScreen)
        self.updateAcctButton.clicked.connect(goToUpdateAcctScreen)
        self.logOutButton.clicked.connect(goToExitScreen)
        self.deleteAcctButton.clicked.connect(deleteAccount)

class AccountDetailsScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(AccountDetailsScreen, self).__init__()
        loadUi("./Screens/AccountDetailsScreen.ui", self)
        self.backButton.clicked.connect(goToAcctOptsScreen)

class TransferScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(TransferScreen, self).__init__()
        loadUi("./Screens/TransferScreen.ui", self)
        self.backButton.clicked.connect(goToAcctOptsScreen)
        self.submitButton.clicked.connect(self.transferAmount)

    def transferAmount(self):
        transAcctNum = self.recAcctNumEdit.text().strip()
        transAmt = self.transferAmountEdit.text().strip()

        # Error check to make sure account information is given
        if len(transAcctNum) == 0:
            showPopUp("Enter Account Number!")
            return

        # Error check to make sure receiving about is valid member.
        exists = config.DB.in_database(config.DB.table, 'acctNum', int(transAcctNum))
        if not exists:
            showPopUp("Invalid Account Number! Member does not exist.")
            return

        # Grab transfer account information from database
        trans_acct_info = config.DB.get_acct_info(config.DB.table, 'acctNum', int(transAcctNum))
        config.TACCT = AccountClass.Account(trans_acct_info[0], trans_acct_info[1], trans_acct_info[2],
                                            trans_acct_info[3], trans_acct_info[4], trans_acct_info[5])

        # Deduct transfer amount from current account
        if self.fromCheckingButton.isChecked():
            config.ACCT.mem_cbalance = config.ACCT.mem_cbalance-float(transAmt)
            acctType = 'checking_balance'
            config.DB.update_balance(config.DB.table, config.ACCT.acct_num, acctType, config.ACCT.mem_cbalance)

        elif self.fromSavingsButton.isChecked():
            config.ACCT.mem_sbalance = config.ACCT.mem_sbalance-float(transAmt)
            acctType = 'savings_balance'
            config.DB.update_balance(config.DB.table, config.ACCT.acct_num, acctType, config.ACCT.mem_sbalance)

        else:
            showPopUp("Select an account type!")

        # Add transfer amount to transfer account
        if self.transCheckingButton.isChecked():
            config.TACCT.mem_cbalance = config.TACCT.mem_cbalance + float(transAmt)
            transAcctType = 'checking_balance'
            config.DB.update_balance(config.DB.table, config.TACCT.acct_num, transAcctType, config.TACCT.mem_cbalance)
            showPopUp("${amt:.2f} has been transferred to the Checking account of "
                      "{fname} {lname}".format(amt=float(transAmt), fname=config.TACCT.mem_first_name,
                                               lname=config.TACCT.mem_last_name))

        elif self.transSavingsButton.isChecked():
            config.TACCT.mem_sbalance = config.TACCT.mem_sbalance + float(transAmt)
            transAcctType = 'savings_balance'
            config.DB.update_balance(config.DB.table, config.TACCT.acct_num, transAcctType, config.TACCT.mem_sbalance)
            showPopUp("${amt:.2f} has been transferred to the Savings account of "
                      "{fname} {lname}".format(amt=float(transAmt), fname=config.TACCT.mem_first_name,
                                               lname=config.TACCT.mem_last_name))

        else:
            showPopUp("Select a transfer account type!")

class CheckDepositScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(CheckDepositScreen, self).__init__()
        loadUi("./Screens/CheckDepositScreen.ui", self)
        self.backButton.clicked.connect(goToAcctOptsScreen)
        self.submitButton.clicked.connect(self.updateBalance)

    def updateBalance(self):
        Amt = self.checkAmountEdit.text().strip()

        if self.depositCheckingButton.isChecked():
            config.ACCT.mem_cbalance = config.ACCT.mem_cbalance+float(Amt)
            acctType = 'checking_balance'
            config.DB.update_balance(config.DB.table, config.ACCT.acct_num, acctType, config.ACCT.mem_cbalance)

        elif self.depositSavingsButton.isChecked():
            config.ACCT.mem_sbalance = config.ACCT.mem_sbalance+float(Amt)
            acctType = 'savings_balance'
            config.DB.update_balance(config.DB.table, config.ACCT.acct_num, acctType, config.ACCT.mem_sbalance)

        else:
            showPopUp("Select an account type!")

        goToAcctOptsScreen()

class UpdateAccountScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(UpdateAccountScreen, self).__init__()
        loadUi("./Screens/UpdateAccountScreen.ui", self)
        self.backButton.clicked.connect(goToAcctOptsScreen)
        self.submitButton.clicked.connect(self.updateInfo)

    def updateInfo(self):
        newFName = self.newMemFNameEdit.text().strip()
        newLName = self.newMemLNameEdit.text().strip()
        newPin   = self.newAcctPinEdit.text().strip()

        # check if there is no information to update
        if len(newFName) == 0 and len(newLName) == 0 and len(newPin) == 0:
            # clear the line edit widget
            self.newMemFNameEdit.clear()
            self.newMemLNameEdit.clear()
            self.newAcctPinEdit.clear()

            showPopUp("Fields are empty!\nUnsuccessful Update!")
            return

        # update account with new first name
        if len(newFName) != 0:
            config.ACCT.mem_first_name = newFName
            config.DB.update_account(config.DB.table,
                                     config.ACCT.acct_num,
                                     'first_name',
                                     config.ACCT.mem_first_name)

        # update account with new last name
        if len(newLName) != 0:
            config.ACCT.mem_last_name = newLName
            config.DB.update_account(config.DB.table,
                                     config.ACCT.acct_num,
                                     'last_name',
                                     config.ACCT.mem_last_name)

        # update account with new pin
        if len(newPin) != 0:
            config.ACCT.mem_pin = int(newPin)
            config.DB.update_account(config.DB.table,
                                     config.ACCT.acct_num,
                                     'pin',
                                     config.ACCT.mem_pin)

        # clear the line edit widget
        self.newMemFNameEdit.clear()
        self.newMemLNameEdit.clear()
        self.newAcctPinEdit.clear()

        # Update member name
        memName = config.ACCT.mem_first_name + ' ' + config.ACCT.mem_last_name
        self.acctHolderName.setText(memName)
        showPopUp("Account Update Successful")

class ExitScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(ExitScreen, self).__init__()
        loadUi("./Screens/ExitScreen.ui", self)
        self.startOverButton.clicked.connect(goToSplashScreen)

# =============================================================================
# GUI Go To Screen Functions
# =============================================================================
def goToSplashScreen():
    config.GUI.setCurrentIndex(config.SCREENS.SPLASHCREEN.value)

def goToLoginScreen():
    config.GUI.setCurrentIndex(config.SCREENS.LOGINSCREEN.value)

def goToNewMemScreen():
    config.GUI.setCurrentIndex(config.SCREENS.NEWMEMSCREEN.value)
    # set widget defaults
    config.GUI.currentWidget().newMemFNameEdit.clear()
    config.GUI.currentWidget().newMemLNameEdit.clear()
    config.GUI.currentWidget().newAcctPinEdit.clear()

    # Grab new account number for new member
    exists = True
    acctNum = 0

    while exists:
        # generate new account number
        acctNum = random.randint(1000, 9999)

        # check for account number in database
        exists = config.DB.in_database(config.DB.table, 'acctNum', int(acctNum))

    acctNum = "{num}".format(num=acctNum)
    config.GUI.currentWidget().newMemAcctNum.setText(acctNum)

def goToAcctOptsScreen():
    config.GUI.setCurrentIndex(config.SCREENS.ACCTOPTSCREEN.value)

    # update member name is bottom left of screen
    memName = config.ACCT.mem_first_name + ' ' + config.ACCT.mem_last_name
    config.GUI.currentWidget().acctOptsMemName.setText(memName)

def goToAccDtlsScreen():
    config.GUI.setCurrentIndex(config.SCREENS.ACCTDETSCREEN.value)

    # Update screen with member details
    acctNum = "{num}".format(num=config.ACCT.acct_num)
    memName = config.ACCT.mem_first_name + ' ' + config.ACCT.mem_last_name
    cbalance = "{balance:.2f}".format(balance=config.ACCT.mem_cbalance)
    sbalance = "{balance:.2f}".format(balance=config.ACCT.mem_sbalance)
    config.GUI.currentWidget().checkingBalance.setText(cbalance)
    config.GUI.currentWidget().savingsBalance.setText(sbalance)
    config.GUI.currentWidget().acctHolderNum.setText(acctNum)
    config.GUI.currentWidget().acctHolderName.setText(memName)

def goToTransferScreen():
    config.GUI.setCurrentIndex(config.SCREENS.TRANSFERSCREEN.value)
    # set widget defaults
    config.GUI.currentWidget().fromCheckingButton.setChecked(True)
    config.GUI.currentWidget().fromSavingsButton.setChecked(False)
    config.GUI.currentWidget().transCheckingButton.setChecked(True)
    config.GUI.currentWidget().transSavingsButton.setChecked(False)
    config.GUI.currentWidget().recAcctNumEdit.clear()
    config.GUI.currentWidget().transferAmountEdit.clear()

def goToCheckDepScreen():
    config.GUI.setCurrentIndex(config.SCREENS.CHECKDEPSCREEN.value)
    # set widget defaults
    config.GUI.currentWidget().depositCheckingButton.setChecked(True)
    config.GUI.currentWidget().depositSavingsButton.setChecked(False)
    config.GUI.currentWidget().checkNumberEdit.clear()
    config.GUI.currentWidget().checkAmountEdit.clear()

def goToUpdateAcctScreen():
    config.GUI.setCurrentIndex(config.SCREENS.UPDATEACCTSCREEN.value)

    # Update screen with member details
    acctNum = "{num}".format(num=config.ACCT.acct_num)
    memName = config.ACCT.mem_first_name + ' ' + config.ACCT.mem_last_name
    config.GUI.currentWidget().acctHolderNum.setText(acctNum)
    config.GUI.currentWidget().acctHolderName.setText(memName)

def goToExitScreen():
    config.GUI.setCurrentIndex(config.SCREENS.EXITSCREEN.value)

    # clear current account and transfer account globals
    config.ACCT  = None
    config.TACCT = None

def showPopUp(msg):
    popup = QMessageBox()
    popup.setWindowTitle("CBP")
    popup.setText(msg)
    popup.setIcon(QMessageBox.Information)
    popup.exec_()

def confirmDialog(msg):
    confirm = QMessageBox()
    confirm.setWindowTitle("CBP")
    confirm.setIcon(QMessageBox.Warning)
    confirm.setText(msg)
    confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    choice = confirm.exec_()
    if choice == QMessageBox.Yes:
        return 1
    else:  # choice == QMessageBox.No
        return 0

# =============================================================================
# GUI Utility Functions
# =============================================================================
def deleteAccount():
    choice = confirmDialog("Are you sure you want to delete your account?\nThis action cannot be undone.")
    if choice:
        config.DB.delete_acct(config.DB.table, config.ACCT.acct_num)

        # account doesn't exist anymore so go straight to exit
        goToExitScreen()

def createStack():
    # Screen 1
    splashScreen = SplashScreen()
    config.GUI.addWidget(splashScreen)
    # Screen 2
    loginScreen = LoginScreen()
    config.GUI.addWidget(loginScreen)
    # Screen 3
    newMemScreen = NewMemberScreen()
    config.GUI.addWidget(newMemScreen)
    # Screen 4
    acctOptsScreen = AccountOptionsScreen()
    config.GUI.addWidget(acctOptsScreen)
    # Screen 5
    accDtlsScreen = AccountDetailsScreen()
    config.GUI.addWidget(accDtlsScreen)
    # Screen 6
    transferScreen = TransferScreen()
    config.GUI.addWidget(transferScreen)
    # Screen 7
    checkDepScreen = CheckDepositScreen()
    config.GUI.addWidget(checkDepScreen)
    # Screen 8
    updateAcctScreen = UpdateAccountScreen()
    config.GUI.addWidget(updateAcctScreen)
    # Screen 9
    exitScreen = ExitScreen()
    config.GUI.addWidget(exitScreen)

def configureApp():
    # Create taskbar icon
    myappid = u'CodeyBank.CBPortal.2.0'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # Create Application
    config.APP = QApplication(sys.argv)
    config.APP.setApplicationName("CB Portal")
    config.APP.setWindowIcon(QtGui.QIcon("Icons/CBP_Icon(50x50).png"))

    # Apply style to newly created application
    apply_stylesheet(config.APP, theme='dark_teal.xml')
    stylesheet = config.APP.styleSheet()
    with open('custom.css') as file:
        config.APP.setStyleSheet(stylesheet + file.read().format(**os.environ))

    # Create main window of GUI
    config.GUI = QtWidgets.QStackedWidget()
    config.GUI.setFixedHeight(400)
    config.GUI.setFixedWidth(500)

    # connect to database
    config.DB = MemDatabase.Database()

    # Add screens to main window
    createStack()
