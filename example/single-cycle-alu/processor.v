/**
 * READ THIS DESCRIPTION!
 *
 * This is your processor module that will contain the bulk of your code submission. You are to implement
 * a 5-stage pipelined processor in this module, accounting for hazards and implementing bypasses as
 * necessary.
 *
 * Ultimately, your processor will be tested by a master skeleton, so the
 * testbench can see which controls signal you active when. Therefore, there needs to be a way to
 * "inject" imem, dmem, and regfile interfaces from some external controller module. The skeleton
 * file, Wrapper.v, acts as a small wrapper around your processor for this purpose. Refer to Wrapper.v
 * for more details.
 *
 * As a result, this module will NOT contain the RegFile nor the memory modules. Study the inputs 
 * very carefully - the RegFile-related I/Os are merely signals to be sent to the RegFile instantiated
 * in your Wrapper module. This is the same for your memory elements. 
 *
 *
 */
module processor(
    // Control signals
    clock,                          // I: The master clock
    reset,                          // I: A reset signal

    // Imem
    address_imem,                   // O: The address of the data to get from imem
    q_imem,                         // I: The data from imem

    // Dmem
    address_dmem,                   // O: The address of the data to get or put from/to dmem
    data,                           // O: The data to write to dmem
    wren,                           // O: Write enable for dmem
    q_dmem,                         // I: The data from dmem

    // Regfile
    ctrl_writeEnable,               // O: Write enable for RegFile
    ctrl_writeReg,                  // O: Register to write to in RegFile
    ctrl_readRegA,                  // O: Register to read from port A of RegFile
    ctrl_readRegB,                  // O: Register to read from port B of RegFile
    data_writeReg,                  // O: Data to write to for RegFile
    data_readRegA,                  // I: Data from port A of RegFile
    data_readRegB                   // I: Data from port B of RegFile
	 
	);

	// Control signals
	input clock, reset;
	
	// Imem
    output [31:0] address_imem;
	input [31:0] q_imem;

	// Dmem
	output [31:0] address_dmem, data;
	output wren;
	input [31:0] q_dmem;

	// Regfile
	output ctrl_writeEnable;
	output [4:0] ctrl_writeReg, ctrl_readRegA, ctrl_readRegB;
	output [31:0] data_writeReg;
	input [31:0] data_readRegA, data_readRegB;

	/* YOUR CODE STARTS HERE */

    // address
    // wire [31:0] pc, newPC;
    // wire pcovf;
    // dffe_ref addressLatch(.q(pc), .d(address_imem), .clk(clock), .en(1'b1), .clr(reset));
    // carry_look_ahead_32 pcAdder(.A(address_imem), .B(32'b1), .S(newPC), .overflow(pcovf), .Cin(1'b0));
    // assign address_imem = reset ? 32'b0 : newPC;
    wire [31:0] oldPC, newPC;
    wire pcovf;
    register addressReg(.clock(clock), .we(1'b1), .reset(1'b0), .dataWrite(newPC), .dataRead(oldPC));
    assign newPC = oldPC + 1;
    assign address_imem = reset ? 32'b0 : newPC;

    assign address_dmem = 32'b0;
    assign data = 32'b0;
    assign wren = 1'b0;

    // control signals
    wire [4:0] opcode, rd, rs, rt, shamt, aluop;
    wire [31:0] immediate;
    wire [26:0] target;

    assign opcode = q_imem[31:27];
	assign rd = q_imem[26:22];
    assign rs = q_imem[21:17];
    assign rt = q_imem[16:12];
    assign shamt = q_imem[11:7];
    assign aluop = (opcode == 5'b00101) ? 5'b00000: q_imem[6:2];

    //sign extend immediate
    assign immediate[16:0] = q_imem[16:0];
    assign immediate[31] = q_imem[16];
    assign immediate[30] = q_imem[16];
    assign immediate[29] = q_imem[16];
    assign immediate[28] = q_imem[16];
    assign immediate[27] = q_imem[16];
    assign immediate[26] = q_imem[16];
    assign immediate[25] = q_imem[16];
    assign immediate[24] = q_imem[16];
    assign immediate[23] = q_imem[16];
    assign immediate[22] = q_imem[16];
    assign immediate[21] = q_imem[16];
    assign immediate[20] = q_imem[16];
    assign immediate[19] = q_imem[16];
    assign immediate[18] = q_imem[16];
    assign immediate[17] = q_imem[16];

    assign target = q_imem[26:0];

    // R-type instructions
    wire [31:0] aluInputA, aluInputB, aluOutput;
    wire neq, ilt, ovf;

    assign aluInputA = data_readRegA;
    assign aluInputB = (opcode == 5'b00101 || opcode == 5'b00111 || 
                        opcode == 5'b01000 || opcode == 5'b00010 || 
                        opcode == 5'b00110) ? immediate : data_readRegB;

    // Reg file values
    assign ctrl_readRegA = rs;
    assign ctrl_readRegB = rt;
    assign ctrl_writeReg = rd;
    assign data_writeReg = aluOutput;
    assign ctrl_writeEnable = 1'b1; //temporary always on

    alu ALU(
        .data_operandA(aluInputA), 
        .data_operandB(aluInputB), 
        .ctrl_ALUopcode(aluop), 
        .ctrl_shiftamt(shamt), 
        .data_result(aluOutput), 
        .isNotEqual(neq), 
        .isLessThan(ilt), 
        .overflow(ovf)
    );

	/* END CODE */

endmodule
