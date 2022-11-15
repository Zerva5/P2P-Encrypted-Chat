from dataclasses import dataclass
import datetime

@dataclass
class Account:
    label: str
    publicKey: str
    IP: str = ""
    privateKey: str = dataclass.field(init=False)
    
    def InitalizeAccount(self):
        """
        Check if this account exists and if not create all the associated folders and files
        """

        return

    


    def DeleteHistory(self, label: str):
        """
        Delete message history from to/from a given label
        """

        return
    
    def DeleteAccount(self):
        """
        Delete this account and associated folders and files
        """

        return
    

