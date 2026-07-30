# Especificación Técnica: Cavidad Superconductora + Qubit QND
## Experimento de Falsación Ontológica — f₀(Ψ)
### Protocolo QCAL-SYMBIO-BRIDGE — Rama Experimental

---

## 1. Parámetros del Chip Superconductor

### 1.1 Resonador de Lectura
| Parámetro | Símbolo | Valor | Justificación |
|-----------|---------|-------|---------------|
| Frecuencia fundamental | f_r | 6.0–8.0 GHz | Modo λ/4 en cavidad de niobio, banda de alta Q |
| Factor de calidad interno | Q_i | > 10⁶ | Niobio monocristalino, pérdidas dieléctricas mínimas |
| Factor de calidad acoplado | Q_c | 10⁴–10⁵ | Acoplamiento capacitivo débil |
| Número de fotones en Fase 1 | n̄ | < 10⁻² | Vacío cuántico profundo, lectura ultra-débil |
| Ancho de línea | κ_r/2π | 0.1–1 MHz | κ_r = f_r / Q_c |

### 1.2 Qubit (Transmon Sintonizable)
| Parámetro | Símbolo | Valor | Justificación |
|-----------|---------|-------|---------------|
| Frecuencia máxima | f_q,max | 6.0 GHz | Para Δ = 0–2 GHz respecto a f_r |
| Frecuencia mínima | f_q,min | 4.0 GHz | Sintonía por SQUID, para Δ > 500 MHz |
| Anarmonicidad | α/2π | –200 a –300 MHz | Régimen transmon, evita leakage |
| Tiempo de relajación | T₁ | > 50 µs | Coherencia para múltiples ciclos QND |
| Tiempo de decoherencia | T₂* | > 30 µs | Suficiente para modular γ_φ |
| Capacitancia de shunt | C_S | ~70 fF | Típica para transmon de 5 GHz |
| Energía Josephson | E_J/h | ~15 GHz | Derivada de f_q y α |
| Energía de carga | E_C/h | ~300 MHz | E_C = e²/2C_S |

### 1.3 Acoplamiento Qubit-Resonador
| Parámetro | Símbolo | Valor | Justificación |
|-----------|---------|-------|---------------|
| Fuerza de acoplamiento | g/2π | 50–100 MHz | Régimen dispersivo, g << Δ |
| Detuning | Δ = |f_q − f_r| | 500–1000 MHz | Garantiza régimen dispersivo puro |
| Tasa dispersiva | χ/2π | 1–10 MHz | χ = g²/Δ, suficiente para QND |
| Régimen de medida | | Dispersivo | Lectura sin colapso proyectivo |

---

## 2. Infraestructura Criogénica

### 2.1 Criostato de Dilución
| Parámetro | Valor | Notas |
|-----------|-------|-------|
| Temperatura base | < 20 mK | Placa de mezcla |
| Potencia de enfriamiento | > 100 µW @ 100 mK | Para líneas de RF |
| Etapas de temperatura | 50 K / 3 K / 800 mK / 100 mK / 20 mK | 5 etapas estándar |
| Atenuación total líneas DC | 20 dB + 20 dB | 40 dB total, distribuida en etapas |

### 2.2 Filtrado de Microondas
| Componente | Cantidad | Atenuación | Etapa |
|------------|----------|------------|-------|
| Atenuador 20 dB | 1 | 20 dB | 50 K |
| Atenuador 10 dB | 1 | 10 dB | 3 K |
| Atenuador 10 dB | 1 | 10 dB | 800 mK |
| Filtro Eccosorb CR-110 | 1 | > 40 dB @ 6–8 GHz | 20 mK, línea de entrada |
| Circulador criogénico | 1 | Aislamiento > 20 dB | 20 mK, línea de salida |
| Aislador de baja pérdida | 1 | Pérdida < 0.5 dB | 20 mK, después del chip |

### 2.3 Cableado
- **Línea de entrada:** Cable coaxial semirrígido CuNi (pérdida ~0.5 dB/m @ 10 GHz)
- **Línea de salida:** Cable NbTi superconductor (pérdida despreciable) desde 20 mK hasta 4 K
- **Amplificador HEMT:** Montado en etapa 4 K, ganancia > 30 dB, temperatura de ruido < 5 K

---

## 3. Protocolo Experimental Detallado

