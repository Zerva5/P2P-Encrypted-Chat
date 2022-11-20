from dataclasses import dataclass
import datetime
from Account import Account as AC
from Chat import Chat
from Encrypt import *


#from Message import Message

validCommands = ["login", "create_account", "delete_account", "chat", "history", "exit"]

def AccountFromLabel(label:str) -> AC:
    #TODO
    return AC.NoneAccount()






def Login(label: str, privateKey: str) -> AC:
    """
    Takes login info and returns true if login was successful.
    If login was successful then return the logged in account"
    """
    return AC.NoneAccount()

def CreateAccount(label: str) -> AC:
    """
    Creates a new account and returns an Account object
    Creates folder for new account
    creates file that store public key
    """

    return AC.NoneAccount()

def DeleteAccount(account: AC) -> bool:
    """
    Take a label and delete the associated account. Account must be the "currently logged in account" for operation to be successful
    """

    return False

def DeleteHistory(account: AC, recipient: AC) -> bool:
    """
    Delete message history with a particular user. Must be logged in to the account in the chat to delete message history
    """
    return False

def InitChat(account: AC, recipientLabel: str, IP: str):
    """
    Tries to find recipient account based on the label, if it can't find it ask for the recipients public key then create a new recipient. Once thats done start a new chat object at the given IP.

    Once connection successful create file for this chat and add recipient public key to first line
    """

def main():
    """Take input and call the different commands"""

    loggedIn = AC.NoneAccount()
    invalidCmd = False
    # Valid commands:
    #3 login $label$ $privatekey$ 
    #2 create_account $label$
    #2 delete_account $label$
    #3-4 chat $label$ $ip$ $port=some default$
    #3 delete_history $label$
    #3 history view $label$
    
    
    # Input loop
    while(True):
        if(invalidCmd):
            print("Invalid command! Please enter 'help' for help")
            invalidCmd = False
        
        commandStr = input("Please type a command then press enter. For help enter 'h'.")

        commandSplit = commandStr.split(' ')

        ### basic input checks

        # Check its not just whitespace
        if(len(commandSplit) == 0):
            continue

        mainCmd = commandSplit[0]

        # make sure the first word is a valid command
        if(not mainCmd in validCommands):
            invalidCmd = True
            continue

        # make sure the number of total words is correct
        if(not(1 < len(commandSplit) and len(commandSplit) < 5)):
            if(mainCmd == "help" and len(commandSplit) == 1):
                print("SOME HELP")
            else:
                invalidCmd = True

            continue
        
        ### Done basic checks

        # commands that take 3 args
        if(len(commandSplit) == 3):
            if(mainCmd == "login"):
                try:
                    Account = Login(commandSplit[1], commandSplit[2])
                except SyntaxError:
                    print("Invalid syntax! Use: login username privatekey")

        elif(len(commandSplit) == 4):
            if(mainCmd == "chat"):
                print("so you wanna chat do you? well I don't want to finish this right now so you can't :(")


        elif(len(commandSplit) == 2):
            if(mainCmd == "create_account"):
                try:
                    Account = CreateAccount(commandSplit[1])
                except SyntaxError:
                    print("Invalid syntax! Use: create_account username")
            elif(mainCmd == "delete_account"):
                try:
                    res = DeleteAccount(AccountFromLabel(commandSplit[1]))
                except SyntaxError:
                    print("Invalid syntax! Use: create_account username")
            elif(mainCmd == "delete_history"):
                try:
                    if(loggedIn == AC.NoneAccount()):
                        raise Exception("Not logged in")

                    res = DeleteHistory(loggedIn, AccountFromLabel(commandSplit[1]))
                except SyntaxError:
                    print("Invalid syntax! Use: create_account username")
                except Exception as e:
                    print(str(e))
            else:
               print("shouldn't get here!")

        else:
            print("wrong number of arguments!")
    
    return


if __name__ == "__main__":
    main()
