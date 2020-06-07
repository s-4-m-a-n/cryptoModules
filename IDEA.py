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






def key_Normalization(bitString,lengthToBe = 128): # takes nth bit binary value returns 64bit binary values by adding extrabits if input binString is less than 64 else throws exceptation

    if len(bitString) > lengthToBe:
        print("error key's length is greater that 64 bits ")
        exit()
    elif len(bitString) < lengthToBe:
        #check if the bPlainText is of even length or not if not then append additional bit at front
        extraBits = lengthToBe - len(bitString)   #extra bits to be added to make 64bits

        bitString = ''.join('0' for i in range(extraBits)) + bitString

        return bitString



def bitNormalization(bitString,blockSize = 64):
    totalBlocks = math.ceil(len(bitString) / blockSize )

    blocks_of_64bits = []

    for i in range(totalBlocks):
        blocks_of_16bits = [] # 64bits plainText are divided into 4 blocks of 16 bits each

        blockString64 = bitString[ i * blockSize : i * blockSize + blockSize]

        if len(blockString64) < blockSize :
            #check if the bPlainText is of even length or not if not then append additional bit at front

            extraBits = blockSize - len(blockString64)   #extra bits to be added to make 64bits

            blockString64 = ''.join('0' for i in range(extraBits)) + blockString64 #adding padding bits 0


        # breaking blockstring into four 16 bits block
        for index in range(4):
            blockString16 = blockString64[index*16: index*16 + 16]
            blocks_of_16bits.append(blockString16)


        blocks_of_64bits.append(blocks_of_16bits)

    return blocks_of_64bits


def circularLeftShift(binary,value): # value defines length bits shift ie one bit or two bit shift
    return binary[value:]+ binary[:value]






def mod_additive_inv(binString,mod = 65536 ):
    return format(((mod - int(binString,2))%mod),'016b')



def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def mod_multiplicative_inv(binString,mod = 65537 ):
    g, x, y = egcd( int(binString,2), mod)
    if g != 1:
        return format(0,'016b')
    else:
        return format((x % mod),'016b')






# ----------------------- round key generate -----------------------------------------------

def  round_key_Generate(actualKey,subKeySize = 16 , reversed = False ): #returns total 54 round keys , each of 8 rounds required 6 subkeys (8*6 = 48) and 4 sub-keys are used in last odd round. so 48+4 = 54
    roundKeys = []

    bActualKey = string2binStr(actualKey) # convert into binary string , binary Actual Key
    bActualKey = key_Normalization(bActualKey) # normatize the key into 128 bits


    while len(roundKeys) < 52 : #loop until 52 keys are not generated
        for index in range(8) :
            if len(roundKeys) == 52 :
                break;

            subKey = bActualKey[index*subKeySize : index * subKeySize + subKeySize ]

            roundKeys.append(subKey)

        bActualKey = circularLeftShift(bActualKey,25)

    if reversed == True:

        # roundKeys = roundKeys[::-1]  # reversing order of round keys

        # for i in range(0,len(roundKeys),3): # jump two steps
        #     roundKeys[i] = mod_additive_inv(roundKeys[i])

        # for i in range(0,len(roundKeys)):
        #     if i%2 != 0 :
        #         roundKeys[i] = mod_additive_inv(roundKeys[i])

        return roundKeys[::-1]


    # print("round key ", roundKeys)
    return roundKeys

# -------------------------------------------------------------------------------------





# -------------------------------------3 major operators --------------------------------------------------

def modular_adder(x1,x2,mod = 65536 ):
    res =  format(((int(x1,2) + int(x2,2)) % mod),'016b')
    return res


def modular_multiplication( x1 , x2 , mod = 65537) :
     # ------------------- converting  0 into 65536 : so that result wont be zero ------------------

    x1 = format(65536,'016b') if x1 == format(0,'016b') else x1
    x2 = format(65536,'016b') if x2 == format(0,'016b') else x2

    # ---------------------------------------------

    res = format(((int(x1,2) * int(x2,2)) % mod),'016b')

    if len(res) > 16 : # for length greater that 16bits , i.e 1000000000000000
        return res[1:]

    return res


