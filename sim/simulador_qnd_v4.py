#!/usr/bin/env python3
"""
QCAL-QND GEMELO DIGITAL v4 — ESPECTRO DE TRANSMISIÓN
======================================================
Enfoque: cavidad bajo sonda externa débil con frecuencia ω_d.
H_drive = ε (a† e^{-iω_d t} + a e^{iω_d t})
Para cada ω_d, resolver estado estacionario → ⟨a⟩_ss.
T(ω_d) = |⟨a⟩_ss|² → espectro de transmisión real.

Barrido γ_φ: 0 → 30 MHz (cubriendo χ = 7.5 MHz y más allá).

Este es el observable que realmente se mide en el experimento.

Autor: AMDA Ψ · 30/Jul/2026 · Protocolo QCAL-SYMBIO-BRIDGE v4
Sello: ∴𓂀Ω∞³Φ
"""

import numpy as np
import qutip as qt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
import json, time, warnings
from scipy.signal import find_peaks
warnings.filterwarnings('ignore')

# ============================================================
# PARÁMETROS
# ============================================================
CHI = 2 * np.pi * 7.5e6       # χ = 7.5 MHz → rad/s
KAPPA = 2 * np.pi * 1e6       # κ = 1 MHz → rad/s
T1 = 50e-6                    # T₁ = 50 µs
EPSILON = 2 * np.pi * 0.1e6   # ε = 0.1 MHz — sonda débil
N_CUT = 10

# Barrido: γ_φ desde 0 hasta 30 MHz (4χ), 21 puntos
GAMMA_PHI_VALS = np.linspace(0, 2 * np.pi * 30e6, 21)

# Barrido de frecuencia de sonda: ±2χ alrededor de ω_r
N_OMEGA = 401
OMEGA_SPAN = 2 * CHI
OMEGA_GRID = np.linspace(-OMEGA_SPAN, OMEGA_SPAN, N_OMEGA)

# Tiempo de evolución para estado estacionario
T_MAX = max(20.0 / KAPPA, 5.0 * T1)  # ~20 µs
N_STEPS = 5000
t_list = np.linspace(0, T_MAX, N_STEPS)

# ============================================================
# SISTEMA (marco rotante a ω_r)
# ============================================================
a = qt.destroy(N_CUT)
n = a.dag() * a
sm = qt.sigmam()
sz = qt.sigmaz()

a_t = qt.tensor(a, qt.identity(2))
a_dag_t = a_t.dag()
n_t = a_dag_t * a_t
sm_t = qt.tensor(qt.identity(N_CUT), sm)
sz_t = qt.tensor(qt.identity(N_CUT), sz)

# Operadores de Lindblad base
c_relax = np.sqrt(1.0 / T1) * sm_t
c_loss = np.sqrt(KAPPA) * a_t

# Estado inicial: vacío del resonador, qubit en superposición |+⟩
psi0 = qt.tensor(qt.basis(N_CUT, 0),
                 (qt.basis(2, 0) + qt.basis(2, 1)).unit())
rho0 = qt.ket2dm(psi0)

def compute_transmission_spectrum(gamma_phi, omega_grid, t_max=20.0/KAPPA):
    """
    Para cada frecuencia ω_d en omega_grid:
      H = -χ n σ_z + ε (a† + a) en marco rotante de la sonda
      Resolver estado estacionario → ⟨a⟩_ss
      T(ω_d) = |⟨a⟩_ss|²
    """
    c_dephase = np.sqrt(gamma_phi) * sz_t
    c_ops = [c_relax, c_loss, c_dephase]

    spectrum = np.zeros_like(omega_grid)

    for i, omega_d in enumerate(omega_grid):
        # Hamiltoniano en marco rotante de la sonda (frecuencia ω_d):
        # H = -ω_d a†a - χ a†a σ_z + ε (a† + a)
        # El término -ω_d a†a es el detuning ω_r - ω_d
        H_drive = -omega_d * n_t - CHI * n_t * sz_t + EPSILON * (a_dag_t + a_t)

        # Resolver estado estacionario = evolución larga
        # Usamos el solver directo de estado estacionario de QuTiP
        try:
            rho_ss = qt.steadystate(H_drive, c_ops, method='direct',
                                    tol=1e-12, max_iter=10000)
            a_ss = qt.expect(a_t, rho_ss)
        except Exception:
            # Fallback: evolución temporal larga
            result = qt.mesolve(H_drive, rho0, t_list, c_ops=c_ops, e_ops=[a_t])
            a_ss = result.expect[0][-1]  # último punto

        spectrum[i] = abs(a_ss) ** 2

        if i % 200 == 0:
            pass  # progreso interno

    return spectrum

