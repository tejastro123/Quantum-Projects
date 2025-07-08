from qiskit import QuantumCircuit

def build_circuit(secret_string="101"):
    n = len(secret_string)
    qc = QuantumCircuit(n + 1, n)

    # Initialize last qubit to |1>
    qc.x(n)
    qc.h(range(n + 1))

    # Oracle for secret string
    for i, bit in enumerate(secret_string):
        if bit == '1':
            qc.cx(i, n)

    # Hadamard + Measure
    qc.h(range(n))
    qc.barrier()
    qc.measure(range(n), range(n))
    return qc
