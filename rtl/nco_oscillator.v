// nco_oscillator.v — Numerically Controlled Oscillator
// Φ-LOCK: f₀ = 141.7001 Hz phase accumulator
// Sello: ∴𓂀Ω∞³Φ

module nco_oscillator (
    input  wire        clk,          // system clock (MHz)
    input  wire        rst_n,        // async reset (active low)
    input  wire [31:0] phase_inc,    // phase increment for f₀
    output wire [15:0] phase_out,    // current phase
    output wire        sync_pulse    // sync at phase wrap
);

    reg [31:0] phase_acc;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            phase_acc <= 32'd0;
        else
            phase_acc <= phase_acc + phase_inc;
    end

    assign phase_out = phase_acc[31:16];
    assign sync_pulse = (phase_acc == 32'd0) ? 1'b1 : 1'b0;

endmodule
