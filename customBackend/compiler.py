#!/bin/env python3
# vim:set noexpandtab

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
	commentEnd	= 0
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
for i in range(len(tokens)):
	tokens[i] = tokens[i].strip("\t").strip(" ")
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

labelTable = []

def parseToken(temp, index):

	if tokens[index] == "func":
		function = {}
		function["type"] = "function"
		index += 1
		function["name"] = tokens[index]
		if functionTable.__contains__(tokens[index]):
			print("Error! redifining symbol: "+str(tokens[index]))
			exit(1)
		if tokens[index] == "_start":
			print("Error! cannot name a function '_start'.")
			exit(1)
		functionTable.append(tokens[index])
		index += 1
		function["take"] = tokens[index]
		index += 1
		if tokens[index] != '>':
			exitPrintTokens(index)
		index += 1
		function["return"] = tokens[index]
		index += 1
		if tokens[index] != ':':
			exitPrintTokens(index)
		index += 1
		function["stack"] = tokens[index]
		index += 1
		if tokens[index] != "begin":
			exitPrintTokens(index)
		index += 1

		function["ast"] = []
		while True:
			if index >= tokenLength:
				print("Function never closed! "+str(tokens[index]))
				exit(1)
			if tokens[index] == "endfunc":
				break
			if tokens[index] == "func":
				print("Cannot define a function within a function! Offending function: "+str(tokens[index+1]))
				exit(1)
			function, index = parseToken(function,index)

		ast.append(function)
		index += 1
		return (temp, index)

	if tokens[index] == "if":
		branch = {}
		branch["type"] = "branch"
		index += 1
		condition = ""

		while tokens[index] != "then":
			if index >= tokenLength:
				print("Branch condition never ended!")
				exitPrintTokens(index)
			condition += " "+str(tokens[index])
			index += 1
		index += 1
		branch["condition"] = condition.strip()

		bIf = {}
		bIf["ast"] = []
		bElse = {}
		bElse["ast"] = []
		bElif = []
		bElifIndex = -1

		b = [bIf,bElse,bElif]
		# TODO: implement elif functionality
		bc = 0
		while True:
			if index >= tokenLength:
				print("Branch never closed! "+str(tokens[index]))
				exit(1)
			if tokens[index] == "else":
				bc = 1
				index += 1
			if tokens[index] == "elif":
				bc += 1
				index += 1
				bElifIndex += 1
				bElif.append({})
				bElif[bElifIndex]["ast"] = []
				condition = ""
				while tokens[index] != "then":
					if index >= tokenLength:
						print("Branch condition never ended!")
						exitPrintTokens(index)
					condition += " "+str(tokens[index])
					index += 1
				index += 1
				bElif[bElifIndex]["condition"] = condition.strip()
			
			if tokens[index] == "end":
				index += 1
				break
			if bElifIndex == -1:
				b[bc], index = parseToken(b[bc],index)
			else:
				bElif[bElifIndex], index = parseToken(bElif[bElifIndex],index)

		branch["if"] = bIf
		branch["elif"] = bElif
		branch["else"] = bElse

		temp["ast"].append(branch)

		return (temp, index)

	try:
		if int(tokens[index]) or int(tokens[index]) == 0:
			temp["ast"].append({
				"type": "push",
				"value": tokens[index]
			})
			index += 1
			return (temp, index)
	except:
		pass

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
	
	if tokens[index] == "return":
		temp["ast"].append({
			"type": "operation",
			"operation": "return",
		})
		index += 1
		return (temp, index)

	if tokens[index] == "dup":
		temp["ast"].append({
			"type": "operation",
			"operation": "dup",
		})
		index += 1
		return (temp, index)

	if tokens[index] == "goto":
		index += 1
		if labelTable.__contains__(tokens[index]):
			temp["ast"].append({
				"type": "goto",
				"label": str(tokens[index])
			})
			index += 1
			return (temp, index)
		else:
			print("Error! label never defined: "+str(tokens[index]))
			exit(1)


	if tokens[index][:1] == "!":
		temp["ast"].append({
			"type": "gotoLabel",
			"label": str(tokens[index][1:]),	
		})
		labelTable.append(str(tokens[index][1:]))
		index += 1
		return (temp, index)

	if functionTable.__contains__(tokens[index]):
		temp["ast"].append({
			"type": "functionCall",
			"function": tokens[index]
		})
		index += 1
		return (temp, index)
	else:
		print("Error! undefined function: "+str(tokens[index]))
		exit(1)

index = 0
tokenLength = len(tokens)
while True:
	if index >= tokenLength:
		break
	tokens, index = parseToken(tokens,index)

pprint(ast)
print("Function table:")
pprint(functionTable)

print("Generating code...")

for i in ast:
	if i["type"] != "function":
		print("Operations must be inside a function!")
		exit(1)
