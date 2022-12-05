import pytest
import unittest
from main import *
from Account import *
import shutil
from Rsa import *

_root = os.getcwd() + "/Accounts/"

class Test_AccountCreation():
    
    COMMANDS = ["", "login", "create_account", "delete_account", "chat", "delete_history", "exit", "help", "logout"]
    NUMARGS = [0, 3, 2, 2, 3, 2, 1, 1, 1]


    def test_create_account(self):

        bob = Account("LordLucas", "1", "1", "1234")
        bob.InitializeLocalAccount()
        
        
        assert os.path.isdir(_root + "LordLucas") 

        bob.NewContact("tracy", "5", "2")
        bob.NewContact("steve", "2", "2")
        bob.NewContact("jonees", "3", "2")
        
        assert os.path.isdir(_root + "LordLucas/" + "0") 
        assert os.path.isdir(_root + "LordLucas/" + "1") 
        assert os.path.isdir(_root + "LordLucas/" + "2") 
        
        # haven't tested this yet
        bob.StoreContacts()
        bob.StoreMessages("tracy", "hey")

        shutil.rmtree(_root + "LordLucas")
        
        
        assert not os.path.isdir(_root + "LordLucas") 
        
        
    def test_encrypt(self):
        
        data = Encrypt("Lucas" + "\n" + "(724723, 1649057)" + "\n" + "localhost", "(730267, 1649057)")
        assert type(data) == str

    def test_decrypt(self):
        a,b = ParseCommand("delete_account")
        
        assert False

    






