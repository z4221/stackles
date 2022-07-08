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

print("Generating AST...")


def exitPrintTokens(index):
    print("Error! token: "+str(tokens[index])+" number: "+str(index))
    for i in range(index-2,index+3):
        print(str(i)+" | "+str(tokens[i]))
    exit(1)

ast = []
astIndex = 0

functionTable = [
        "dumpStack",
        "popPrint",
        ]


def parseToken(temp, index):

    if tokens[index].isnumeric():
        temp["ast"].append({
                    "type": "push",
                    "value": int(tokens[index])
                })
        index += 1
        return (temp, index)

    if tokens[index] == "*":
        temp["ast"].append({
                "type": "operation",
                "operation": "*",
            })
        index += 1
        return (temp, index)

    if tokens[index] == "/":
        temp["ast"].append({
                "type": "operation",
                "operation": "/",
            })
        index += 1
        return (temp, index)

    if tokens[index] == "+":
        temp["ast"].append({
                "type": "operation",
                "operation": "+",
            })
        index += 1
        return (temp, index)

    if tokens[index] == "-":
        temp["ast"].append({
                "type": "operation",
                "operation": "-",
            })
        index += 1
        return (temp, index)

    functionTable.append("cf_"+tokens[index])
    temp["ast"].append({
            "type": "functionCall",
            "function": tokens[index],
        })
    index += 1
    return (temp, index)



index = 0
tokenLength = len(tokens)
while True:
    if index >= tokenLength:
        break

    if tokens[index] == "func":
        temp = {}
        temp["type"] = "function"
        index += 1
        temp["name"] = tokens[index]
        if functionTable.__contains__(tokens[index]):
            print("Error! redefining symbol: "+str(tokens[index]))
            exit(1)
        index += 1
        temp["take"] = tokens[index]
        index += 1
        if tokens[index] != ">":
            exitPrintTokens(index)
        index += 1
        temp["return"] = tokens[index]
        index += 1
        if tokens[index] != ":":
            exitPrintTokens(index)
        index += 1
        temp["stack"] = tokens[index]
        index += 1
        if tokens[index] != "begin":
            exitPrintTokens(index)
        index += 1

        temp["ast"] = []
        while True:
            if index >= tokenLength:
                print("Function never closed! ",end="")
                print(temp["name"])
                exit(1)

            if tokens[index] == "endfunc":
                break

            temp, index = parseToken(temp,index)


        ast.append(temp)
        index += 1

pprint(ast)
print()
pprint(functionTable)

print("Generating code...")

template = """
#include "stackmachine.c"

"""

operations = {
        "+": "stackAdd();",
        "-": "stackSub();",
        "/": "stackDiv();",
        "*": "stackMul();",
        }
mainSize = ""

for i in range(len(ast)):
    if ast[i]["type"] == "function":
        temp = ""
        temp += "void cf_"+str(ast[i]["name"])+"() {\n"
        if ast[i]["name"] == "main":
            mainSize = ast[i]["stack"]
        k = ast[i]["ast"]
        for j in range(len(k)):
            if k[j]["type"] == "push":
                op = "stackPush({C}, "
                count = 1
                op += str(k[j]["value"])
                try:
                    while k[j+1]["type"] == "push":
                        op += ", "
                        op += str(k[j+1]["value"])
                        count += 1
                        j += 1
                except:
                    pass
                op += ");\n"
                op = op.replace("{C}",str(count));
                temp += op

            if k[j]["type"] == "operation":
                temp += str(operations.get(k[j]["operation"])) + "\n"

            if k[j]["type"] == "functionCall":
                func = k[j]["function"]
                for i in functionTable:
                    if i == func:
                        temp += func+"();\n"
                        break;
                    elif i == "cf_"+func:
                        temp += "cf_"+func+"();\n"
                        break;

        template += temp + "}\n"

template += """
int main() {
    initRuntime({SIZE});
    cf_main();
}
""".replace("{SIZE}",mainSize)

print(template);

outfile = open("compilerout.c","w")
outfile.write(template)
outfile.close()

print("Compiling...")

exitCode = os.system("./make.sh")
if exitCode != 0:
    exit(1)

print("Done!")
