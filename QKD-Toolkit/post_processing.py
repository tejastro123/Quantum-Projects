import hashlib
import math
import random
from simulator import BB84Simulator

def parity_reconciliation(alice_key, bob_key):
    """
    Perform basic parity block reconciliation.
    If parities don't match, drop the block (simple, non-interactive).
    Returns reconciled keys for both parties.
    """
    block_size = 4
    alice_blocks = [alice_key[i:i+block_size] for i in range(0, len(alice_key), block_size)]
    bob_blocks = [bob_key[i:i+block_size] for i in range(0, len(bob_key), block_size)]

    reconciled_key = []

    for ablock, bblock in zip(alice_blocks, bob_blocks):
        if len(ablock) != len(bblock):
            continue  # skip incomplete blocks

        alice_parity = sum(ablock) % 2
        bob_parity = sum(bblock) % 2

        if alice_parity == bob_parity:
            reconciled_key.extend(bblock)  # keep Bob's version
        # else: discard this block

    return reconciled_key


def privacy_amplification(shared_key, target_length=None):
    """
    Simple privacy amplification using XOR folding.
    Reduces the length of the key to ensure any info Eve has is minimized.
    """
    if target_length is None:
        # Default: halve the key length
        target_length = len(shared_key) // 2

    if len(shared_key) < 2:
        return shared_key  # nothing to fold

    while len(shared_key) > target_length:
        half = len(shared_key) // 2
        folded_key = [shared_key[i] ^ shared_key[i + half] for i in range(half)]
        shared_key = folded_key

    return shared_key


def sha256_hash_bits(bits, target_length=128):
    """
    Hashes the bitstring using SHA-256 and returns the first target_length bits.
    """
    bit_string = ''.join(map(str, bits))
    hashed = hashlib.sha256(bit_string.encode()).hexdigest()
    bin_hash = bin(int(hashed, 16))[2:].zfill(256)
    return [int(b) for b in bin_hash[:target_length]]


def apply_post_processing(alice_bits, bob_bits):
    """
    Main function: Reconcile and amplify keys
    """
    print(f"\n[Post-Processing] Starting with raw key of length {len(bob_bits)}")

    # 1. Reconciliation
    reconciled = parity_reconciliation(alice_bits, bob_bits)
    print(f"[Reconciliation] Key length after parity check: {len(reconciled)}")

    # 2. Privacy Amplification
    final_key = privacy_amplification(reconciled)
    print(f"[Privacy Amplification] Final key length: {len(final_key)}")

    return final_key




if __name__ == "__main__":
    # Run protocol
    sim = BB84Simulator(num_qubits=100, eavesdropper=True)
    sim.run()
    result = sim.summary()

    # Get Alice's original and Bob's raw key (at matching indices)
    alice_key = [result['alice_bits'][i] for i in result['matching_indices']]
    bob_key = result['raw_key']

    # Apply post-processing
    final_secure_key = apply_post_processing(alice_key, bob_key)

    print(f"[Final Key] {''.join(map(str, final_secure_key))}")