# =============================================================================
# Created By  : ShaunCodes
# Created Date: July 3, 2021
# =============================================================================
"""
This file contains the driver code for the CBPortal
"""
# =============================================================================
# Imports
# =============================================================================
import sys

import AccountClass
import config
import Screens

# =============================================================================
# Main Functions
# =============================================================================
if __name__ == '__main__':
    # Create and show CB Portal Application
    Screens.configureApp()
    config.GUI.show()

    sys.exit(config.APP.exec_())
