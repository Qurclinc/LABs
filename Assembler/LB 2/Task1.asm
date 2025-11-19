ORG 100h ; start

a dw 20
b dw 10

mov ax, [a]
mov bx, [b]

cmp ax, bx
je nullify
jne getGreater

getGreater:
  cmp ax, bx
  ja getA
  jb getB
  
getA:
  mov bx, ax
  jmp finish
 
getB:
  mov ax, bx
  jmp finish
  
nullify:
  mov ax, 0
  mov bx, 0
  jmp finish
  
finish:
  mov [a], ax
  mov [b], bx
  mov ax, [a]
  mov bx, [b] ; Print out
  jmp exit

exit:           
  INT 21h ; end