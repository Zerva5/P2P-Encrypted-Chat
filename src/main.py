from ctypes import ArgumentError
from dataclasses import dataclass
import datetime
from Account import Account as AC
from Chat import Chat as CH
from Encrypt import *
from collections import namedtuple

#from Message import Message


COMMANDS = ["", "login", "create_account", "delete_account", "chat", "delete_history", "exit", "help"]
NUMARGS = [0, 3, 2, 2, 4, 2, 1, 1]

Status = namedtuple('Status', ['chat', 'account'])

def Exit_Wrapper(status: Status, argList: list):
    print("exit?")
    return status, None
 
def Help_Wrapper(status: Status, argList: list):
    print("lmao no help 4 u")
    return status, None

def Login_Wrapper(status: Status,argStr: list):
    print("Login::")
    print(argStr)

    return status, None

def Login(label: str, privateKey: str) -> AC:
    """
    Takes login info and returns true if login was successful.
    If login was successful then return the logged in account"
    """
    return AC.NoneAccount()

def CreateAccount_Wrapper(status: Status,argStr: list):
    print("Create account::")
    print(argStr)
    return status, None

def CreateAccount(label: str) -> AC:
    """
    Creates a new account and returns an Account object
    Creates folder for new account
    creates file that store public key
    """

    return AC.NoneAccount()

def DeleteAccount_Wrapper(status: Status,argStr: list):
    print("Delete account::")
    print(argStr)
    return status, None

def DeleteAccount(account: AC) -> bool:
    """
    Take a label and delete the associated account. Account must be the "currently logged in account" for operation to be successful
    """

    return False

def DeleteHistory_Wrapper(status: Status, argStr: list):
    print("Delete history::")
    print(argStr)
    return status, None

def DeleteHistory(account: AC, recipient: AC) -> bool:
    """
    Delete message history with a particular user. Must be logged in to the account in the chat to delete message history
    """
    return False

def InitChat_Wrapper(status: Status,argStr: list):
    print("init chat::")
    print(argStr)
    return status, None

def InitChat(account: AC, recipientLabel: str, IP: str):
    """
    Tries to find recipient account based on the label, if it can't find it ask for the recipients public key then create a new recipient. Once thats done start a new chat object at the given IP.

    Once connection successful create file for this chat and add recipient public key to first line
    """


def ParseCommand(cmdStr: str):

    # empty line!
    if(len(cmdStr) == 0):
        return 0, []
        

    strSplit = cmdStr.split()

    cmdIndex = -1

    for index,element in enumerate(COMMANDS):
        if(element == strSplit[0]):
           cmdIndex = index
           break
    else:
        # command not found!
        return cmdIndex,[]

    ## Now we parse the parameters
    if(NUMARGS[cmdIndex] != len(strSplit)):
        raise ArgumentError("Invalid number of arguments!")

    ## now we can assume they are the right number of args
    argList = []

    # get all but the actual command
    for arg in strSplit[1:]:
        argList.append(arg)

    return cmdIndex, argList

def NoCommand(status, cmdArgs):
    return status, None

def InputLoop():
    """Take input and call the different commands"""

    commands = [NoCommand, Login_Wrapper, CreateAccount_Wrapper, DeleteAccount_Wrapper, InitChat_Wrapper, DeleteHistory_Wrapper, Exit_Wrapper, Help_Wrapper]

    status = Status(CH.NoneChat(), AC.NoneAccount())
    
    # Input loop
    while(True):

        if(status.chat.active):
            ## Need to make thread safe print!
            chatStr = input(status.account.label)
            ## send input to the chat!

        else:
            commandStr = input("Please type a command then press enter. For help enter 'h'. > ")

            cmdIndex = -1
            cmdArgs = []

            try:
                cmdIndex, cmdArgs = ParseCommand(commandStr)
            except ArgumentError as e:
                print("Argument Error: " + str(e))
                continue

            # No command!
            if(cmdIndex == -1):
                print("invalid command!")
                continue

            status, res = commands[cmdIndex](status, cmdArgs)
        
        
    

def main():
    InputLoop()
    return

if __name__ == "__main__":
    main()
