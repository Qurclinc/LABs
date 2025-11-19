include 'emu8086.inc'

ORG 100h
    
    ; input text  
    mov ah, 0Ah
    lea dx, input_text
    int 21h
    
    CALL print_newline    
    
    ; save text length
    mov bl, [input_text + 1]
    mov [real_length], bx
    
    ; input gamma       
    mov ah, 0Ah
    lea dx, gamma
    int 21h
    
    CALL print_newline
    
    ; save gamma length
    mov bl, [gamma + 1]
    mov [gamma_len], bx
    
    ; encrypt
    lea si, input_text + 2  ; source text
    lea di, gamma + 2       ; gamma key
    lea bx, encrypted_text  ; destination
    call do_crypt
    
    ; printing it out
    mov ah, 09h
    lea dx, encrypt_label
    int 21h
     
    lea si, encrypted_text
    call PRINT_STRING 
    
    ; decrypt
    lea si, encrypted_text  ; source
    lea di, gamma + 2       ; gamma key
    lea bx, decrypted_text  ; destination
    call do_crypt
    
    CALL print_newline    
    
    ; printing it out
    mov ah, 09h
    lea dx, decrypt_label
    int 21h
    
    lea si, decrypted_text
    call PRINT_STRING
                     
INT 20h


do_crypt PROC
    mov cx, [real_length] ; length of text
    pusha                 ; saving all registers
    mov [gamma_start], di ; save original gamma pointer
    
while:
    mov al, [si]         ; source text symbol
    mov ah, [di]         ; gamma symbol
    
    cmp ah, 13           ; check if gamma ended up (noting there)
    jne restart       ; if its ended lets start from the beggining
    mov di, [gamma_start] ; reset gamma to start
    mov ah, [di]
        
restart:
    xor al, ah           ; encrypt/decrypt
    mov [bx], al         ; store result
    
    inc si               ; next text symbol
    inc di               ; next gamma symbol
    inc bx               ; next output byte
    dec cx               ; iterator
    cmp cx, 0            ; if its over - break
    je break
    jmp while
break:    
    popa
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




length         dw 255
real_length    dw ?
gamma_len      dw ?
gamma_start    dw ?

input_text     db 255, 0, 255 dup('$')
gamma          db 255, 0, 255 dup('$')
encrypted_text db length dup(0)
decrypted_text db length dup(0)

encrypt_label  db "Encrypted: ", '$'
decrypt_label  db "Decrypted: ", '$'

DEFINE_PRINT_STRING

