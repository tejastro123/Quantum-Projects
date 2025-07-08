import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_bloch_multivector, plot_histogram, circuit_drawer
from qiskit.quantum_info import Statevector, DensityMatrix, state_fidelity
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Backend
sim = Aer.get_backend('aer_simulator')

# Function to create teleportation circuit
def create_teleportation_circuit(alpha, beta):
    qc = QuantumCircuit(3, 3)
    qc.initialize([alpha, beta], 0)
    qc.barrier()
    qc.h(1)
    qc.cx(1, 2)
    qc.barrier()
    qc.cx(0, 1)
    qc.h(0)
    qc.barrier()
    qc.measure(0, 0)
    qc.measure(1, 1)
    qc.measure(2, 2)
    # qc.x(2).c_if(qc.cregs[0], 1)
    # qc.z(2).c_if(qc.cregs[0], 2)
    # qc.z(2).c_if(qc.cregs[0], 3)
    return qc

class TeleportationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum Teleportation Simulator")
        self.root.geometry("1300x850")
        self.setup_gui()

    def setup_gui(self):
        self.notebook = ttk.Notebook(self.root)
        self.sim_tab = ttk.Frame(self.notebook)
        self.tutorial_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.sim_tab, text="Simulation")
        self.notebook.add(self.tutorial_tab, text="Tutorial")
        self.notebook.pack(fill="both", expand=True)

        # Sliders
        self.alpha_scale = tk.Scale(self.sim_tab, from_=0, to=1, resolution=0.01,
                                    orient=tk.HORIZONTAL, label="Alpha (Re)", length=300)
        self.alpha_scale.set(0.707)
        self.alpha_scale.pack()

        self.beta_scale = tk.Scale(self.sim_tab, from_=-1, to=1, resolution=0.01,
                                   orient=tk.HORIZONTAL, label="Beta (Im)", length=300)
        self.beta_scale.set(0.707)
        self.beta_scale.pack()

        ttk.Button(self.sim_tab, text="Run Teleportation", command=self.run_simulation).pack(pady=10)

        # Save Buttons
        btn_frame = ttk.Frame(self.sim_tab)
        btn_frame.pack()
        ttk.Button(btn_frame, text="Save Bloch Sphere", command=self.save_bloch).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Save Circuit", command=self.save_circuit).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Save Histogram", command=self.save_hist).grid(row=0, column=2, padx=5)

        # Canvas Frame
        self.canvas_frame = ttk.LabelFrame(self.sim_tab, text="Visualizations")
        self.canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.fig, self.axs = plt.subplots(1, 3, figsize=(15, 4))
        self.fig.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # State + Fidelity Info
        self.state_text = tk.Text(self.sim_tab, height=8, wrap=tk.WORD)
        self.state_text.pack(fill="both", padx=10, pady=5)

        # Tutorial Tab
        tutorial_info = """
        🔄 Quantum Teleportation Tutorial

        Quantum teleportation is a protocol to transfer an unknown quantum state |ψ⟩ from Alice (qubit 0) to Bob (qubit 2) using:
        1. Entangled Bell pair shared between Alice and Bob
        2. Classical communication of measurement results
        3. Conditional operations by Bob

        Steps:
        - Prepare |ψ⟩ on qubit 0
        - Create Bell pair between qubits 1 and 2
        - Apply CNOT and H to entangle qubit 0 with 1
        - Measure qubits 0 and 1 (Alice)
        - Bob applies corrections to recover |ψ⟩ on his qubit (qubit 2)
        """
        text_widget = tk.Text(self.tutorial_tab, wrap=tk.WORD)
        text_widget.insert(tk.END, tutorial_info)
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)

    def run_simulation(self):
        alpha = self.alpha_scale.get()
        beta = self.beta_scale.get()
        norm = np.sqrt(alpha ** 2 + beta ** 2)
        if norm == 0:
            messagebox.showerror("Invalid State", "Alpha and Beta cannot both be zero.")
            return
        alpha /= norm
        beta = complex(0, beta / norm)

        self.input_state = Statevector([alpha, beta])
        qc = create_teleportation_circuit(alpha, beta)
        qc.save_statevector()
        transpiled = transpile(qc, sim)
        result = sim.run(transpiled).result()

        self.statevector = result.get_statevector()
        self.counts = result.get_counts()

        # Clear previous plots
        for ax in self.axs:
            ax.clear()

        # Plot Bloch
        # plot_bloch_multivector(self.statevector, ax=self.axs[0])
        bloch_fig = plot_bloch_multivector(self.statevector)
        bloch_fig.savefig("temp_bloch.png")
        img = plt.imread("temp_bloch.png")
        self.axs[0].imshow(img)
        self.axs[0].set_title("Bob's Qubit (Q2)")

        # Plot Circuit
        circuit_drawer(qc, output="mpl", ax=self.axs[1])
        self.axs[1].set_title("Teleportation Circuit")

        # Plot Histogram
        plot_histogram(self.counts, ax=self.axs[2])
        self.axs[2].set_title("Measurement Histogram")

        self.canvas.draw()

        # Show statevector
        self.state_text.delete("1.0", tk.END)
        self.state_text.insert(tk.END, f"Final Statevector:\n{self.statevector}\n\n")

    # Save visualizations
    def save_bloch(self):
        self.fig.savefig("bloch_sphere.png")
        messagebox.showinfo("Saved", "Bloch Sphere saved as 'bloch_sphere.png'")

    def save_circuit(self):
        self.fig.savefig("circuit_diagram.png")
        messagebox.showinfo("Saved", "Circuit saved as 'circuit_diagram.png'")

    def save_hist(self):
        self.fig.savefig("histogram.png")
        messagebox.showinfo("Saved", "Histogram saved as 'histogram.png'")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = TeleportationApp(root)
    root.mainloop()
