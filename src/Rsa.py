import random

def Encrypt(msg: str, key: str) -> str:
    """
    Encrypt the given message with the given key, return encrypted bytes
    """
    return msg

def Decrypt(msg: str, key: str) -> str:
    """
    decrypt the given message with the given key, return decrypted bytes
    """

    return msg




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

    # choose int e s.t. 1 < r < totient(n) and gcd(r, totienT(n)) = 1
    # if gcd = 1 that means they are coprime
    # keep generating r till they are coprime
    public_key = get_prime(totient)
    while find_gcd(public_key, totient) != 1:
        public_key = get_prime(totient)
    
    private_key = extended_ecleudian_algo(public_key, totient)[0] % totient

    return((public_key, n), (private_key, n))



# function that determines if in is prime
def prime(i: int) -> bool:
    if i <= 1:
        return False
    
    # check from x -> sqrt(i) or x^2 -> i
    j = 2
    while j*j <= i:
        #print("stuck in loop %d <= %d", j*j, i)
        # i does have factor between x and sqrt(1)
        if i % j == 0:
            return False
        j += 1
    # number is prime
    return True



    

# find greatest common divisor, use Euclidean algo
def find_gcd(a, b):
    # base case, b = 0
    while b != 0:
        a = b
        b = a % b
    return a


# returns the  bezout coefficents x and y, where ax + by = d
def extended_ecleudian_algo(a,b):
    # algo from pseudo code https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
    old_r, r = a, b
    old_s, s = 1, 0

    while r != 0:
        quotient = a // b 
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
    
    if b != 0:
        bezout_t = (old_r - old_s * a) // b
    else:
        bezout_t = 0

    return (old_s, bezout_t)


# generate random prime number
def get_prime(ksize: int):
    # getrandbits -> generate number within max number of bits used to represent key 
    # finding the floor of the key size with 2 gives us how many bits are needed to represent the key
    i = random.getrandbits(ksize // 2)
    while not prime(i):
        i = random.getrandbits(ksize // 2)
        print(i//2, i)
    return i



def main():
    
    print(GeneratePair(16))

if __name__ == "__main__":
    main()