def xor_(binStr1,binStr2):
    binString = ''
    # print("l",binStr1)
    # print("2",binStr2)

    # ------------------- converting 65536 (17 bits ( bit 1 + 16 bits zer0)) into 16 bits zeros ------------------

    binStr1 = format(0,'016b') if binStr1 == format(65536,'016b') else binStr1
    binStr2 = format(0,'016b') if binStr2 == format(65536,'016b') else binStr2


    # -------------------------------------------------------------------------------------------------------------
    for i in range(len(binStr1)):
        if binStr1[i] == binStr2[i]:
            binString += '0'
        else:
            binString += '1'

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
    s0 = modular_multiplication(p[0] , k[0] , mod = 65537 ) # pow(2,16) + 1  = 65536 + 1
    s1 = modular_adder(p[1] , k[1] , mod = 65536 )  # pow(2,16)  = 65536
    s2 = modular_adder(p[2] , k[2] , mod = 65536)
    s3 = modular_multiplication(p[3] , k[3] , mod = 65537)

    return [s0,s1,s2,s3]



def process_even_round(s,k):

    s4 = xor_(s[0],s[2])
    s5 = xor_(s[1],s[3])
    s6 = modular_multiplication(s4,k[0])
    s7 = modular_adder(s5,s6)
    s8 = modular_multiplication(s7 , k[1])
    s9 = modular_adder(s6,s8)
    s10 = xor_(s[0],s8)
    s11 = xor_(s[2],s8)
    s12 = xor_(s[1],s9)
    s13 = xor_(s[3] ,s9)

    return [s10,s12,s11,s13] # s12 and s11 are permuted / swapped



# ---------------------------------------------------------------------------------------------------------------

def IDEA_encryption(plainText,key):

    bPlainText = string2binStr(plainText)

    bPlainText_Blocks = bitNormalization(bPlainText) # 64 bits blocksize contain four 16 bits sub-blocks

    cipherText = ''
    cipherText_hex = ''
    roundKeys = []

    for  block in  bPlainText_Blocks:

        roundKeys = round_key_Generate(key)

        startingIndex = 0
        p = block

        for round in range(8):

            s = process_odd_round(p, roundKeys[ startingIndex : startingIndex + 4 ] ) # returns result of each four steps
            p = process_even_round(s,roundKeys[ startingIndex + 4 : startingIndex + 6 ] )

            startingIndex = startingIndex + 6

        # last round
        c = process_odd_round( p, roundKeys[ startingIndex : startingIndex + 4 ] )
        # print("index :" , startingIndex + 4)


        combinedValue = c[0] + c[1] + c[2] + c[3]
        cipherText += binStr2string(combinedValue)

        cipherText_hex += bin2hex (c[0] + c[1] + c[2] + c[3] )

    # print("cipher Text:" , cipherText)
    # print("cipherText_hex :",cipherText_hex)

    return cipherText_hex




def IDEA_decryption(cipherText , key) :
        bCipherText = hex2bin(cipherText)  #binary  representation of the plain Text

        bCipherText_Blocks =  bitNormalization(bCipherText)

        plainText =''
        plainText_hex = ''
        roundKeys = []
        #initital permutation


        for index , block in enumerate(bCipherText_Blocks):

                roundKeys = round_key_Generate(key,reversed = True)

                # print("round key rev : ",roundKeys)

                startingIndex = 0
                p = block

                for round in range(8):

                    s = process_odd_round(p, (roundKeys[ startingIndex : startingIndex + 4 ])[::-1] ,decryption = True ) # returns result of each four steps
                    p = process_even_round(s,(roundKeys[ startingIndex + 4 : startingIndex + 6 ])[::-1] )

                    startingIndex = startingIndex + 6



                # last round
                c = process_odd_round( p, (roundKeys[ startingIndex : startingIndex + 4  ]) [::-1] , decryption = True )
                # print("index :" , startingIndex + 4)
                 # result of last round are not permuted , so we permute c1 and c2 to undo permutation that has been done in process odd round function

                plainText += binStr2string(c[0] + c[1] + c[2] + c[3])

                plainText_hex += bin2hex (c[0] + c[1] + c[2] + c[3] )


        # print("cipher Text:" , plainText)
        # print("cipherText_hex :",plainText_hex)

        return plainText







if __name__ == '__main__':

    cipherText = IDEA_encryption("this is a quick brown fox jumps over the lazy dogs 12545679","apple")
    plainText = IDEA_decryption(cipherText,"apple")

    print("plainText :", plainText)
    print("cipherText:",cipherText)







