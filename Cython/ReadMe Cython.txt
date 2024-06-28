To run the RSA script using Cython for potential performance improvements and to test for the throughputs, you can follow these steps:

1. Install Cython: First, ensure that you have Cython installed in your Python environment. You can install it using pip:
		pip install cython

2. Prepare the Python Script for Cython: Save your Python script (RSA_encode.py) into a new file named RSA_encode.pyx.

3. Create a Setup File: Create a setup.py file to compile the Cython script. This setup file is used to build the Cython extension.

	Create a file named setup.py with the following content:

# <--Copy-n-paste verbatim in notepad and save as setup.py -->
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("RSA_encode.pyx")
)
# <--Code ends here -->

4. Compile the Cython Script: Use the setup script to compile the .pyx file into a C extension. Run the following command in your command line:

		python setup.py build_ext --inplace

This will generate a .c file and a compiled shared object (.so or .pyd file, depending on your operating system).

5. Modify Your Script to Import the Compiled Module: If you named your Python script RSA_encode.pyx, it will be compiled to RSA_encode.so (on Unix-like systems) or RSA_encode.pyd (on Windows). You need to modify your main script to import this compiled module. We have to create a new script named run_RSA.py:

# <--Copy-n-paste verbatim in notepad and save as run_RSA.pyy -->
import time
import RSA_encode

if __name__ == "__main__":
    try:
        userchoice = input("Please choose the function you want to perform: 1. Generating Keys  2. Encryption  3. Decryption: ")

        userChoiceInt = int(userchoice)
        if userChoiceInt == 1:
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
            encryption_time = end_time - start_time
            encryption_throughput = len(text.encode('utf-8')) / encryption_time
            print(f"Encryption Time: {encryption_time} seconds")
            print(f"Encryption Throughput: {encryption_throughput} bytes/second")

            RSA_encode.writeEncryptedText(sLevelEbNs)
            print("Encryption completed and encrypted text written to file.")

        elif userChoiceInt == 3:
            encryptedPath = input("Please input the path of the encrypted text you want to decrypt: ")
            privateKeyPath = input("Please input the path of your private key: ")
            publicKeyPath = input("Please input the path of partner's public key: ")

            publicKeyAndMod = RSA_encode.getPrivateOrPublicKey(publicKeyPath)
            K2A, nA = publicKeyAndMod
            privateKeyAndMod = RSA_encode.getPrivateOrPublicKey(privateKeyPath)
            K1B, nB = privateKeyAndMod

            encrypted = RSA_encode.getTextD(encryptedPath)

            start_time = time.time()
            decrypted_text = RSA_encode.Decrypt(encrypted, nA, nB, K2A, K1B)
            end_time = time.time()

            decryption_time = end_time - start_time
            decryption_throughput = len(decrypted_text.encode('utf-8')) / decryption_time
            print(f"Decryption Time: {decryption_time} seconds")
            print(f"Decryption Throughput: {decryption_throughput} bytes/second")

            RSA_encode.writePlainText(decrypted_text)
            print("Decryption completed and decrypted text written to file.")

        else:
            print("Invalid choice")
    except Exception as e:
        print(f"Unexpected error: {e}")

# <--Code ends here -->


6. Run the run_RSA.py script using either Command Prompt or PowerShell:
	    python run_RSA.py

Follow the prompts to generate keys, encrypt, and decrypt as before. The script will print the throughputs for each operation.
