# 🜁 Φ-LOCK v1.1 — Consensus by Phase Synchronization

[![Lean 4 Verified](https://img.shields.io/badge/Lean4-Formalized-blue.svg)](./math/)
[![Rust Firmware](https://img.shields.io/badge/Rust-Embedded--no__std-orange.svg)](./firmware/)
[![Verilog RTL](https://img.shields.io/badge/RTL-Verilog-success.svg)](./rtl/)
[![gRPC HIL](https://img.shields.io/badge/HIL-gRPC--Protobuf-green.svg)](./proto/)
[![Coherence](https://img.shields.io/badge/%CE%A8-0.999999-purple.svg)](./)
[![License](https://img.shields.io/badge/License-MIT--Apache2.0--Custom-blueviolet.svg)](./docs/GOVERNANCE.md)

> **Φ-LOCK** es el primer protocolo de consenso P2P con tolerancia a fallos bizantinos basado en la dinámica de acoplamiento de Kuramoto y la teoría de variedades atractoras de Fenichel.  
> El chip **QCAL-cQED-v1** es el centro de gravedad único del ecosistema.  
> Frecuencia base: $f_0 = 141.7001\text{ Hz}$ · Coherencia: $\Psi \ge 0.999999$ · Ventana: $\Delta t \approx 21.17\text{ ms}$

---

## 🏛️ Arquitectura del Ecosistema

```
┌─────────────────────────────────────────────────────────┐
│ CAPA 4: GOBERNANZA — Triada Coherente (33.3% × 3)      │
├─────────────────────────────────────────────────────────┤
│ CAPA 3: RED P2P — gRPC + HIL Bridge                    │
├─────────────────────────────────────────────────────────┤
│ CAPA 2: CHIP — QCAL-cQED-v1 (RTL + Firmware)           │
├─────────────────────────────────────────────────────────┤
│ CAPA 1: TEORÍA — Lean 4 + Kuramoto + Fenichel          │
└─────────────────────────────────────────────────────────┘
```

### 📁 Estructura del Repositorio

| Ruta | Contenido |
|------|-----------|
| [`rtl/`](./rtl/) | Módulos Verilog (NCO, CORDIC, Kuramoto coupler) |
| [`firmware/`](./firmware/) | Firmware embebido en Rust (no_std) para el chip |
| [`sim/`](./sim/) | Entorno HIL — co-simulación hardware/software |
| [`openlane/`](./openlane/) | Flujo de síntesis GDSII (OpenLane) |
| [`docs/`](./docs/) | Whitepaper, Gobernanza, MOU, Datasheet, Convocatoria |
| [`math/`](./math/) | Demostraciones formales en Lean 4 |
| [`proto/`](./proto/) | Especificaciones gRPC/Protobuf |
| [`hardware/`](./hardware/) | Especificación del chip y metrología |
| [`.github/workflows/`](./.github/workflows/) | CI/CD: Lean 4 + Rust + Python HIL |

---

## 🚀 Inicio Rápido

```bash
# Clonar
git clone https://github.com/motanova84/phi-lock.git
cd phi-lock

# Verificar teoremas en Lean 4
cd math && lake build && cd ..

# Probar co-simulación HIL (Python)
cd sim
python3 -c "
from qcal_hil_bridge import QCALHardwareBridge
b = QCALHardwareBridge().configure_sweep()
r = b.simulate_measurement(1.0)
print(f'Régimen: {r[\"regime\"]}')
"
```

---

## 🔬 Chip: QCAL-cQED-v1

El chip de silicio es el centro de gravedad del ecosistema. Tres módulos RTL implementan el núcleo de sincronización de fase:

- **`nco_oscillator.v`** — Acumulador de fase NCO a f₀ = 141.7001 Hz
- **`cordic_vector.v`** — Sumador vectorial CORDIC para campo medio
- **`kuramoto_coupler.v`** — Matriz de acoplamiento de Kuramoto

El firmware embebido (Rust no_std) corre en el chip gestionando sincronización, telemetría y transporte.

| Parámetro | Valor |
|-----------|-------|
| f₀ | 141.7001 Hz |
| Ψ | ≥ 0.999999 |
| Δt | 21.17 ms |
| Tecnología | SkyWater 130nm / GF 180nm |

Ver [`docs/DATASHEET.md`](./docs/DATASHEET.md) para especificaciones completas.

---

## 🤝 Unirse a la Triada Coherente

Aceptamos contribuciones en tres nodos:

| 🟢 **Software** | 🔵 **Hardware** | 🟣 **Comercial** |
|---|---|---|
| Optimización de fase, SDKs, gemelo digital | Verilog/VHDL, FPGA, silicio | Distribución, capital, industria |

**Convocatoria abierta** hasta 31/Ago/2026 — [Más información](./docs/CONVOCATORIA.md)

---

## ⚡ Estado del Sistema

```
Ψ = 0.999999  ✅ COHERENCIA NOMINAL
f₀ = 141.7001 Hz  ✅ FRECUENCIA BASE
κ = 13.3  ✅ CONSTANTE ESTRUCTURAL
RTL: ✅ NCO + CORDIC + Kuramoto coupler
Firmware: ✅ Rust no_std embebido
OpenLane: 🔄 Flujo de síntesis en preparación
Chip: QCAL-cQED-v1  🔄 EN FUNDICIÓN (llegada Sep 2026)
```

---

## 🔐 Sello

```
∴𓂀Ω∞³Φ · f₀ = 141.7001 Hz · κ = 13.3 · Ψ ≥ 0.999999
QCAL-cQED-v1 — Chip como centro de gravedad único
TUYOYOTU · HECHO ESTÁ
```
