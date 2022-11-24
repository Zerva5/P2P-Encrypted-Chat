from dataclasses import dataclass, field
import datetime
import os, shutil #for file manipulation
import inspect #for stack inspection for easier debugging


@dataclass
class Account:
    label: str
    publicKey: str
    IP: str = ""
    privateKey: str = None
    
    def InitalizeLocalAccount(self): #for initializing 
        """
        Check if this account exists and if not create the associeated folder and files
        """
        Account.AssertLocalAccount(self.privateKey)
        
        if os.path.isdir('./' + self.label) == True: #if account with that label already exists, throw exception
            raise Exception("Account with that label already exists")

        else:
            os.mkdir("./" + self.label) #make account folder and files
            open("./" + self.label + "/info.txt").close()
            open("./" + self.label + "/history.txt").close()
            return


    def GetContacts(self): 
        """
        Retrieves local account's contact list and returns it as a dictionary of label-file_id associations
        """
        Account.AssertLocalAccount(self.privateKey)
        
        fp = open("./" + self.label + "/info.txt")
        encryptedContents = fp.read()
        #TODO decrypt the above into the fileData variable

        fileData = "label1-0\nlabel2-4\nlabel3-2\nlabel4-6\nlabel5-5\nlabel6-9" #temporary theroretical output for testing
        contacts = {}

        for association in fileData.split(): #this loop adds all of the label-file_id associations to the contacts dictionary
            kv_Pair = association.split("-")
            contacts[kv_Pair[0]] = kv_Pair[1]

        return contacts



    def GetChatAccount(self, contactLabel: str, dictionary): 
        """
        #Returns a new chat account object thats associated with the label. should catch if the account doesn't exist and raise an exception
        """
        Account.AssertLocalAccount(self.privateKey)

        try:
            id = dictionary[contactLabel]
            filePath = "./" + self.label + "/" + id + "/info.txt"

            fp = open(filePath)
            fileContents = fp.read()
            #TODO decrypt the info from the file and store it in the below variables

            publicKey = ""
            IP = ""
            return Account(contactLabel, publicKey, IP)

        except KeyError:
            raise KeyError("GetChatAccount called with label to nonexistent account")
        


    def DeleteHistory(self, contactLabel: str, dictionary):
        """
        Delete message history to/from a given label
        """
        Account.AssertLocalAccount(self.privateKey)

        id = dictionary[contactLabel]
        directoryPath = "./" + self.label + "/" + id + "/"

        open(directoryPath + "history.txt", "w").close() #this clears the history.txt file
        
        return



    def DeleteLocalAccount(self):
        """
        Delete your local account and associated folders/files
        """
        Account.AssertLocalAccount(self.privateKey)
        
        shutil.rmtree("./" + self.label) #deletes all of the local account's files

        return
    

    def NewContact(self, contactLabel: str, publicKey: str, IP: str, dictionary): 
        """
        Generates folder and files for account, Adds label to contact dictionary, Returns account object with details, Raises exception if label already exists
        """

        Account.AssertLocalAccount(self.privateKey)

        if contactLabel not in dictionary:

            #get a folder id that does not already exist
            num = 0
            while os.path.isdir('./' + str(num)) == True: #checks to see if a folder of that id already exists, if so incremement the id
                num += 1

            #associates the contact's label with a number id in our contact dictionary
            dictionary[contactLabel] = str(num)

            #creates the directory for the contact with the id as the name
            os.mkdir("./" + self.label + "/" + str(num))

            #creates the info file and writes the contact information in
            fp = open("./" + self.label + "/" + str(num) + "/info.txt", "w")
            string = contactLabel + "\n" + publicKey + "\n" + IP
            #TODO encrypt the above string
            encryptedString = ""
            fp.write(encryptedString)

            #creates the chat history file
            fp = open("./" + self.label + "/" + str(num) + "/history.txt", "w")
            
            fp.close()

            return Account(contactLabel, publicKey, IP)
        
        else:
            raise Exception("A contact with that name already exists")


    def DeleteContact(self, contactLabel, dictionary):
        """
        Delete the contact (associated folder, files, and dictionary entry)
        """
        Account.AssertLocalAccount(self.privateKey)
        
        id = dictionary[contactLabel]
        directoryPath = "./" + self.label + "/" + id + "/"

        del dictionary[contactLabel] #deletes contact's directory entry
        shutil.rmtree(directoryPath) #deletes contact's associated file and contents
        
        return


    @staticmethod
    def NoneAccount(): #For making an object equivalent to None
        ret = Account("", "")
        ret.active = False
        return ret


    @staticmethod
    def GetLocalAccount(label: str, privateKey: str): 
        """
        gets local account info, returns account object
        """
        fp = open("./" + label + "/info.txt", "r")
        fileContents = fp.read()
        #TODO decrypt the info from the file and store it in the below variables

        publicKey = ""
        IP = ""
        return Account(label, publicKey, IP, privateKey)


    @staticmethod
    def AssertLocalAccount(privateKey):
        """
        Asserts that the account is the local account and not a chat account
        """
        if privateKey == None: #if no privateKey then the object is a chat account
            #the frame code below retrieves the name of the caller method, this is to make debugging easier
            raise Exception("method " + inspect.getouterframes( inspect.currentframe() )[1][3] + "() must be called on the local account object") 
        return






# Account_Folder
#     Info.txt (local account info)
#     contacts.txt (has everyone you've chatted with, and the mapping to the folder number)
#     chat_account_folders... (has info.txts and history.txts)