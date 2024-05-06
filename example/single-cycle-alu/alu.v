module alu(data_operandA, data_operandB, ctrl_ALUopcode, ctrl_shiftamt, data_result, isNotEqual, isLessThan, overflow);
        
    input [31:0] data_operandA, data_operandB;
    input [4:0] ctrl_ALUopcode, ctrl_shiftamt;

    output [31:0] data_result;
    output isNotEqual, isLessThan, overflow; 

    wire [2:0] adjusted_opcode;
    assign adjusted_opcode[0] = ctrl_ALUopcode[0];
    assign adjusted_opcode[1] = ctrl_ALUopcode[1];
    assign adjusted_opcode[2] = ctrl_ALUopcode[2];


    wire [31:0] add_s;
    assign add_s = data_operandA + data_operandB;

    wire [31:0] sub_s;
    assign sub_s = data_operandA - data_operandB;

    // selector for overflow
    assign overflow = 1'b0;

    wire [31:0] and_res, or_res, sll_res, sra_res;
    assign and_res = data_operandA & data_operandB;
    assign or_res = data_operandA | data_operandB;
    assign sll_res = data_operandA << ctrl_shiftamt;
    assign sra_res = $signed(data_operandA) >>> ctrl_shiftamt;

    // selector for data_result
    mux_8 data_mux(.out(data_result), .in0(add_s), .in1(sub_s), .in2(and_res), .in3(or_res), .in4(sll_res), .in5(sra_res), .in6(32'b0), .in7(32'b0), .select(adjusted_opcode));

endmodule