from DES import *

# _=%

def doubleDES_encryption(plainText,key1,key2):
    middleText = DES_encryption(plainText,key1)
    cipherText =  DES_encryption(middleText,key2)

    return [cipherText,middleText]


def doubleDES_decryption(cipherText,key1,key2):
    middleText  = DES_decryption(cipherText,key2)
    plainText = DES_decryption(middleText,key1)
    return [plainText,middleText]




if __name__ == '__main__':

    plainText = "a quick brown fox jumps over the lazy dog"
    key1= "apple"
    key2 = "ball"

    cipherText,middleTextEnc = doubleDES_encryption(plainText,key1,key2)
    plainText,middleTextDec = doubleDES_decryption(cipherText,key1,key2)

    print("------------------------------")
    print("cipherText : ",cipherText)
    print("plainText :",plainText)
    print("------------------------------")
    print("middle Text Encryption:",middleTextEnc)
    print("middle Text Decryption : ",middleTextDec)
