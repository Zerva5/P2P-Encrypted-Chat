
# SENG360 SM

SENG360 Assignment 3: Message Application

Group members:

Lucas Mayall

Dylan Hughes

Sylvain Taghaoussi

Josh Blanch

=======

# ONLY WORKS ON UNIX!
This is because of the usage of `signal.alarm()`. 

See [`signal.alarm()`](https://docs.python.org/3/library/signal.html#signal.alarm) documentation. There are [workarounds](https://stackoverflow.com/questions/8420422/python-windows-equivalent-of-sigalrm) but they were not discovered until after the project was complete.


# Video
https://www.youtube.com/watch?v=7m4rYDt7DeE


# Usage
1. Clone the repo
2. Run `python main.py` or `python main.py -debug`.
3. type `help` to see commands. 
4. Start chatting!


# Requirements
- SM must support 1:1 messaging and may support group chats (that’s optional)

- Text messages must be supported. Multi-media (such as pictures) are optional

- Message history is kept in encrypted form (at-rest encryption)

- Message history (for a particular conversation) can be deleted by a user. (This will not delete the message history on the other user's side.)

- Message transport uses end-to-end encryption with perfect forward secrecy (https://en.wikipedia.org/wiki/Forward_secrecy)

- Users are authenticated (i.e.,they should be guaranteed to talk to the right person)

- Message integrity must be assured

- Users can plausibly deny having sent a message (see https://signal.org/blog/simplifying-otr-deniability/)

- Users can sign up for an account and also delete their account

- SM must be implemented in Python

# Key Exchange
Bob initializes chat with Alice and sends her his public key encrypted with her public key. 

Alice checks that public key against her contact list to find if Bob is in her contacts

If he is in her contacts she generates a temporary RSA keypair. She sends one of the keys to Bob, she encrypts that key with her private key and Bob's public key.

Bob recieves this key, and decrypts it with his private key and her public key. Then he saves it as the "session key" for that chat. 

Bob and Alice have now exchanged keys and will use this session key to encrypt and decryt their messages.

# Code breakdown
## Netcode
- Message format: timestamp, message hash, message
- Message hash for message integrity
- Encrypt with sender private key and reciever public key
## Encryption/Decryption
Generate public/private key pair
    - this was done by using the RSA key generation method
    - to do this, function such as euclidean algorithm and extended euclidean algorithm, get_prime(), is_prime() were created
    - the GeneratePair() function returns a tuple of tuples: ((pubKey, modula), (privKey, modula))

Forward secrecy handshake (see docs)
    - This security method is explained in the key exchange section

Encrypt strings via key
    - the message is encrypted using the specified key and returns a encrypted string of hexadecimals representing characters

Decrypt bytes via key
    - the decrypt function uses the corresponding key to decrypt the encrypted hexadecimals back into a string

## Saving & Parsing message history
- Save label, public key at top of file
- save timestamp, sender label, and message for each message


## "main.py"
IMPORTANT: 
The code only works on unix due to use of SIGNAL,
and only run the code while inside the /src directory

1. Run it with "python main.py" or "python3 main.py"
2. Waits for you to input valid commands listed below.

COMMANDS:
login
create_account
delete_account
chat
delete_history
exit
help
logout
create_contact
list_contacts

## Initiate Chat
- User gives label and IP to initiate chat with someone 
- If label doesn't exist user will have to provide label, IP, and public key.
- When saving message history it will also save the label and public key if the connection was successful.

## Login
- PRovide username and private key
- If successful unlock

## Delete message history
- Have to be logged in
- User provides "contact name" of conversation to be deleted
- Delete that file

## Create Account
- Generate "long term" public and private keys
- Create folder with "username" for message history and key pair storage

## Delete
- Delete folder with username



