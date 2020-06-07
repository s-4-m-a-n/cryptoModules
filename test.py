# _=%
# International Data Encryption Algorithm (IDEA)
import math




def string2binStr(plainText) : # convert string into binary string
    return ''.join(format(ord(x),'08b') for x in plainText)

def binStr2string(binstring,blockLength = 8 ):
    index = 0
    string = ''
    for i in range(int(len(binstring)/blockLength)):
        bin = binstring[index:index+blockLength]
        string += chr(int(bin,2)) if int(bin,2) != 0 else ''  # ignoring padding zeros if all 8 bits are zero
        index += blockLength

    return string



def bin2hex(binString):
    hexString = ""

    for i in range(0,int(len(binString)/4)):
        temp = binString[i*4:i*4+4]

        hexString += format(int(temp,2),'x')

    return hexString

def hex2bin(hexString):
    binString = ""

    for i in range(len(hexString)):
        binString += format(int(hexString[i],16),'04b')

    return binString






def key_Normalization(bitString,lengthToBe = 32): # takes nth bit binary value returns 64bit binary values by adding extrabits if input binString is less than 64 else throws exceptation

    if len(bitString) > lengthToBe:
        print("error key's length is greater that 64 bits ")
        exit()
    elif len(bitString) < lengthToBe:
        #check if the bPlainText is of even length or not if not then append additional bit at front
        extraBits = lengthToBe - len(bitString)   #extra bits to be added to make 64bits

        bitString = ''.join('0' for i in range(extraBits)) + bitString

        return bitString



def bitNormalization(bitString,blockSize = 4):
    totalBlocks = math.ceil(len(bitString) / blockSize )

    # blocks_of_64bits = []
    blocks_of_16bits = [] # 64bits plainText are divided into 4 blocks of 16 bits each

    for i in range(totalBlocks):

        blockString64 = bitString[ i * blockSize : i * blockSize + blockSize]

        if len(blockString64) < blockSize :
            #check if the bPlainText is of even length or not if not then append additional bit at front

            extraBits = blockSize - len(blockString64)   #extra bits to be added to make 64bits

            blockString64 = ''.join('0' for i in range(extraBits)) + blockString64 #adding padding bits 0


        # breaking blockstring into four 16 bits block
        # for index in range(4):
        # blockString16 = blockString64[i*4: i*4 + 4]
        blocks_of_16bits.append(blockString64)


        # blocks_of_64bits.append(blocks_of_16bits)

    return blocks_of_16bits


def circularLeftShift(binary,value): # value defines length bits shift ie one bit or two bit shift
    return binary[value:]+ binary[:value]






def mod_additive_inv(binString,mod = 16 ):
    return format(((mod - int(binString,2))%mod),'04b')



def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def mod_multiplicative_inv(binString,mod = 17 ):
    g, x, y = egcd( int(binString,2), mod)
    if g != 1:
        return format(0,'04b')
    else:
        return format((x % mod),'04b')






# ----------------------- round key generate -----------------------------------------------

def  round_key_Generate(actualKey,subKeySize = 4 , reversed = False ): #returns total 54 round keys , each of 8 rounds required 6 subkeys (8*6 = 48) and 4 sub-keys are used in last odd round. so 48+4 = 54
    roundKeys = []

    # bActualKey = string2binStr(actualKey) # convert into binary string , binary Actual Key
    # bActualKey = key_Normalization(bActualKey) # normatize the key into 128 bits
    bActualKey = actualKey

    while len(roundKeys) < 28 : #loop until 52 keys are not generated
        for index in range(8) :
            if len(roundKeys) == 28 :
                break;

            subKey = bActualKey[index*subKeySize : index * subKeySize + subKeySize ]

            roundKeys.append(subKey)

        bActualKey = circularLeftShift(bActualKey,6)
        # roundKeys.append("*")

    if reversed == True:

        return roundKeys[::-1]


    # print("round key ", roundKeys)
    return roundKeys

# -------------------------------------------------------------------------------------





# -------------------------------------3 major operators --------------------------------------------------

def modular_adder(x1,x2,mod = 16 ):
    res =  format(((int(x1,2) + int(x2,2)) % mod),'04b')
    return res


def modular_multiplication( x1 , x2 , mod = 17) :
    # print("mul",x1,x2)
    x1 = '10000' if x1 == '0000' else x1
    x2 = '10000' if x2 == '0000' else x2

    res = format(((int(x1,2) * int(x2,2)) % mod),'04b')

               #-------------------------- bug

    return  res

def xor_(binStr1,binStr2):
    binString = ''
    # print("l",binStr1)
    # print("2",binStr2)

    length1 = len(binStr1)
    length2 = len(binStr2)

    for i in range(min(length1,length2)):
        if binStr1[length1-1] == binStr2[length2-1]:
            binString =  '0' + binString
        else:
            binString =  '1' + binString

        length1 -= 1
        length2 -= 1


    return binString

