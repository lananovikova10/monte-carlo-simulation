import tkinter as tk


def main():
    root = tk.Tk()
    root.title("Test Window")
    root.geometry("300x200")  # Set a default size

    label = tk.Label(root, text="Hello, tkinter!")
    label.pack(pady=20)

    button = tk.Button(root, text="Exit", command=root.destroy)
    button.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    main()