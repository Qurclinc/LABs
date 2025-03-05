ORG 100h

a dw ?
b dw ?
c dw ?
min dw ?
max dw ?

mov ax, 10
mov a, ax
mov ax, 20
mov b, ax
mov ax, 30
mov c, ax ; Initializing variables

mov ax, a
cmp ax, b ; compare a 'n' b
jae AnC ; if a >= b lets compare a and c
jbe BnC ; else b >= a so lets compare b and c
       
AnC:
cmp ax, c ; compare a 'n' c
jae GetMin ; if a >=c (and so a >=b) then a is max
jbe BnC ; other way c >= a and so lets comapre b and c

BnC:
  mov ax, b
  cmp ax, c
  jae GetMin ; if b >= c (and b is definitely >= a) then b is max
  mov ax, c ; else c >= c
  jmp GetMin

GetMin:
mov max, ax ; max is always in ax   

mov ax, a ; and here we go again
cmp ax, b ; compare a 'n' b
jbe lAnC ; if a <= b lets compare a and c
jae lBnC ; else b <= a so lets compare b and c
       
lAnC:
cmp ax, c ; compare a 'n' c
jbe GetRes ; if a >=c (and so a >=b) then a is max
jae lBnC ; other way c >= a and so lets comapre b and c

lBnC:
  mov ax, b
  cmp ax, c
  jbe GetRes ; if b >= c (and b is definitely >= a) then b is max
  mov ax, c ; else c >= c
  jmp GetRes

GetRes:
mov min, ax ; min is always in ax

mov ax, max
mov bx, min
mul bx
    
exit:
INT 21h
