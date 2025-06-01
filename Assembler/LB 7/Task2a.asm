ORG 100h
    
    ; input text  
    mov ah, 0Ah ; 0Ah - instruction to enter a line
    lea dx, input_text ; and it has to be into dx
    INT 21h            ; summons console 
    
    CALL print_newline    
    
    mov bx, 0 ; for safety
    mov bl, [input_text + 1]
    mov real_length, bx
    mov bx, 0 ; for safety
           
    ; input gamma       
    mov ah, 0Ah
    lea dx, gamma ; and it has to be into dx
    INT 21h            ; summons console 
    
    CALL print_newline
    
    lea di, gamma + 2
    CALL bin_to_dec ; translate to dec to correct XOR
    
    ; encrypting
    lea di, input_text + 2
    lea si, encrypted_text
    CALL do_crypt
    
    ; printing it out       
    mov ah, 09h ; 09h - instruction to print out line
    lea dx, encrypt_label
    INT 21h
    
    mov ah, 09h
    lea dx, encrypted_text
    INT 21h
    
    ; decrypting
    lea di, encrypted_text ; source text uwu
    lea si, decrypted_text ; res text x_x
    CALL do_crypt
    
    CALL print_newline    
    
    ; printing it out       
    mov ah, 09h ; 09h - instruction to print out line
    lea dx, decrypt_label
    INT 21h
    
    mov ah, 09h
    lea dx, decrypted_text
    INT 21h
                     

INT 20h

bin_to_dec proc  
    lea si, gamma + 1  ; here stores current length
    mov cl, [si] ; actual length of gamma!
    mov ax, 0  ; initial zero
    mov ch, 2  ; for multiplying
for:
    mov bl, [di] ; current symbol
    dec cl ; counter  
    
    cmp bl, '1' ; if bit == 1 lets add it :p other way no. :(
    je add_one
    jne dont_add_one
    
add_one:
    add ax, 1
dont_add_one:
    cmp cl, 0 ; if len is 0 we shouldn't *2
    je stop
    mul ch  ; *2 for each bit
    inc di ; go to next symbol
    
    jmp for     
stop: 
    mov cl, al ; saving to cl got decimal number  
    RET
ENDP

do_crypt proc
    mov bx, real_length
while:
    mov al, [di] ; byte from di
    cmp bx, 0  ; if line is over - break :)
    je break     
    
    xor al, cl   ; just XOR. nothing interesting :O
    

    mov [si], al ; now in al swapped bits so lets clone them into si
    inc di       ; simple increment for getting further
    inc si       ; OwO
    dec bx
    jmp while    ; do it until its done w_w

break:
    mov byte ptr [si], '$' ; adding marker that line is finished
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
gamma             db 8, 0, 8 dup('$')
input_text        db 255, 0, 255 dup('$')
encrypted_text    db length dup('$')
decrypted_text    db length dup('$')
encrypt_label     db "Encrypted: ", '$'
decrypt_label     db "Decrypted: ", '$'