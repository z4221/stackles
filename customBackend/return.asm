
global _start

section .bss
callStackBegin:
	resq 1024
callStackEnd:

section .text
_start:
	call main
	mov rax, 60
	pop rdi
	syscall

main:
pop r11
mov r10, 10
push r10
mov r10, 2
push r10
xor rdx, rdx
pop r10
pop rax
div r10
push rax
push r11
ret