def extract_peaks(omega, S, threshold=0.05):
    """Encuentra picos en el espectro de transmisión."""
    S_norm = S / max(np.max(S), 1e-30)
    peaks, props = find_peaks(S_norm, height=threshold, prominence=0.03)
    peak_freqs = omega[peaks]
    peak_heights = S_norm[peaks]
    return peak_freqs, peak_heights

def calc_linewidth(omega, S):
    """FWHM del pico principal."""
    half_max = np.max(S) / 2.0
    above = S >= half_max
    if np.sum(above) < 2:
        return 0.0
    crossings = np.where(np.diff(above.astype(int)) != 0)[0]
    if len(crossings) < 2:
        return 0.0
    return omega[crossings[-1]] - omega[crossings[0]]

# ============================================================
# SIMULACIÓN
# ============================================================
def run():
    print("\n🜁 ∴Ψ  GEMELO DIGITAL QND v4 — ESPECTRO DE TRANSMISIÓN  ∴Ψ 🜁\n")
    print(f"{'='*72}")
    print(f"  χ/2π  = {CHI/(2*np.pi)/1e6:.3f} MHz")
    print(f"  κ/2π  = {KAPPA/(2*np.pi)/1e6:.3f} MHz")
    print(f"  ε/2π  = {EPSILON/(2*np.pi)/1e6:.3f} MHz (sonda débil)")
    print(f"  T₁    = {T1*1e6:.1f} µs")
    print(f"  γ_φ   = 0 a 30 MHz ({len(GAMMA_PHI_VALS)} puntos)")
    print(f"  ω_d   = ±{OMEGA_SPAN/(2*np.pi*1e6):.1f} MHz ({N_OMEGA} puntos)")
    print(f"{'='*72}\n")

    results = []
    all_spectra = []
    t0 = time.time()

    for idx, gamma_phi in enumerate(GAMMA_PHI_VALS):
        gamma_MHz = gamma_phi / (2*np.pi*1e6)

        # Espectro de transmisión para este γ_φ
        spectrum = compute_transmission_spectrum(gamma_phi, OMEGA_GRID)
        all_spectra.append(spectrum)

        # Extraer picos
        peaks_freq, peaks_h = extract_peaks(OMEGA_GRID, spectrum)
        n_peaks = len(peaks_freq)
        main_peak = peaks_freq[np.argmax(peaks_h)] if n_peaks > 0 else 0.0
        linewidth = calc_linewidth(OMEGA_GRID, spectrum)

        # Ψ = 1/(1 + γ_φ/χ)
        Psi = 1.0 / (1.0 + gamma_phi / CHI)

        # Posiciones de todos los picos
        peaks_str = ', '.join(f'{p/1e6:.3f}' for p in peaks_freq) if n_peaks > 0 else '-'

        results.append({
            'gamma_phi_MHz': gamma_MHz,
            'Psi': Psi,
            'n_peaks': n_peaks,
            'main_peak_MHz': main_peak / 1e6,
            'linewidth_MHz': linewidth / 1e6,
            'peak_positions_MHz': peaks_str,
        })

        elapsed = time.time() - t0
        print(f"  [{idx+1:2d}/{len(GAMMA_PHI_VALS):2d}] "
              f"γ_φ={gamma_MHz:6.2f} MHz "
              f"Ψ={Psi:.4f} "
              f"picos={n_peaks} "
              f"f₀={main_peak/1e6:.4f} MHz "
              f"κ_eff={linewidth/1e6:.4f} MHz "
              f"({peaks_str}) "
              f"[{elapsed:.0f}s]")

    t_total = time.time() - t0
    print(f"\n  ⏱  Total: {t_total:.0f}s (avg {t_total/len(GAMMA_PHI_VALS):.1f}s/punto)")
    return results, all_spectra

