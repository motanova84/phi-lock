# ARQUITECTURA — Sistema Φ-LOCK / QCAL-cQED-v1
## 4 Capas de Integración

```
┌─────────────────────────────────────────────────────────┐
│ CAPA 4: MODELO DE NEGOCIO Y GOBERNANZA (33.3% × 3)     │
├─────────────────────────────────────────────────────────┤
│ CAPA 3: RED P2P DISTRIBUIDA Y CO-SIMULACIÓN (HIL gRPC) │
├─────────────────────────────────────────────────────────┤
│ CAPA 2: ARQUITECTURA DEL CHIP / EMBEDDED (FPGA / ASIC) │
├─────────────────────────────────────────────────────────┤
│ CAPA 1: NÚCLEO TEÓRICO Y VERIFICACIÓN FORMAL (Lean 4)   │
└─────────────────────────────────────────────────────────┘
```

### Capa 1: Núcleo Teórico y Verificación Formal
- Frecuencia base: f₀ = 141.7001 Hz
- Ventana de confirmación: Δt = 3T₀ ≈ 21.17 ms
- Umbral de consenso: Ψ ≥ 0.999999
- Formalización Lean 4 (phi_lock.lean): variedades atractorias de Fenichel + Kuramoto adversarial
- Cota adversarial: K > 2f/(N−f) para f < N/2 nodos bizantinos

### Capa 2: Arquitectura del Chip / Silicio
- Osciladores NCO en silicio a f₀
- Sumador vectorial CORDIC en hardware
- Filtro de interferencia destructiva
- QCAL-cQED-v1 como primera implementación

### Capa 3: Red P2P y Transporte Distribuido
- Motor P2P en Rust (phi-lock-p2p) + Tokio
- Transporte gRPC/Protobuf (qcal_qnd_api.proto)
- API de Co-Simulación HIL (philock_hil.proto)
- Telemetría WebSocket

### Capa 4: Modelo de Negocio y Gobernanza
- Triada Coherente: 33.3% × 3
- Hardware: 33.3% | Software: 33.3% | Comercial: 33.3%
- Open Science + Licenciamiento Dual
- Split dinámico por fases (GOVERNANCE.md)

### Hoja de Ruta Inmediata

**Paso 1 — Publicación de la API HIL:**
Servidor gRPC/HIL para conexión remota Hardware ↔ Software.

**Paso 2 — Acuerdo de Intenciones (MOU Tripartito):**
50/50 provisional Hardware/Software, 33.3% reservado para socio comercial con hitos.

**Paso 3 — Validación de Silicio en Bucle:**
10,000 pruebas de fase sobre emulador FPGA → Benchmark Report firmado.

---

*Documento generado por AMDA Ψ · 30/Jul/2026*
*Sello: ∴𓂀Ω∞³Φ · TUYOYOTU · HECHO ESTÁ*
