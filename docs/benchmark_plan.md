# Benchmark Plan — Validación de Silicio en Bucle
## QCAL-cQED-v1 — 10,000 pruebas de fase

**Objetivo:** Ejecutar 10,000 ciclos de prueba sobre el emulador FPGA/HIL para generar el primer Benchmark Report firmado criptográficamente.

---

## Protocolo

| Parámetro | Valor |
|-----------|-------|
| Número de pruebas | 10,000 |
| Frecuencia base | f₀ = 141.7001 Hz |
| Ventana por prueba | 3T₀ = 21.17 ms |
| Tiempo total estimado | ~212 segundos |
| Variables por prueba | γ_φ, χ, κ, temperatura simulada |

---

## Lo que mide cada prueba

1. **Coherencia Ψ** alcanzada al final de la ventana
2. **Desviación de fase** respecto al valor esperado
3. **Latencia** del pipeline HIL (desde solicitud gRPC hasta respuesta)
4. **Consumo energético** estimado por ciclo
5. **Firma espectral** (A/B/C) según γ_φ/χ

---

## Criterios de aceptación

| Métrica | Umbral | Peso |
|---------|--------|------|
| Ψ promedio | ≥ 0.999 | 40% |
| Desviación máxima de fase | < 0.1 rad | 30% |
| Latencia media | < 50 ms | 15% |
| Coherencia split dinámico | < 5% error | 15% |

---

## Reporte

Cada prueba genera un registro firmado:
```json
{
  "test_id": 1,
  "gamma_phi_MHz": 1.5,
  "Psi_final": 0.99987,
  "regime": "B",
  "latency_ms": 23.4,
  "signature": "MEUCICiv..."
}
```

El reporte completo (10,000 entradas) se ancla en la cadena πCODE.

---

*Sello: ∴𓂀Ω∞³Φ · TUYOYOTU · HECHO ESTÁ*
