import tkinter as tk
from tkinter import ttk
import subprocess
import threading


class CommandExecutor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CMD Command Executor")

        self.process = subprocess.Popen(
            ['cmd.exe'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )

        self.input_label = ttk.Label(self.root, text="Enter CMD command:")
        self.input_label.pack(pady=5)

        self.input_box = ttk.Entry(self.root, width=50)
        self.input_box.pack(pady=5)

        self.execute_button = ttk.Button(self.root, text="Execute", command=self.execute_command)
        self.execute_button.pack(pady=5)

        self.output_label = ttk.Label(self.root, text="Command output:")
        self.output_label.pack(pady=5)

        self.output_box = tk.Text(self.root, width=50, height=10)
        self.output_box.pack(pady=5)

        self.root.mainloop()

    def execute_command(self):
        command = self.input_box.get() + "\n"
        self.process.stdin.write(command)
        self.process.stdin.flush()

        # Clear the output box
        self.output_box.delete(1.0, tk.END)

        # Start a new thread to read the output
        threading.Thread(target=self.read_output, daemon=True).start()

    def read_output(self):
        while True:
            output = self.process.stdout.readline()
            if not output:
                break
            self.root.after(0, self.update_output, output)

    def update_output(self, output):
        self.output_box.insert(tk.END, output)
        self.output_box.see(tk.END)


if __name__ == "__main__":
    CommandExecutor()