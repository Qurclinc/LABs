ORG 100h ; start

mov ax, 2025 ; current year
mov bx, 2005 ; birth year

sub ax,bx           
mov bx, 365 ; 365 days in a year
mul bx
           
INT 21h ; end