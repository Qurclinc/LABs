ORG 100h

mov ax, m 
mov bx, 60 
mul bx 
mov m, ax 
mov cx, N 

mov ax, result 
mov bx, m 

while: 
cmp cx, 0 
je break
add ax, bx 
add bx, delta 

loop while 
break:    

mov bx, 60 
div bx 

cmp dx, 0 
je finish
add ax, 1 

finish:
mov result, ax 
INT 20h

N dw 3 
m dw 1 
delta dw 10 
result dw ? 
