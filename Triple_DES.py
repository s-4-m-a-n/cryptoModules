

from DES import *


# _=%

def tripleDES_encryption(plainText,key1,key2,key3):
    middleText1 = DES_encryption(plainText,key1)
    middleText2 =  DES_decryption(middleText1,key2)
    cipherText  =  DES_encryption(middleText2,key3)

    print("middleTExt:",middleText1)
    print("middleText:",middleText2)
    time.sleep(4)
    return [cipherText,middleText1,middleText2]


def tripleDES_decryption(cipherText,key1,key2,key3):
    middleText1  = DES_decryption(cipherText,key3)
    middleText2 = DES_encryption(middleText1,key2)
    plainText = DES_decryption(middleText2,key1)
    return [plainText,middleText1,middleText2]




if __name__ == '__main__':

    plainText = "plain Text"
    key1= "appl"
    key2 = "ballls"
    key3 = "cat"

    cipherText,middleTextEnc1,middleTextEnc2 = tripleDES_encryption(plainText,key1,key2,key3)
    plainText,middleTextDec1,middleTextDec2 = tripleDES_decryption(cipherText,key1,key2,key3)

    print("------------------------------")
    print("cipherText : ",cipherText)
    print("plainText :",plainText)
    print("------------------------------")
    print("middle Text Encryption 1:",middleTextEnc1)
    print("middle Text Decryption 1: ",middleTextDec1)
    print("------------------------------")
    print("middle Text Encryption 2:",middleTextEnc2)
    print("middle Text Decryption 2: ",middleTextDec2)
