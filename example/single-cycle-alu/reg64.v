module reg64 (clock, we, reset, dataWrite, dataRead);
	input clock, we, reset;
    input [63:0] dataWrite; 
	output [63:0] dataRead;

	genvar i;
	generate
		for (i = 0; i < 64; i = i + 1) begin: loop1
			dffe_ref d_flip_flop(.q(dataRead[i]), .d(dataWrite[i]), .clk(clock), .en(we), .clr(reset));
		end
	endgenerate
endmodule