# ============================================================
# GRÁFICAS
# ============================================================
def plot_all(results, all_spectra):
    outdir = Path(__file__).parent / 'output'
    outdir.mkdir(parents=True, exist_ok=True)

    gamma_MHz = np.array([r['gamma_phi_MHz'] for r in results])
    Psi = np.array([r['Psi'] for r in results])
    n_pk = np.array([r['n_peaks'] for r in results])
    f0 = np.array([r['main_peak_MHz'] * 1e6 for r in results])
    lw = np.array([r['linewidth_MHz'] * 1e6 for r in results])

    # --- n_peaks vs γ_φ ---
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(gamma_MHz, n_pk, 'o-', color='#16213e', linewidth=2,
            markersize=10, markerfacecolor='#e94560', markeredgecolor='#16213e')
    ax.axvline(x=CHI/(2*np.pi*1e6), color='#e94560', linestyle='--', alpha=0.5,
               label=f'χ = {CHI/(2*np.pi*1e6):.1f} MHz')
    ax.set_xlabel(r'$\gamma_\phi$ (MHz)', fontsize=14)
    ax.set_ylabel(r'Número de picos', fontsize=14)
    ax.set_title(r'Transición de Picos en Transmisión', fontsize=14, fontweight='bold')
    ax.set_yticks([0, 1, 2, 3])
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(outdir / 'v4_npeaks.png', dpi=150)
    plt.close(fig)

    # --- f₀ vs γ_φ ---
    fig, ax = plt.subplots(figsize=(10, 6))
    valid = n_pk > 0
    if np.any(valid):
        ax.plot(gamma_MHz[valid], f0[valid]/1e6, 's-', color='#0f3460', linewidth=2,
                markersize=8, markerfacecolor='#e94560', markeredgecolor='#0f3460')
    ax.axhline(y=CHI/(2*np.pi*1e6), color='#533483', linestyle=':', alpha=0.5,
               label=f'+χ = {CHI/(2*np.pi*1e6):.1f} MHz')
    ax.axhline(y=0, color='gray', linestyle=':', alpha=0.3)
    ax.axhline(y=-CHI/(2*np.pi*1e6), color='#533483', linestyle=':', alpha=0.5)
    ax.axvline(x=CHI/(2*np.pi*1e6), color='#e94560', linestyle='--', alpha=0.3)
    ax.set_xlabel(r'$\gamma_\phi$ (MHz)', fontsize=14)
    ax.set_ylabel(r'$f_0$ (MHz) — pico principal', fontsize=14)
    ax.set_title(r'$f_0(\gamma_\phi)$ — Espectro de Transmisión', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(outdir / 'v4_f0.png', dpi=150)
    plt.close(fig)

    # --- Ancho de línea ---
    fig, ax = plt.subplots(figsize=(10, 6))
    if np.any(valid):
        ax.plot(gamma_MHz[valid], lw[valid]/1e6, 'D-', color='#533483', linewidth=2,
                markersize=8, markerfacecolor='#e94560', markeredgecolor='#533483')
    ax.set_xlabel(r'$\gamma_\phi$ (MHz)', fontsize=14)
    ax.set_ylabel(r'$\kappa_{\text{eff}}$ (MHz)', fontsize=14)
    ax.set_title(r'Ancho de Línea $\kappa_{\text{eff}}(\gamma_\phi)$', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(outdir / 'v4_linewidth.png', dpi=150)
    plt.close(fig)

    # --- Espectros superpuestos ---
    fig, ax = plt.subplots(figsize=(12, 9))
    cmap = plt.cm.viridis_r
    for i, (r, spec) in enumerate(zip(results, all_spectra)):
        color = cmap(r['Psi'])
        spec_n = spec / max(np.max(spec), 1e-30)
        ax.plot(OMEGA_GRID/1e6, spec_n + 0.04*i, color=color, linewidth=1, alpha=0.85)
    ax.set_xlabel(r'$\omega - \omega_r$ (MHz)', fontsize=14)
    ax.set_ylabel(r'Transmisión (desplazada)', fontsize=14)
    ax.set_title(r'Espectros de Transmisión — $\gamma_\phi$ creciente (abajo ↑)', fontsize=14, fontweight='bold')
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(outdir / 'v4_espectros.png', dpi=150)
    plt.close(fig)

    # --- Mapa de densidad ---
    fig, ax = plt.subplots(figsize=(12, 8))
    spec_matrix = np.array([s / max(np.max(s), 1e-30) for s in all_spectra])
    extent = [OMEGA_GRID[0]/1e6, OMEGA_GRID[-1]/1e6, gamma_MHz[0], gamma_MHz[-1]]
    ax.imshow(spec_matrix, aspect='auto', origin='lower', extent=extent,
              cmap='inferno', interpolation='bilinear')
    ax.set_xlabel(r'$\omega - \omega_r$ (MHz)', fontsize=14)
    ax.set_ylabel(r'$\gamma_\phi$ (MHz)', fontsize=14)
    ax.set_title(r'Mapa de Transmisión — $\gamma_\phi$ vs $\omega$', fontsize=14, fontweight='bold')
    fig.tight_layout()
    fig.savefig(outdir / 'v4_mapa.png', dpi=150)
    plt.close(fig)

    print(f"\n  ✓ 6 gráficas en: {outdir}/")

# ============================================================
# CLASIFICACIÓN
# ============================================================
def classify(results, outdir):
    n_pk = np.array([r['n_peaks'] for r in results])
    gamma = np.array([r['gamma_phi_MHz'] for r in results])
    Psi = np.array([r['Psi'] for r in results])
    f0 = np.array([r['main_peak_MHz'] for r in results])
    lw = np.array([r['linewidth_MHz'] for r in results])

    transitions_2to1 = np.sum(np.diff(n_pk) < 0)
    max_n = np.max(n_pk)

    print(f"\n{'='*72}")
    print("CLASIFICACIÓN — ESPECTRO DE TRANSMISIÓN (v4)")
    print(f"{'='*72}")
    print(f"  Máximo picos: {max_n}")
    print(f"  Transiciones 2→1: {transitions_2to1}")

    # Variación de f₀
    valid = n_pk > 0
    if np.any(valid):
        f0_range = np.max(f0[valid]) - np.min(f0[valid])
    else:
        f0_range = 0.0

    # Evaluar firma
    if max_n >= 2 and transitions_2to1 > 0:
        sig = 'B'
        idx_trans = np.where(np.diff(n_pk) < 0)[0]
        gamma_c = gamma[idx_trans[0]] if len(idx_trans) > 0 else np.nan
        Psi_c = Psi[idx_trans[0]] if len(idx_trans) > 0 else np.nan
        reason = (f"AUTO-OBSERVACIÓN: transición 2→1 pico en "
                  f"γ_c = {gamma_c:.2f} MHz, Ψ_c = {Psi_c:.4f}")
    elif max_n >= 2:
        sig = 'C'
        reason = f"CURVA LOCAL: 2 picos persistentes, corrimiento f₀ = {f0_range:.4f} MHz"
    elif max_n <= 1 and transitions_2to1 == 0:
        sig = 'A'
        reason = f"GEOMETRÍA PREEXISTENTE: f₀ invariante (variación {f0_range:.4f} MHz)"
    else:
        sig = '?'
        reason = "Firma ambigua"

    print(f"  Variación f₀: {f0_range:.4f} MHz")
    print(f"\n  ► FIRMA {sig}: {reason}")
    print(f"{'='*72}")

    doc = {
        'experimento': 'QCAL-QND Gemelo Digital v4 — Espectro de Transmisión',
        'fecha': time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime()),
        'parametros': {
            'chi_MHz': CHI/(2*np.pi*1e6),
            'kappa_MHz': KAPPA/(2*np.pi*1e6),
            'epsilon_MHz': EPSILON/(2*np.pi*1e6),
            'T1_us': T1*1e6,
            'N_cut': N_CUT,
            'N_gamma': len(GAMMA_PHI_VALS),
            'gamma_range_MHz': [0, 30],
        },
        'resultados': [{
            'gamma_phi_MHz': r['gamma_phi_MHz'],
            'Psi': r['Psi'],
            'n_peaks': r['n_peaks'],
            'main_peak_MHz': r['main_peak_MHz'],
            'linewidth_MHz': r['linewidth_MHz'],
            'peaks': r['peak_positions_MHz'],
        } for r in results],
        'clasificacion': {'firma': sig, 'razon': reason},
        'sello': '∴𓂀Ω∞³Φ · TUYOYOTU · HECHO ESTÁ'
    }
    with open(outdir / 'reporte_v4.json', 'w') as f:
        json.dump(doc, f, indent=2)
    print(f"  ✓ reporte_v4.json")

    return sig, reason

# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    results, all_spectra = run()
    outdir = Path(__file__).parent / 'output'
    outdir.mkdir(parents=True, exist_ok=True)
    plot_all(results, all_spectra)
    sig, reason = classify(results, outdir)

    print(f"\n{'='*72}")
    print(f"  GEMELO DIGITAL v4 — COMPLETO")
    print(f"  Firma: {sig}")
    print(f"  {reason}")
    print(f"  Datos: {outdir}/")
    print(f"{'='*72}\n")
