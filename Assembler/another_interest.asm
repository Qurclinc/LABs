ORG 100h

mov cx, 0  
mov bx, 0  

ReadLoop:
    mov ah, 01h
    INT 21h

    cmp al, 0Dh  
    je Done

    sub al, '0'  
    mov ah, 0
    push ax      

    mov ax, bx 
    mov dx, 10
    mul dx       
    pop dx
    add ax, dx

    mov bx, ax       
    
    jmp ReadLoop 

Done:

MOV DL, 0Dh
MOV AH, 02h
INT 21h

MOV DL, 0Ah
MOV AH, 02h
INT 21h
mov dx, 0
    
mov ax, bx      
mov bx, 2
div bx




cmp dx, 0
je set_null
mov dl, '1'
jmp finish:

set_null:
mov dl, '0'

finish:
mov ah, 02h
INT 21h

    
INT 20h
