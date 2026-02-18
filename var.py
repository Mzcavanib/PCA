#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calcular varianza explicada y acumulada de GROMACS (primeros 3 componentes).
Imprime resultados en la terminal con etiquetas de variantes.
"""

import numpy as np
import glob
import os

def load_xvg(path, max_components=None):
    data = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("@"):
                continue
            parts = line.split()
            try:
                val = float(parts[1]) if len(parts) >= 2 else float(parts[0])
                data.append(val)
            except (ValueError, IndexError):
                continue
            if max_components is not None and len(data) >= max_components:
                break
    return np.array(data, dtype=float)

def main():
    eigenval_files = sorted(glob.glob("eigenval*.xvg"))
    if not eigenval_files:
        print("No se encontraron archivos eigenval*.xvg")
        return

    # Etiquetas de variantes
    run_labels = [
        "Wild type",
        "Variante Alpha",
        "Variante Gamma",
        "Variante Delta",
        "Variante Omicron BA.1"
    ]

    print("=== Resultados de varianza explicada y acumulada ===")
    for idx, f in enumerate(eigenval_files, start=1):
        eigenvalues = load_xvg(f, max_components=20)
        if eigenvalues.size == 0:
            print(f"WARNING: {f} no contiene datos válidos")
            continue

        total = np.sum(eigenvalues)
        if total == 0:
            print(f"WARNING: {f} suma de eigenvalues es 0")
            continue

        explained = eigenvalues / total
        cumulative = np.cumsum(explained)

        label = run_labels[idx-1] if idx-1 < len(run_labels) else f"Run {idx}"

        print(f"\n{label}:")
        for comp in range(3):
            print(f"  Componente {comp+1}: {explained[comp]*100:.2f}% explicado, "
                  f"{cumulative[comp]*100:.2f}% acumulado")

if __name__ == "__main__":
    main()

