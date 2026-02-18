#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Graficar múltiples curvas de eigenvalues y varianza explicada de GROMACS.
Busca archivos enumerados como eigenval1.xvg, eigenval2.xvg, etc.
Valida que exista el par eigenvecN.trr correspondiente.
"""

import numpy as np
import matplotlib.pyplot as plt
import glob
import os

def load_xvg(path):
    """Carga eigenvalores desde archivo .xvg ignorando comentarios (#,@)."""
    data = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("@"):
                continue
            parts = line.split()
            try:
                val = float(parts[-1])
                data.append(val)
            except ValueError:
                continue
    return np.array(data, dtype=float)

def main():
    # --- Checkpoint: Detectar archivos eigenval*.xvg ---
    eigenval_files = sorted(glob.glob("eigenval*.xvg"))
    if not eigenval_files:
        print("No se encontraron archivos eigenval*.xvg")
        return

    print("Archivos encontrados:", eigenval_files)

    # --- Gráfico de la curva de eigenvalues ---
    plt.figure(figsize=(9,6))
    cmap = plt.cm.get_cmap("tab10", len(eigenval_files))

    for idx, f in enumerate(eigenval_files, start=1):
        eigenvalues = load_xvg(f)
        components = np.arange(1, len(eigenvalues) + 1)

        # CHeckpoint: Validar existencia del eigenvec correspondientes
        trr_file = f.replace("eigenval", "eigenvec").replace(".xvg", ".trr")
        if os.path.isfile(trr_file):
            print(f"CHECK: {trr_file} encontrado para {f}")
        else:
            print(f"WARNING: No existe {trr_file} para {f}")

        # Curva de eigenvalues
        plt.plot(components, eigenvalues, marker="o",
                 color=cmap(idx-1), label=f"Run {idx}")

    plt.xlabel("Componentes principales")
    plt.ylabel("Eigenvalues")
    plt.title("Comparación de Eigenvalues Componentes principales")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()

    # --- Varianza explicada ---
    plt.figure(figsize=(9,6))

    for idx, f in enumerate(eigenval_files, start=1):
        eigenvalues = load_xvg(f)
        components = np.arange(1, len(eigenvalues) + 1)

        # Cálculo de la varianza explicada y acumulada
        total = np.sum(eigenvalues)
        explained = eigenvalues / total
        cumulative = np.cumsum(explained)

        # Gráfico de las barras de varianza explicada
        plt.bar(components + 0.1*idx, explained*100, width=0.1,
                label=f"Run {idx} varianza")

        # Gráfico de línea acumulada
        plt.plot(components, cumulative*100, marker="o",
                 color=cmap(idx-1), linestyle="--",
                 label=f"Run {idx} acumulada")

    plt.xlabel("Componentes principales")
    plt.ylabel("Porcentaje (%)")
    plt.title("Varianza explicada y acumulada por componente")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()

