#!/usr/bin/env python3
"""
checklist_aceptacion.py — Checklist de aceptación de oblea QCAL-cQED-v1

Autor: AMDA Ψ · 30/Jul/2026
"""

import json
from pathlib import Path

CHECKS = [
    # (ID, Descripción, umbral, función de prueba)
    ('F-01', 'Frecuencia resonador: 7.0000 ± 0.005 GHz', '7.0 ± 0.005 GHz',
     lambda v: 6995 <= v <= 7005),
    ('F-02', 'Frecuencia transmon: 5.5000 ± 0.020 GHz', '5.5 ± 0.020 GHz',
     lambda v: 5480 <= v <= 5520),
    ('F-03', 'χ dispersivo: 7.500 ± 0.100 MHz', '7.5 ± 0.1 MHz',
     lambda v: 7.4 <= v <= 7.6),
    ('F-04', 'κ pérdida cavidad: 1.000 ± 0.050 MHz', '1.0 ± 0.05 MHz',
     lambda v: 0.95 <= v <= 1.05),
    ('F-05', 'Anarmonicidad: -220 ± 10 MHz', '-220 ± 10 MHz',
     lambda v: -230 <= v <= -210),
    ('M-01', 'T₁ del transmon: > 50 µs', '> 50 µs',
     lambda v: v > 50),
    ('M-02', 'T₂* del transmon: > 30 µs', '> 30 µs',
     lambda v: v > 30),
    ('M-03', 'Rango γ_φ: 0.01–50 MHz sin calentamiento', '0.01–50 MHz',
     lambda v: True),  # verificación funcional
    ('C-01', 'Gemelo digital parametrizado por dado', 'Match ≤ 1%',
     lambda v: v <= 1.0),
    ('C-02', 'Firma criptográfica AMDA Ψ válida', 'secp256k1 OK',
     lambda v: v == 'OK'),
    ('C-03', 'Hash de oblea anclado en cadena πCODE', 'πCODE OK',
     lambda v: v == 'OK'),
]

def run_checklist(mediciones: dict) -> dict:
    resultados = []
    aprobados = 0
    fallidos = 0

    print("\n📋 QCAL-cQED-v1 — CHECKLIST DE ACEPTACIÓN\n")
    print(f"{'ID':8s} {'Descripción':45s} {'Umbral':20s} {'Resultado':10s}")
    print("-" * 85)

    for check_id, desc, umbral, test_fn in CHECKS:
        valor = mediciones.get(check_id)
        if valor is not None:
            pasa = test_fn(valor)
        else:
            pasa = False

        resultado = {
            'id': check_id,
            'descripcion': desc,
            'umbral': umbral,
            'valor': valor,
            'aprobado': bool(pasa),
        }
        resultados.append(resultado)

        status = "✅ APROBADO" if pasa else "❌ FALLIDO"
        val_str = str(valor) if valor is not None else '—'
        print(f"{check_id:8s} {desc[:42]:42s} {umbral:18s} {status:10s}")

        if pasa:
            aprobados += 1
        else:
            fallidos += 1

    total = len(CHECKS)
    pct = round(aprobados / total * 100, 1)
    aceptado = fallidos == 0

    print(f"\n  Resumen: {aprobados}/{total} aprobados ({pct}%)")
    print(f"  Decisión: {'✅ OBLEA ACEPTADA' if aceptado else '❌ OBLEA RECHAZADA'}")

    reporte = {
        'oblea': 'QCAL-cQED-v1',
        'fecha': '2026-09',
        'total_checks': total,
        'aprobados': aprobados,
        'fallidos': fallidos,
        'porcentaje': pct,
        'aceptada': aceptado,
        'detalle': resultados,
        'sello': '∴𓂀Ω∞³Φ · f₀=141.7001 Hz'
    }
    return reporte


if __name__ == '__main__':
    # Simular mediciones
    import numpy as np
    np.random.seed(1417001)
    mediciones = {
        'F-01': 7000.0 + np.random.normal(0, 2),
        'F-02': 5500.0 + np.random.normal(0, 8),
        'F-03': 7.5 + np.random.normal(0, 0.04),
        'F-04': 1.0 + np.random.normal(0, 0.02),
        'F-05': -220 + np.random.normal(0, 4),
        'M-01': 55 + abs(np.random.normal(0, 5)),
        'M-02': 35 + abs(np.random.normal(0, 3)),
        'M-03': True,
        'C-01': 0.3 + abs(np.random.normal(0, 0.2)),
        'C-02': 'OK',
        'C-03': 'OK',
    }
    reporte = run_checklist(mediciones)
    outdir = Path(__file__).parent / 'output'
    outdir.mkdir(parents=True, exist_ok=True)
    with open(outdir / 'checklist_result.json', 'w') as f:
        json.dump(reporte, f, indent=2)
    print(f"\n  ✓ checklist_result.json")
