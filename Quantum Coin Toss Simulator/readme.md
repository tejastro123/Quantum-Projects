
# 🪙 Quantum Coin Toss Simulator

## 📌 Overview

**Title**: Quantum Coin Toss Simulator
**Goal**: Simulate coin tosses using quantum mechanics (Hadamard gate), compare with classical RNG, and visualize results to understand quantum superposition and measurement.

---

## 🔍 Introduction

In classical computing, coin tosses are simulated using pseudo-random number generators. In quantum computing, however, we can simulate a coin toss using **quantum superposition** and **measurement** of a qubit in the computational basis.

A quantum coin toss uses a **Hadamard gate** to place a qubit in a 50/50 superposition of `|0⟩` and `|1⟩`. Measuring this qubit collapses the state to either `0` (heads) or `1` (tails), with equal probability.

---

## 📖 Quantum Concept

### ❓ What is a Qubit?

A qubit is the fundamental unit of quantum information. Unlike classical bits (`0` or `1`), qubits can exist in a **superposition** of both states:

$$
|\psi⟩ = \alpha|0⟩ + \beta|1⟩ \quad \text{with } |\alpha|^2 + |\beta|^2 = 1
$$

### ⚙️ How Coin Toss Works

1. **Initialize**: Start with a qubit in the `|0⟩` state.
2. **Apply Hadamard Gate**: Brings the qubit into a superposition:

$$
H|0⟩ = \frac{1}{\sqrt{2}}(|0⟩ + |1⟩)
$$

3. **Measure**: Collapses to either `0` or `1` with 50% probability each.

---

## 🧪 Implementation (Quantum)

### ✅ Tools Used

* [Qiskit](https://qiskit.org)
* Python 3.x
* Matplotlib for visualization


## 📊 Results & Analysis

| Method    | Heads (0) | Tails (1) |
| --------- | --------- | --------- |
| Quantum   | \~500     | \~500     |
| Classical | \~500     | \~500     |

* Both methods **approximate 50/50 probability** over large trials.
* Quantum method is **inherently non-deterministic**, based on physical principles of quantum mechanics.
* Classical RNGs are **pseudo-random** — deterministic algorithms emulating randomness.

---

## 📚 Learning Outcomes

1. 🧠 Understood **quantum measurement** and **Hadamard gates**.
2. 🪙 Learned how to **simulate quantum coin tosses** using Qiskit.
3. 📈 Visualized and **compared quantum vs classical randomness**.
4. 🛠️ Gained hands-on practice with **quantum circuits and classical Python RNGs**.

---

## 🌱 Extensions & Future Work

* 🧪 Run the quantum toss on real IBMQ hardware (using `IBMQ.load_account()`).
* 📉 Plot multiple runs and analyze statistical variance.
* 🔐 Use QRNG in cryptographic applications.
* 🧮 Extend to **quantum dice simulator** or **multi-qubit games**.

---

## 📦 Project Structure

```
Quantum-Coin-Toss/
│
├── quantum_coin_toss.py       # Qiskit-based simulation
├── classical_coin_toss.py     # Python RNG-based simulation
├── README.md                  # Project overview and instructions
└── results/                   # (optional) Plots and saved outputs
```

---

## 📜 License & Credits

* Qiskit © IBM
* Project by **Tejas Mellimpudi**
* Licensed under MIT License

---

Would you like a `README.md` and GitHub structure for this project too?
