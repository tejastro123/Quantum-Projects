from qiskit import QuantumCircuit
from qiskit_aer import Aer
from typing import List

def create_qrng_circuit(n_bits: int) -> QuantumCircuit:
    qc = QuantumCircuit(n_bits, n_bits)
    for i in range(n_bits):
        qc.h(i)              # Apply Hadamard to place qubit in superposition
        qc.measure(i, i)     # Measure to collapse into 0 or 1
    return qc

def run_qrng(qc: QuantumCircuit) -> str:
    backend = Aer.get_backend('qasm_simulator')
    job = backend.run(qc, shots=1, memory=True)
    result = job.result()
    return ''.join(result.get_memory()[0][::-1])  # Reverse due to Qiskit bit ordering

def generate_random_numbers(n_bits: int, n_samples: int) -> List[str]:
    results = []
    for _ in range(n_samples):
        qc = create_qrng_circuit(n_bits)
        random_bitstring = run_qrng(qc)
        results.append(random_bitstring)
    return results
