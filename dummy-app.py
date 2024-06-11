import tkinter as tk
from tkinter import ttk


class MonteCarloSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Monte Carlo Simulator")

        # Ensure layout dynamically resizes with the window
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Setting frame to place widgets
        frame = ttk.Frame(self.root)
        frame.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.N, tk.W, tk.E, tk.S))

        # Only add a couple of widgets initially
        ttk.Label(frame, text="Small Customer Range (low, high):").grid(column=0, row=0, sticky=tk.W)
        self.small_range = ttk.Entry(frame)
        self.small_range.grid(column=1, row=0)

        self.run_button = ttk.Button(frame, text="Simulate", command=self.run_simulation)
        self.run_button.grid(column=0, row=4, columnspan=2, pady=10)

        self.result_label = ttk.Label(frame, text="")
        self.result_label.grid(column=0, row=5, columnspan=2, pady=5)

    def run_simulation(self):
        # Dummy function for starting the GUI
        self.result_label.config(text="Simulation button pressed.")


if __name__ == "__main__":
    root = tk.Tk()
    app = MonteCarloSimulator(root)
    root.mainloop()