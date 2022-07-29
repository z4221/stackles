#!/bin/env python3
# vim:set noexpandtab

import sys
import os
import re
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
	"printInt",
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
	
	if tokens[index] == "exit":
		temp["ast"].append({
			"type": "operation",
			"operation": "exit",
		})
		index += 1
		return (temp, index)

	if tokens[index] == "drop":
		temp["ast"].append({
			"type": "operation",
			"operation": "drop",
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
	
	if tokens[index] == "ret":
		temp["ast"].append({
			"type": "operation",
			"operation": "ret",
		})
		index += 1
		return (temp, index)


	if tokens[index] == "goto":
		index += 1
		temp["ast"].append({
			"type": "goto",
			"label": str(tokens[index])
		})
		index += 1
		return (temp, index)


	if tokens[index][:1] == "!":
		temp["ast"].append({
			"type": "gotoLabel",
			"label": str(tokens[index][1:]),	
		})
		labelTable.append(str(tokens[index][1:]))
		index += 1
		return (temp, index)

	if tokens[index] == "asm":
		instructions = []
		while True:
			index += 1
			if tokens[index] == "endasm":
				index += 1
				break
			instructions.append(tokens[index])
		temp["ast"].append({
			"type": "inlineAssembly",
			"instructions": instructions,
		})
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

code = """
global _start

section .bss

callStackBegin:
	resq 2048
callStackEnd:

section .text

stk_printInt:
	mov eax, [rsp+8]

	mov ecx, 10
	push rcx
	mov rsi, rsp
	sub rsp, 16

.L1:
	xor edx, edx
	div ecx

	add edx, '0'
	dec rsi
	mov [rsi], dl
	
	test eax, eax
	jnz .L1

	mov eax, 1
	mov edi, 1
	lea edx, [rsp+16 + 1]
	sub edx, esi
	syscall

	add rsp, 24
	ret

_start:
	xor r15, r15
	call stk_main
	mov rax, 60
	pop rdi
	syscall

"""

saveReturn = """
	pop r11
	add r15, 8
	mov [callStackBegin + r15], r11

"""

loadReturn = """
	push qword [callStackBegin + r15]
	sub r15, 8
	ret

"""

def parseOpt(operation):
	code = ""
	if operation == "+":
		code += "pop r10\n\t"
		code += "add [rsp], r10\n\t"

	if operation == "-":
		code += "pop r10\n\t"
		code += "sub [rsp], r10\n\t"

	if operation == "*":
		code += "pop rax\n\t"
		code += "mul qword [rsp]\n\t"
		code += "push rax\n\t"

	if operation == "/":
		code += "xor rdx, rdx\n\t"
		code += "mov rax, qword [rsp+8]\n\t"
		code += "pop r10\n\t"
		code += "div r10\n\t"
		code += "mov [rsp], rax\n\t"

	if operation == "drop":
		code += "add rsp, 8\n\t"

	if operation == "dup":
		code += "mov r10, [rsp]\n\t"
		code += "push r10\n\t"

	if operation == "exit":
		code += "mov rax, 60\n\t"
		code += "pop rdi\n\t"
		code += "syscall\n\t"
	
	if operation == "ret":
		code += loadReturn

	return code

def parseAst(i):
	code = ""

	for i in node["ast"]:
		if i["type"] == "push":
			code += "push qword "+str(i["value"])+"\n\t"

		if i["type"] == "operation":
			code += parseOpt(i["operation"])

		if i["type"] == "functionCall":
			code += "call stk_" + str(i["function"]) + "\n\t"

		if i["type"] == "inlineAssembly":
			temp = ""
			for word in i["instructions"]:
				if word[-1:] != ".":
					temp += word + " "
				else:
					temp += word[:-1] + "\n\t"
			code += temp

		if i["type"] == "gotoLabel":
			code += "\n" + i["label"] + ":"

		if i ["type"] == "goto":
			code += "jmp " + i["label"] + "\n\t"

		if i["type"] == "branch":
			condition = i["condition"]
			test = ""
			if condition[0] == "_":
				temp = re.split(">|<|=|!",condition)
				try:
					temp = int(temp[-1])
				except:
					print("Hey dipshit you cannot compare to a non int!")
					print("Also we do not support fancy comparing soz")
					exit(1)

				test = "cmp [rsp], "+str(temp)

			else:
				print("Comparing constants is not a thing yet")
				pass

			code += test

	return code


for node in ast:
	if node["type"] != "function":
		print("Operations must be inside a function!")
		exit(1)

	for i in node:
		if i == "name":
			code += "\nstk_" + node[i] + ":\n\t"
		if i == "ast":
			code += saveReturn

			code += parseAst(i)

			code += loadReturn
		

outfile = open(args[1].replace(".cofb",".asm"),"w")
outfile.write(code)
outfile.close()
object = args[1].replace(".cofb",".o")

if os.system("nasm -f elf64 -o {1} {2}"
		.replace("{1}",object)
		.replace("{2}",args[1].replace(".cofb",".asm"))) == 0:
	os.system("ld.lld -o {1} {2}"
			.replace("{1}",object.replace(".o",""))
			.replace("{2}",object))
