import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from simulator import BB84Simulator
from post_processing import apply_post_processing

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class QKDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum Cryptography Toolkit - BB84 Simulator")
        self.root.geometry("900x650")

        self.num_qubits_var = tk.IntVar(value=100)
        self.eve_var = tk.BooleanVar(value=False)

        self.sim_result = None
        self.final_key = []
        self.current_figure = None

        self.build_ui()

    def build_ui(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill="both", padx=5, pady=5)

        # Tabs
        self.tab_config = ttk.Frame(notebook)
        self.tab_visuals = ttk.Frame(notebook)
        self.tab_output = ttk.Frame(notebook)

        notebook.add(self.tab_config, text="⚙️ Configuration")
        notebook.add(self.tab_visuals, text="📊 Visualizations")
        notebook.add(self.tab_output, text="📄 Output & Export")

        self.build_config_tab()
        self.build_visuals_tab()
        self.build_output_tab()

    def build_config_tab(self):
        frame = ttk.LabelFrame(self.tab_config, text="Simulation Settings", padding=10)
        frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(frame, text="Number of Qubits:").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.num_qubits_var, width=10).grid(row=0, column=1)

        ttk.Checkbutton(frame, text="Enable Eve (Eavesdropper)", variable=self.eve_var).grid(row=1, column=0, columnspan=2, sticky="w", pady=5)

        ttk.Button(frame, text="▶ Run BB84 Simulation", command=self.run_simulation).grid(row=2, column=0, pady=10)
        ttk.Button(frame, text="🔐 Run Post-Processing", command=self.run_post_processing).grid(row=2, column=1, pady=10)

    def build_visuals_tab(self):
        top_frame = ttk.LabelFrame(self.tab_visuals, text="Plot Controls", padding=10)
        top_frame.pack(padx=10, pady=5, fill="x")

        ttk.Button(top_frame, text="QBER Comparison", command=self.show_qber_comparison).grid(row=0, column=0, padx=5)
        ttk.Button(top_frame, text="Basis Match", command=self.show_basis_match).grid(row=0, column=1, padx=5)
        ttk.Button(top_frame, text="Bit Agreement", command=self.show_bit_agreement).grid(row=0, column=2, padx=5)
        ttk.Button(top_frame, text="Matching Index Map", command=self.show_match_index).grid(row=0, column=3, padx=5)

        self.plot_frame = ttk.Frame(self.tab_visuals)
        self.plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.save_btn = ttk.Button(self.tab_visuals, text="💾 Save Plot as PNG", command=self.save_plot)
        self.save_btn.pack(pady=5)

    def build_output_tab(self):
        self.output_text = tk.Text(self.tab_output, height=20, bg="#ffffff", font=("Courier", 10))
        self.output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        button_frame = ttk.Frame(self.tab_output)
        button_frame.pack(pady=5)

        ttk.Button(button_frame, text="💾 Export Key to File", command=self.export_key).pack()

    def run_simulation(self):
        num_qubits = self.num_qubits_var.get()
        eavesdropper = self.eve_var.get()

        sim = BB84Simulator(num_qubits=num_qubits, eavesdropper=eavesdropper)
        sim.run()
        self.sim_result = sim.summary()
        self.final_key = []

        raw_key = ''.join(map(str, self.sim_result['raw_key']))
        qber = self.sim_result['qber']

        output = (
            f"[Simulation Result]\n"
            f"Qubits Sent         : {num_qubits}\n"
            f"Eavesdropper Present: {eavesdropper}\n"
            f"QBER                : {qber}%\n"
            f"Raw Key             : {raw_key}\n"
            f"Matching Indices    : {self.sim_result['matching_indices']}\n"
        )

        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, output)

    def run_post_processing(self):
        if not self.sim_result:
            messagebox.showwarning("Run Simulation First", "Please run the simulation first.")
            return

        alice_key = [self.sim_result['alice_bits'][i] for i in self.sim_result['matching_indices']]
        bob_key = self.sim_result['raw_key']
        self.final_key = apply_post_processing(alice_key, bob_key)

        key_str = ''.join(map(str, self.final_key))
        self.output_text.insert(tk.END, f"\n[Post-Processing Final Key]:\n{key_str}\n")

    def export_key(self):
        if not self.sim_result:
            messagebox.showerror("Error", "No simulation data to export.")
            return

        key_to_save = self.final_key if self.final_key else self.sim_result['raw_key']
        key_str = ''.join(map(str, key_to_save))

        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filepath:
            with open(filepath, 'w') as f:
                f.write(key_str)
            messagebox.showinfo("Export Complete", f"Key saved to {filepath}")

    def display_plot(self, fig: Figure):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.current_figure = fig

    def save_plot(self):
        if not self.current_figure:
            messagebox.showwarning("No Plot", "No plot to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
        if file_path:
            self.current_figure.savefig(file_path)
            messagebox.showinfo("Saved", f"Plot saved to {file_path}")

    def show_qber_comparison(self):
        sim_eve = BB84Simulator(self.num_qubits_var.get(), eavesdropper=True)
        sim_eve.run()

        sim_no_eve = BB84Simulator(self.num_qubits_var.get(), eavesdropper=False)
        sim_no_eve.run()

        values = [sim_eve.qber * 100, sim_no_eve.qber * 100]
        labels = ["With Eve", "Without Eve"]

        fig = Figure(figsize=(5, 4))
        ax = fig.add_subplot(111)
        sns.barplot(x=labels, y=values, palette='Set2', ax=ax)
        ax.set_title("QBER Comparison")
        ax.set_ylabel("QBER (%)")
        ax.set_ylim(0, 100)
        ax.grid(True, linestyle='--', alpha=0.6)

        self.display_plot(fig)

    def show_basis_match(self):
        if not self.sim_result:
            messagebox.showwarning("No Data", "Run the simulation first.")
            return

        alice_bases = self.sim_result['alice_bases']
        bob_bases = self.sim_result['bob_bases']
        match = [1 if a == b else 0 for a, b in zip(alice_bases, bob_bases)]
        indices = np.arange(len(alice_bases))

        fig = Figure(figsize=(8, 3))
        ax = fig.add_subplot(111)
        ax.scatter(indices, match, c=match, cmap='coolwarm', marker='|', s=100)
        ax.set_title("Alice vs Bob Basis Match")
        ax.set_xlabel("Qubit Index")
        ax.set_yticks([0, 1])
        ax.set_ylabel("Match")
        ax.grid(True, linestyle='--', alpha=0.6)

        self.display_plot(fig)

    def show_bit_agreement(self):
        if not self.sim_result:
            messagebox.showwarning("No Data", "Run the simulation first.")
            return

        agreements = [
            1 if self.sim_result['alice_bits'][i] == self.sim_result['bob_results'][i] else 0
            for i in self.sim_result['matching_indices']
        ]
        indices = np.arange(len(agreements))

        fig = Figure(figsize=(8, 2))
        ax = fig.add_subplot(111)
        sns.heatmap([agreements], cmap='Greens', cbar=True, xticklabels=indices, ax=ax)
        ax.set_title("Bit Agreement in Matching Bases")
        ax.set_xlabel("Matching Index")
        ax.set_yticks([])

        self.display_plot(fig)

    def show_match_index(self):
        if not self.sim_result:
            messagebox.showwarning("No Data", "Run the simulation first.")
            return

        total = self.sim_result['num_qubits']
        data = [1 if i in self.sim_result['matching_indices'] else 0 for i in range(total)]

        fig = Figure(figsize=(8, 2))
        ax = fig.add_subplot(111)
        ax.bar(range(total), data, color='skyblue')
        ax.set_title("Basis Matching Distribution")
        ax.set_xlabel("Qubit Index")
        ax.set_ylabel("Match")
        ax.set_yticks([0, 1])

        self.display_plot(fig)


if __name__ == "__main__":
    root = tk.Tk()
    app = QKDApp(root)
    root.mainloop()
