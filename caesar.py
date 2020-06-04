import json
import datetime
import time

def caesarCipher(plainText,key,jsonReturn = True ):
    if jsonReturn :
        inititalTimeStamp =  datetime.datetime.now() #starting time

        cipherText = []

        data = {}
        data["plainText"] = plainText
        data["finiteLength"] = "26"
        data["charset"] = "ascii"
        data["iterations"] = []

        for i in range(len(plainText)):
            temp = {}
            temp["iter"] = i+1

            cT = ord(plainText[i])+key
            cipherText.append(chr(cT))

            temp["character"] = chr(cT) + " = " + plainText[i] + "+" + str(key)
            temp["math"] = str(cT) +" = " + str(ord(plainText[i]))+ "+" + str(key)
            data["iterations"].append(temp)

        data["cipherText"] = ''.join(cipherText)

        finalTimeStamp = datetime.datetime.now() #final time

        data["executionTime"] = str((finalTimeStamp - inititalTimeStamp).total_seconds() * 1000)+"ms"

        jsonObj = json.dumps(data)

        return jsonObj

    else :
        cipherText =  ''.join(list(map(lambda x : chr(ord(x) + key) , plainText)))

        return cipherText



if __name__ == '__main__':
    print(type(json.loads(caesarCipher("apple",3,True))))



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