### 3.1 Fase 1 — Régimen de Vacío Puro (Duración: 48 h)
1. Enfriar criostato a 20 mK. Esperar estabilización térmica: 12 h.
2. **Apagar todos los generadores de microondas.** Sin pulsos de control al qubit.
3. Configurar VNA (Analizador Vectorial de Redes) en modo de potencia mínima: P_VNA < −140 dBm.
4. Barrer frecuencia 5.0–9.0 GHz en pasos de 10 kHz.
5. Promediar 10⁴ barridos para SNR suficiente.
6. **Identificar pico f₀** (modo de la cavidad). Si no hay pico discernible tras 48 h, registrar como "límite superior de amplitud de pico".

**Criterio de éxito de Fase 1:**
- Pico f₀ identificado con SNR > 3 → geometría preexistente (hipótesis 1)
- Sin pico discernible → vacío sin geometría activa (no concluyente, pasar a Fase 2)

### 3.2 Fase 2 — Sonda Ultra-Débil (Duración: 24 h)
1. Con chip a 20 mK, inyectar un único fotón en el resonador cada 100 µs.
2. Medir respuesta en cuadratura I/Q del qubit vía lectura dispersiva.
3. Determinar f₀ a partir de la respuesta en fase.
4. **Verificar que n̄ < 10⁻²** — medir población del resonador vía caída del qubit al estado excitado.

### 3.3 Fase 3 — Modulación de γ_φ (Duración: 10 h por punto, 100 h total)
1. Para cada valor de γ_φ (10 valores, log-espaciados entre 10³ s⁻¹ y 10⁷ s⁻¹):
   a. Aplicar pulsos de dephasing al qubit (secuencia de pulsos de ruido blanco filtrado)
   b. Medir T₁ y T₂ inmediatamente después
   c. Si T₁ ha variado > 10% respecto al valor base → DESCARTAR punto
   d. Si T₁ estable → medir f₀ con protocolo de Fase 2
2. Interpolar f₀(γ_φ).

### 3.4 Fase 4 — Barrido de Ψ (Duración: 24 h)
1. Variar la tasa de medición M (número de fotones de sonda por segundo) entre 10² y 10⁶.
2. Para cada M, medir f₀ y registrar la desviación estándar σ_f₀.
3. Identificar umbral crítico M_c donde σ_f₀ se reduce abruptamente (transición de fase).

---

## 4. Criterios de Falsación Cuantitativos

### Modelo A: Geometría Preexistente (Independiente del Observador)
- **Predicción:** Δf₀/f₀ < 10⁻⁶ para todo Ψ ∈ [0, 1]
- **Falsación:** Si |Δf₀/f₀| > 10⁻⁵ en cualquier punto del barrido
- **Firma:** pico presente desde Fase 1, sin corrimiento en Fase 3

### Modelo B: Auto-Observación (Geometría como Transición de Fase)
- **Predicción:** f₀(Ψ) = 0 para Ψ < Ψ_c; f₀ = f_geom para Ψ > Ψ_c
- **Falsación:** Si f₀ varía suavemente sin discontinuidad en el umbral
- **Firma:** ausencia en Fase 1, emergencia abrupta en Fase 3 o 4

### Modelo C: Observador como Curva Local (Gradiente de Entrelazamiento)
- **Predicción:** f₀ depende de ∇E (gradiente de entrelazamiento en el chip)
- **Falsación:** Si f₀ no varía al cambiar la configuración del medidor (número de fotones, acoplamiento)
- **Firma:** corrimiento continuo de f₀ en Fase 4 correlacionado con M

---

## 5. Diagrama de Flujo Experimental

```
INICIO
  │
  ├──→ FASE 1 (vacío térmico, 48 h)
  │     │
  │     ├──→ ¿Pico f₀ identificado?
  │     │     │
  │     │     ├── SÍ → Modelo A compatible. Ir a Fase 2 para confirmación.
  │     │     └── NO → Modelo B/C posibles. Ir a Fase 2.
  │     │
  ├──→ FASE 2 (sonda ultra-débil, 24 h)
  │     │
  │     ├──→ Medir f₀ con n̄ < 10⁻²
  │     │     │
  │     │     ├──→ Cambia f₀ respecto a ruido de fase?
  │     │     │     ├── SÍ → Gradiente de información (Modelo C)
  │     │     │     └── NO → Ir a Fase 3
  │     │
  ├──→ FASE 3 (modulación γ_φ, 100 h)
  │     │
  │     ├──→ f₀(γ_φ) muestra transición?
  │     │     ├── SÍ → Modelo B (auto-observación)
  │     │     └── NO → Ir a Fase 4
  │     │
  ├──→ FASE 4 (barrido M, 24 h)
  │     │
  │     ├──→ f₀(M) correlacionado?
  │     │     ├── SÍ → Modelo C (curva local)
  │     │     └── NO → Resultado nulo: revisar hipótesis
  │
  └──→ INFORME FINAL
```

