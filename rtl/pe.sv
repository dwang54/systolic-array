// pe.sv — Processing element for an output-stationary systolic array.
//
// Each cycle with en=1:
//   acc   <= (clear ? 0 : acc) + a_in * b_in
//   a_out <= a_in   (forwarded to the PE on the right)
//   b_out <= b_in   (forwarded to the PE below)
// en=0 holds all state. clear without en zeroes acc.
// See docs/spec.md §3 for how PEs are tiled into the array.

module pe #(
  parameter int DATA_W = 8,   // signed operand width
  parameter int ACC_W  = 32   // signed accumulator width (see docs/decisions.md D2)
) (
  input  logic                     clk,
  input  logic                     rst_n,   // async, active-low
  input  logic                     en,      // advance one step
  input  logic                     clear,   // start a new accumulation
  input  logic signed [DATA_W-1:0] a_in,
  input  logic signed [DATA_W-1:0] b_in,
  output logic signed [DATA_W-1:0] a_out,
  output logic signed [DATA_W-1:0] b_out,
  output logic signed [ACC_W-1:0]  acc
);

  logic signed [2*DATA_W-1:0] prod;
  logic signed [ACC_W-1:0]    prod_ext;
  logic signed [ACC_W-1:0]    acc_base;

  assign prod     = a_in * b_in;
  // Explicit sign extension (avoids relying on context-dependent extension rules).
  assign prod_ext = {{(ACC_W-2*DATA_W){prod[2*DATA_W-1]}}, prod};
  assign acc_base = clear ? '0 : acc;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      a_out <= '0;
      b_out <= '0;
      acc   <= '0;
    end else if (en) begin
      a_out <= a_in;
      b_out <= b_in;
      acc   <= acc_base + prod_ext;
    end else if (clear) begin
      acc   <= '0;
    end
  end

endmodule
