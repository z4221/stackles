
global _start

extern printf

section .data
format db "%lu" 10 0

section .bss

callStackBegin:
	resq 2048
callStackEnd:

section .text

_start:
	xor r15, r15
	call main
	mov rax, 60
	pop rdi
	syscall

test:
	
	pop r11
	add r15, 8
	mov [callStackBegin + r15], r11
mov r10, 42
	push r10
	mov r10, 2
	push r10
	mov r10, 42
	push r10
	xor rdx, rdx
	pop r10
	pop rax
	div r10
	push rax
	call dumpStack
	
	push qword [callStackBegin + r15]
	sub r15, 8
	ret

add:
	
	pop r11
	add r15, 8
	mov [callStackBegin + r15], r11
pop r10
	add [rsp], r10
	
	push qword [callStackBegin + r15]
	sub r15, 8
	ret

fib:
	
	pop r11
	add r15, 8
	mov [callStackBegin + r15], r11
cmp [rsp], 0mov r10, 1
	push r10
	pop r10
	sub [rsp], r10
	call fib
	mov r10, 2
	push r10
	pop r10
	sub [rsp], r10
	call fib
	pop r10
	add [rsp], r10
	
	push qword [callStackBegin + r15]
	sub r15, 8
	ret

main:
	
	pop r11
	add r15, 8
	mov [callStackBegin + r15], r11
mov r10, 10
	push r10
	mov r10, 20
	push r10
	pop r10
	add [rsp], r10
	call popPrint
	mov r10, 10
	push r10
	mov r10, 20
	push r10
	pop r10
	sub [rsp], r10
	call popPrint
	mov r10, 10
	push r10
	mov r10, 20
	push r10
	xor rdx, rdx
	pop r10
	pop rax
	div r10
	push rax
	call popPrint
	mov r10, 10
	push r10
	mov r10, 20
	push r10
	pop rax
	pop r10
	mul r10
	push rax
	call popPrint
	mov r10, 10
	push r10
	mov r10, 10
	push r10
	pop r10
	sub [rsp], r10
	cmp [rsp], 0mov r10, 0
	push r10
	cmp [rsp], 0mov r10, 0
	push r10
	cmp [rsp], 1cmp [rsp], 10cmp [rsp], 10cmp [rsp], 10cmp [rsp], 10call test
	mov r10, 10
	push r10
	mov r10, 10
	push r10
	call add
	call popPrint
	
	push qword [callStackBegin + r15]
	sub r15, 8
	ret
