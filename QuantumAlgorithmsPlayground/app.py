import tkinter as tk
from tkinter import ttk, messagebox
from backend import simulate
from plot_utils import show_circuit, show_results
import deutsch_jozsa
import grover
import bernstein_vazirani

class QuantumApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum Algorithms Playground")
        self.root.geometry("900x600")

        self.setup_widgets()

    def setup_widgets(self):
        # Dropdown
        self.label = ttk.Label(self.root, text="Select Quantum Algorithm:")
        self.label.pack(pady=10)

        self.algorithm_var = tk.StringVar()
        self.dropdown = ttk.Combobox(self.root, textvariable=self.algorithm_var)
        self.dropdown['values'] = ["Deutsch-Jozsa", "Grover", "Bernstein-Vazirani"]
        self.dropdown.pack(pady=5)

        # Input box for Oracle string (for BV and Grover)
        self.oracle_label = ttk.Label(self.root, text="Oracle (optional for BV/Grover, e.g. 101)")
        self.oracle_label.pack()
        self.oracle_entry = ttk.Entry(self.root)
        self.oracle_entry.pack(pady=5)

        # Run Button
        self.run_button = ttk.Button(self.root, text="Run Algorithm", command=self.run_algorithm)
        self.run_button.pack(pady=15)

        # Output Frame
        self.output_frame = tk.Frame(self.root)
        self.output_frame.pack(fill="both", expand=True)

    def run_algorithm(self):
        algo = self.algorithm_var.get()
        oracle = self.oracle_entry.get()

        try:
            if algo == "Deutsch-Jozsa":
                qc = deutsch_jozsa.build_circuit()
            elif algo == "Grover":
                qc = grover.build_circuit(oracle)
            elif algo == "Bernstein-Vazirani":
                qc = bernstein_vazirani.build_circuit(oracle)
            else:
                messagebox.showerror("Error", "Please select a valid algorithm.")
                return

            # Simulate and plot
            result, counts = simulate(qc)
            show_circuit(qc)
            show_results(result, counts)

        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == '__main__':
    root = tk.Tk()
    app = QuantumApp(root)
    root.mainloop()
