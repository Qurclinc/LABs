ORG 100h
    
    push X0 ; as we get X0 damaged during crypt we need to save it
    pop X0_backup ; uwu
    
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
    ;mov ah, 0Ah
    ;lea dx, gamma ; and it has to be into dx
    ;INT 21h            ; summons console 
    
    ;CALL print_newline
    
    ;lea di, gamma + 2
    ;CALL bin_to_dec ; translate to dec to correct XOR
    
    ; encrypting
    lea di, input_text + 2
    lea si, encrypted_text
    CALL do_crypt
    
    ; adding '$' as it got damaged (somewhy...)
    lea di, encrypted_text ; string
    add di, real_length ; len(string) + 1 sym should be '$'
    mov byte ptr [di], '$'  ; and its done
    
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
                     
stop_it:
INT 20h

do_crypt proc
    push X0_backup
    pop X0    
while:
    ; lets find some gamma xD
    push X0
    pop X
    mov ax, a
    mul X
    add ax, c
    div m
    mov X0, dx ; X0 overwritten for countingsequence
     
    ; now its decimal anyway SOO its even easier!
    mov al, [di] ; byte from di
    cmp al, '$'  ; if line is over - break :)
    je break     
    
    xor al, dl   ; just XOR. nothing interesting :O
    

    mov [si], al ; now in al swapped bits so lets clone them into si
    inc di       ; simple increment for getting further
    inc si       ; OwO
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

m                 dw 90
a                 dw 25
c                 dw 55
X0                dw 10
X0_backup         dw ?
X                 dw ?