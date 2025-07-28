import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from evaluation.avalanche_criterion import avalanche_criterion
from evaluation.fixed_points import fixed_ponts
from evaluation.uniformity import get_ddt
from sboxes.loader import load as load_sbox


def get_metrics(specs: list[dict], non_linearities: list[float]):
    """
    Calcula métricas básicas para un conjunto de S-Boxes.
    """
    metrics = []

    for i, spec in enumerate(specs):
        sbox = spec['sbox']
        ddt = get_ddt(sbox)
        max_ddt = np.max(ddt[1:])        # ignoramos dx = 0
        uniformity = max_ddt
        fixed = fixed_ponts(sbox, detail=True)[1]
        non_lin = non_linearities[i] if i < len(non_linearities) else None

        # Avalanche
        avg_sac, _, stds, max_std = avalanche_criterion(sbox)

        metrics.append({
            'name': spec['name'],
            'uniformity': uniformity,
            'max_ddt': np.max(ddt),
            'fixed_points': fixed,
            'non_linearity': non_lin,
            'avg_sac': avg_sac,
            'max_std_sac': max_std
        })

    return pd.DataFrame(metrics)


def plot_metric_bars(df: pd.DataFrame, metric: str, title: str = None):
    """
    Crea un gráfico de barras para una métrica específica.
    """
    plt.figure(figsize=(7, 4))
    sns.barplot(data=df, x='name', y=metric, hue='name', palette='tab10', legend=False)
    #sns.barplot(data=df, x='name', y=metric, palette='tab10')
    plt.title(title or metric.replace('_', ' ').title())
    plt.xlabel('S-Box')
    plt.ylabel(metric.replace('_', ' ').title())
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.show()


def run_all_metrics(specs, non_linearities, filename:str ="sbox_metrics_summary"):
    df = get_metrics(specs, non_linearities)

    # Mostrar como tabla
    print("\n=== Métricas de S-Boxes ===")
    print(df.to_string(index=False))

    # Graficar cada métrica
    for col in ['uniformity', 'max_ddt', 'fixed_points', 'non_linearity', 'avg_sac', 'max_std_sac']:
        plot_metric_bars(df, col, title=f"{col.replace('_', ' ').title()}")
    df.to_csv(f"{filename}.csv", index=False)
    return df


if __name__ == "__main__":
    # Carga ejemplo
    specs = []
    to_proof = ["ascon", "nuestro 5.v1", "nuestro 5.v2", "nuestro 5.v3"]
    for sbox_link in to_proof:
        sbox = load_sbox(f"sboxes/data/{sbox_link}.json")
        specs.append({
            'name': sbox_link,
            'table': sbox.table.tolist(),
            'n_in': sbox.input_size,
            'n_out': sbox.output_size,
            'color': None,
            'sbox': sbox
        })

    non_linearities = [12, 14, 16, 16]  # ejemplo, reemplaza con tus valores reales

    run_all_metrics(specs, non_linearities)
