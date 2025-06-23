#!/usr/bin/env python3
"""
Script de lanzamiento para el Simulador Electoral Bolivia 2025
"""

import sys
import os

# Agregar el directorio src al path de Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gui.main_app import SimuladorElectoralApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorElectoralApp(root)
    root.mainloop() 