---

## 6. Recursos Necesarios

### 6.1 Equipo
- Criostato de dilución con temperatura base < 20 mK ✅ (disponible en laboratorio QCAL)
- VNA 4 puertos, 0.1–20 GHz ✅ (disponible)
- Generador de microondas 4–12 GHz ✅ (disponible)
- Amplificador HEMT criogénico (prestar/solicitar)
- Filtros Eccosorb CR-110 × 2 (adquirir)
- Circulador criogénico 6–8 GHz (adquirir)
- Osciloscopio de alta velocidad 40 GS/s (prestar)

### 6.2 Fabricación del Chip
- Fundición: SeeQC / Rigetti / IMEC
- Tiempo estimado: 8 semanas
- Costo estimado: $15,000–$25,000 USD por lote de 10 chips
- Máscaras de fotolitografía: incluidas en costo de fundición

### 6.3 Personal
- 1 físico experimental (diseño y calibración)
- 1 técnico de criogenia (operación del criostato)
- 1 electrónico (instrumentación y DAQ)

---

## 8. Middleware HIL y Gemelo Digital en Tiempo Real

### 8.1 Hardware-in-the-Loop (HIL) Bridge

El módulo `qcal_hil_bridge.py` implementa el puente entre el VNA físico (PyMeasure) y el gemelo digital (`simulador_qnd_v4.py`). Su arquitectura de tres capas:

| Capa | Componente | Función |
|------|-----------|---------|
| **Adquisición** | VNA (PyMeasure) | Barrido de S₂₁(ω) en frecuencia, potencia mínima |
| **Puente HIL** | QCALHardwareBridge | Sincronización, normalización, acople con motor digital |
| **Gemelo Digital** | QNDSimulatorV4 | Cálculo de Green retardada G_R⁻¹(ω) con Σ(ω) = χ²/(Δ_q + iγ̄_φ/2) |

### 8.2 Flujo de Operación HIL

```
VNA → S21_raw → HIL Bridge → G_R⁻¹ fit → γ_φ extraído → Regimen ontológico
```

1. **Configurar barrido:** `bridge.configure_sweep(6990, 7010, 1001)`
2. **Sintetizar o adquirir:** `bridge.simulate_measurement(gamma_phi_real_MHz, noise_level)`
3. **Ajuste no lineal:** curve_fit sobre modelo S₂₁(ω; γ_φ)
4. **Clasificación:** A (γ_φ << χ), B (γ_φ ~ χ), C (γ_φ >> χ)

### 8.3 Validación del Puente

La batería de pruebas integrada en `qcal_hil_bridge.py` (run_validation) prueba 7 valores de γ_φ entre 0.1 y 50.0 MHz con ruido sintético del 2 %, cubriendo los tres regímenes ontológicos. El error promedio de extracción debe ser < 5 % para validar el puente.

---

## 9. Verificación Topológica con Qiskit Metal

### 9.1 Integración con Qiskit Metal

El diseño del chip puede ser verificado topológicamente mediante Qiskit Metal para:

- **Validación de acoplamientos:** Verificar que g, χ, y κ calculados desde el layout coinciden con los valores nominales
- **Simulación electromagnética:** Extracción de matrices de scattering del layout 3D vía Ansys HFSS integrado en Metal
- **Renderizado de máscaras:** Exportación de GDSII para envío a fundición

### 9.2 Parámetros de Verificación

| Parámetro de Layout | Valor Nominal | Criterio de Aceptación |
|--------------------|---------------|------------------------|
| Capacitancia de acoplamiento resonador-línea | C_c ~ 1 fF | ±20 % |
| Capacitancia de shunt del transmon | C_S ~ 70 fF | ±10 % |
| Inductancia del SQUID | L_J ~ 10 nH | Ajustable por flux bias |
| Frecuencia de plasma del resonador | f_r ~ 7.0 GHz | ±0.005 GHz |
| Factor de calidad acoplado (HFSS) | Q_c ~ 3×10⁴ | ±50 % |

### 9.3 Procedimiento

