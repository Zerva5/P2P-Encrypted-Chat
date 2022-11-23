from dataclasses import dataclass, field
import datetime
from Account import Account
from Message import Message
import socket as Socket
#import _thread
import threading
 
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
    chatSocket: Socket.socket = Socket.socket()
    listenSocket: Socket.socket = Socket.socket()

    sendPort: int = field(init=False)
    recvPort: int = field(init=False)

    def __post_init__(self):
        """
        DOn't think anything should go here for now, but adding it because I dind't know it was a thing and it may be useful

        Maybe print out messages from last connection with this person?
        """
        return

    @staticmethod
    def NoneChat():
        return Chat(Account.NoneAccount(), Account.NoneAccount())


    def InitConnection(self) -> bool:
        """
        Connect to IP
        Request a chat
         - Verify identity of other user
         - Perform some form of key exchange (https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange) for example.
        Return once connection is established, identify verified, and keys exchanged
        """
        try:
            self.chatSocket.connect((self.sendIP, self.sendPort))

            print("Chat connection complete")
            self.active = True

            self.chatSocket.send(("port:"+str(self.recvPort)).encode())

        except ConnectionRefusedError as e:
            print("Connection refused!")

        return True

    def Send(self, message: Message):
        """
        Encrypt and send the message.
        Format message to have the message hash and timestamp
        """
        self.chatSocket.send(message.body.encode())
        self.messages.append(message)
        return

    def Receive(self, raw: str) -> Message:
        """
        Check for recieved messages and decrpyt them.
        Also decode them, verify message integrity using message hash and timestamp
        Raise exception if message can't be decrypted or can't be verified by message hash
        """


        return Message("", datetime.datetime.now(), Account("", ""), Account("", ""))

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

        return
        
        
