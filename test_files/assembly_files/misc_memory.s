nop             # Misc memory tests
nop             # Tests several memory edge cases
nop             # Author: Vincent Chen
nop             
nop
addi $r1, $r0, 10
addi $r2, $r0, 20
sw $r1, 5($r0)      # setup: puts 10 into memory address 5
sw $r2, 6($r0)      # setup: puts 20 into memory address 6
nop
nop
md:                 # [SECTION] multdiv following lw
lw $r3, 5($r0)      # [CHECK] r3 should be 10 (WX bypassing)
lw $r4, 6($r0)      # [CHECK] r4 should be 20 (WX bypassing)
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
lw $r13, 20($r0)     # [CHECK] r13 should be 10
nop
