from dataclasses import dataclass
import datetime
from Account import Account

@dataclass
class Message:
    body: str
    timestamp: datetime.datetime
    sender: Account
    recipient: Account
    
    
    def toString(self):
        return ""
        
