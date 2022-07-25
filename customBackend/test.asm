
global _start

section .text
_start:
	call main
	mov rax, 60
	pop rdi
	syscall

main:
pop r15
mov rax, 8
push rax
mov rax, 2
push rax
xor rdx, rdx
pop rax
pop rcx
div rcx
push rax
push r15
ret
