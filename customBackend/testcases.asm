
global _start

section .text
_start:
	call main
	mov rax, 60
	pop rdi
	syscall

test:
pop r15
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
push r15
ret
add:
pop r15
pop r10
add [rsp], r10
push r15
ret
fib:
pop r15
mov r10, 1
push r10
pop r10
sub [rsp], r10
mov r10, 2
push r10
pop r10
sub [rsp], r10
pop r10
add [rsp], r10
push r15
ret
main:
pop r15
mov r10, 10
push r10
mov r10, 20
push r10
pop r10
add [rsp], r10
mov r10, 10
push r10
mov r10, 20
push r10
pop r10
sub [rsp], r10
mov r10, 10
push r10
mov r10, 20
push r10
xor rdx, rdx
pop r10
pop rax
div r10
push rax
mov r10, 10
push r10
mov r10, 20
push r10
pop rax
pop r10
mul r10
push rax
mov r10, 10
push r10
mov r10, 10
push r10
pop r10
sub [rsp], r10
mov r10, 0
push r10
mov r10, 0
push r10
mov r10, 10
push r10
mov r10, 10
push r10
push r15
ret
