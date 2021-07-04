# =============================================================================
# Created By  : ShaunCodes
# Created Date: July 03, 2021
# =============================================================================
"""
This file contains global variables to use across CodeyBank modules
"""
# =============================================================================
# Imports
# =============================================================================
from enum import Enum

# =============================================================================
# Global Variables
# =============================================================================
GUI   = None   # Variable for stacked widget as main gui container
APP   = None   # Variable for application window
DB    = None   # Variable for member database
ACCT  = None   # Variable to hold information about current account
TACCT = None   # Variable to hold information of specified transfer account

# =============================================================================
# Enumerated Variables
# =============================================================================
class SCREENS(Enum):
    SPLASHCREEN = 0
    LOGINSCREEN = 1
    NEWMEMSCREEN = 2
    ACCTOPTSCREEN = 3
    ACCTDETSCREEN = 4
    TRANSFERSCREEN = 5
    CHECKDEPSCREEN = 6
    UPDATEACCTSCREEN = 7
    EXITSCREEN = 8
