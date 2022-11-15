from _typeshed import SupportsNoArgReadline
from dataclasses import dataclass
import datetime
from Account import Account
from Chat import Chat
from Encrypt import *

#from Message import Message

def main():
    """Take input and call the different commands"""

    print("hello world")
    
    return

def Login(label: str, privateKey: str) -> Account:
    """
    Takes login info and returns true if login was successful.
    If login was successful then return the logged in account"
    """ 
    return Account("", "", "")

def CreateAccount(label: str) -> Account:
    """
    Creates a new account and returns an Account object
    Creates folder for new account
    creates file that store public key
    """

    return Account("", "", "")

def DeleteAccount(account: Account) -> bool:
    """
    Take a label and delete the associated account. Account must be the "currently logged in account" for operation to be successful
    """

    return False

def DeleteHistory(account: Account, recipient: Account) -> bool:
    """
    Delete message history with a particular user. Must be logged in to the account in the chat to delete message history
    """
    return False

def InitChat(account: Account, recipientLabel: str, IP: str):
    """
    Tries to find recipient account based on the label, if it can't find it ask for the recipients public key then create a new recipient. Once thats done start a new chat object at the given IP.

    Once connection successful create file for this chat and add recipient public key to first line
    """


    
    

if __name__ == "__main__":
    main()
