import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, simpledialog
import numpy as np
import csv
from scipy import stats
import matplotlib.pyplot as plt


class MonteCarloSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Monte Carlo Simulator")
        self.root.geometry("600x550")
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        labels = [
            "Small Customer Range:", "Medium Customer Range:", "Big Customer Range:",
            "Small Customer Probability:", "Medium Customer Probability:", "Big Customer Probability:",
            "Small Revenue Range:", "Medium Revenue Range:", "Big Revenue Range:"
        ]
        defaults = [
            "5000, 10000", "1000, 2500", "10, 500",
            "0.1, 0.5", "0.02, 0.05", "0.002, 0.005",
            "150, 450", "7500, 15000", "50000, 100000"
        ]

        self.entries = []
        for i, (label, default) in enumerate(zip(labels, defaults)):
            ttk.Label(frame, text=f"{label} (low, high):").grid(column=0, row=i, sticky=tk.W)
            entry = ttk.Entry(frame)
            entry.grid(column=1, row=i, sticky=(tk.W, tk.E))
            entry.insert(0, default)
            self.entries.append(entry)

        # Number of simulations input
        self.sim_count_var = tk.IntVar(value=1000)
        ttk.Label(frame, text="Number of Simulations:").grid(column=0, row=len(labels), sticky=tk.W)
        simulation_entry = ttk.Entry(frame, textvariable=self.sim_count_var)
        simulation_entry.grid(column=1, row=len(labels), sticky=(tk.W, tk.E))

        # Simulation and results buttons
        self.simulate_button = ttk.Button(frame, text="Simulate", command=self.run_simulation)
        self.simulate_button.grid(column=0, row=len(labels) + 1, columnspan=2, pady=10)

        self.save_button = ttk.Button(frame, text="Save Results", command=self.save_results)
        self.save_button.grid(column=0, row=len(labels) + 2, columnspan=2, pady=10)

        self.visualize_button = ttk.Button(frame, text="Visualize Results", command=self.plot_results)
        self.visualize_button.grid(column=0, row=len(labels) + 3, columnspan=2, pady=10)

        self.stat_label = ttk.Label(frame, text="", justify=tk.LEFT)
        self.stat_label.grid(column=0, row=len(labels) + 4, columnspan=2, sticky='ew', pady=10)

        self.results = []

    def parse_entry(self, index):
        return list(map(float, self.entries[index].get().split(',')))

    def run_simulation(self):
        try:
            small_range = self.parse_entry(0)
            medium_range = self.parse_entry(1)
            big_range = self.parse_entry(2)
            small_prob = self.parse_entry(3)
            medium_prob = self.parse_entry(4)
            big_prob = self.parse_entry(5)
            small_revenue = self.parse_entry(6)
            medium_revenue = self.parse_entry(7)
            big_revenue = self.parse_entry(8)
            num_simulations = self.sim_count_var.get()
        except ValueError:
            self.stat_label.config(text='Please enter values in the format: low, high')
            return

        self.results = []
        for _ in range(num_simulations):
            num_small = np.random.randint(*small_range)
            num_medium = np.random.randint(*medium_range)
            num_big = np.random.randint(*big_range)
            prob_small = np.random.uniform(*small_prob)
            prob_medium = np.random.uniform(*medium_prob)
            prob_big = np.random.uniform(*big_prob)
            rev_small = np.random.randint(*small_revenue)
            rev_medium = np.random.randint(*medium_revenue)
            rev_big = np.random.randint(*big_revenue)

            total_revenue = (rev_small * num_small * prob_small +
                             rev_medium * num_medium * prob_medium +
                             rev_big * num_big * prob_big)
            self.results.append(total_revenue)

        results_np = np.array(self.results)
        self.summary_statistics(results_np)

    def summary_statistics(self, results_np):
        mean = np.mean(results_np)
        median = np.median(results_np)
        std_dev = np.std(results_np)
        variance = np.var(results_np)
        skew = stats.skew(results_np)
        kurtosis = stats.kurtosis(results_np)
        confidence_interval = stats.norm.interval(0.95, loc=mean, scale=std_dev / np.sqrt(len(self.results)))

        stat_text = (f'Average Revenue: ${mean:.2f}\n'
                     f'5% Percentile: ${np.percentile(results_np, 5):.2f}\n'
                     f'95% Percentile: ${np.percentile(results_np, 95):.2f}\n'
                     f'Median: ${median:.2f}\nStandard Deviation: ${std_dev:.2f}\n'
                     f'Variance: ${variance:.2f}\nSkewness: {skew:.2f}\n'
                     f'Kurtosis: {kurtosis:.2f}\n95% Confidence Interval: ${confidence_interval[0]:.2f} to ${confidence_interval[1]:.2f}')
        self.stat_label.config(text=stat_text)

    def plot_results(self):
        if not self.results:
            tk.messagebox.showerror("Error", "Please run the simulation first.")
            return

        results_np = np.array(self.results)
        plt.figure(figsize=(10, 6))
        plt.hist(results_np, bins=50, color='skyblue', alpha=0.7)
        plt.axvline(x=np.percentile(results_np, 5), color='red', label='5th Percentile', linestyle='dashed',
                    linewidth=1)
        plt.axvline(x=np.percentile(results_np, 95), color='green', label='95th Percentile', linestyle='dashed',
                    linewidth=1)
        plt.title("Revenue Distribution")
        plt.xlabel("Revenue")
        plt.ylabel("Frequency")
        plt.legend()
        plt.show()

    def save_results(self):
        if not self.results:
            self.stat_label.config(text='No simulation results to save. Please run simulation first.')
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Revenue"])
                for revenue in self.results:
                    writer.writerow([revenue])


if __name__ == "__main__":
    root = tk.Tk()
    app = MonteCarloSimulator(root)
    root.mainloop()
