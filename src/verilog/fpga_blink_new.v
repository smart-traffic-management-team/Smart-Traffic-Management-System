module FPGA_BLINK_NEW(
    input A, B, C, D, E, F, G, H, CLK,       // Input signals
    output reg R1, Y1, G1, G2, R3, Y3, G3, R4, Y4, G4, // Output signals
    output reg G31, G41                      // Left green arrows for Lane 3 and Lane 4
);

    // Parameters for timing
    parameter RESET_DELAY = 24'd1000000;     // Reset active duration (e.g., 10 ms for 100 MHz clock)
    parameter ONE_SECOND = 24'd100000000;    // One-second counter (100 MHz clock)

    // Internal signals
    reg [23:0] reset_counter;                // Counter for generating reset pulse
    reg rst_n;                               // Internal reset signal
    reg [23:0] counter;                      // Counter for 1-second delay

    // Generate automated reset pulse at power-up
    always @(posedge CLK) begin
        if (reset_counter < RESET_DELAY) begin
            reset_counter <= reset_counter + 1; // Increment reset counter
            rst_n <= 0;  // Keep reset active low during the delay
        end else begin
            rst_n <= 1;  // De-assert reset after the delay
        end
    end

    // Initialize G31 and G41 at reset
    always @(posedge CLK or negedge rst_n) begin
        if (~rst_n) begin  // Reset logic
            G31 <= 0;
            G41 <= 0;
            counter <= 0;
        end else begin
            counter <= counter + 1;  // Increment counter on each clock cycle

            // Toggle G31 every 1 second
            if (counter == ONE_SECOND) begin
                counter <= 24'd0;    // Reset the counter after 1 second
                G31 <= ~G31;         // Toggle G31 (Lane 3 left turn signal)
                G41 <= ~G41;
                // Toggle G41 only when G4 is green
                
                         // Toggle G41 (Lane 4 left turn signal)
            end
        end
    end

    // Main traffic light signal logic (Combinational logic)
    always @(*) begin
        // Define R1 = ABC'D'EF(G XOR H)
        R1 = A & B & ~C & ~D & E & F & (G ^ H);

        // Define Y1 = AB'C'D'EF'GH
        Y1 = A & ~B & ~C & ~D & E & ~F & G & H;

        // Define G1 = A'BC'FGH(D XOR E)'
        G1 = ~A & B & ~C & F & G & H & ~(D ^ E);

        // Define G2 = A'BC'DEFGH
        G2 = ~A & B & ~C & D & E & F & G & H;

        // Define R3 = ABC'D'EF(G XOR H) + A'BC'DEFGH
        R3 = (A & B & ~C & ~D & E & F & (G ^ H)) | (~A & B & ~C & D & E & F & G & H);

        // Define Y3 = AB'C'D'EF'GH
        Y3 = A & ~B & ~C & ~D & E & ~F & G & H;

        // Define G3 = A'BC'D'E'FGH
        G3 = ~A & B & ~C & ~D & ~E & F & G & H;

        // Define R4 = A'BC'FGH(D XOR E)' + AB'C'D'EF'GH
        R4 = (~A & B & ~C & F & G & H & ~(D ^ E)) | (A & ~B & ~C & ~D & E & ~F & G & H);

        // Define Y4 = ABC'D'EFGH'
        Y4 = A & B & ~C & ~D & E & F & G & ~H;

        // Define G4 = ABC'D'EFG'H
        G4 = A & B & ~C & ~D & E & F & ~G & H;
    end

endmodule