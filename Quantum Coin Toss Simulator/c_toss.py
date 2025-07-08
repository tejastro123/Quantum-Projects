import random
import matplotlib.pyplot as plt

def classical_coin_toss(trials=1000):
    results = {"0": 0, "1": 0}
    for _ in range(trials):
        toss = str(random.randint(0, 1))
        results[toss] += 1

    # Plotting
    labels = ['Heads (0)', 'Tails (1)']
    values = [results['0'], results['1']]
    plt.bar(labels, values, color=['green', 'orange'])
    plt.title(f"Classical Coin Toss - {trials} Trials")
    plt.ylabel("Frequency")
    plt.show()

    return results

if __name__ == "__main__":
    counts = classical_coin_toss(1000)
    print("Classical Toss Result:", counts)
