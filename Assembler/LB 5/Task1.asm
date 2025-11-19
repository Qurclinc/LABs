ORG 100h

mov si, 0 ; iterating from the beggining (index 0); indexes at all
mov cx, 0 ; counter for iterating
mov ax, arr[si]
mov min, ax

for:
cmp cx, len
je break
mov ax, arr[si]
add cx, 1 ; incrementing
add si, 2 ; we add 2 as dw means 2 bytes 
cmp ax, min
jbe change_min ; if arr[si] <= min then min = arr[si]
jmp for       
       
change_min:
mov min, ax
jmp for

break:
mov ax, min

INT 20h

arr dw 14,20,30,10,5,78,52,11,30 ; array itself :p
len dw $-arr ; len of arr
min dw ?