ORG 100h
       
n dw ?
mult dw ?

mov ax, 6 ; n - needed first number input!
mov bx, 2
mul bx ; 5 * 2 = 10 => we'll get mult of 5 first odd nums!
mov n, ax
mov ax, 1

mov cx, 1 ; Start

For:
  cmp cx, n
  jbe isOdd
  ja break
      

isOdd:
mov mult, ax
mov ax, cx
div bx
cmp dx, 1
je doMult
add cx, 1
mov ax, mult
jne For

doMult:
mov ax, mult
mul cx
mov mult, ax
add cx, 1
jmp For

break:
  
INT 21h