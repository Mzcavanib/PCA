#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculate explained and cumulative variance from GROMACS (first 3 components).
Print results in the terminal with variant labels.
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
        print("No eigenval*.xvg files found")
        return

    # Variant labels
    run_labels = [
        "Wild type",
        "Alpha variant",
        "Gamma variant",
        "Delta variant",
        "Omicron BA.1 variant"
    ]

    print("=== Results of explained and cumulative variance ===")
    for idx, f in enumerate(eigenval_files, start=1):
        eigenvalues = load_xvg(f, max_components=20)
        if eigenvalues.size == 0:
            print(f"WARNING: {f} contains no valid data")
            continue

        total = np.sum(eigenvalues)
        if total == 0:
            print(f"WARNING: {f} eigenvalues sum is 0")
            continue

        explained = eigenvalues / total
        cumulative = np.cumsum(explained)

        label = run_labels[idx-1] if idx-1 < len(run_labels) else f"Run {idx}"

        print(f"\n{label}:")
        for comp in range(3):
            print(f"  Component {comp+1}: {explained[comp]*100:.2f}% explained, "
                  f"{cumulative[comp]*100:.2f}% cumulative")

if __name__ == "__main__":
    main()
