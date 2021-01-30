`timescale 1ns / 1ps
`include "mac_manual.v"

module mac_manual_tb ();

    reg clk,rst,ce;
    reg [`N-1:0] a;
    reg [`N-1:0] b;
    reg [`N-1:0] c;
    wire [`N-1:0] p;
    integer ip_file,op_file,r3,r4,r5,r6;

mac_manual #(`N,`Q) a1(clk,rst,ce,a,b,c,p);

initial begin

$dumpfile("mac_manual_tb.vcd");
$dumpvars(0,mac_manual_tb);

a = 0;
b = 0;
clk = 0;
rst = 0;
ce = 0;
#50;

ip_file = $fopen("input.txt","r");
op_file = $fopen("output.txt","w");

rst = 1;

r3 = $fscanf(ip_file,"%b\n",a);
r4 = $fscanf(ip_file,"%b\n",b);
r5 = $fscanf(ip_file,"%b\n",c);
#50;
rst = 0;
ce = 1;
#50;
$fdisplay(op_file,"%b\n",p);

$display("test complete");
$fclose(ip_file);
$fclose(op_file);
$finish();
end
always #10 clk =~clk;
endmodule