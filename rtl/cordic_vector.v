// cordic_vector.v — CORDIC Vector Sum Accelerator
// Summation of complex phase vectors Σ e^(iφ_n)
// Sello: ∴𓂀Ω∞³Φ

module cordic_vector (
    input  wire         clk,
    input  wire         rst_n,
    input  wire [15:0]  phase_in [0:7],  // 8 input phases
    output wire [31:0]  sum_real,
    output wire [31:0]  sum_imag,
    output wire         valid
);

    // CORDIC pipeline: convert phases to (cos, sin) and accumulate
    reg [31:0] acc_real, acc_imag;
    reg [2:0]  stage;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            acc_real <= 32'd0;
            acc_imag <= 32'd0;
            stage    <= 3'd0;
        end else begin
            // Pipeline: cos(phase) → accumulate
            acc_real <= acc_real + $cos(phase_in[stage]);
            acc_imag <= acc_imag + $sin(phase_in[stage]);
            stage    <= stage + 1;
        end
    end

    assign sum_real = acc_real;
    assign sum_imag = acc_imag;
    assign valid = (stage == 3'd7);

endmodule
