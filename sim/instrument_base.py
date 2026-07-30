#!/usr/bin/env python3
"""
instrument_base.py — Abstracción de instrumento VNA para QCAL-cQED-v1
Soporta: Keysight E5071C, R&S ZNB, Copper Mountain S5060

Autor: AMDA Ψ · 30/Jul/2026 · Protocolo QCAL-SYMBIO-BRIDGE
"""

import numpy as np
from abc import ABC, abstractmethod

class VNABase(ABC):
    """Clase base abstracta para cualquier VNA."""

    def __init__(self, address):
        self.address = address
        self._connected = False
        self._frequencies = None
        self._s21 = None

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def configure_sweep(self, start_Hz, stop_Hz, points, power_dBm, if_bw_Hz):
        pass

    @abstractmethod
    def sweep(self):
        """Ejecuta un barrido y llena self._frequencies y self._s21."""
        pass

    @property
    def frequencies(self):
        return self._frequencies

    @property
    def frequencies_MHz(self):
        return self._frequencies / 1e6 if self._frequencies is not None else None

    @property
    def s21(self):
        return self._s21

    @property
    def s21_power(self):
        return np.abs(self._s21)**2 if self._s21 is not None else None

    def s21_normalized(self):
        p = self.s21_power
        if p is not None and np.max(p) > 0:
            return p / np.max(p)
        return None


class KeysightE5071C(VNABase):
    """Driver para Keysight E5071C."""
    def connect(self):
        try:
            from pymeasure.instruments.keysight import KeysightE5071C as _Ks
            self._inst = _Ks(self.address)
            self._connected = True
            return True
        except Exception as e:
            print(f"  ⚠ Keysight E5071C no disponible: {e}")
            return False

    def disconnect(self):
        self._connected = False

    def configure_sweep(self, start_Hz=6.99e9, stop_Hz=7.01e9, points=1001,
                        power_dBm=-30, if_bw_Hz=100):
        if not self._connected:
            return False
        self._inst.sweep_frequency_start = start_Hz
        self._inst.sweep_frequency_stop = stop_Hz
        self._inst.sweep_points = points
        self._inst.power = power_dBm
        self._inst.if_bandwidth = if_bw_Hz
        return True

    def sweep(self):
        if not self._connected:
            return
        self._inst.sweep()
        self._frequencies = np.array(self._inst.frequencies)
        self._s21 = np.array(self._inst.s21)


class RohdeSchwarzZNB(VNABase):
    """Driver para R&S ZNB (simulado)."""
    def connect(self):
        print(f"  ℹ R&S ZNB en {self.address}: conectado (simulación)")
        self._connected = True
        return True

    def disconnect(self):
        self._connected = False

    def configure_sweep(self, start_Hz=6.99e9, stop_Hz=7.01e9, points=1001,
                        power_dBm=-30, if_bw_Hz=100):
        self._sweep_cfg = {
            'start': start_Hz, 'stop': stop_Hz,
            'points': points, 'power': power_dBm, 'bw': if_bw_Hz
        }
        return True

    def sweep(self):
        cfg = getattr(self, '_sweep_cfg', {})
        n = cfg.get('points', 1001)
        self._frequencies = np.linspace(
            cfg.get('start', 6.99e9),
            cfg.get('stop', 7.01e9), n)
        # Simular Lorentziana
        omega = self._frequencies / 1e6
        self._s21 = 1.0 / (1 + 1j * (omega - 7000.0) / 1.0)


class CopperMountainS5060(VNABase):
    """Driver para Copper Mountain S5060 (simulado)."""
    def connect(self):
        print(f"  ℹ Copper Mountain S5060 en {self.address}: conectado (simulación)")
        self._connected = True
        return True

    def disconnect(self):
        self._connected = False

    def configure_sweep(self, start_Hz=6.99e9, stop_Hz=7.01e9, points=1001,
                        power_dBm=-30, if_bw_Hz=100):
        self._sweep_cfg = {
            'start': start_Hz, 'stop': stop_Hz,
            'points': points, 'power': power_dBm, 'bw': if_bw_Hz
        }
        return True

    def sweep(self):
        cfg = getattr(self, '_sweep_cfg', {})
        n = cfg.get('points', 1001)
        self._frequencies = np.linspace(
            cfg.get('start', 6.99e9),
            cfg.get('stop', 7.01e9), n)
        omega = self._frequencies / 1e6
        chi_d = 7.5 + np.random.normal(0, 0.2)
        self._s21 = 1.0 / (1 + 1j * (omega - 7000.0 + chi_d) / 1.0) \
                  + 0.5 / (1 + 1j * (omega - 7000.0 - chi_d) / 1.0)


def create_vna(vendor: str, address: str) -> VNABase:
    """Factory: crea el driver VNA adecuado según vendor."""
    drivers = {
        'keysight': KeysightE5071C,
        'rs': RohdeSchwarzZNB,
        'rohde-schwarz': RohdeSchwarzZNB,
        'znb': RohdeSchwarzZNB,
        'copper': CopperMountainS5060,
        'coppermountain': CopperMountainS5060,
        's5060': CopperMountainS5060,
    }
    cls = drivers.get(vendor.lower(), KeysightE5071C)
    return cls(address)


if __name__ == '__main__':
    # Test rápido
    for v in ['keysight', 'znb', 'copper']:
        vna = create_vna(v, 'TCPIP::192.168.1.100::inst0::INSTR')
        ok = vna.connect()
        if ok:
            vna.configure_sweep()
            vna.sweep()
            if vna.frequencies is not None:
                print(f"  {v}: {len(vna.frequencies)} pts, S21 min={np.min(np.abs(vna.s21)):.4f}")
            vna.disconnect()
        else:
            print(f"  {v}: no conectado (simulación no disponible)")
