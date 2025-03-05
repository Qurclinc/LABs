include "emu8086.inc"

ORG 100h

CALL input
mov a, ax

CALL endline

CALL input
mov b, ax

CALL endline

mov ax, a
mov bx, b
add ax, bx
mov addition, ax

mov ax, a
mov bx, b
sub ax, bx
mov subtraction, ax


mov ax, addition
CALL PRINT_NUM
CALL endline

mov ax, subtraction
CALL PRINT_NUM


INT 20h

input PROC
    mov bx, 0 ; we should reset bx-storage to not have errors
    ReadLoop:
    mov ah, 01h ; Triggering console
    INT 21h     

    cmp al, 0Dh ; checking if "enter" pressed
    je Done ; if so then break this loop

    sub al, '0' ; other way we should subract AL value (pressed key) 
    mov ah, 0 ; and '0': we get number itself this way
    push ax ; AH contains some stuff so get rid of it and save
    ; this single number

    mov ax, bx ; numbers are decimal: so we have to consider this 
    mov dx, 10 
    mul dx ; multiplication gives category accounting on each step
    pop dx ; now DX contains saved number      
    add ax, dx ; and we're adding them  

    mov bx, ax ; BX saves this  

    jmp ReadLoop ; let's do it again for another number

Done:    
    mov ax, bx    
    RET
ENDP     

endline PROC   
    
    mov dl, 0Dh ; carrige return
    mov ah, 02h
    INT 21h
    
    mov dl, 0Ah   ; new line
    mov ah, 02h
    INT 21h
    RET
ENDP

a dw ?
b dw ?
addition dw ?
subtraction dw ?
DEFINE_PRINT_NUM
DEFINE_PRINT_NUM_UNS