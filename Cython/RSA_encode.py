import random
import math
import time

def isEven(n):
    return n % 2 == 0

def gcd(x, y):
    while y != 0:
        (x, y) = (y, x % y)
    return x

def GeneratePrimeNumber(m):
    """Generate a prime number with approximately m digits."""
    p = random.randint(10**(m-1), 10**m - 1)  # Generate a random number with m digits
    if isEven(p):
        p += 1  # Make it odd if it's even
    while pow(2, p-1, p) != 1:  # Check if p is prime using Fermat's little theorem
        p += 2  # Increment by 2 to ensure it remains odd
    return p

def egcd(a, b):
    """Extended Euclidean Algorithm."""
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)

def modinv(a, m):
    """Find modular inverse of a under modulo m."""
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    return x % m

def generateKeys(m, p, q):
    """Generate public and private keys."""
    z = (p - 1) * (q - 1)
    d = random.randint(10**(m-1), 10**m - 1)
    while gcd(d, z) != 1:
        d += 1
    e = modinv(d, z)
    return [e, d]

def BuildSubTokens(text, lengthOfToken):
    """Divide text into chunks of specified length."""
    result = []
    while len(text) > lengthOfToken:
        result.append(text[:lengthOfToken])
        text = text[lengthOfToken:]
    result.append(text)
    return result

def fromDigits(digits, b):
    """Convert a list of digits in base b to a number."""
    n = 0
    for d in digits:
        n = b * n + d
    return n

def Encrypt(text, n1, n2, keyPair1A, KeyPair2B):
    """Encrypt the text using RSA encryption."""
    textNum = list(map(ord, text))  # Convert text to ASCII values
    k1 = int(math.floor(math.log(n1, 256)))
    k2 = int(math.floor(math.log(n2, 256)))
    k = min(k1, k2)  # Find the maximum length of the chunk
    subTokens = BuildSubTokens(textNum, k)  # Split text into chunks
    bigNumbers = [fromDigits(sublist, 256) for sublist in subTokens]  # Convert chunks to numbers
    encrypted = [pow(eachBigNumber, keyPair1A, n1) for eachBigNumber in bigNumbers]  # Encrypt each chunk
    sEncryted = [pow(eachFLEBigNumber, KeyPair2B, n2) for eachFLEBigNumber in encrypted]  # Second layer encryption
    return sEncryted

def toDigits(n, b):
    """Convert a number to a list of digits in base b."""
    digits = []
    while n > 0:
        digits.insert(0, n % b)
        n //= b
    return digits

def Decrypt(encryptedLst, n1, n2, keyPair2A, KeyPair1B):
    """Decrypt the encrypted list."""
    fDecryted = [pow(eachSLEBigNumber, KeyPair1B, n2) for eachSLEBigNumber in encryptedLst]  # First layer decryption
    decrypted = [pow(eachDecrypted, keyPair2A, n1) for eachDecrypted in fDecryted]  # Second layer decryption
    allCharacters = [toDigits(eachBigNumber, 256) for eachBigNumber in decrypted]
    return ''.join(chr(eachCharater) for eachBigNumberlist in allCharacters for eachCharater in eachBigNumberlist)

def writeFiles(lsKeys, n):
    """Write the public and private keys to files."""
    with open("PublicKey.txt", "w") as filepuK:
        filepuK.write(f"{lsKeys[1]}\n{n}")
    with open("PrivateKey.txt", "w") as fileprK:
        fileprK.write(f"{lsKeys[0]}\n{n}")
    print("Done generating private and public keys to files.")
    print("You can share your public key file, but please keep the private key in a safe place")

def getText(path):
    """Read text from a file."""
    with open(path, "r") as file:
        return file.read()

def getTextD(path):
    """Read encrypted text from a file."""
    with open(path, "r") as file:
        return [int(line) for line in file]

def getPrivateOrPublicKey(path):
    """Read keys from a file."""
    with open(path, "r") as file:
        return [int(line.strip()) for line in file]

def writeEncryptedText(sLevelEbNs):
    """Write encrypted text to a file."""
    with open("encryptedText.txt", "w") as fileEncrypt:
        for encypted in sLevelEbNs:
            fileEncrypt.write(f"{encypted}\n")
    print("Done encrypting. Encryption has been written to file encryptedText.txt")
    print("Please send the encrypted file to your communication partner")

def writePlainText(plainText):
    """Write decrypted text to a file."""
    with open("plainTextGen.txt", "w") as filePlain:
        filePlain.write(plainText)
    print("Done decrypting. Decrypted file has been written to file plainTextGen.txt")

if __name__ == "__main__":
    try:
        userchoice = input("Please choose the function you want to perform: 1. Generating Keys  2. Encryption  3. Decryption: ")

        userChoiceInt = int(userchoice)
        if userChoiceInt == 1:
            lengthPrime = int(input("Please input the length of prime numbers to use (up to 100 digits): "))
            lengthPubKey = int(input("Please input the length of public key: "))

            p = GeneratePrimeNumber(lengthPrime)
            q = GeneratePrimeNumber(lengthPrime)
            lsKeys = generateKeys(lengthPubKey, p, q)
            n = p * q

            writeFiles(lsKeys, n)

        elif userChoiceInt == 2:
            plainTextPath = input("Please input the path of the plain text you want to encrypt: ")
            privateKeyPath = input("Please input the path of your private key: ")
            publicKeyPath = input("Please input the path of partner's public key: ")

            text = getText(plainTextPath)
            privateKeyAndMod = getPrivateOrPublicKey(privateKeyPath)
            K1A, nA = privateKeyAndMod
            publicKeyAndMod = getPrivateOrPublicKey(publicKeyPath)
            K2B, nB = publicKeyAndMod

            start_time = time.time()
            sLevelEbNs = Encrypt(text, nA, nB, K1A, K2B)
            end_time = time.time()
            encryption_time = end_time - start_time
            encryption_throughput = len(text.encode('utf-8')) / encryption_time
            print(f"Encryption Time: {encryption_time} seconds")
            print(f"Encryption Throughput: {encryption_throughput} bytes/second")
            writeEncryptedText(sLevelEbNs)

        elif userChoiceInt == 3:
            encryptedPath = input("Please input the path of the encrypted text you want to decrypt: ")
            privateKeyPath = input("Please input the path of your private key: ")
            publicKeyPath = input("Please input the path of partner's public key: ")

            publicKeyAndMod = getPrivateOrPublicKey(publicKeyPath)
            K2A, nA = publicKeyAndMod
            privateKeyAndMod = getPrivateOrPublicKey(privateKeyPath)
            K1B, nB = privateKeyAndMod

            encrypted = getTextD(encryptedPath)

            start_time = time.time()
            plainText = Decrypt(encrypted, nA, nB, K2A, K1B)
            end_time = time.time()
            decryption_time = end_time - start_time
            decryption_throughput = len(plainText.encode('utf-8')) / decryption_time
            print(f"Decryption Time: {decryption_time} seconds")
            print(f"Decryption Throughput: {decryption_throughput} bytes/second")
            writePlainText(plainText)

        else:
            print("Invalid choice")
    except Exception as e:
        print(f"Unexpected error: {e}")
