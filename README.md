# CodeyBank_v2.0
Update to the personal project, [CodeyBank](https://github.com/deshaunnascott/CodeyBank.git), to practice database 
and GUI development with Python. The GUI went through a complete overhaul. This project now uses PyQt5 as the GUI
framework instead of Tkinter.
 
This project is intended to mock the basic operations of a bank account owner at Codey Bank

## Table of Contents
* [Current Features](#current-features)
* [Resources](#resources)
* [Setup](#local-setup)
* [Extra Information](#extra-information)
* [Possible Future Developments](#possible-future-development)

## Current Features
    * View Account Balance
    * Transfer
    * Check Deposit
    * Update Account Details
	* Delete Bank Account

## Resources

    random
    PyQt5
	qt_material
    sqlite

I created the credit card graphic on the splash screen in Inkscape following this Logos By Nick 
[tutorial](https://youtu.be/6YSauUjjSqk). I also created the CBP Icon in Inkscape.

## Local Setup
1) Navigate to your local CodeyBank_v2.0 project folder

2) Run Main Driver File

		python CBPortal.py

## Extra Information
Something to note about these accounts is that they currently allow for the user to overdraw their account.
So it is possible for an account to have a negative balance.

## Possible Future Development
* Add a sample database
* Create a CodeyBank Manager Portal for access to total bank database