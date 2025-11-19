ORG 100h

mov ax, x1
CALL f(x)
mov bx, 4
mul bx
mov fx1, ax

mov ax, x2
CALL f(x)
add ax, fx1

INT 20h
       
f(x) PROC ; x should be in ax!!!
    mov cx, ax ; original x stores in cx
    mul cx
    mul cx
    mov bx, 5
    mul bx ; 5x^3 now in ax
    mov 5cube_x, ax
    
    mov ax, cx
    mul cx
    mov square_x, ax
    mov ax, 5cube_x
    mov bx, square_x
    sub ax, bx
    add ax, const
    
    RET
ENDP
       
       
x1 dw 3
x2 dw 4
x dw ? ; tmp var to save source x
5cube_x dw ?
square_x dw ?
const dw 6
fx1 dw ?