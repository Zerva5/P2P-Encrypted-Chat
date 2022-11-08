# SENG360 SM

SENG360 Assignment 3: Message Application

Group members:

Lucas Mayall

Dylan Hughes

Sylvain Taghaoussi

Josh Blanch

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