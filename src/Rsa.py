import random
import math

def Encrypt(msg: str, key: tuple):
    """
    Encrypt the given message with the given key, return encrypted string
    This function will need to retain string sentences and characters
    Therefore we will store the string within a list where each element is an integer
    Then it is encrypted and changed to a hex value
    Those hex values are then concatenated in a string to maintain the sentence structure
    The return type of the message will be a string
    """
    (k, modula) = key

    # int list stores integer representation of each char from string
    int_lst = [int(hex(ord(i))[-2]+hex(ord(i))[-1], 16) for i in msg]
    
    # encrypt ints of list and converts them to hex values
    enc_lst = []
    for num in int_lst:
        enc_lst.append(hex(pow(num, k, modula)))

    # join list of hex values and create a string which retains sentence structure
    return ''.join(enc_lst)


def Decrypt(msg: str, key: tuple):
    """
    decrypt the given message with the given key, return decrypted msg
    This function needs to decipher the string of hex values into a string
    First separate string into int_list, each element is represented by an integer
    Then decrypt all the integers of the list and join the list of chars together
    return the decrypted string
    """
    (k, modula) = key

    # int list stores the integer representation of each char from string
    int_list = []
    ele = ""
    for i in msg:
        if(i == 'x'):
           ele = ele[:-1]
           if len(ele) != 0:
            int_list.append(int(ele, 16))
           ele = ""
        else:
            ele += i
    int_list.append(int(ele, 16))

    # decrypt ints of int list
    dec_lst = []
    for num in int_list:
        dec_lst.append(chr(pow(num, k, modula)))

    # join the list of strings and return the decrypted message
    return ''.join(dec_lst)




#### All following functions are used for generating rsa key pairs
def GeneratePair(kSize: int):
    """
    Generate public and private keys
    return public, private
    followed : https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Key_generation
    """
    p = get_prime(kSize)
    q = get_prime(kSize)
    
    
    n = p*q

    totient = (p-1) * (q-1)

    # choose int public_key s.t. 1 < public_key < totient(n) and gcd(public_key, totienT(n)) = 1
    # if gcd = 1 that means they are coprime
    # keep generating public_key till they are coprime
    public_key = get_prime(totient)
    while find_gcd(public_key, totient) != 1:
        public_key = get_prime(totient)

    # the private key is being calulated by the bézout coefficient x returned by the result of extended_eucledian_algo()=(x,y) and is modulo'd with totient
    private_key = extended_ecleudian_algo(public_key, totient)[0] % totient

    # n is the modulo used for encryption and decryption
    return((public_key, n), (private_key, n))

def bit_length(num):
    # the -2 is to get rid of 0b in ex: 0b1011
    return len(bin(num)) - 2

# function that determines if in is prime
def prime(i: int) -> bool:
    
    # 2 is prime, check if i = 2
    if i == 2:
        return True
    # check if i is even or i is less than 2
    if i % 2 == 0 or i < 2:
        return False
    for j in range(3, int(math.sqrt(i)) + 1, 2):
        if i % j == 0:
            # factor found
            return False

    # no factor 
    # number is prime
    return True
 

# find greatest common divisor, use Euclidean algo
def find_gcd(a, b):
    
    if a == 0:
        return b
    if b == 0:
        return a
    # euclidean algo
    while b != 0:
        t = b
        b = a % b
        a = t
    return a


# returns the  bezout coefficents x and y, where ax + by = d
def extended_ecleudian_algo(a,b):
    # algo from pseudo code https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
    old_r, r = 1, 0
    old_s, s = 0, 1

    while b != 0:

        # get the quotient and remainder
        quotient, remainder = divmod(a, b)
        a, b = b, remainder
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
    return (old_r, old_s)


# generate random prime number
def get_prime(ksize: int):
    # getrandbits -> generate number within max number of bits used to represent key 
    # finding the floor of the key size with 2 gives us how many bits are needed to represent the key
    i = random.getrandbits(bit_length(ksize))
    while not prime(i):
        i = random.getrandbits(bit_length(ksize))
    return i
