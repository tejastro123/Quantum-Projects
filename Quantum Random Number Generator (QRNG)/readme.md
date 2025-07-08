# 🧿 Quantum Random Number Generator (QRNG)

A true quantum random number generator using Qiskit's quantum circuits. Uses Hadamard gates to generate unpredictable results.

## 🔧 Features

- Generates n-bit truly random numbers using superposition and quantum measurement.
- Can generate multiple samples efficiently.
- Useful for cryptography, secure keys, lotteries, simulations, etc.
- Simple CLI output and file export.

## 🧠 Concept

A Hadamard gate places a qubit in a superposition of |0⟩ and |1⟩. Measurement collapses it randomly. This process, repeated across multiple qubits and samples, gives you truly random binary numbers.

## 📦 Installation

```bash
git clone https://github.com/YOUR_USERNAME/qrng-project
cd qrng-project
pip install -r requirements.txt
