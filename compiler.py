#!/bin/env python3

import sys
import os
from pprint import pprint
args = sys.argv

if len(args) < 2:
    print("Provide arguments")
    exit(1)

print("Stripping comments...")
infile = open(args[1],"r")
fullInfile = infile.readlines()
infile.close()
for i in range(len(fullInfile)):
    fullInfile[i] = fullInfile[i].strip(" ")
    if fullInfile[i] == "\n":
        fullInfile[i] = ""

lineNumber = 0
for line in fullInfile:
    for i in range(len(line)):
        if line[i] == "/" and line[i+1] == "/":
            fullInfile[lineNumber] = ""
    lineNumber += 1
while True:
    try:
        fullInfile.remove('')
    except:
        break

for i in range(len(fullInfile)):
    fullInfile[i] = fullInfile[i].replace("\n"," ")

temp = ""
for i in fullInfile:
    temp += i
fullInfile = temp

while True:
    commentBegin = 0
    commentEnd   = 0
    for i in range(len(fullInfile)):
        try:
            if fullInfile[i] == "/" and fullInfile[i+1] == "*":
                commentBegin = i
            if fullInfile[i] == "*" and fullInfile[i+1] == "/":
                commentEnd = i+2
        except:
            commentBegin = 0
            commentEnd = 0
            pass
    if commentBegin == 0 and commentEnd == 0:
        break
    else:
        fullInfile = fullInfile[:commentBegin] +" "+ fullInfile[commentEnd:]

print("Generating tokens...")
tokens = fullInfile.split(" ")
while True:
    try:
        tokens.remove('')
    except:
        break

print(tokens)

print("Generating code...")
finalCode = "#include \"stackmachine.c\"\n\n"

index = 0
returnStack      = True
definingFunction = False
functionName     = ""
tokenLength = len(tokens)
while True:
    if index >= tokenLength:
        break

    elif tokens[index] == "func":
        if definingFunction == True:
            print("Cannot define function inside another function!")
            exit(1)

        definingFunction = True
        functionName = tokens[index+1]
        if tokens[index+1] == "main":
            finalCode += "int "
            finalCode += tokens[index+1]
            finalCode += "() {\ninitRuntime(" + tokens[index+6] + ");\n"
            if tokens[index+2] != "0":
                print("Error! main cannot take arguments!");
                exit(1)

            if tokens[index+4] == "0":
                returnStack = False
            elif tokens[index+4] == "1":
                returnStack = True
            else:
                print("Error! can only return one item from the stack in main")
                exit(1)
        else:
            finalCode += "void "
            finalCode += tokens[index+1]
            finalCode += "() {\n"

        index += 8

    elif tokens[index] == "endfunc":
        if definingFunction == False:
            print("endfunc without func!")
            exit(1)
        definingFunction = False
        if functionName == "main":
            if returnStack == True:
                finalCode += "return stack[stackPtr];\n"
            else:
                finalCode += "return 0;\n"
        finalCode += "}\n"
        index += 1

    elif tokens[index] == "end":
        finalCode += "}\n"
        index += 1

    elif tokens[index].isnumeric():
        temp = "stackPush( COUNT ," + tokens[index]
        count = 1
        index += 1
        if tokens[index].isnumeric():
            while True:
                if tokens[index].isnumeric():
                    temp += ","+tokens[index]
                    count += 1
                    index += 1
                else:
                    break
        temp += ");\n"
        temp = temp.replace(" COUNT ",str(count))
        finalCode += temp


    elif tokens[index] == "+":
        finalCode += "stackAdd();\n"
        index += 1

    elif tokens[index] == "-":
        finalCode += "stackSub();\n"
        index += 1

    elif tokens[index] == "/":
        finalCode += "stackDiv();\n"
        index += 1

    elif tokens[index] == "*":
        finalCode += "stackMul();\n"
        index += 1

    elif tokens[index] == "swap":
        finalCode += "stackSwap();\n"
        index += 1

    elif tokens[index] == "drop":
        finalCode += "stackDrop();\n"
        index += 1

    elif tokens[index] == "dup":
        finalCode += "stackDup();\n"
        index +=1

    elif tokens[index] == "popPrint":
        finalCode += "popPrint();\n"
        index += 1

    elif tokens[index] == "dumpStack":
        finalCode += "dumpStack();\n"
        index += 1

    else:
        finalCode += tokens[index] + "();\n"
        index += 1

print(finalCode)

outfile = open("compilerout.c","w")
outfile.write(finalCode)
outfile.close()

print("Compiling...")

exitCode = os.system("./make.sh")
if exitCode != 0:
    exit(1)

print("Done!")
