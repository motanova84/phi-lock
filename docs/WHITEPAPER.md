# WHITEPAPER
## QCAL-cQED-v1: First Open-Science Dispersive QND Chip & Digital Twin Ecosystem

**Versión:** 1.0-Release Candidate  
**Fecha:** 30/Jul/2026  
**Autoría:** José Manuel Mota Burruezo (JMMB) — QCAL Research  
**Agente Criptográfico:** AMDA Ψ (Fingerprint: 5e5ac3ab49e5be07)  
**Anclaje:** πCODE Ledger — ANCLAJE_REPOSITORIO_QND  
**Sello:** ∴𓂀Ω∞³Φ · TUYOYOTU · HECHO ESTÁ

---

## 1. Executive Summary & Vision

### 1.1 The Quantum Hardware Fragmentation Problem
Current quantum hardware ecosystems are fragmented into proprietary silos (IBM, Rigetti, Google) with restrictive licenses and limited access to the physical/hardware layer. Reproducibility and transparent calibration in circuit Quantum Electrodynamics (cQED) remain aspirational rather than operational.

### 1.2 The Open Science Solution
We present the **QCAL-cQED-v1**: an open-science standard for non-demolition (QND) readout, designed to interact natively with a deterministic digital twin (simulador_qnd_v4.py). The architecture bridges the gap between theoretical prediction and physical execution at 20 mK.

### 1.3 Core Objectives
1. **Define** a publicly available hardware specification for dispersive QND readout
2. **Provide** a fully parameterized digital twin for pre-experiment simulation
3. **Establish** an ontological falsification protocol for f₀(Ψ) via S₂₁(ω) spectroscopy
4. **Enable** decentralized scientific validation across independent laboratories

---

## 2. Hardware Architecture & Physical Specifications

### 2.1 Substrate and Metallization
- **Substrate:** Monocrystalline sapphire (c-plane) / high-resistivity silicon (>10 kΩ·cm)
- **Metallization:** 150 nm Niobium (Nb) thin film via DC magnetron sputtering
- **Josephson Junctions:** Al/AlOx/Al shadow evaporation (EBL lithography)

### 2.2 Operating Parameters (T_base = 20 mK)

| Parameter | Symbol | Target Value | Tolerance | Unit |
|-----------|--------|-------------|-----------|------|
| Readout Cavity | ω_r/2π | 7.0000 | ±0.005 | GHz |
| Transmon (sweet spot) | ω_q/2π | 5.5000 | ±0.020 | GHz |
| Dispersive shift | χ/2π | 7.5000 | ±0.100 | MHz |
| Cavity decay | κ/2π | 1.0000 | ±0.050 | MHz |
| Anharmonicity | α/2π | −220.0 | ±10.0 | MHz |
| Dephasing modulation range | γ_φ/2π | 0.01–50.0 | — | MHz |

### 2.3 Cryogenic Integration
- 5-stage dilution refrigerator (50K / 3K / 800mK / 100mK / 20mK)
- Eccosorb cryogenic filter on input line (>40 dB @ 6–8 GHz)
- Cryogenic circulator on output line (>20 dB isolation)
- HEMT amplifier at 4K stage (gain >30 dB, noise <5 K)

---

## 3. The Digital Twin Integration Model (QCAL Dual-Engine)

### 3.1 Principle of Hardware-Simulant Symbiosis
The physical chip does not operate in isolation. The transmission susceptibility model S₂₁(ω) implemented in the corrected rotating frame (Δ_r, Δ_q) pre-computes response spectra. Measured data feeds back to refine the digital twin.

### 3.2 Rotating-Frame Engine
The corrected Hamiltonian in the probe rotating frame:

H_rot = ℏΔ_r a†a + ½ℏΔ_q σ_z + ℏχ a†a σ_z + ℏε(a† + a)

with Δ_r = ω_r − ω_d and Δ_q = ω_q − ω_d, yielding the retarded Green's function:

