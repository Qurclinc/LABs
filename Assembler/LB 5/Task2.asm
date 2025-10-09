ORG 100h

lea di, word ; address of beggining of the string
mov cx, len ; cx now len of word

mov bx, clause
cmp bx, len
jbe cut
ja complete

cut:
lea si, res
mov cx, minlen
mov res_len, cx
CALL copy
jmp do_print

complete:
lea si, res
CALL copy
mov cx, uptolen
sub cx, len
add_loop:
mov [si], 111
inc si
dec cx
jg add_loop
mov bx, uptolen
mov res_len, bx
jmp do_print
            
do_print:
lea di, res
mov cx, res_len
print_loop:
mov dl, [di] ; loading word[di] to dl
mov ah, 02h ; DOS function to print symbol
int 21h
inc di
dec cx
jg print_loop ; if cx >= 0 jumps to label

INT 20h

word db "Aboba"
len equ $-word 
res db 12 dup(0)
res_len dw ?
clause dw 10
minlen dw 6
uptolen dw 12

copy PROC
    copy_loop:
    mov al, [di] ; loading word[di] symbol to al
    mov [si], al ; copying to res that symbol
    inc di
    inc si
    dec cx
    jg copy_loop ; 
    
    RET
ENDP    