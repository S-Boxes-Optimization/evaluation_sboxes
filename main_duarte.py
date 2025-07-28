# compare_relaxation_and_bounds.py

import numpy as np
import math
from sboxes.loader import load as load_sbox
from evaluation.uniformity import ddt
from evaluation.markov_chains.basic_markov_chain import DifferentialMarkovChain, create_transition_matrix
from evaluation.avalanche_criterion import avalanche_criterion


import numpy as np
import matplotlib.pyplot as plt
from sboxes.loader import load as load_sbox
from evaluation.uniformity import ddt
from evaluation.markov_chains.basic_markov_chain import DifferentialMarkovChain
from evaluation.avalanche_criterion import print_avalanche_summary, plot_avalanche_matrix, IdentitySBox




def create_transition_matrix(sbox):
    """
    Crea la matriz de transición P para la DDT de la sbox.
    """
    table_list = list(sbox.table)
    # ddt espera (table, input_size, output_size)
    counts = ddt(table_list, int(sbox.input_size), int(sbox.output_size))
    # descartar dx = 0
    P = counts[1:,1:].astype(np.float64)
    # normalizar filas
    P /= P.sum(axis=1, keepdims=True)
    return P


def test_sbox_markov(sbox, epsilon=1e-4, r_values=[1,2,5,10]):
    """
    Prueba propiedades de la cadena de Markov generada por la sbox:
    - ergodicidad
    - doble estocasticidad
    - mixing times (iterativo y espectral)
    - tv_distance y max_probability para pasos r
    """
    print(f"\n=== Pruebas Markov para {type(sbox).__name__} ===")
    P = create_transition_matrix(sbox)
    chain = DifferentialMarkovChain(P)

    # Propiedades
    print("Doble estocástica:", chain.is_doubly_stochastic())
    print("Irreducible:", chain.is_irreducible())
    print("Aperiodic:", chain.is_aperiodic())
    print("Ergódica:", chain.is_ergodic())

    # Mixing times
    tau_iter = chain.mixing_time_iterative(epsilon)
    tau_spec = chain.mixing_time_spectral(epsilon)
    print(f"Mixing time iterativo (ε={epsilon}): {tau_iter}")
    print(f"Mixing time espectral  (ε={epsilon}): {tau_spec}")

    # TV distance y max prob
    for r in r_values:
        tv = chain.tv_distance(r)
        mp = chain.max_probability(r)
        print(f"Paso {r}: TV_distance={tv:.6f}, max_probability={mp:.6f}")

    # Graficar TV distance vs r
    rs = list(range(1, max(r_values)+1))
    tvs = [chain.tv_distance(r) for r in rs]
    plt.figure()
    plt.plot(rs, tvs, marker='o')
    plt.title(f"TV Distance vs Steps for {type(sbox).__name__}")
    plt.xlabel("Steps r")
    plt.ylabel("TV Distance")
    plt.grid(True)
    plt.show()
    

from evaluation.fixed_points import fixed_ponts

def main():
    # Cargar ASCON
    ascon = load_sbox("sboxes/data/proof.json")

    flag, counter = fixed_ponts(ascon, detail = True)
    
    print(f"ASCON tiene punto fijo: {flag}, cantidad: {counter}")
    # Avalanche Criterion
    #print("=== Avalancha: ASCON ===")
    #print_avalanche_summary(ascon)
    #plot_avalanche_matrix(ascon)

    # Markov chain tests ASCON
    """test_sbox_markov(ascon)

    # Identity SBox
    print("\n=== Avalancha: Identity 4x4 ===")
    sbox_id = IdentitySBox(4)
    print_avalanche_summary(sbox_id)
    plot_avalanche_matrix(sbox_id)

    test_sbox_markov(sbox_id)
    
    
    ascon = load_sbox("sboxes/data/ascon.json")
    print("=== Avalanche Criterion: ASCON ===")
    print_avalanche_summary(ascon)
    plot_avalanche_matrix(ascon)

    print("\n=== Avalanche Criterion: Identity 4x4 ===")
    id4 = IdentitySBox(4)
    print_avalanche_summary(id4)
    plot_avalanche_matrix(id4)

    """


from evaluation.markov_chains.test_markov_chain import main as run_markov_tests
from evaluation.markov_chains.all_test_markov_chains import main as run_markov_tests_all
from evaluation.avalanche_criterion   import print_avalanche_summary, plot_avalanche_matrix
from sboxes.loader                    import load as load_sbox
from evaluation.identity_sbox         import IdentitySBox

def main_markov():
    run_markov_tests_all()
    
    
from sboxes.loader import load as load_sbox
from evaluation.identity_sbox import IdentitySBox
from evaluation.markov_chains.all_test_markov_chains import (
    compare_tv_distance,
    compare_max_probability,
    compare_mixing_times
)

def main_markov2():
    # Define la lista de S-Boxes para comparar
    specs = [
        {
            'name': 'ASCON',
            'table': load_sbox("sboxes/data/ascon.json").table.tolist(),
            'n_in': load_sbox("sboxes/data/ascon.json").input_size,
            'n_out': load_sbox("sboxes/data/ascon.json").output_size,
            'color': 'blue'
        },
        {
            'name': 'Identity 4x4',
            'table': IdentitySBox(4).table,
            'n_in': 4,
            'n_out': 4,
            'color': 'green'
        },
        # Agrega más S-Boxes aquí...
    ]

    # Comparaciones
    compare_tv_distance(specs)
    compare_max_probability(specs)
    compare_mixing_times(specs)


if __name__ == "__main__":
    #main_markov()
    main_markov2()
