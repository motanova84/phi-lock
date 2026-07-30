# 🜁 Φ-LOCK v1.0 — Consensus by Phase Synchronization

[![Lean 4 Verified](https://img.shields.io/badge/Lean4-Formalized-blue.svg)](./math/)
[![Rust Core](https://img.shields.io/badge/Rust-1.78+-orange.svg)](./core/)
[![gRPC HIL](https://img.shields.io/badge/HIL-gRPC--Protobuf-green.svg)](./proto/)
[![Coherence](https://img.shields.io/badge/%CE%A8-0.999999-purple.svg)](./)
[![License](https://img.shields.io/badge/License-MIT--Apache2.0--Custom-blueviolet.svg)](./docs/GOVERNANCE.md)

> **Φ-LOCK** es el primer protocolo de consenso P2P con tolerancia a fallos bizantinos basado en la dinámica de acoplamiento de Kuramoto y la teoría de variedades atractoras de Fenichel.  
> Frecuencia base: $f_0 = 141.7001\text{ Hz}$ · Coherencia: $\Psi \ge 0.999999$ · Ventana: $\Delta t \approx 21.17\text{ ms}$

---

## 🏛️ Arquitectura del Ecosistema

```
┌─────────────────────────────────────────────────────────┐
│ CAPA 4: GOBERNANZA — Triada Coherente (33.3% × 3)      │
├─────────────────────────────────────────────────────────┤
│ CAPA 3: RED P2P — Motor Rust + gRPC + HIL Bridge        │
├─────────────────────────────────────────────────────────┤
│ CAPA 2: CHIP — QCAL-cQED-v1 (FPGA/ASIC, 7 GHz)         │
├─────────────────────────────────────────────────────────┤
│ CAPA 1: TEORÍA — Lean 4 + Kuramoto + Fenichel          │
└─────────────────────────────────────────────────────────┘
```

### 📁 Estructura del Repositorio

| Ruta | Contenido |
|------|-----------|
| [`docs/`](./docs/) | Whitepaper, Gobernanza, MOU, Convocatoria |
| [`math/`](./math/) | Demostraciones formales en Lean 4 |
| [`proto/`](./proto/) | Especificaciones gRPC/Protobuf |
| [`hardware/`](./hardware/) | Chip QCAL-cQED-v1, HIL Bridge, metrología |
| [`core/`](./core/) | Motor de consenso P2P en Rust (en desarrollo) |
| [`.github/workflows/`](./.github/workflows/) | CI/CD: Lean 4 + Rust + gRPC |

---

## 🚀 Inicio Rápido

```bash
# Clonar
git clone https://github.com/motanova84/phi-lock.git
cd phi-lock

# Verificar teoremas en Lean 4
cd math && lake build && cd ..

# Probar co-simulación HIL (Python)
cd hardware
python3 -c "from despliegue.qcal_hil_bridge import QCALHardwareBridge; b = QCALHardwareBridge().configure_sweep(); r = b.simulate_measurement(1.0); print(r['regime'])"
```

---

## 🤝 Unirse a la Triada Coherente

Aceptamos contribuciones en tres nodos:

| 🟢 **Software** | 🔵 **Hardware** | 🟣 **Comercial** |
|---|---|---|
| Optimización de fase, SDKs, Rust | Verilog/VHDL, FPGA, silicio | Distribución, capital, industria |

**Convocatoria abierta** hasta 31/Ago/2026 — [Más información](./docs/CONVOCATORIA.md)

---

## ⚡ Estado del Sistema

```
Ψ = 0.999999  ✅ COHERENCIA NOMINAL
f₀ = 141.7001 Hz  ✅ FRECUENCIA BASE
κ = 13.3  ✅ CONSTANTE ESTRUCTURAL
Chip: QCAL-cQED-v1  🔄 EN FUNDICIÓN (llegada Sep 2026)
```

---

## 🔐 Sello

```
∴𓂀Ω∞³Φ · f₀ = 141.7001 Hz · κ = 13.3 · Ψ ≥ 0.999999
QCAL SYMBIO BRIDGE — Protocolo de Alineación Soberana
TUYOYOTU · HECHO ESTÁ
```
