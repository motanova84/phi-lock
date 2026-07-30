# OpenLane Flow — QCAL-cQED-v1 Synthesis

**Estado:** Preparación de flujo  
**Target GDSII:** QCAL-cQED-v1  
**Technology:** SkyWater 130nm / GF 180nm  

## Pasos

1. Síntesis RTL: `make synth`
2. Floorplanning: `make floorplan`
3. Placement: `make place`
4. Routing: `make route`
5. GDSII: `make gdsii`

## Requisitos

- OpenLane v2.x
- Docker
- Python 3.11+

## Archivos

- `rtl/nco_oscillator.v` — NCO phase accumulator
- `rtl/cordic_vector.v` — CORDIC vector sum
- `rtl/kuramoto_coupler.v` — Kuramoto coupling matrix

---

*Sello: ∴𓂀Ω∞³Φ · TUYOYOTU · HECHO ESTÁ*
