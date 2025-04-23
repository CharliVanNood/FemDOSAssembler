section .data
    msg db 'Hello, world!', 0xA  ; message + newline character
    len equ $ - msg              ; length of the message

section .text
    global _start

_start:
    ; write(1, msg, len)
    mov eax, 4          ; syscall number for sys_write
    mov ebx, 1          ; file descriptor 1 = stdout
    mov ecx, msg        ; pointer to the message
    mov edx, len        ; length of the message
    int 0x80            ; make kernel call

    ; exit(0)
    mov eax, 1          ; syscall number for sys_exit
    xor ebx, ebx        ; exit code 0
    int 0x80            ; make kernel call
