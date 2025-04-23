org 0x100           ; COM file starts at 0x100
start:
    ; Set video mode 13h (320x200 256-color)
    mov ah, 0x00
    mov al, 0x13
    int 0x10

    ; ES:DI will point to video memory
    mov ax, 0xA000
    mov es, ax
    xor di, di       ; Start at offset 0

    ; Let's draw a diagonal line (just an example pattern)
    ; Each row is 320 bytes
    mov cx, 100      ; Draw 100 pixels

draw_loop:
    mov al, cl       ; Color varies with position
    stosb            ; Write AL to ES:DI and increment DI
    add di, 319      ; Move to next row (di += 320 - 1)
    loop draw_loop

    ; Wait for key press before exiting
    mov ah, 0x00
    int 0x16

    ; Return to text mode (mode 3)
    mov ah, 0x00
    mov al, 0x03
    int 0x10

    ret
