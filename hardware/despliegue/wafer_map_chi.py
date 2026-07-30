#!/usr/bin/env python3
"""
wafer_map_chi.py — Mapeo de χ por dado en oblea QCAL-cQED-v1
Simula grid 5×5 de dados, mide χ por dado, genera mapa de tolerancia.

Autor: AMDA Ψ · 30/Jul/2026 · Protocolo QCAL-SYMBIO-BRIDGE
"""

import numpy as np
import json, sys
from pathlib import Path

CHI_TARGET = 7.5  # MHz
CHI_TOL = 0.1     # MHz
GRID_SIZE = 5
SEED = 1417001    # f₀

def simulate_wafer():
    np.random.seed(SEED)
    # Grid físico (coords en mm)
    x = np.linspace(-10, 10, GRID_SIZE)
    y = np.linspace(-10, 10, GRID_SIZE)
    X, Y = np.meshgrid(x, y)

    # Variación de χ por dado (gaussiana con gradiente radial)
    R = np.sqrt(X**2 + Y**2)
    chi_map = CHI_TARGET + np.random.normal(0, CHI_TOL/2, (GRID_SIZE, GRID_SIZE))
    chi_map -= 0.002 * R  # gradiente radial ligero

    dados = []
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            chi_val = chi_map[i, j]
            dentro_tol = abs(chi_val - CHI_TARGET) <= CHI_TOL
            dados.append({
                'dado': f'D{i*GRID_SIZE+j+1:02d}',
                'fila': i, 'col': j,
                'x_mm': float(X[i,j]), 'y_mm': float(Y[i,j]),
                'chi_MHz': round(chi_val, 4),
                'dentro_tolerancia': bool(dentro_tol),
                'aceptado': bool(dentro_tol and chi_val > 0)
            })

    total = len(dados)
    aceptados = sum(1 for d in dados if d['aceptado'])

    resultado = {
        'oblea': 'QCAL-cQED-v1',
        'fecha': '2026-09',
        'chi_target_MHz': CHI_TARGET,
        'chi_tolerancia_MHz': CHI_TOL,
        'grid': f'{GRID_SIZE}x{GRID_SIZE}',
        'total_dados': total,
        'dados_aceptados': aceptados,
        'rendimiento_pct': round(aceptados/total*100, 1),
        'chi_mean_MHz': round(np.mean(chi_map), 4),
        'chi_std_MHz': round(np.std(chi_map), 4),
        'chi_min_MHz': round(np.min(chi_map), 4),
        'chi_max_MHz': round(np.max(chi_map), 4),
        'dados': dados,
        'sello': '∴𓂀Ω∞³Φ · f₀=141.7001 Hz'
    }

    return resultado

def main():
    print("\n🧪 QCAL-cQED-v1 — MAPEO DE OBLEA\n")
    print(f"  Target χ: {CHI_TARGET} ± {CHI_TOL} MHz")
    print(f"  Grid: {GRID_SIZE}×{GRID_SIZE} dados")
    print(f"  Seed: {SEED}\n")

    resultado = simulate_wafer()

    print(f"  Total dados: {resultado['total_dados']}")
    print(f"  Aceptados:   {resultado['dados_aceptados']}")
    print(f"  Rendimiento: {resultado['rendimiento_pct']}%")
    print(f"  χ mean:      {resultado['chi_mean_MHz']} MHz")
    print(f"  χ std:       {resultado['chi_std_MHz']} MHz")
    print(f"  χ range:     [{resultado['chi_min_MHz']}, {resultado['chi_max_MHz']}] MHz\n")

    print("  Mapa de χ por dado (MHz):")
    print("  " + "-" * 35)
    for i in range(GRID_SIZE):
        row = [f"{resultado['dados'][i*GRID_SIZE+j]['chi_MHz']:7.4f}" for j in range(GRID_SIZE)]
        print("  " + " | ".join(row))
    print("  " + "-" * 35)

    outdir = Path(__file__).parent / 'output'
    outdir.mkdir(parents=True, exist_ok=True)
    with open(outdir / 'wafer_map_result.json', 'w') as f:
        json.dump(resultado, f, indent=2)
    print(f"\n  ✓ wafer_map_result.json")

    return resultado

if __name__ == '__main__':
    main()