#---------------------------------------------R O U N D S------------------------------------------------------------------
def process_odd_round(p,k , decryption = False):
    # print("ksss",k)
    if decryption: # inverting the key for decryption
        k[0] = mod_multiplicative_inv(k[0])
        k[1] = mod_additive_inv(k[1])
        k[2] = mod_additive_inv(k[2])
        k[3] = mod_multiplicative_inv(k[3])


    # print("k inverse",k)
    # print("odd keys " , k )

    s0 = modular_multiplication(p[0] , k[0] , mod = 17 ) # pow(2,16) + 1  = 65536 + 1
    s1 = modular_adder(p[1] , k[1] , mod = 16 )  # pow(2,16)  = 65536
    # print("s0",s1)
    s2 = modular_adder(p[2] , k[2] , mod = 16)
    s3 = modular_multiplication(p[3] , k[3] , mod = 17)

    # print("S3",p[3],k[3], s3)

    return [s0,s1,s2,s3]



def process_even_round(s,k):
    # print("rk",s,"sdf",k)
    s4 = xor_(s[0],s[2])
    s5 = xor_(s[1],s[3])

    print("s4 key0",s4,k[0])

    s6 = modular_multiplication(s4,k[0])

    s7 = modular_adder(s5,s6)
    s8 = modular_multiplication(s7 , k[1])
    s9 = modular_adder(s6,s8)
    # print("S9",s6,s8,s9)
    s10 = xor_(s[0],s8)
    s11 = xor_(s[2],s8)
    s12 = xor_(s[1],s9)
    s13 = xor_(s[3] ,s9)

    # print("s13",s9,s[3],s13)

    return [s10,s12,s11,s13] # s12 and s11 are permuted / swapped



# ---------------------------------------------------------------------------------------------------------------

def IDEA_encryption(plainText,key):

        bPlainText = plainText

        bPlainText_Blocks = bitNormalization(bPlainText) # 64 bits blocksize contain four 16 bits sub-blocks

        # print("plain text ",bPlainText_Blocks)
        cipherText = ''
        cipherText_hex = ''
        roundKeys = []

        # for index , block in enumerate(bPlainText_Blocks):

        roundKeys = round_key_Generate(key)


        print("round key",roundKeys)

        startingIndex = 0
        p = bPlainText_Blocks
        # print(index)


        for round in range(4):

            s = process_odd_round(p,roundKeys[ startingIndex : startingIndex + 4 ] ) # returns result of each four steps

            print("odd round :",s)

            p = process_even_round(s,roundKeys[ startingIndex + 4 : startingIndex + 6 ] )

            print("even round : ",p)

            startingIndex = startingIndex + 6

            # print("i",round)

        # last round
        c = process_odd_round( p, roundKeys[ startingIndex : startingIndex + 4 ] )

        print("last round :", c)
        # print("index :" , startingIndex + 4)
         # result of last round are not permuted , so we permute c1 and c2 to undo permutation that has been done in process odd round function

        combinedValue = c[0] + c[2] + c[1] + c[3]
        cipherText += combinedValue

        cipherText_hex += c[0] + c[1] + c[2] + c[3]

    # print("cipher Text:" , cipherText)
    # print("cipherText_hex :",cipherText_hex)

        return cipherText_hex




def IDEA_decryption(cipherText , key) :
                bCipherText = cipherText  #binary  representation of the plain Text

                bCipherText_Blocks =  bitNormalization(bCipherText)

                # print(bCipherText_Blocks)

                plainText =''
                plainText_hex = ''
                roundKeys = []
                #initital permutation


                # for index , block in enumerate(bCipherText_Blocks):

                roundKeys = round_key_Generate(key,reversed = True)

                print("round key rev : ",roundKeys)

                startingIndex = 0
                p = bCipherText

                for round in range(4):

                    s = process_odd_round(p, (roundKeys[ startingIndex : startingIndex + 4 ])[::-1] ,decryption = True ) # returns result of each four steps
                    p = process_even_round(s,(roundKeys[ startingIndex + 4 : startingIndex + 6 ])[::-1] )

                    startingIndex = startingIndex + 6



                # last round
                c = process_odd_round( p, (roundKeys[ startingIndex : startingIndex + 4  ]) [::-1] , decryption = True )
                # print("index :" , startingIndex + 4)
                 # result of last round are not permuted , so we permute c1 and c2 to undo permutation that has been done in process odd round function

                plainText += c[0] + c[2] + c[1] + c[3]

                plainText_hex += c[0] + c[2] + c[1] + c[3]


        # print("cipher Text:" , plainText)
        # print("cipherText_hex :",plainText_hex)

                return plainText







if __name__ == '__main__':

    cipherText = IDEA_encryption("1001110010101100","11011100011011110011111101011001")
    # plainText = IDEA_decryption(cipherText,"110111000110111100111111")

    # print("plainText :", plainText)
    print("cipherText:",cipherText)







