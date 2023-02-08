from dataclasses import dataclass, field
from typing import ClassVar
import sys
import datetime
from Account import Account as AC
from Message import Message
import socket as Socket
#import _thread
import threading
import queue
import datetime
import Rsa

 
print_lock = threading.Lock()



@dataclass    
class Chat:
    sender: AC
    recipient: AC

    DEBUGMODE: ClassVar[bool] = False

    sendIP: str = field(init=False)
    recvIP: str = field(init=False)
    sessionKey: tuple = field(init=False) # Not 100% if its one key or two.
    messages: list[Message] = field(default_factory=list)# list is the same as an array
    active: bool = False
    awaitingKey: bool = False
    needToSendKey: bool = False
    chatSocket: Socket.socket = Socket.socket(Socket.AF_INET, Socket.SOCK_STREAM)
    listenSocket: Socket.socket = Socket.socket(Socket.AF_INET, Socket.SOCK_STREAM)

    sendPort: int = field(init=False)
    recvPort: int = field(init=False)

    #sendQueue: queue.Queue = field(init=False)
    recvQueue: queue.Queue = queue.Queue()

    # states of the chat: inactive, waiting for key exchange, chatting

    def __post_init__(self):
        """
        DOn't think anything should go here for now, but adding it because I dind't know it was a thing and it may be useful

        Maybe print out messages from last connection with this person?
        """
        return

    

    @staticmethod
    def NoneChat():
        return Chat(AC.NoneAccount(), AC.NoneAccount())

    def EndConnection(self, response=False):
        """
        """

        if(not self.active):
            return

        # Save message history

        print("Encrypting and saving message history...")

        strArray = []
        for m in self.messages:
            strArray.append(m.encode())
            
        self.sender.StoreMessages(self.recipient.label, strArray)

        # If we initiated the end of the chat
        if(not response):
            # Send the other person an "end chat" message
            endMessage = Message("ENDING THE CHAT", datetime.datetime.now(), self.sender, self.recipient, flag="END")
            self.Send(endMessage)
            #self.chatSocket.send(endMessage.encode().encode())


        # Get the chat ready for 
        self.active = False
        self.recipient = AC.NoneAccount()
        self.sendIP = ""
        self.sendPort = 0
        self.chatSocket.close()
        self.chatSocket = Socket.socket(Socket.AF_INET, Socket.SOCK_STREAM)


        return
    
    def InitConnection(self, response=False) -> bool:
        """
        Connect to IP
        Request a chat
         - Verify identity of other user
         - Perform some form of key exchange (https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange) for example.
        Return once connection is established, identify verified, and keys exchanged
        """
        
        try:

            ## Make sure socket is closed
            try:
                self.chatSocket.close()
            except:
                pass

                
            self.chatSocket = Socket.socket()

            #print(self.sendIP, self.sendPort)

            self.chatSocket.connect((self.sendIP, self.sendPort))

            if(response): # someone initiated a chat with us
                print("Generating session keys...")

                senderKey, recipientKey = Rsa.GeneratePair(2048)

                keyMessage = Message("KEY:" + Rsa.KeyToString(recipientKey), datetime.datetime.now(), self.sender, self.recipient)
                keyMessage.flag = "INIT"

                self.sessionKey = senderKey

                self.needToSendKey = True

                self.Send(keyMessage)

                print("Keys Sent!")

                self.needToSendKey = False
                self.active = True
                
                pass
            else: # we are initiating the chat


                #initMessage = Message("PORT:"+str(self.recvPort). datetime.datetime.now(), self.sender, self.recipient)
                initMessage = Message("PORT:"+str(self.recvPort) + ",KEY:" + str(Rsa.KeyToString(self.sender.publicKey)), datetime.datetime.now(), self.sender, self.recipient)
                initMessage.flag = "INIT"

                self.Send(initMessage)

                print("Waiting for session keys...")

                self.awaitingKey = True
                self.active = True

                #self.chatSocket.send(initMessage.encode().encode())
            #self.chatSocket.send("NEW".encode())

        except ConnectionRefusedError as e:
            print("Connection refused!")

        return True

    def Send(self, message: Message):
        """
        Encrypt and send the message.
        Format message to have the message hash and timestamp
        """

        if(Chat.DEBUGMODE):
            print("Before encryption:", message.encode())

        if(self.needToSendKey): # We need to send the session key
            cipherText = Rsa.Encrypt(Rsa.Encrypt(message.encode(), self.sender.privateKey), self.recipient.publicKey)
            print("===DEBUG:", "Encrypting with my private key and recipient public key in that order. Public key:", self.recipient.publicKey)
            self.needToSendKey = False

        elif(not self.active): # We aren't active but we are initializing the chat
            cipherText = Rsa.Encrypt(message.encode(), self.recipient.publicKey)
            if(Chat.DEBUGMODE):
                print("===DEBUG:","Encrypting with recipient public key:", self.recipient.publicKey)
            
        else: # We are in the chat and just need to encrypt with the session key
            cipherText = Rsa.Encrypt(message.encode(), self.sessionKey)
            if(Chat.DEBUGMODE):
                print("===DEBUG: Encrypting with session key:", self.sessionKey)            

        if(Chat.DEBUGMODE):
            print("===DEBUG","After Encryption:", cipherText)
    
        self.chatSocket.send(cipherText.encode()) # Encode message into bytes and send it
        self.messages.append(message) # add the message to the messages list

        
        return

    def InputPrompt(self):
        return self.sender.label + " >>>> "
     
    

    def Receive(self, raw) -> Message:
        """
        Check for recieved messages and decrpyt them.
        Also decode them, verify message integrity using message hash and timestamp
        Raise exception if message can't be decrypted or can't be verified by message hash
        """

        #print("From receive: " + str(self.active))
        msgStr = ""

        msgStr = raw[1].decode()

        
        #print(self.sender.privateKey)
        if(Chat.DEBUGMODE):
            print("Before decrypting:", msgStr)
            
        try:
            if(not self.active): # if this is the first message being receieved. IE someone is initing a connection
                if(Chat.DEBUGMODE):
                    print("decrypting with my private key")
                msgStr = Rsa.Decrypt(msgStr, self.sender.privateKey)


            elif(self.awaitingKey): # if we've send the init and we are waiting for the key to be generated
                if(Chat.DEBUGMODE):
                    print("Decrypting session key with my private key and their public key in that order")
                half = Rsa.Decrypt(msgStr, self.sender.privateKey)
                msgStr = Rsa.Decrypt(half, self.recipient.publicKey) # decrypt using our key first and then their key


            else: # if we aren't waiting for the key then we just decrypt normally
                if(Chat.DEBUGMODE):
                    print("Decrypting using sesion key")
                msgStr = Rsa.Decrypt(msgStr, self.sessionKey)

                
            #print(msgStr)
        except Exception as e:
            raise e
            print("some exception decrypting:", str(e))
        
        addr = raw[0]

        if(Chat.DEBUGMODE):
            print("After decrypting:", msgStr)

        try:
            msg = Message.decode(msgStr, self.sender, self.recipient)
            #print(msg)
        except Exception as e:
            print(str(e))
            
            return Message("---Message Integrity Error---", datetime.datetime.now(), self.recipient, self.sender)
        

        if(msg.flag == "END"):
            self.EndConnection(response=True)
            msg.body = "---Chat Terminated---"
            return msg

        if(self.active):
            #print(msgStr)
            if(msg.flag == "CON"):
                return msg

            elif(msg.flag=="INIT"):
                msgSplit = msg.body.split(':', 1)
                #print(msgSplit)
                if(msgSplit[0] == "KEY"):
                    self.sessionKey = Rsa.KeyFromString(msgSplit[1])
                    self.awaitingKey = False
                else:
                    raise Exception("wrong initial message format, something is wrong")

        else:
            if(msg.flag == "INIT"):
                print("New connection request, going to verify then send keys...")

                msgSplit = msg.body.split(',')

                portSplit = msgSplit[0].split(':')
                keySplit = msgSplit[1].split(':', 1)

                if(portSplit[0] == "PORT"):
                    self.sendPort = int(portSplit[1])
                    self.sendIP = addr[0]
                else:
                    raise Exception("wrong initial message format, something is wrong")
                    
                if(keySplit[0] == "KEY"):
                    keyTuple = Rsa.KeyFromString(keySplit[1])

                    try:
                        label = self.sender.VerifyContact(keySplit[1])
                        print("VERIFIED: Request is from:", label)
                    except:
                        return Message("Person trying to connect not recognized", datetime.datetime.now(), self.sender, self.recipient)

                    #print(label)
                
                    if(label in self.sender.contacts):

                        self.recipient.label = label
                        self.recipient.publicKey = keyTuple
                        self.recipient.IP = self.sendIP                        
                        self.InitConnection(response=True)

                else:
                    print("wrong initial message format, something is wrong")

            else:
                raise Exception("Got a message flag that wasn't INIT:" + msg.flag)


            

        #else: # probably an incoming connection
            
                

        

        return Message("", datetime.datetime.now(), self.sender, self.recipient)

    def SaveHistory(self):
        """
        Save the contents of "messages" to a file and encrypt it
        """

        return

    def PrintMessage(self, msg: Message):
        """
        Format and print the message
        ex 10:35 - Lucas: Hey guys this is a message

        Don't care what format thats just an example
        """

        printStr = "({}) {}: {}".format(msg.timestamp.strftime("%X"), msg.recipient.label, msg.body)

        
        print(printStr)

        return
        
        
