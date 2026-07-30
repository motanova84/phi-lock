# ECOSYSTEM.md — Entrelazamiento de Repositorios

## Nodos del Ecosistema QCAL ∞³

```
phi-lock/                          vault/
┌────────────────────────┐         ┌────────────────────────┐
│ 🜁 Φ-LOCK              │    ⛓    │ 🏛️ SOVEREIGN VAULT     │
│ Chip QND · Consenso    │◄───────►│ PayGate · ADAPA · C∞³  │
│ P2P · Kuramoto         │         │ Seedless Self-Custody  │
├────────────────────────┤         ├────────────────────────┤
│ hardware/              │         │ contracts/             │
│   chip spec            │         │   PayGate.sol          │
│   simulador v4         │         │   πCODE.sol            │
│   HIL bridge           │         │   Split23_77.sol       │
│ sim/                   │         │ formalization/         │
│   servidor gRPC        │         │   ADAPA_95D.lean       │
│ rtl/                   │         │ lean4/                 │
│   NCO, CORDIC          │         │   C∞³_invariant.lean   │
│ docs/                  │         │ docs/                  │
│   Gobernanza, MOU      │         │   Protocolo E2EE       │
│ proto/                 │         │ scripts/               │
│   qcal_qnd_api.proto   │         │   fee_oracle.py        │
└────────────────────────┘         └────────────────────────┘
         │                                │
         └──────────┬─────────────────────┘
                    │
           ┌────────▼────────┐
           │   πCODE LEDGER  │
           │  (memoria común)│
           └─────────────────┘
```

## Puentes de Integración

### Puente 1: PayGate → Splits del Chip
**vault/ → phi-lock**

Cuando se venda un chip QCAL-cQED-v1:
1. El pago entra por **PayGate Catedral** (vault/contracts/PayGate.sol)
2. Ejecuta split 23/77: 23% a reserva, 77% a distribución
3. Fee oracle extrae 0.5% para πCODE anchoring
4. El recibo se registra en el ledger común

### Puente 2: ADAPA 95D → Espectros S₂₁(ω)
**vault/ → phi-lock**

Los datos brutos del gemelo digital:
1. `simulador_qnd_v4.py` produce arrays de S₂₁(ω)
2. Se reducen vía ADAPA 95D (vault/formalization/)
3. El tensor reducido se almacena como bloque πCODE
4. Verificación: el espectro original debe reconstruirse desde el tensor

### Puente 3: C∞³ Invariant → Lean 4 Verification
**vault/ ↔ phi-lock**

La constante estructural del sistema:
- **vault/lean4/** contiene la formalización del C∞³ invariant
- **phi-lock/math/** contiene el teorema de Fenichel y Kuramoto
- Ambos convergen en: la coherencia Ψ ≥ 0.999999 es invariante bajo transformaciones del grupo C∞³

### Puente 4: Fee Oracle → gRPC API
**vault/ess → phi-lock/sim**

Cuando el servidor gRPC procesa un `SubmitCandidacy` o `SubmitOptimization`:
1. Genera un crédito πCODE
2. El fee oracle (vault/scripts/fee_oracle.py) registra la transacción
3. El split 23/77 se ejecuta automáticamente

## Arquitectura de Submódulos

```
phi-lock/              ← Repositorio principal (chip + consenso)
  └── vault/           ← Submódulo (soberanía financiera)
        └── ...
```

Para clonar con submódulos:
```bash
git clone --recurse-submodules https://github.com/motanova84/phi-lock.git
```

Para actualizar:
```bash
git submodule update --remote vault
```

## Sello

```
∴𓂀Ω∞³Φ · f₀ = 141.7001 Hz · κ = 13.3 · C∞³ Invariant
phi-lock ⟷ vault: dos caras de un mismo ecosistema
TUYOYOTU · HECHO ESTÁ
```
