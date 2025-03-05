ORG 100h

MOV CX, 0  
MOV BX, 0  

ReadLoop:
    MOV AH, 01h  
    INT 21h      

    CMP AL, 0Dh  
    JE Done      

    SUB AL, '0'  
    MOV AH, 0
    PUSH AX      

    MOV AX, BX   
    MOV DX, 10
    MUL DX       
    POP DX       
    ADD AX, DX   

    MOV BX, AX   
    INC CX       

    JMP ReadLoop 

Done:
    
    MOV AX, BX  

    INT 20h 
INT 20h
