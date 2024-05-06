nop             # Misc memory tests
nop             # Tests several memory edge cases
nop             # Author: Vincent Chen
nop             
nop
addi $r1, $r0, 10
addi $r2, $r0, 20
sw $r1, 5($r0)      # WX bypassing
sw $r2, 6($r0)      # WX bypassing
nop
nop
md:                 # [SECTION] multdiv following lw
lw $r3, 5($r0)      # [CHECK] r3 should be 10 (WX bypassing on previous sw)
lw $r4, 6($r0)      # [CHECK] r4 should be 20 (WX bypassing on previous sw)
mul $r6, $r3, $r4   # [CHECK] r6 should be 200
nop
lw $r7, 5($r0)
lw $r8, 6($r0)
div $r9, $r8, $r7   # [CHECK] r9 should be 2
nop
nop
lwsw:               # [SECTION] various lw/sw bypassing tests
lw $r10, 5($r0)     # lw -> sw rd bypassing
sw $r10, 7($r0)
lw $r11, 7($r0)     # [CHECK] r11 should be 10
nop
lw $r12, 6($r0)     # lw -> sw rs bypassing
sw $r1, 0($r12)
lw $r13, 20($r0)    # [CHECK] r13 should be 10
nop
sw $r1, 8($r0)      # sw -> sw rd no bypassing
sw $r1, 9($r0)
nop
nop
nop
lw $r14, 8($r0)     # [CHECK] r14 should be 10
lw $r15, 9($r0)     # [CHECK] r15 should be 10
nop
nop
sw $r2, 10($r0)
lw $r16, 5($r0)     # lw -> lw rd -> rs bypassing 
lw $r17, 0($r16)    # [CHECK] r17 should be 20
nop
nop
lw $r18, 6($r0)     # lw -> lw rd -> rd no bypassing 
lw $r18, 5($r0)     # [CHECK] r18 should be 10
nop
nop