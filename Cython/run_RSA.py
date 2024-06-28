# Import necessary modules
import time
import RSA_encode

# Entry point of the script
if __name__ == "__main__":
    try:
        # Prompt user to choose an operation
        userchoice = input("Please choose the function you want to perform: 1. Generating Keys  2. Encryption  3. Decryption: ")
        userChoiceInt = int(userchoice)

        if userChoiceInt == 1:
            # Generate keys
            lengthPrime = int(input("Please input the length of prime numbers to use: "))
            lengthPubKey = int(input("Please input the length of public key: "))

            start_time = time.time()
            p = RSA_encode.GeneratePrimeNumber(lengthPrime)
            q = RSA_encode.GeneratePrimeNumber(lengthPrime)
            lsKeys = RSA_encode.generateKeys(lengthPubKey, p, q)
            n = p * q
            end_time = time.time()

            RSA_encode.writeFiles(lsKeys, n)
            print(f"Key generation throughput: {end_time - start_time} seconds")

        elif userChoiceInt == 2:
            # Encrypt the plain text
            plainTextPath = input("Please input the path of the plain text you want to encrypt: ")
            privateKeyPath = input("Please input the path of your private key: ")
            publicKeyPath = input("Please input the path of partner's public key: ")

            text = RSA_encode.getText(plainTextPath)
            privateKeyAndMod = RSA_encode.getPrivateOrPublicKey(privateKeyPath)
            K1A, nA = privateKeyAndMod
            publicKeyAndMod = RSA_encode.getPrivateOrPublicKey(publicKeyPath)
            K2B, nB = publicKeyAndMod

            start_time = time.time()
            sLevelEbNs = RSA_encode.Encrypt(text, nA, nB, K1A, K2B)
            end_time = time.time()

            RSA_encode.writeEncryptedText(sLevelEbNs)
            print(f"Encryption throughput: {end_time - start_time} seconds")

        elif userChoiceInt == 3:
            # Decrypt the encrypted text
            encryptedPath = input("Please input the path of the encrypted text you want to decrypt: ")
            privateKeyPath = input("Please input the path of your private key: ")
            publicKeyPath = input("Please input the path of partner's public key: ")

            publicKeyAndMod = RSA_encode.getPrivateOrPublicKey(publicKeyPath)
            K2A, nA = publicKeyAndMod
            privateKeyAndMod = RSA_encode.getPrivateOrPublicKey(privateKeyPath)
            K1B, nB = privateKeyAndMod

            encrypted = RSA_encode.getTextD(encryptedPath)

            start_time = time.time()
            plainText = RSA_encode.Decrypt(encrypted, nA, nB, K2A, K1B)
            end_time = time.time()

            RSA_encode.writePlainText(plainText)
            print(f"Decryption throughput: {end_time - start_time} seconds")

        else:
            print("Invalid choice")
    except Exception as e:
        print(f"Unexpected error: {e}")
