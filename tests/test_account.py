import pytest
import unittest
from main import *

class Test_AccountCreation():
    
    COMMANDS = ["", "login", "create_account", "delete_account", "chat", "delete_history", "exit", "help", "logout"]
    NUMARGS = [0, 3, 2, 2, 3, 2, 1, 1, 1]

    
    def test_login(self):
        a,b = ParseCommand("login")
        
        assert False
    
    def test_create_account(self):
        a,b = ParseCommand("create_account")
        
        assert False
        
    def test_delete_account(self):
        a,b = ParseCommand("delete_account")
        
        assert False

    def test_chat(self):
        a,b = ParseCommand("chat")
        
        assert False
        
    def test_exit(self):
        a,b = ParseCommand("exit")
        
        assert False
        
    def test_help(self):
        a,b = ParseCommand("help")
        
        assert False
    
    def test_logout(self):
        a,b = ParseCommand("logout")
        
        assert False
        






