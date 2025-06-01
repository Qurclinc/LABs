include 'emu8086.inc'

ORG 100h
      
    mov ah, 0Ah ; 0Ah - instruction to enter a line
    lea dx, input_text ; and it has to be into dx
    INT 21h            ; summons console 
    
    CALL print_newline
    
    mov bx, 0 ; for safety
    mov bl, [input_text + 1]
    mov real_length, bx
    mov bx, 0 ; for safety
                 
    ; encrypting             
    lea di, input_text + 2 ; source text uwu
    lea si, encrypted_text ; res text x_x
    CALL do_crypt       
           
    ; printing it out       
    mov ah, 09h ; 09h - instruction to print out line
    lea dx, encrypt_label
    INT 21h
    
    lea si, encrypted_text
    CALL PRINT_STRING
    
    ; decrypting
    lea di, encrypted_text ; source text uwu
    lea si, decrypted_text ; res text x_x
    CALL do_crypt
    
    CALL print_newline    
    
    ; printing it out       
    mov ah, 09h ; 09h - instruction to print out line
    lea dx, decrypt_label
    INT 21h
    
    
    lea si, decrypted_text
    CALL PRINT_STRING
                     

    

INT 20h

do_crypt proc
    mov cx, real_length
while:
    mov al, [di] ; byte from di
    cmp cx, 0  ; if line is over - break :)
    je break

    mov bl, al   ; copy symbol to bl and bh
    mov bh, al   ; to make bit operations $_$
    and bl, 00000010b ; saving only 1st bit -_-
    and bh, 00001000b ; saving only 3rd bit :0
    shl bl, 2 ; moving 1st bit to 3rd pos        
    shr bh, 2 ; moving 3rd bit to 1st pos and now its swapped 0_0         
    and al, 11110101b ; erasing 1st and 3rd bits saving others
    or al, bl         ; injecting 3rd bit into source sequence
    or al, bh         ; injecting 1st bit into source sequence

    mov bl, al        ; another one copy and overwriting
    mov bh, al        ; ^~^
    and bl, 00010000b ; saving 4th bit 
    and bh, 10000000b ; saving 7th bit 
    shr bh, 3         ; swapping them 
    shl bl, 3         ; ^^"
    and al, 01101111b ; erasing 4th and 7th bits to replace them 
    or al, bl         ; same way
    or al, bh          

    mov [si], al ; now in al swapped bits so lets clone them into si
    inc di       ; simple increment for getting further
    inc si       ; OwO
    dec cx
    jmp while    ; do it until its done w_w

break:
    RET
ENDP

 
print_newline PROC   
    
    mov dl, 0Dh ; carrige return
    mov ah, 02h
    INT 21h
    
    mov dl, 0Ah   ; new line
    mov ah, 02h
    INT 21h
    RET
ENDP

real_length       dw ?
length            dw 255
input_text        db 255, 0, 255 dup('$')
encrypted_text    db length dup(0???)
decrypted_text    db length dup(0)
encrypt_label     db "Encrypted: ", '$'
decrypt_label     db "Decrypted: ", '$'


DEFINE_PRINT_STRING