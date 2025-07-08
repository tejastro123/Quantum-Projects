from qiskit import QuantumCircuit
from qiskit_aer import Aer
import matplotlib.pyplot as plt

def quantum_coin_toss(shots=1000):
    # Step 1: Build circuit
    qc = QuantumCircuit(1, 1)
    qc.h(0)               # Apply Hadamard gate
    qc.measure(0, 0)      # Measure qubit

    # Step 2: Simulate
    backend = Aer.get_backend('qasm_simulator')
    job = backend.run(qc, shots=shots)
    result = job.result()
    counts = result.get_counts()

    # Step 3: Plot
    labels = ['Heads (0)', 'Tails (1)']
    values = [counts.get('0', 0), counts.get('1', 0)]
    plt.bar(labels, values, color=['skyblue', 'salmon'])
    plt.title(f"Quantum Coin Toss - {shots} Trials")
    plt.ylabel("Frequency")
    plt.show()

    return counts

if __name__ == "__main__":
    counts = quantum_coin_toss(1000)
    print("Quantum Toss Result:", counts)
