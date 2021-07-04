# =============================================================================
# Created By  : ShaunCodes
# Created Date: July 3, 2021
# =============================================================================
"""
This file contains the code to create Account Objects
"""
# =============================================================================
# Class Definitions for Account
# =============================================================================
class Account:

    # Object constructor
    def __init__(self, acct_num=0, mem_pin=0, mem_first_name='John', mem_last_name='Doe', mem_cbalance=0.0,
                 mem_sbalance=0.0):
        self.acct_num = acct_num
        self.mem_pin = mem_pin
        self.mem_first_name = mem_first_name
        self.mem_last_name = mem_last_name
        self.mem_cbalance = mem_cbalance
        self.mem_sbalance = mem_sbalance
