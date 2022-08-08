"""
    This file contains all exceptions raised by models in this module
    All exceptions are subclass of class Exception
"""

class FirstDepositMinimumBalanceError(Exception):
    """An error occured while making first deposit on an account with minimum balance constraint."""
    def __init__(self, message="", code=None, params=None):
        if not message:
            message = "Amount too low for first deposit on an account with active minimum balance constraint"
        super().__init__(message, code, params)

class MinimumBalanceError(Exception):
    """An error occured: Amount lower than balance or minimum balance"""
    def __init__(self, message="", code=None, params=None):
        if not message:
            message = "Amount lower than balance or minimum balance"
        super().__init__(message, code, params)

class DebitError(Exception):
    """An error occured: Balance too low to complete debit transaction"""
    def __init__(self, message="", code=None, params=None):
        if not message:
            message = "Balance too low to complete debit transaction"
        super().__init__(message, code, params)