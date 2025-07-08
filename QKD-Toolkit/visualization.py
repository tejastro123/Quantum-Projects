import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from simulator import BB84Simulator


def plot_qber_comparison(qber_with_eve, qber_without_eve):
    labels = ['With Eve', 'Without Eve']
    values = [qber_with_eve, qber_without_eve]

    plt.figure(figsize=(6, 4))
    sns.barplot(x=labels, y=values, palette='hue')
    plt.title('QBER Comparison')
    plt.ylabel('QBER (%)')
    plt.ylim(0, 100)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()


def plot_basis_comparison(alice_bases, bob_bases):
    match = [1 if a == b else 0 for a, b in zip(alice_bases, bob_bases)]
    indices = np.arange(len(alice_bases))

    plt.figure(figsize=(10, 3))
    plt.scatter(indices, match, c=match, cmap='coolwarm', marker='|', s=100)
    plt.title("Alice vs Bob Basis Match")
    plt.xlabel("Qubit Index")
    plt.ylabel("Match (1=True, 0=False)")
    plt.yticks([0, 1])
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()


def plot_bit_agreement(alice_bits, bob_results, matching_indices):
    agreements = [1 if alice_bits[i] == bob_results[i] else 0 for i in matching_indices]
    indices = np.arange(len(agreements))

    plt.figure(figsize=(10, 3))
    sns.heatmap([agreements], cmap='Greens', cbar=True, xticklabels=indices)
    plt.title("Bit Agreement in Matching Bases (Alice vs Bob)")
    plt.xlabel("Matching Index")
    plt.yticks([])
    plt.tight_layout()
    plt.show()


def plot_matching_index_distribution(matching_indices, total_qubits):
    data = [1 if i in matching_indices else 0 for i in range(total_qubits)]

    plt.figure(figsize=(10, 2))
    plt.bar(range(total_qubits), data, color='skyblue')
    plt.title("Basis Matching Distribution")
    plt.xlabel("Qubit Index")
    plt.ylabel("Match")
    plt.yticks([0, 1])
    plt.tight_layout()
    plt.show()


def plot_qber_vs_key_length(qber_values, key_lengths, eavesdropper_flags):
    colors = ['red' if e else 'green' for e in eavesdropper_flags]

    plt.figure(figsize=(8, 5))
    plt.scatter(qber_values, key_lengths, c=colors, s=80, edgecolors='black')
    for i, e in enumerate(eavesdropper_flags):
        label = "Eve" if e else "No Eve"
        plt.text(qber_values[i] + 0.5, key_lengths[i] + 0.5, label, fontsize=8)

    plt.title("Key Length vs QBER")
    plt.xlabel("QBER (%)")
    plt.ylabel("Key Length (bits)")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    
    # Run simulations
    sim_eve = BB84Simulator(100, eavesdropper=True)
    sim_eve.run()
    res_eve = sim_eve.summary()

    sim_no_eve = BB84Simulator(100, eavesdropper=False)
    sim_no_eve.run()
    res_no_eve = sim_no_eve.summary()

    # Visualize QBER comparison
    plot_qber_comparison(res_eve['qber'], res_no_eve['qber'])

    # Basis match
    plot_basis_comparison(res_eve['alice_bases'], res_eve['bob_bases'])

    # Bit agreement heatmap
    plot_bit_agreement(res_eve['alice_bits'], res_eve['bob_results'], res_eve['matching_indices'])

    # Matching index distribution
    plot_matching_index_distribution(res_eve['matching_indices'], res_eve['num_qubits'])

    # For multi-run QBER vs key length plot:
    qbers = [res_eve['qber'], res_no_eve['qber']]
    key_lengths = [len(res_eve['raw_key']), len(res_no_eve['raw_key'])]
    flags = [True, False]
    plot_qber_vs_key_length(qbers, key_lengths, flags)
    

