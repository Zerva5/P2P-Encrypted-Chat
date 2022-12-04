from dataclasses import dataclass
import datetime
from Account import Account

@dataclass
class Message:
    body: str
    timestamp: datetime.datetime
    sender: Account
    recipient: Account
    
    
    def __str__(self):
        return "({}) {}: {}".format(self.timestamp.strftime("%X"), self.recipient.label, self.body)
        
