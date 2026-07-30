# GOVERNANCE.md — Modelo de Gobernanza QCAL-cQED-v1

**Versión:** 1.3  
**Válido para:** QCAL-cQED-v1 (único chip, diseño sellado)  
**Autoría:** José Manuel Mota Burruezo (JMMB) + AMDA Ψ  
**Anclaje πCODE:** v1.3  
**Sello:** ∴𓂀Ω∞³Φ

---

## 1. Estructura de Dos Capas

### Capa 1: Gobernanza (Contrato Social)
**Modelo:** Triada Coherente 33.3% × 3  
**Estática.** Se firma una vez. Rige las relaciones entre los tres polos.

| Vórtice | % | Rol | Aportación |
|---------|---|-----|------------|
| 🔬 Hardware | 33.3% | Diseño, fabricación, calibración | Chip físico, GDSII, metrología, criogenia |
| 💻 Software | 33.3% | Gemelo digital, simulación, optimización | Código, HIL bridge, API, SDK |
| 🌐 Distribución | 33.3% | Ecosistema, soporte, comercialización | Canal, comunidad, formación, ventas |

**Condición Φ-LOCK:** Ningún vórtice actúa sin validación de los otros dos.

### Capa 2: Económica (Split Dinámico)
**Modelo:** Split Resonante por Fases (converge a 23/13.3/63.7)  
**Dinámica.** Se recalcula por fase del ciclo de vida.

| Fase | Hardware | Software | Distribución | Cuándo |
|------|----------|----------|--------------|--------|
| 0 — Fundición | 72% | 18% | 10% | t=0, CAPEX inicial |
| 1 — Validación | 50% | 25% | 25% | Post-chip, primeros barridos |
| 2 — Adopción | 33% | 25% | 42% | Múltiples laboratorios activos |
| 3 — Madurez | 23% | 13.3% | 63.7% | Límite asintótico (valores πCODE) |

---

## 2. Cláusula de Entrada del Tercer Vórtice

El 33.3% del Vórtice Distribución está **reservado pero no asignado.**

Se materializa cuando el socio cumple **todos** estos hitos:
1. Financiar una tirada mínima de 25 chips
2. Asegurar ≥3 contratos de integración con laboratorios
3. Abrir canal de venta en ≥2 países
4. Aportar capital de escalado ≥ $X

Plazo máximo: 12 meses desde la activación de la API pública.
Si no cumple: el 33.3% revierte en 50/50 a Hardware y Software.

---

## 3. API de Cocreación (qcal_qnd_api.proto)

La interfaz gRPC es el mecanismo de gobernanza técnica.

Endpoints:
- `ComputeTransmission(γ_φ, dado_id, χ) → Stream<S₂₁(ω)>`
- `SubmitOptimization(patch, descripción, firma) → πCODE_credit`
- `GetCurrentSplit() → Split(%, fase)`
- `GetContributionLog(address) → []Contribution`

Cada invocación genera un evento πCODE.  
Cada optimización firmada ajusta el split dinámico.

---

## 4. Licencia Específica del QCAL-cQED-v1

Este modelo de gobernanza NO es transferible a otros chips, proyectos o derivados sin autorización expresa firmada por JMMB y validada por AMDA Ψ.

El chip QCAL-cQED-v1, su gemelo digital, su HIL bridge, su whitepaper, y su modelo económico constituyen una **unidad sellada e indivisible**.

---

## 5. Sello

```
∴𓂀Ω∞³Φ · f₀ = 141.7001 Hz · κ = 13.3

QCAL-cQED-v1 — GOBERNANZA SELLADA
Gobernanza: 33.3% × 3 Triada Coherente
Económica: Split Dinámico → 23/13.3/63.7
API: qcal_qnd_api.proto
Φ-LOCK: Consenso por fase, no por voto

TUYOYOTU · HECHO ESTÁ
```
