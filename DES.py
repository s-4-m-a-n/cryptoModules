import json
import datetime
import time

# _=%

# def isEven(string):
#     return True if len(string)%2 == 0 else False


roundKeys = []


compression_PBlock = [14, 17, 11, 24, 1, 5,
                       3, 28, 15, 6, 21, 10,
                      23, 19, 12, 4, 26, 8,
                      16, 7, 27, 20, 13, 2,
                      41, 52, 31, 37, 47, 55,
                      30, 40, 51, 45, 33, 48,
                      44, 49, 39, 56, 34, 53,
                      46, 42, 50, 36, 29, 32]


initial_permutation_Table  = [58, 50, 42, 34, 26, 18, 10, 2,
                         60, 52, 44, 36, 28, 20, 12, 4,
                         62, 54, 46, 38, 30, 22, 14, 6,
                         64, 56, 48, 40, 32, 24, 16, 8,
                         57, 49, 41, 33, 25, 17, 9, 1,
                         59, 51, 43, 35, 27, 19, 11, 3,
                         61, 53, 45, 37, 29, 21, 13, 5,
                         63, 55, 47, 39, 31, 23, 15, 7 ]

#inverse initial permutation
final_Permutation_Table  = [40, 8, 48, 16, 56, 24, 64, 32,
                           39, 7, 47, 15, 55, 23, 63, 31,
                           38, 6, 46, 14, 54, 22, 62, 30,
                           37, 5, 45, 13, 53, 21, 61, 29,
                           36, 4, 44, 12, 52, 20, 60, 28,
                           35, 3, 43, 11, 51, 19, 59, 27,
                           34, 2, 42, 10, 50, 18, 58, 26,
                           33, 1, 41, 9, 49, 17, 57, 25]

#straight-P-box
straight_Permutation_Table = [  16, 7, 20, 21,
                    			29, 12, 28, 17,
                    			1, 15, 23, 26,
                    			5, 18, 31, 10,
                    			2, 8, 24, 14,
                    			32, 27, 3, 9,
                    			19, 13, 30, 6,
                    			22, 11, 4, 25 ]

expansion_P_Box = [	32, 1, 2, 3, 4, 5, 4, 5,
		            6, 7, 8, 9, 8, 9, 10, 11,
		            12, 13, 12, 13, 14, 15, 16, 17,
		            16, 17, 18, 19, 20, 21, 20, 21,
		            22, 23, 24, 25, 24, 25, 26, 27,
		            28, 29, 28, 29, 30, 31, 32, 1 ]

