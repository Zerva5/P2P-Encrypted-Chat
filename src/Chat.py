from dataclasses import dataclass, field
import sys
import datetime
from Account import Account
from Message import Message
import socket as Socket
#import _thread
import threading
import queue
import datetime
 
print_lock = threading.Lock()

@dataclass    
class Chat:
    sender: Account
    recipient: Account

    sendIP: str = field(init=False)
    recvIP: str = field(init=False)
    sessionKey: str = field(init=False) # Not 100% if its one key or two.
    messages: list[Message] = field(default_factory=list)# list is the same as an array
    active: bool = False
    awaitingKey: bool = False
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
        return Chat(Account.NoneAccount(), Account.NoneAccount())

    def EndConnection(self, response=False):
        """
        """

        if(not self.active):
            return

        # Save message history

        # strArray = []
        # for m in self.messages:
        #     strArray.append(m.encode())
            
        # self.sender.StoreMessages(self.recipient.label, strArray)

        # If we initiated the end of the chat
        if(not response):
            # Send the other person an "end chat" message
            endMessage = Message("ENDING THE CHAT", datetime.datetime.now(), self.sender, self.recipient, flag="END")
            self.Send(endMessage)
            #self.chatSocket.send(endMessage.encode().encode())


        # Get the chat ready for 
        self.active = False
        self.recipient = Account.NoneAccount()
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

            self.chatSocket.connect((self.sendIP, self.sendPort))

            if(response): # someone initiated a chat with us
                
                pass
            else: # we are initiating the chat
                print("Chat connection complete")
                self.active = True
                #initMessage = Message("PORT:"+str(self.recvPort). datetime.datetime.now(), self.sender, self.recipient)
                initMessage = Message("PORT:"+str(self.recvPort), datetime.datetime.now(), self.sender, self.recipient)
                initMessage.flag = "INIT"

                self.Send(initMessage)

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
    
        self.chatSocket.send(message.encode().encode()) # Encode message into str then encode into bytes and send it
        self.messages.append(message) # add the message to the messages list

        
        return

    def InputPrompt(self):
        return self.sender.label + " >>>> "

    def IncomingConnection(self, addr, initialMessage):
        ## somehow figure out their name
        ## If they 

        ## do the key handshake
        pass
        
    

    def Receive(self, raw) -> Message:
        """
        Check for recieved messages and decrpyt them.
        Also decode them, verify message integrity using message hash and timestamp
        Raise exception if message can't be decrypted or can't be verified by message hash
        """

        print("From receive: " + str(self.active))
        
        msgStr = raw[1].decode()
        addr = raw[0]

        try:
            msg = Message.decode(raw[1], self.recipient, self.sender)
        except Exception as e:
            print(str(e))
            return Message("---Message Integrity Error---", datetime.datetime.now(), self.recipient, self.sender)
        

        #print("Addr", addr)
        #print(msgStr)

        if(msg.flag == "END"):
            self.EndConnection(response=True)
            msg.body = "---Chat Terminated---"
            return msg

        if(self.active):
            #print(msgStr)
            if(msg.flag == "CON"):
                return msg

            elif(msg.flag=="INIT"):
                raise Exception("got init while still in a chat")
        else:
            if(msg.flag == "INIT"):
                print("New connection request, awaiting key exchange...")

                msgSplit = msg.body.split(':')
                if(msgSplit[0] == "PORT"):
                    self.sendPort = int(msgSplit[1])
                    self.sendIP = addr[0]

                    self.InitConnection(response=True)
                else:
                    print("wrong initial message format, something is wrong")

                    
                self.active = True
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
        
        
