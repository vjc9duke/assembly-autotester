module regfile (
	clock,
	ctrl_writeEnable, ctrl_reset, ctrl_writeReg,
	ctrl_readRegA, ctrl_readRegB, data_writeReg,
	data_readRegA, data_readRegB
);

	input clock, ctrl_writeEnable, ctrl_reset;
	input [4:0] ctrl_writeReg, ctrl_readRegA, ctrl_readRegB;
	input [31:0] data_writeReg;

	output [31:0] data_readRegA, data_readRegB;

	wire [31:0] readRegA, readRegB;
	wire [31:0] write_reg;

	//decode write and read registers
	
	// assign write_reg = ctrl_writeEnable ? write_reg : 32'b0;
	decoder32 read_decodeA(.out(readRegA), .select(ctrl_readRegA), .enable(1'b1));
	decoder32 read_decodeB(.out(readRegB), .select(ctrl_readRegB), .enable(1'b1));
	decoder32 write_reg_decode(.out(write_reg), .select(ctrl_writeReg), .enable(ctrl_writeEnable));
	// assign write_reg = 32'b1;

	genvar i;
	generate
		for (i = 1; i <= 31; i = i + 1) begin: loop1
			wire [31:0] regOut;
			register reg32(.clock(clock), .we(write_reg[i]), .reset(ctrl_reset), .dataWrite(data_writeReg), .dataRead(regOut));
			assign data_readRegA = readRegA[i] ? regOut : 32'bz; 
			assign data_readRegB = readRegB[i] ? regOut : 32'bz; 
		end
	endgenerate

	assign data_readRegA = readRegA[0] ? 32'b0 : 32'bz;
	assign data_readRegB = readRegB[0] ? 32'b0 : 32'bz;
endmodule
