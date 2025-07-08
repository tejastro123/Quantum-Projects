from qiskit import QuantumCircuit
from qiskit.circuit.library import ZGate

def build_circuit(oracle_string="11"):
    n = len(oracle_string)
    qc = QuantumCircuit(n, n)

    # Step 1: Hadamard all qubits
    qc.h(range(n))

    # Step 2: Oracle (Z gate on target state)
    oracle = QuantumCircuit(n)
    for i, bit in enumerate(oracle_string):
        if bit == '0':
            oracle.x(i)
    oracle.h(n - 1)
    oracle.mcx(list(range(n - 1)), n - 1)
    oracle.h(n - 1)
    for i, bit in enumerate(oracle_string):
        if bit == '0':
            oracle.x(i)
    qc.append(oracle.to_gate(label="Oracle"), range(n))

    # Step 3: Diffuser
    qc.h(range(n))
    qc.x(range(n))
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    qc.x(range(n))
    qc.h(range(n))

    qc.measure(range(n), range(n))
    return qc
