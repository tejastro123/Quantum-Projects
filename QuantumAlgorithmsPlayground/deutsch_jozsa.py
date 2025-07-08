from qiskit import QuantumCircuit
from qiskit.circuit.library import ZGate

def build_circuit():
    n = 3  # Number of input qubits
    qc = QuantumCircuit(n + 1, n)

    # Initialize last qubit to |1>
    qc.x(n)
    qc.h(range(n + 1))

    # Oracle: Constant or Balanced
    # Here: Balanced oracle (Z on first qubit)
    qc.cz(0, n)

    # Hadamard before measurement
    qc.h(range(n))
    qc.barrier()

    qc.measure(range(n), range(n))
    return qc
