from dataclasses import dataclass, field
import datetime
import os, shutil #for file manipulation
import inspect #for stack inspection for easier debugging
from Rsa import *
from collections import namedtuple


ContactInfo = namedtuple("ContactInfo", ["fileNumber", "publicKey"])

_root = os.getcwd() + "/Accounts/"

@dataclass
class Account:
    label: str
    IP: str = ""
    
    publicKey: tuple = tuple()
    privateKey: tuple = tuple()
    
    active: bool = False

    @property
    def contacts(self):
        try:
            return self._contacts
        except AttributeError:
            self._contacts = self.GetContacts()
            return self.contacts
        
        
    
    def InitializeLocalAccount(self): #for initializing 
        """
        Check if this account exists and if not create the associated folder and files
        """
        Account.AssertLocalAccount(self.privateKey)
        
        if os.path.isdir(_root + self.label) == True: #if account with that label already exists, throw exception
            raise FileExistsError("Account with that label already exists")

        if os.path.isdir(_root) == False: # Accounts folder is not made yet
            os.mkdir(_root)

        os.mkdir(_root + self.label) #make account folder and files
        with open(_root + self.label + "/info.txt", 'w') as fp:
            clearText = self.label + '\n' + KeyToString(self.publicKey) + '\n' + self.IP
            data = Encrypt(clearText, self.publicKey)
            
            fp.write(data)

        with open(_root + self.label + "/contacts.txt", 'w') as fp:
            pass


        return


    def __eq__(self, other):
        return self.label == other.label and self.publicKey == other.publicKey
        

    def GetContacts(self): 
        """
        Retrieves local account's contact list and returns it as a dictionary of label<->(file_id, publicKey) associations
        """

        Account.AssertLocalAccount(self.privateKey)

        contacts = {}

        
        fp = open(_root + self.label + "/contacts.txt", "r")
        
        fileData = Decrypt(fp.read(), self.privateKey)

        for association in fileData.split(): #this loop adds all of the label<->(file_id, publicKey) associations to the contacts dictionary
            kv_Pair = association.split("-")
            contacts[kv_Pair[0]] = ContactInfo(kv_Pair[1], kv_Pair[2])

        return contacts

    
    def VerifyContact(self, publicKey):
        """
        Returns the label of the contact with the given public key, Raising an exception if they don't exist
        """

        print("In verify contact:", publicKey)
        print(self.contacts.items())
        
        for k,v in self.contacts.items():
            if v.publicKey == publicKey :
                return k
        
        raise Exception("Contact with that privateKey not found")


    def StoreContacts(self):
        """
        Stores all of the contacts in the local account's contact dictionary
        """
        Account.AssertLocalAccount(self.privateKey)
        fp = open(_root + self.label + "/contacts.txt", "w")
        string = ""

        #adds all dictionary entries into a string to be encrypted
        for k,v in self.contacts.items():
            string += k + "-" + v.fileNumber + "-" + v.publicKey + "\n"

            
        fp.write(Encrypt(string, self.publicKey))
        fp.close()

        return




    def GetChatAccount(self, contactLabel: str): 
        """
        #Returns a new chat account object thats associated with the label. should catch if the account doesn't exist and raise an exception
        """
        Account.AssertLocalAccount(self.privateKey)

        try:
            id = self.contacts[contactLabel].fileNumber
            filePath = _root + self.label + "/" + id + "/info.txt"

            fp = open(filePath, "r")
            fileContents = fp.read()
            info = Decrypt(fileContents, self.privateKey)
            info = info.splitlines()

            publicKey = KeyFromString(info[1])
            #IP = info[2]
            return Account(contactLabel, publicKey = publicKey)

        except KeyError:
            raise KeyError("GetChatAccount called with label to nonexistent account")
        

    def StoreMessages(self, contactLabel: str, messages: list[str]):
        """
        Appends a message plus a \n onto the history.txt file of the given contactLabel
        """
        Account.AssertLocalAccount(self.privateKey)

        id = self.contacts[contactLabel].fileNumber
        historyPath = _root + self.label + "/" + id + "/history.txt"

        fp = open(historyPath, "a")
        fp.write('\n'.join(messages)) 
        fp.close()
        
        return



    def DeleteHistory(self, contactLabel: str):
        """
        Delete message history to/from a given label
        """
        Account.AssertLocalAccount(self.privateKey)

        id = self.contacts[contactLabel].fileNumber
        directoryPath = _root + self.label + "/" + id + "/"

        open(directoryPath + "history.txt", "w").close() #this clears the history.txt file
        
        return



    def DeleteLocalAccount(self):
        """
        Delete your local account and associated folders/files
        """
        Account.AssertLocalAccount(self.privateKey)
        
        shutil.rmtree(_root + self.label) #deletes all of the local account's files

        return
    

    def NewContact(self, contactLabel: str, publicKey: str, IP: str = ""): 
        """
        Generates folder and files for account, Adds label to contact dictionary, Returns account object with details, Raises exception if label already exists
        """

        Account.AssertLocalAccount(self.privateKey)

        if contactLabel not in self.contacts:

            #get a folder id that does not already exist
            num = 0
            while os.path.isdir(_root + self.label + "/" + str(num)) == True: #checks to see if a folder of that id already exists, if so incremement the id
                num += 1

            #creates the directory for the contact with the id as the name
            os.mkdir(_root + self.label + "/" + str(num))

            #associates the contact's label with a number id and their publicKey in our contact dictionary
            self.contacts[contactLabel] = ContactInfo(str(num), publicKey)

            #creates the info file and writes the contact information in
            fp = open(_root + self.label + "/" + str(num) + "/info.txt", "w")
            clearText = contactLabel + "\n" + publicKey
            info = Encrypt(clearText, self.publicKey)
            fp.write(info)
            fp.close()

            #creates the chat history file
            open(_root + self.label + "/" + str(num) + "/history.txt", "w").close()

            self.StoreContacts()

            return Account(contactLabel, IP=IP, publicKey = KeyFromString(publicKey))
        
        else:
            raise Exception("A contact with that name already exists")


    def DeleteContact(self, contactLabel):
        """
        Delete the contact (associated folder, files, and dictionary entry)
        """
        Account.AssertLocalAccount(self.privateKey)
        
        id = self.contacts[contactLabel].fileNumber
        directoryPath = _root + self.label + "/" + id + "/"

        del self.contacts[contactLabel] #deletes contact's directory entry
        shutil.rmtree(directoryPath) #deletes contact's associated file and contents
        
        return


    @staticmethod
    def NoneAccount(): #For making an object equivalent to None
        ret = Account("", "")
        #ret.active = False
        return ret


    @staticmethod
    def GetLocalAccount(label: str, privateKey: tuple): 
        """
        gets local account info, returns account object
        """
        fp = open(_root + label + "/info.txt", "r")
            
        fileContents = fp.read()
        info = Decrypt(fileContents, privateKey)
        info = info.splitlines()

        if info[0] == label: # if the decryption was successful
            publicKey = KeyFromString(info[1])
            #IP = info[2]
            return Account(label, publicKey=publicKey, privateKey=privateKey)
        
        else:
            raise Exception("Incorrect Login Credentials")
            


    @staticmethod
    def AssertLocalAccount(privateKey):
        """
        Asserts that the account is the local account and not a chat account
        """

        
        if (not privateKey): #if no privateKey then the object is a chat account
            #the frame code below retrieves the name of the caller method, this is to make debugging easier
            raise Exception("method " + inspect.getouterframes( inspect.currentframe() )[1][3] + "() must be called on the local account object", "AKA this thing doesn't have the private key set") 
        return




# bob = Account("bob", "1", "1", "1234")
# bob.InitializeLocalAccount()
# bob.NewContact("tracy", "5", "2")
# bob.NewContact("steve", "2", "2")
# bob.NewContact("jonees", "3", "2")
# bob.StoreContacts()
# bob.StoreMessages("tracy", "hey")



# Account_Folder
#     Info.txt (local account info)
#     contacts.txt (has everyone you've chatted with, and the mapping to the folder number)
#     chat_account_folders... (has info.txts and history.txts)
