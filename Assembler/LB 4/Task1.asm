ORG 100h

mov bx, A
CALL factorial
mov fact_A, ax

mov bx, B
CALL factorial
mov fact_B, ax

mov bx, C
CALL factorial
mov fact_C, ax

mov ax, fact_A
add ax, fact_B
add ax, fact_C

INT 20h

factorial PROC ; value to find factorial should be in bx!!!
    mov ax, 1 ; start value
    add bx, 1
    mov cx, 1 ; iterator
    for:
    cmp cx, bx
    je done
    mul cx
    add cx, 1
    jmp for
    
done: ; result stores in ax!
    
RET ; returning to main    
ENDP

A dw 3
B dw 4
C dw 5
fact_A dw ?
fact_B dw ?
fact_C dw ?