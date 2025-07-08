import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram, circuit_drawer

def show_circuit(qc):
    fig = circuit_drawer(qc, output="mpl")
    plt.show()

def show_results(result, counts):
    plot_histogram(counts)
    plt.title("Measurement Results")
    plt.show()
