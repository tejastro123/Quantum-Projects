import random
import numpy as np


class BB84Simulator:
    def __init__(self, num_qubits=100, eavesdropper=False, seed=None):
        self.num_qubits = num_qubits
        self.eavesdropper = eavesdropper
        self.random = random.Random(seed)

        # Protocol data
        self.alice_bits = []
        self.alice_bases = []
        self.bob_bases = []
        self.bob_results = []
        self.eve_bases = []
        self.eve_results = []

        self.matching_indices = []
        self.raw_key = []
        self.qber = 0.0

    def generate_random_bits(self, length):
        return [self.random.randint(0, 1) for _ in range(length)]

    def generate_random_bases(self, length):
        return [self.random.choice(['Z', 'X']) for _ in range(length)]

    def encode_qubits(self):
        self.alice_bits = self.generate_random_bits(self.num_qubits)
        self.alice_bases = self.generate_random_bases(self.num_qubits)

    def intercept_eavesdropper(self):
        self.eve_bases = self.generate_random_bases(self.num_qubits)
        self.eve_results = []

        for bit, basis, eve_basis in zip(self.alice_bits, self.alice_bases, self.eve_bases):
            if basis == eve_basis:
                self.eve_results.append(bit)
            else:
                self.eve_results.append(self.random.randint(0, 1))

    def bob_measurement(self):
        self.bob_bases = self.generate_random_bases(self.num_qubits)
        self.bob_results = []

        for i in range(self.num_qubits):
            bit = self.alice_bits[i]
            alice_basis = self.alice_bases[i]
            bob_basis = self.bob_bases[i]

            if self.eavesdropper:
                eve_bit = self.eve_results[i]
                eve_basis = self.eve_bases[i]

                # Bob gets qubit from Eve
                if eve_basis == bob_basis:
                    self.bob_results.append(eve_bit)
                else:
                    self.bob_results.append(self.random.randint(0, 1))
            else:
                if alice_basis == bob_basis:
                    self.bob_results.append(bit)
                else:
                    self.bob_results.append(self.random.randint(0, 1))

    def extract_key(self):
        self.matching_indices = []
        self.raw_key = []

        for i in range(self.num_qubits):
            if self.alice_bases[i] == self.bob_bases[i]:
                self.matching_indices.append(i)
                self.raw_key.append(self.bob_results[i])

    def compute_qber(self):
        if not self.matching_indices:
            self.qber = 0.0
            return

        error_count = 0
        for i in self.matching_indices:
            if self.alice_bits[i] != self.bob_results[i]:
                error_count += 1
        self.qber = error_count / len(self.matching_indices)

    def run(self):
        self.encode_qubits()
        if self.eavesdropper:
            self.intercept_eavesdropper()
        self.bob_measurement()
        self.extract_key()
        self.compute_qber()

    def summary(self):
        return {
            "num_qubits": self.num_qubits,
            "eavesdropper": self.eavesdropper,
            "alice_bits": self.alice_bits,
            "alice_bases": self.alice_bases,
            "bob_bases": self.bob_bases,
            "bob_results": self.bob_results,
            "matching_indices": self.matching_indices,
            "raw_key": self.raw_key,
            "qber": round(self.qber * 100, 2)
        }

if __name__ == "__main__":
    sim = BB84Simulator(num_qubits=100, eavesdropper=False, seed=42)
    sim.run()
    result = sim.summary()

    print(f"Qubits Sent: {result['num_qubits']}")
    print(f"Eavesdropper Present: {result['eavesdropper']}")
    print(f"QBER: {result['qber']}%")
    print(f"Matching Positions: {result['matching_indices']}")
    print(f"Final Shared Key: {''.join(map(str, result['raw_key']))}")