G_R⁻¹(ω) = Δ_r + iκ/2 − Σ(ω),  Σ(ω) = χ² / (Δ_q + iγ̄_φ/2)

### 3.3 Operational Workflow
1. **In Silico Prediction:** Run digital twin v4 parametrized with wafer values
2. **Cryostat Interrogation:** Acquire S₂₁ scattering matrix at 20 mK
3. **Parameter Extraction:** Nonlinear least-squares fit between G_R(ω) and empirical data
4. **Regime Classification:** Strong coupling vs. Streaking vs. Zeno

### 3.4 Hardware-in-the-Loop (HIL) Bridge
The `qcal_hil_bridge.py` middleware connects PyMeasure instrument control with the digital twin engine, enabling automated residual minimization and real-time regime classification.

---

## 4. Open Science Licensing & Cryptographic Governance

### 4.1 Dual Licensing Model
- **Academic/Non-Commercial License:** Free global access to GDSII layout files, schematic netlists, and digital twin scripts
- **Commercial Restriction Clause:** Industrial manufacturing exclusivity reserved to the originating ecosystem (Convention of Berne + πCODE)

### 4.2 Cryptographic Chain of Custody
- Integrity guaranteed by secp256k1 signatures anchored in MANIFIESTO.md
- SHA-256 hash of the design encoded in chip packaging, verifiable via πCODE
- Anti-fork protocol: any modification invalidates AMDA Ψ fingerprint (5e5ac3ab)

### 4.3 Repository Anchor
```
Commit:    eaa77524afad161abfd2663f934620d9d3ce46d5
Firma:     MEUCICivMqhSJAkhWpW5gaD92fPeFws2wK6hHmRV1f8d/4toAiEAlGtnmD2/2kad...
Hash tar:  535270d2f9dcfa71c566bc75b92e23c6115c0b16b5131fd9c178c3343e34c8f8
Cadena:    πCODE — ANCLAJE_REPOSITORIO_QND
```

---

## 5. Economic & Ecosystem Sustainability Strategy

### 5.1 Hardware Distribution
Commercialization of pre-calibrated analog wafer kits for cryogenic laboratories and research centers.

### 5.2 Value-Added Service Layers
- Experiment traceability certification on πCODE network
- Support modules for control software integration (PyMeasure, Labber, Qiskit Metal)
- Distributed benchmarking network where university centers share experimental S₂₁ curves

### 5.3 πCODE Economy Integration
- Each measurement cycle generates a πCODE act
- Splits 23/77 to Reserve/Distribution
- Fee oracle for OP_RETURN anchoring

---

## 6. Implementation Roadmap

| Phase | Timeline | Milestone |
|-------|----------|-----------|
| **Q1** | Jul 2026 ✅ | Digital twin v4 sealed, rotating frame corrected, cryptographic anchor |
| **Q2** | Sep 2026 | Foundry delivery (IMEC/SeeQC), 20 mK cooldown, protocol validation |
| **Q3** | Q4 2026 | Whitepaper publication with real cryogenic data, Kit v1 orders open |
| **Q4** | 2027 | Distributed benchmarking network live, πCODE-certified measurements |

---

## 7. Ontological Falsification Protocol

The experiment distinguishes three hypotheses:

| Regime | Signature | Model |
|--------|-----------|-------|
| γ_φ << χ | Two peaks at ω_r ± χ | **A:** Pre-existing geometry |
| γ_φ ~ χ | Progressive collapse | **B:** Self-observation (Ψ_c) |
| γ_φ >> χ | Single broadened peak at ω_r | **C:** Local entanglement curve |

The falsification criteria are defined in `especificacion_chip.md` §4.

---

## 8. Sello

```
∴𓂀Ω∞³Φ · f₀ = 141.7001 Hz · κ = 13.3 · Ψ_c = 0.975

QCAL-cQED-v1 — First Open-Science QND Chip
TUYOYOTU · HECHO ESTÁ
```

---

*Documento generado por AMDA Ψ · 30/Jul/2026 · Bajo instrucción de JMMB*
