from qiskit_aer import Aer
from qiskit import transpile
from qiskit.visualization import plot_histogram

def simulate(qc):
    backend = Aer.get_backend('qasm_simulator')
    transpiled = transpile(qc, backend)
    job = backend.run(transpiled, shots=1024)
    result = job.result()
    counts = result.get_counts()
    return result, counts
