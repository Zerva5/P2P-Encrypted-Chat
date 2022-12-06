from ctypes import ArgumentError
from dataclasses import dataclass
import datetime

from Account import Account as AC

import Message
#from Message import Message as MSG
from Chat import Chat as CH
import Rsa
from collections import namedtuple
import threading
import socket as Socket
import sys
import signal
import queue

#from Message import Message


COMMANDS = ["", "login", "create_account", "delete_account", "chat", "delete_history", "exit", "help", "logout", "create_contact", "list_contacts"]
NUMARGS = [0, 3, 2, 2, 4, 2, 1, 1, 1, 3, 1]

Status = namedtuple('Status', ['chat', 'account'])

PORT = 14555

def RecvLoop(status: Status, listenSocket: Socket.socket):

    connection = None
    addr = ""
    
    while True:
        try:

            if(connection is None):

                connection, addr = listenSocket.accept()

                #print("done")
            else:
                messageStr = connection.recv(4096)

                
                if(messageStr):
                    # if we are currently chatting
                    # have this happen in this thread as input is still blocking
                    
                    status.chat.recvQueue.put([addr, messageStr])
                    
                else:
                    #print("message empty :(")
                    status.chat.active = False
                    connection = None
        except:
            continue
    return

def StartRecv(status: Status):
    listenSocket = Socket.socket()
    
    port=PORT

    recvIP = "127.0.0.1"

    while True:
        try:
            listenSocket.bind((recvIP, port))
            break
        except OSError as e:
            port += 1
        
    listenSocket.listen(1)
    print("Listening on port #", port)

    #RecvLoop(status, listenSocket)

    t = threading.Thread(target = RecvLoop, args=(status, listenSocket))
    t.daemon = True
    t.start()

    

    status.chat.recvPort = port

    return status

class InputTimeout(Exception):
    pass

def InputTimedOut(signum, frame):
    raise InputTimeout
    

signal.signal(signal.SIGALRM, InputTimedOut)

def Exit_Wrapper(status: Status, argList: list):

    if(status.account.active):
        print("Encrypting and saving contacts...")
        status.account.StoreContacts()

    print("exiting...")        

    exit()

    return status, None
 
def Help_Wrapper(status: Status, argList: list):
    print("""
        Secure Messaging Application
        
        Options:
        
            login           arguments: <account_name> <password>
            
            create_account  arguments: <account_name> 
            
            delete_account  arguments: <account_name> <password>
            
            chat            arguments: <account_name> <IP> <port> 
            
            delete_history  arguments: <account_namee> <password>
            
            exit            arguments: None
            
            logout          arguments: None
        
        
        """)
    return status, None



def Login(label: str, privateKey: tuple) -> AC:
    """
    Takes login info and returns true if login was successful.
    If login was successful then return the logged in account"
    """
    #print("here")
    
    retAccount = AC.GetLocalAccount(label, privateKey)
    retAccount.active = True
    retAccount.privateKey = privateKey
    
    return retAccount

def Login_Wrapper(status: Status,argStr: list):

    #print(argStr)

    try:
        newAccount = Login(argStr[0], Rsa.KeyFromString(argStr[1]))
        
        status = Status(status.chat, newAccount)
        status.chat.sender = newAccount
        status = StartRecv(status)

        print("Logged in as", status.account.label)
        print("Your public Key: ", Rsa.KeyToString(status.account.publicKey))
    except IndexError as e:
        print(str(e))
    except FileNotFoundError as e:
        print("Account not found!")
    except Exception as e:
        print("Some other login error!", str(e))


    return status, None



def CreateAccount(label: str) -> AC:
    """
    Creates a new account and returns an Account object
    Creates folder for new account
    creates file that store public key
    """

    # Generate keypair for the account
    public,private = Rsa.GeneratePair(2048)

    retAccount = AC(label)

    retAccount.privateKey = private
    retAccount.publicKey = public

    retAccount.InitializeLocalAccount()

    return retAccount

def CreateAccount_Wrapper(status: Status,argStr: list):
    #print("Create account::")
    #print(argStr)

    try:
        tempAcc = CreateAccount(argStr[0])
        

        print("Public key: " + Rsa.KeyToString(tempAcc.publicKey))
        print("Private key: " + Rsa.KeyToString(tempAcc.privateKey))
        print("DO NOT FORGET THIS")
        
    except FileExistsError as e:
        print(str(e))
    
    return status, None




def DeleteAccount(account: AC) -> bool:
    """
    Take a label and delete the associated account. Account must be the "currently logged in account" for operation to be successful
    """

    account.DeleteLocalAccount()

    return True

def DeleteAccount_Wrapper(status: Status,argStr: list):
    #print("Delete account::")
    #print(argStr)

    
    if(status.account.active and status.account != AC.NoneAccount()):
        
        DeleteAccount(status.account)
    else:
        print("Please login to the account you wish to delete!")

    status = Status(status.chat, AC.NoneAccount())
    
    return status, None


def DeleteHistory(account: AC, recipient: str) -> bool:
    """
    Delete message history with a particular user. Must be logged in to the account in the chat to delete message history
    """

    account.DeleteHistory(recipient)
    
    return True

def DeleteHistory_Wrapper(status: Status, argStr: list):
    #print("Delete history::")
    #print(argStr)

    if(DeleteHistory(status.account, argStr[0])):
        print("History with contact", argStr[0], "has been deleted")
    else:
        print("SOME ERROR DELETING THE HISTORY")
    
    return status, None

def CreateContact(status: Status, label: str, publicKey: str):
    newContact = status.account.NewContact(label, publicKey)

    return newContact


