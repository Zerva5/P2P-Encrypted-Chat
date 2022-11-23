from dataclasses import dataclass, field
import datetime
import os


@dataclass
class Account:
    label: str
    publicKey: str
    IP: str = ""
    privateKey: str = field(init=False)
    active: bool = True
    
    def InitalizeAccount(self):
        """
        Check if this account exists and if not create all the associated folders and files
        """

        #if the account does not have a folder (i.i. does not yet exist) make the folder and files
        #if os.path.isdir('./Accounts/' + self.label) == False: 
        #TODO finish this function

        return

    @staticmethod
    def NoneAccount():
        ret = Account("", "")
        ret.active = False
        return ret

    @staticmethod
    def GetFromLabel(label: str, privKey: str):
        """
        Try and find previously created account with the given label, throw exception if not found, return account if found
        """
        # if os.path.isdir('./Accounts/' + label) == True or True: 
        #     fp = open("./Accounts/" + label, "r")
        #     attributes = fp.readlines()
        #     pubKey = attributes[1].strip()
        #     IP = attributes[2].strip()


        return Account(label, "pubKey", "localhost")

        # else:
            
        #     raise FileNotFoundError("AccountNotFound in GetFromLabel") 



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
    

