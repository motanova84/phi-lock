# API QCAL ∞³ — Especificación de Endpoints

**Versión:** v1  
**Protocolo:** gRPC + REST (gateway)  
**Autenticación:** Φ-LOCK (clave de fase) + secp256k1  
**Ledger:** πCODE  
**Sello:** ∴𓂀Ω∞³Φ

---

## Endpoints

### 1. Simulación del Gemelo Digital
`POST /v1/simulacion`
Ejecuta el gemelo digital v4 con parámetros dados.
→ `Stream<TransmissionResponse>`

### 2. Optimización de Parámetros
`POST /v1/optimizacion`
Busca χ, κ, γ_φ óptimos para un objetivo dado.
→ `OptimizationReceipt`

### 3. Validación de Firmas (A/B/C)
`POST /v1/validacion`
Contrasta datos experimentales con las tres firmas.
→ `{firma_detectada, confianza}`

### 4. Simulación de Fabricación
`POST /v1/fabricacion`
Simula variación de oblea (wafer_map_chi).
→ `WaferMap`

### 5. Consenso Φ-LOCK
`POST /v1/consenso`
Ejecuta consenso por fase sobre un conjunto de fases.
→ `{psi, decision}`

### 6. Trazabilidad πCODE
`GET /v1/trazabilidad/{hash}`
Consulta el ledger πCODE.
→ `Contribution`

### 7. Propuesta / Candidatura
`POST /v1/propuesta`
Envía una mejora o candidatura con firma secp256k1.
→ `{propuesta_id, estado, hash}`

---

## Autenticación

Todas las requests deben incluir:
- `X-Phi-Key`: clave pública de fase
- `X-Signature`: firma secp256k1 del body
- `X-Contributor`: wallet πCODE

## Rate Limits

| Tipo | Límite | Costo |
|------|--------|-------|
| Academia | 100 req/h | Gratuito |
| Comercial | 10,000 req/h | Suscripción |
| Validación | Ilimitado | Por contribución πCODE |

---

*Sello: ∴𓂀Ω∞³Φ*
