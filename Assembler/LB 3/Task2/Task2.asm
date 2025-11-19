ORG 100h

mov cx, 1 ; initializing iterator      
for:
cmp cx, N ; if cx (iterator) equal to N so we're done
je exit      
jne do_check ; other way we should check this value

do_check: ; we have to compare dx to 0 for cx and 2,3,5
mov ax, cx
mov bx, 2 ; does number % 2 == 0 ?
div bx
cmp dx, 0
je wrong

mov dx, 0
mov ax, cx
mov bx, 3 ; does number % 3 == 0 ?
div bx
cmp dx, 0
je wrong

mov dx, 0
mov ax, cx
mov bx, 5 ; does number % 5 == 0 ?
div bx
cmp dx, 0
je wrong

; and if for now we're still here we can increase value of k
mov dx, 0
mov ax, k
add ax, 1
mov k, ax ; saving to k incremented value
add cx, 1 ; and increasing iterator
jmp for


wrong: ; if number % (2,3,5) == 0 we can skip it
add cx, 1
jmp for

exit:
mov ax, k
       
INT 20h

N dw 20
k dw 0




















mov ax, bx 
    pop cur ; testing for 2
    div cur
    cmp dx, 0