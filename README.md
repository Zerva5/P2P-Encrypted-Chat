
# SENG360 SM

SENG360 Assignment 3: Message Application

Group members:

Lucas Mayall

Dylan Hughes

Sylvain Taghaoussi

Josh Blanch

=======
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

# Design

Use a Data Flow Diagrams (DFD) to design your application. Specify all security mechanisms used in your system, including cryptographic ciphers, keys, key generation mechanisms, and security protocols. Use the gitlab Wiki page for your work. Make sure that each team member edits their own contribution / annotation themselves.

Explain how your design implements the requirements above.

# Code breakdown
## Netcode
- Message format: timestamp, message hash, message
- Message hash for message integrity
- Encrypt with sender private key and reciever public key
## Encryption/Decryption
- Generate public/private key pair
- Forward secrecy handshake (see docs)
- Encrypt bytes via key
- Decrypt bytes via key

## Saving & Parsing message history
- Save label, public key at top of file
- save timestamp, sender label, and message for each message


## "main.py"
1. Run it
2. Waits for you to run command.
Commands are: Login, create account, delete account, delete message history, initiate chat.

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



