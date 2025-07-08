# app.py
import streamlit as st
from simulator import BB84Simulator
from post_processing import apply_post_processing
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(page_title="Quantum Cryptography Toolkit", layout="wide")
st.title("🔐 Quantum Cryptography Toolkit – BB84 Protocol Simulator")

# Sidebar Configuration
st.sidebar.header("Simulation Settings")
num_qubits = st.sidebar.slider("Number of Qubits", min_value=10, max_value=500, value=100, step=10)
eavesdropper = st.sidebar.checkbox("Include Eavesdropper (Eve)", value=False)
run_button = st.sidebar.button("▶ Run Simulation")

if "sim_result" not in st.session_state:
    st.session_state.sim_result = None
    st.session_state.final_key = None

if run_button:
    sim = BB84Simulator(num_qubits=num_qubits, eavesdropper=eavesdropper)
    sim.run()
    st.session_state.sim_result = sim.summary()
    st.session_state.final_key = None
    st.success("Simulation completed!")

if st.session_state.sim_result:
    res = st.session_state.sim_result
    st.subheader("🧪 Simulation Output")
    st.write(f"**Qubits Sent:** {res['num_qubits']}")
    st.write(f"**Eavesdropper Present:** {res['eavesdropper']}")
    st.write(f"**QBER:** {res['qber']}%")
    st.write(f"**Raw Key:** `{''.join(map(str, res['raw_key']))}`")

    with st.expander("📊 Visualizations", expanded=True):
        tabs = st.tabs(["QBER Comparison", "Basis Match", "Bit Agreement", "Match Index"])

        with tabs[0]:
            sim_eve = BB84Simulator(num_qubits, eavesdropper=True)
            sim_eve.run()
            sim_no_eve = BB84Simulator(num_qubits, eavesdropper=False)
            sim_no_eve.run()

            values = [sim_eve.qber * 100, sim_no_eve.qber * 100]
            labels = ["With Eve", "Without Eve"]

            fig, ax = plt.subplots()
            sns.barplot(x=labels, y=values, palette='Set2', ax=ax)
            ax.set_title("QBER Comparison")
            ax.set_ylabel("QBER (%)")
            ax.set_ylim(0, 100)
            ax.grid(True, linestyle='--', alpha=0.6)
            st.pyplot(fig)

        with tabs[1]:
            alice_bases = res["alice_bases"]
            bob_bases = res["bob_bases"]
            match = [1 if a == b else 0 for a, b in zip(alice_bases, bob_bases)]
            indices = np.arange(len(alice_bases))

            fig, ax = plt.subplots()
            ax.scatter(indices, match, c=match, cmap='coolwarm', marker='|', s=100)
            ax.set_title("Alice vs Bob Basis Match")
            ax.set_xlabel("Qubit Index")
            ax.set_ylabel("Match")
            ax.set_yticks([0, 1])
            ax.grid(True, linestyle='--', alpha=0.6)
            st.pyplot(fig)

        with tabs[2]:
            agreements = [
                1 if res["alice_bits"][i] == res["bob_results"][i] else 0
                for i in res["matching_indices"]
            ]
            fig, ax = plt.subplots(figsize=(10, 1.5))
            sns.heatmap([agreements], cmap='Greens', cbar=True, xticklabels=False, ax=ax)
            ax.set_title("Bit Agreement in Matching Bases")
            ax.set_yticks([])
            st.pyplot(fig)

        with tabs[3]:
            total = res["num_qubits"]
            match_index = [1 if i in res["matching_indices"] else 0 for i in range(total)]

            fig, ax = plt.subplots()
            ax.bar(range(total), match_index, color="skyblue")
            ax.set_title("Matching Index Distribution")
            ax.set_xlabel("Qubit Index")
            ax.set_ylabel("Match")
            ax.set_yticks([0, 1])
            st.pyplot(fig)

    st.subheader("🔐 Post-Processing")
    if st.button("Run Reconciliation + Privacy Amplification"):
        alice_key = [res["alice_bits"][i] for i in res["matching_indices"]]
        bob_key = res["raw_key"]
        st.session_state.final_key = apply_post_processing(alice_key, bob_key)
        st.success("Post-processing complete!")

    if st.session_state.final_key:
        key_str = "".join(map(str, st.session_state.final_key))
        st.code(key_str, language="plaintext")
        st.download_button("💾 Download Final Key", key_str, file_name="final_key.txt")
else:
    st.info("Run a simulation to view results.")