def CreateContact_Wrapper(status: Status, argStr: list):

    newAccount = CreateContact(status, argStr[0], argStr[1])

    print("Added", newAccount.label, "as a new contact. Their public key is", Rsa.KeyToString(newAccount.publicKey))

    return status, None
    



def InitChat(account: AC, recipientLabel: str, IP: str, sendPort=PORT, recvPort = PORT):
    """
    Tries to find recipient account based on the label, if it can't find it ask for the recipients public key then create a new recipient. Once thats done start a new chat object at the given IP.

    Once connection successful create file for this chat and add recipient public key to first line
    """
    recipientAccount = AC.NoneAccount()
    recipientAccount.label = recipientLabel

    try:
        #print(account.privateKey)
        recipientAccount = account.GetChatAccount(recipientLabel)
    except KeyError:
        
        pubKey = input("This person isn't a contact yet, please enter their public key: ")
        publicKey = Rsa.KeyFromString(pubKey)
        recipientAccount = account.NewContact(recipientLabel, Rsa.KeyToString(publicKey))
        recipientAccount.IP = IP
        recipientAccount.publicKey = publicKey
        

        # Save contact?

    newChat = CH(account, recipientAccount)
    newChat.sendIP = recipientAccount.IP
    newChat.sendPort = sendPort
    newChat.recvPort = recvPort

    newChat.InitConnection()


    return newChat
    
def InitChat_Wrapper(status: Status,argStr: list):
    #print("init chat::")
    #print(argStr)

    if(not status.account.active):
        print("Need to be logged in to start a chat!")
        return status,None

    try:
        #print(argStr[2])
        newChat = InitChat(status.account, argStr[0], argStr[1], int(argStr[2]), status.chat.recvPort)
    except ConnectionRefusedError:
        print("Connection refused!")
        return status, None
    except ValueError:
        print("Port needs to be numeric value from 0-65535")
        return status, None

        
    status = Status(newChat, status.account)
    
    return status, None

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
        print("Need {} argument but given {}".format(NUMARGS[cmdIndex],len(strSplit)-1))
        raise ArgumentError("Invalid number of arguments!")

    ## now we can assume they are the right number of args
    argList = []

    # get all but the actual command
    for arg in strSplit[1:]:
        argList.append(arg)

    return cmdIndex, argList

def NoCommand(status, cmdArgs):
    return status, None

def Logout(Account: AC):
    """
    Save all the chat history, contacts, etc. Encrypt everything and 
    """

    return 

def Logout_Wrapper(status, cmdArgs):
    if(status.account.active):
        print(status.account.label, "has been logged out")

        status.account.StoreContacts()
        
        Logout(status.account)
        status = Status(status.chat, AC.NoneAccount())
    else:
        print("No account currently logged in")

    
    return status, None

def ListContacts_Wrapper(status: Status, cmdArgs):

    #print(status.account.contacts)

    print("Contacts:")
    for key in status.account.contacts:
        print(key + ":" + status.account.contacts[key][1])
        

    return status, None


def delete_current_line():
    # move the cursor up one line
    print("\033[F", end="")
    # clear the line
    print("\033[K", end="")

def move_current_line_down():
    # save the current cursor position
    print("\033[s", end="")
    # move the cursor down one line
    print("\033[E", end="")
    # restore the saved cursor position
    print("\033[u", end="")
    # delete the current line
    print("\033[1M", end="")


def InputLoop(status: Status):
    """Take input and call the different commands"""



    commands = [NoCommand, Login_Wrapper, CreateAccount_Wrapper, DeleteAccount_Wrapper, InitChat_Wrapper, DeleteHistory_Wrapper, Exit_Wrapper, Help_Wrapper, Logout_Wrapper, CreateContact_Wrapper, ListContacts_Wrapper]

    timeout = 1
    noPrompt = False

    
    # Input loop
    while(True):

        try:
            signal.alarm(timeout)
            if(status.chat.active):
                # Don't rewrite the ">" prompt
                if(noPrompt):
                    chatStr = input()
                else:
                    chatStr = input(status.chat.InputPrompt())
                    
                #signal.alarm(0)
                
                if(chatStr == "exit"):
                    status.chat.EndConnection()
                    print("Exited")
                    noPrompt = False
                else:
                    newMsg = Message.Message(chatStr, datetime.datetime.now(), status.account, status.chat.recipient)

                    ## send input to the chat!
                    status.chat.Send(newMsg)

                    noPrompt = False
            
            else:
                #if(status.account.active):
                if(noPrompt):
                    commandStr = input()
                else:
                    commandStr = input(status.account.label + " > ")

                # Stop the signal timeout 
                signal.alarm(0)
                    
                cmdIndex = -1
                cmdArgs = []

                noPrompt = False

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

        except InputTimeout:
            ## Check message queue
            #print("checking messages")

            if(status.chat.recvQueue.empty()):
                noPrompt = True
                continue
            else:
                while(not status.chat.recvQueue.empty()):
                    #print(status.chat.active)
                    recvdMsg = status.chat.Receive(status.chat.recvQueue.get())

                    move_current_line_down() # moves the input prompt down one line
                    sys.stdout.write("\x1b[1G") # moves cursor to the very left side of the console
                    #print("\033[F", end="")
                    if(recvdMsg.body != ""):
                        print(recvdMsg)
                    
                noPrompt = False

        except BrokenPipeError:
            #move_current_line_down() # moves the input prompt down one line
            #sys.stdout.write("\x1b[1G") # moves cursor to the very left side of the console

            status.chat.EndConnection(response = True)

            print("Connection dropped")


            
            
        





def main():
    status = Status(CH.NoneChat(), AC.NoneAccount())
    #status = StartRecv(status)
    #print(status.chat.recvPort)

    print("Please type a command then press enter. For help enter 'help'.")
    InputLoop(status)
    return



if __name__ == "__main__":
    main()
