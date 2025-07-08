import tkinter as tk
from tkinter import ttk
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization.bloch import Bloch
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class QuantumBlochApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum Gate Bloch Visualizer")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f0f0f0")

        self.angle = tk.DoubleVar(value=0.0)
        self.gate_var = tk.StringVar()
        self.available_gates = [
            'I', 'X', 'Y', 'Z', 'H', 'S', 'T', 'SX', 'SDG', 'TDG',
            'Rx', 'Ry', 'Rz', 'U3'
        ]

        self.create_widgets()
        self.update_bloch_sphere()

    def create_widgets(self):
        title = ttk.Label(self.root, text="Quantum Gate Bloch Sphere Visualizer",
                          font=("Helvetica", 18, "bold"), background="#f0f0f0")
        title.pack(pady=10)

        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10)

        ttk.Label(control_frame, text="Select Gate:").grid(row=0, column=0, padx=5)
        gate_menu = ttk.OptionMenu(control_frame, self.gate_var, 'I', *self.available_gates,
                                   command=lambda _: self.update_bloch_sphere())
        gate_menu.grid(row=0, column=1, padx=5)

        self.angle_slider = ttk.Scale(control_frame, from_=-np.pi, to=np.pi, orient=tk.HORIZONTAL,
                                      variable=self.angle, command=lambda _: self.update_bloch_sphere(), length=200)
        self.angle_label = ttk.Label(control_frame, text="Angle: 0.00 rad")

        self.angle_slider.grid(row=0, column=2, padx=10)
        self.angle_label.grid(row=0, column=3)

        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, subplot_kw={'projection': '3d'}, figsize=(10, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

        export_btn = ttk.Button(self.root, text="Save Bloch Sphere Image", command=self.save_image)
        export_btn.pack(pady=5)

    def save_image(self):
        self.fig.savefig("bloch_visualization.png")

    def apply_gate(self, gate, angle=0.0):
        qc = QuantumCircuit(1)
        if gate == 'I':
            pass
        elif gate == 'X':
            qc.x(0)
        elif gate == 'Y':
            qc.y(0)
        elif gate == 'Z':
            qc.z(0)
        elif gate == 'H':
            qc.h(0)
        elif gate == 'S':
            qc.s(0)
        elif gate == 'T':
            qc.t(0)
        elif gate == 'SX':
            qc.sx(0)
        elif gate == 'SDG':
            qc.sdg(0)
        elif gate == 'TDG':
            qc.tdg(0)
        elif gate == 'Rx':
            qc.rx(angle, 0)
        elif gate == 'Ry':
            qc.ry(angle, 0)
        elif gate == 'Rz':
            qc.rz(angle, 0)
        elif gate == 'U3':
            theta = angle
            phi = angle / 2
            lam = angle / 3
            qc.u3(theta, phi, lam, 0)
        return qc

    def bloch_vector(self, state):
        rho = np.outer(state, np.conj(state))
        paulis = [
            np.array([[0, 1], [1, 0]]),             # X
            np.array([[0, -1j], [1j, 0]]),          # Y
            np.array([[1, 0], [0, -1]])             # Z
        ]
        return [np.real(np.trace(rho @ p)) for p in paulis]

    def update_bloch_sphere(self):
        gate = self.gate_var.get()
        angle = self.angle.get()
        self.angle_label.config(text=f"Angle: {angle:.2f} rad")

        # Enable slider only for parametric gates
        if gate in ['Rx', 'Ry', 'Rz', 'U3']:
            self.angle_slider.state(['!disabled'])
        else:
            self.angle_slider.state(['disabled'])

        initial_sv = Statevector.from_label('0')
        circuit = self.apply_gate(gate, angle)
        final_sv = initial_sv.evolve(circuit)

        vec1 = self.bloch_vector(initial_sv.data)
        vec2 = self.bloch_vector(final_sv.data)

        self.ax1.cla()
        self.ax2.cla()

        b1 = Bloch(axes=self.ax1)
        b1.add_vectors(vec1)
        b1.title = "Before Gate"

        b2 = Bloch(axes=self.ax2)
        b2.add_vectors(vec2)
        b2.title = f"After {gate}"

        b1.render()
        b2.render()
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = QuantumBlochApp(root)
    root.mainloop()
