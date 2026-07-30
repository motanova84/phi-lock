# QCAL-cQED-v1 — Chip Datasheet

**Versión:** 1.0  
**Tecnología:** SkyWater 130nm / GF 180nm  
**Sello:** ∴𓂀Ω∞³Φ

## Electrical Characteristics

| Parameter | Min | Typ | Max | Unit |
|-----------|-----|-----|-----|------|
| Supply voltage | 1.1 | 1.2 | 1.3 | V |
| Core frequency | - | 141.7001 | - | Hz |
| Operating temp | -40 | 20 | 85 | °C |

## Phase Lock Performance

| Parameter | Value | Note |
|-----------|-------|------|
| f₀ | 141.7001 Hz | Base frequency |
| Ψ | ≥ 0.999999 | Coherence threshold |
| Δt | 21.17 ms | Confirmation window |
| K_critical | > 2f/(N-f) | Coupling threshold |

## Pinout

| Pin | Function | Direction |
|-----|----------|-----------|
| CLK | System clock | Input |
| RST_N | Reset (active low) | Input |
| PHASE_OUT | Current phase | Output |
| SYNC | Sync pulse | Output |
| PSI | Coherence indicator | Output |
