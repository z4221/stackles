
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


stk_exitOK:
	
	pop r11
	add r15, 8
	mov [callStackBegin + r15], r11

push qword 0
	mov rax, 60
	pop rdi
	syscall
	
	push qword [callStackBegin + r15]
	sub r15, 8
	ret


stk_main:
	
	pop r11
	add r15, 8
	mov [callStackBegin + r15], r11

push qword 10
	push qword 10
	pop r10
	add [rsp], r10
	call stk_printInt
	add rsp, 8
	push qword 10
	push qword 10
	pop r10
	sub [rsp], r10
	call stk_printInt
	add rsp, 8
	push qword 10
	push qword 10
	xor rdx, rdx
	mov rax, qword [rsp+8]
	pop r10
	div r10
	mov [rsp], rax
	call stk_printInt
	add rsp, 8
	push qword 10
	push qword 10
	pop rax
	mul qword [rsp]
	push rax
	call stk_printInt
	add rsp, 8
	push qword 10
	mov r10, [rsp]
	push r10
	add rsp, 8
	call stk_printInt
	push qword 10
	
loop:call stk_printInt
	dec qword [rsp]
	cmp qword [rsp], qword 0
	je en
	jmp loop
	
en:call stk_exitOK
	
	push qword [callStackBegin + r15]
	sub r15, 8
	ret

