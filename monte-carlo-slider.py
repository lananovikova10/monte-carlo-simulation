import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import numpy as np
import csv


class MonteCarloSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Monte Carlo Simulator")
        self.root.geometry("700x600")
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        labels = [
            "Small Customer Range", "Medium Customer Range", "Big Customer Range",
            "Small Customer Probability", "Medium Customer Probability", "Big Customer Probability",
            "Small Revenue Range", "Medium Revenue Range", "Big Revenue Range"
        ]
        ranges = [
            (5000, 10000), (1000, 2500), (10, 500),
            (0.1, 0.5), (0.02, 0.05), (0.002, 0.005),
            (150, 450), (7500, 15000), (50000, 100000)
        ]

        self.scale_vars = []
        for i, (label, rng) in enumerate(zip(labels, ranges)):
            ttk.Label(frame, text=f"{label}:").grid(column=0, row=i, sticky=tk.W, columnspan=2)
            # Creating two scales per range, one for low and one for high
            low_var = tk.DoubleVar(value=rng[0])
            high_var = tk.DoubleVar(value=rng[1])

            low_scale = ttk.Scale(frame, from_=min(rng), to=max(rng), variable=low_var, orient=tk.HORIZONTAL)
            high_scale = ttk.Scale(frame, from_=min(rng), to=max(rng), variable=high_var, orient=tk.HORIZONTAL)

            low_scale.grid(column=0, row=i + 1, sticky=(tk.W, tk.E, tk.N, tk.S))
            high_scale.grid(column=1, row=i + 1, sticky=(tk.W, tk.E, tk.N, tk.S))

            self.scale_vars.append((low_var, high_var))

            ttk.Label(frame, text="Low:").grid(column=0, row=i + 1, sticky=tk.W)
            ttk.Label(frame, text="High:").grid(column=1, row=i + 1, sticky=tk.W)

        self.simulate_button = ttk.Button(frame, text="Simulate", command=self.run_simulation)
        self.simulate_button.grid(column=0, row=len(labels) * 2, columnspan=2, pady=10)

        self.save_button = ttk.Button(frame, text="Save Results", command=self.save_results)
        self.save_button.grid(column=0, row=len(labels) * 2 + 1, columnspan=2, pady=10)

        self.result_label = ttk.Label(frame, text="")
        self.result_label.grid(column=0, row=len(labels) * 2 + 2, columnspan=2, pady=5)

        self.results = []

    def run_simulation(self):
        self.results = []
        for _ in range(1000):
            revenues = []
            for vars in self.scale_vars:
                num = np.random.randint(vars[0].get(), vars[1].get() + 1)
                prob = np.random.uniform(vars[0].get(), vars[1].get())
                rev = num * prob
                revenues.append(rev)

            total_revenue = sum(revenues)
            self.results.append(total_revenue)

        avg_revenue = np.average(self.results)
        p5 = np.percentile(self.results, 5)
        p95 = np.percentile(self.results, 95)

        self.result_label.config(
            text=f'Average Revenue: ${avg_revenue:.2f}, 5% Percentile: ${p5:.2f}, 95% Percentile: ${p95:.2f}')

    def save_results(self):
        if not self.results:
            self.result_label.config(text='No simulation results to save. Please run simulation first.')
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