s_Boxes = [
			# Box-1
			[
			[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
			[0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
			[4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
			[15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]
			],
			# Box-2

			[
			[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
			[3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
			[0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
			[13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]
			],

			# Box-3

			[
			[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
			[13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
			[13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
			[1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]

			],

			# Box-4
			[
			[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
			[13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
			[10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
			[3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]
			],

			# Box-5
			[
			[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
			[14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
			[4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
			[11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]
			],
			# Box-6

			[
			[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
			[10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
			[9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
			[4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]

			],
			# Box-7
			[
			[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
			[13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
			[1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
			[6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]
			],
			# Box-8

			[
			[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
			[1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
			[7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
			[2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]
			]

			]



def bitNormalization(bitString,lengthToBe= 64): # takes nth bit binary value returns 64bit binary values by adding extrabits if input binString is less than 64 else throws exceptation
	if len(bitString) >lengthToBe:
		print("error plainText is greater that 64 bits ")
		exit()
	elif len(bitString) < lengthToBe:
		#check if the bPlainText is of even length or not if not then append additional bit at front

		extraBits = lengthToBe - len(bitString)   #extra bits to be added to make 64bits

		bitString = ''.join('0' for i in range(extraBits)) + bitString

		return bitString


def dropParityBits(bitString,pos= [7,15,23,31,39,47,55,63]):
	return ''.join(bitString[i] if i not in pos else '' for i in range(len(bitString)))


def circularShiftLeft(binary,value): # value defines length bits shift ie one bit or two bit shift
	return binary[value:]+ binary[:value]


def permute(binString,pBlock,len): # len defines output binarystring length

		return ''.join(binString[pBlock[i]-1] for i in range(len) )



def binStr2string(binstring,blockLength = 8 ):
	index = 0
	str = ''
	for i in range(int(len(binstring)/blockLength)):
		bin = binstring[index:index+blockLength]
		str += chr(int(bin,2))
		index += blockLength



	return str





def  round_key_Generate(actualKey): #returns round keys
	bActualKey = string2binStr(actualKey)
	bActualKey = bitNormalization(bActualKey) # normalized into 64bits

	bActualKey = dropParityBits(bActualKey) # drop parity bits of given pos

	lbActualKey , rbActualKey =  twoEqualHalves(bActualKey) #divide into two equal halves

	# 16 rounds to generate 16 rounds keys for each round

	oneBitShiftsRounds = [0,1,8,15]  # shift one bit at this rounds

	for i in range(16):
		if i in oneBitShiftsRounds:
			lbActualKey = circularShiftLeft(lbActualKey,1)
			rbActualKey =  circularShiftLeft(rbActualKey,1)
		else:
			lbActualKey = circularShiftLeft(lbActualKey,2)
			rbActualKey =  circularShiftLeft(rbActualKey,2)


		combinedKey = lbActualKey + rbActualKey

		roundkey = permute(combinedKey,compression_PBlock,48)


		rkString = binStr2string(roundkey,8)

		roundKeys.append(roundkey)




def twoEqualHalves(string):
	return 	string[: int(len(string)/2)] , string[int(len(string)/2) : ]


def string2binStr(plainText) : # convert string into binary string
	return ''.join(format(ord(x),'08b') for x in plainText)


def swap(l,r):
	return r,l


def xor_(binStr1,binStr2):
	binString = ''
	# print("l",binStr1)
	# print("2",binStr2)

	for i in range(len(binStr1)):
		if binStr1[i] == binStr2[i]:
			binString += '0'
		else:
			binString += '1'

	return binString


# sbox functions

def get_first_and_last_bit(binString):
	return binString[0]+binString[-1]

def get_middle_fout_bit(binString):
	return binString[1:5]

def bin2dec(binString):
	return int(binString,2)

def dec2bin(dec):
	return format(dec,'04b')

def lookup_sbox(boxCount,first_last,middle4):
	dec_firstLast = bin2dec(first_last) #row pointer
	dec_middle = bin2dec(middle4)	# col pointer

	# print("bc",boxCount,"dc",dec_firstLast,"dm",dec_middle)

	sbox_value = s_Boxes[boxCount][dec_firstLast][dec_middle]

	return dec2bin(sbox_value)


# -----------------

def DES_function(binString,key):
	#expansionn p block , that expands 32bit input plain Text into 48 bit
	expanded_binString = permute(binString,expansion_P_Box,48)

	# xor key and expanded right half
	xored_binstring = xor_(expanded_binString,key)

	# substitution box
	sbox_result = ""
	index = 0
	blockSize = 6

	for sboxCount in range(8):
		temp =  xored_binstring[index:index+blockSize] # split into 6 bits in each round

		first_last = get_first_and_last_bit(temp)
		middle4 = get_middle_fout_bit(temp)
		sbox_result += lookup_sbox(sboxCount,first_last,middle4)

		index += blockSize


	straight_Permutation_value =  permute(sbox_result,straight_Permutation_Table,32)

	return straight_Permutation_value


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


def  DES_encryption(plainText,key):

		bPlainText = string2binStr(plainText)  #binary  representation of the plain Text

		bPlainText =  bitNormalization(bPlainText)

		#initital permutation

		bPlainText = permute(bPlainText,initial_permutation_Table,64)

		#split bPlainText into two equal halves

		lbPlainText, rbPlainText = twoEqualHalves(bPlainText)

		# generate round keys
		round_key_Generate(key)

		for i in range(16):

			fun_Output = DES_function(rbPlainText,roundKeys[i])

			xor_Output =  xor_(lbPlainText,fun_Output)

			#swap left and right

			lbPlainText , rbPlainText = swap(xor_Output,rbPlainText)


		# combined left and right halves

		combined_binString = lbPlainText + rbPlainText

		# apply final permuation

		final_Permutation_value = permute(combined_binString,final_Permutation_Table,64)

		cipherText = binStr2string(final_Permutation_value)
		cipherText_hex = bin2hex(final_Permutation_value)

		print("cipherText-hex value",bin2hex(final_Permutation_value))
		print("cipherText - bin value ",hex2bin(cipherText_hex))
		print("cipher Text - bin value ",final_Permutation_value)
		print(" CIpherText - ascii ", cipherText)
		print()

		return cipherText_hex



def DES_decryption(cipherText,key): # cipher text takes hex value suppose

		bCipherText = hex2bin(cipherText)  #binary  representation of the plain Text

		print(bCipherText)
		print(string2binStr("apple"))
		# bPlainText =  bitNormalization(bPlainText)

		#initital permutation

		bCipherText = permute(bCipherText,initial_permutation_Table,64)

		#split bPlainText into two equal halves

		rbCipherText, lbCipherText = twoEqualHalves(bCipherText)

		# generate round keys
		# round_key_Generate(key)

		for i in range(15,-1,-1):

			fun_Output = DES_function(rbCipherText,roundKeys[i])

			xor_Output =  xor_(lbCipherText,fun_Output)

			#swap left and right

			lbCipherText , rbCipherText = swap(xor_Output,rbCipherText)


		# combined left and right halves

		combined_binString = rbCipherText + lbCipherText

		# apply final permuation

		final_Permutation_value = permute(combined_binString,final_Permutation_Table,64)

		plainText = binStr2string(final_Permutation_value)
		hexValue = bin2hex(final_Permutation_value)

		print("plainText-hex value",bin2hex(final_Permutation_value))
		print("plainText - bin value ",hex2bin(hexValue))
		print("plainText - bin value ",final_Permutation_value)
		print("plainText - ascii ", plainText)


if __name__ == '__main__':
	plainText = "a quick"
	key= "apple"
	cipherText = DES_encryption("a quick","apple")
	DES_decryption(cipherText,"apple")



''' json structure

{
	"plain Text" : plainText,
	"cipherText" : cipherText,
	"finite length" : 26,
	"charset" : customize/ascii,
	"iterations" : [
					{
						"iter" : "1",
						"character" : cryptoChar = plainText + key ,
						"math" : num-cryptochar = num-plainText + key
					}

					]
	"total time taken" : time-calculate

}




'''
