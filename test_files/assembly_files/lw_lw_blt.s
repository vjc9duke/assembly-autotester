nop            # Specifically tests two lws into blt
nop            # Author: Philip Xue
nop
nop            # EDGE CASE: lw -> lw -> blt
nop            # blt depends on both lw values
addi $1, $0, 830        # r1 = 830
nop
nop
addi $2, $0, 831        # r2 = 831
nop
nop
sw $1, 0($0)  # mem[0] = r1 = 830
sw $2, 1($0)  # mem[1] = r2 = 831
nop
nop
lw $4, 1($0)  # r4 = mem[1] = 831
lw $3, 0($0)  # r3 = mem[0] = 830
blt $3, $4, skip1  # branch should be taken
nop
nop
addi $7, $0, 1  # This line should never be reached
skip1:
lw $5, 0($0)  # r5 = mem[0] = 830
lw $6, 1($0)  # r6 = mem[1] = 831
blt $5, $6, skip2  # branch should be taken
nop
nop
addi $7, $0, 2  # This line should never be reached
skip2: