ORG 100h ; start


a dw 10
b dw 20
avg dw ?
ax2 dw ?
bx2 dw ?
avgx2 dw ? ; memory allocation

mov ax, a 
mov bx, b
mov cl, 2
add ax,bx
div cl
mov [avg], ax ; finding 'n' saving avg

mov ax, a
mov bx, a
mul bx
mov [ax2], ax ; a * a

mov ax, b
mov bx, b
mul bx
mov [bx2], ax ; b * b

mov ax, ax2
mov bx, bx2
add ax,bx
div cl
mov [avgx2], ax ; finding 'n' saving square avg

mov ax, [avg]
mov bx, [avgx2] ; print result

int 21h ; end