from dataclasses import dataclass
import datetime
#from Account import Account
import Account
import re
import hashlib

@dataclass
class Message:
    body: str
    timestamp: datetime.datetime
    sender: Account.Account
    recipient: Account.Account
    flag: str = "CON"
    checksum: str = ""
    
    
    def __str__(self):
        return "({}) {}: {}".format(self.timestamp.strftime("%X"), self.recipient.label, self.body)

    def encode(self):
        timestampStr = str(int(self.timestamp.timestamp()))
        self.checksum = hashlib.md5(self.body.encode()).hexdigest()
        
        return f"{timestampStr}-{self.flag}-{self.checksum}-{self.body}"

    @staticmethod
    def decode_string(msgStr: str):
        """
        Takes a message and looks for the format TIME-FLAG-CHECKSUM-BODY, extracts the data
        """

        #print(msgStr)
        regex = r"^(\d+)-(INIT|CON|END)-([\da-fA-F]{32})-(.*)$"
        match = re.match(regex, msgStr)
        
        if not match:
            raise Exception("No match! Wrong connection format?")
        
        timestamp = int(match.group(1))
        dt = datetime.datetime.fromtimestamp(timestamp)
        
        flag = match.group(2)
        checksum = match.group(3)

        
        body = match.group(4)

        computed_checksum = hashlib.md5(body.encode()).hexdigest()

        if(computed_checksum != checksum):
            raise Exception("Checksum is wrong! Data integrity not confirmed")
        
        return (dt, flag, checksum, body)



    @staticmethod
    def decode(msg: str, sender, recipient):
        time, flag, checksum, body = Message.decode_string(msg)

        return Message(body, time, sender, recipient, flag, checksum=checksum)    
        

# from Account import Account
        
# def testing():
#     x = Message.encode(datetime.datetime.now(), "CON", "hey this is some BLAH BLAH BLAHtext!")

#     print(x)

#     print(Message.decode(x.encode(), Account.NoneAccount(), Account.NoneAccount()))

# testing()