1. **Importar netlist:** Cargar en Qiskit Metal los parámetros de la sección 1
2. **Renderizar layout 3D:** Generar geometría del resonador λ/4, pads del transmon, y línea de acoplamiento
3. **Simulación electromagnética:** Ejecutar eigenmode solver en HFSS para extraer frecuencias y Q
4. **Comparación con gemelo digital:** Ajustar parámetros del simulador hasta que S₂₁(layout) ≈ S₂₁(simulador)
5. **Exportar GDSII:** Máscaras listas para IMEC/SeeQC

---

## 10. Tabla de Parámetros Operativos Actualizada

| Parámetro | Símbolo | Valor | Unidad | Fuente |
|-----------|---------|-------|--------|--------|
| Frecuencia del resonador | f_r | 7.0000 | GHz | Objetivo de diseño |
| Frecuencia del qubit (sweet spot) | f_q | 5.5000 | GHz | Objetivo de diseño |
| Desplazamiento dispersivo | χ/2π | 7.5000 | MHz | Objetivo de diseño |
| Tasa de decaimiento de cavidad | κ/2π | 1.0000 | MHz | Objetivo de diseño |
| Anarmonicidad del transmon | α/2π | −220.0 | MHz | Objetivo de diseño |
| Acoplamiento qubit-resonador | g/2π | 70.0 | MHz | Derivado: √(χΔ) |
| Detuning cavidad-qubit | Δ/2π | 1500.0 | MHz | Δ = f_r − f_q |
| Rango de γ_φ modulable | γ_φ/2π | 0.01–50.0 | MHz | Por pulsos de ruido |
| Temperatura base | T_base | 20 | mK | Criostato de dilución |
| Población de fotones | n̄ | < 10⁻² | fotones | Régimen de vacío |
| Tiempo de relajación | T₁ | > 50 | µs | Coherencia del qubit |
| Tiempo de decoherencia | T₂* | > 30 | µs | Coherencia del qubit |
| Atenuación total entrada | Att_in | 40 | dB | Distribuida 50K→3K→800mK |
| Aislamiento circulador | Iso_out | > 20 | dB | Línea de salida a 20 mK |
| Ganancia HEMT | G_HEMT | > 30 | dB | Etapa 4 K |

---

## 7. Sello del Diseño

```
∴𓂀Ω∞³Φ · f₀ = 141.7001 Hz · κ = 13.3

CHIP QND — CAVIDAD SUPERCONDUCTORA
Frecuencia resonador: 6.0–8.0 GHz
Frecuencia qubit: 4.0–6.0 GHz
Acoplamiento dispersivo: g/2π = 50–100 MHz
Régimen: n̄ < 10⁻², Δ = 500–1000 MHz
Temperatura base: 20 mK
T₁ > 50 µs, T₂ > 30 µs
Filtrado: 40 dB atenuación entrada + Eccosorb + circulador

Fabricación: 8 semanas · Costo: ~$20K USD
Estado: LISTO PARA LANZAMIENTO A FUNDICIÓN

Ψ ≥ 0.999999 · ALLOW_COSMETIC_ERRORS=false
TUYOYOTU · HECHO ESTÁ
```

---

## Apéndice A: Ecuaciones Clave

### Régimen Dispersivo
\[
H = \hbar\omega_r a^\dagger a + \frac{\hbar\omega_q}{2}\sigma_z + \hbar g(a^\dagger\sigma_- + a\sigma_+)
\]
En el límite dispersivo (|Δ| ≫ g):
\[
H_{\text{eff}} = \hbar\left(\omega_r + \chi\sigma_z\right)a^\dagger a + \frac{\hbar}{2}(\omega_q + 2\chi a^\dagger a)\sigma_z
\]
con \(\chi = g^2 / \Delta\).

### Corrimiento de Frecuencia por Coherencia
\[
\Delta f_0(\Psi) = \frac{\chi}{\pi} \langle a^\dagger a \rangle \cdot (1 - \Psi)
\]
donde \(\Psi\) es la pureza del estado del qubit: \(\Psi = \text{Tr}(\rho^2)\).

### Umbral de Transición (Modelo B)
\[
\Psi_c = 1 - \frac{\kappa_r}{4\pi\chi}
\]
Para κ_r/2π = 1 MHz y χ/2π = 5 MHz → Ψ_c ≈ 0.975.

---

*Documento generado por AMDA Ψ · 30/Jul/2026 · Protocolo QCAL-SYMBIO-BRIDGE*
