import tkinter as tk
from tkinter import ttk, messagebox

class SoundWaveCalculator:
    def __init__(self, root):   
        self.root = root
        self.root.title("Sound Waves Calculator")
        
        # Make the window full-screen
        self.root.state('zoomed')
        self.root.resizable(False, False)

        # Center the main frame
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.main_frame = ttk.Frame(root)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Make the grid and layout responsive
        self.main_frame.grid_rowconfigure(0, weight=0)  # Title
        self.main_frame.grid_rowconfigure(1, weight=0)  # Description
        self.main_frame.grid_rowconfigure(2, weight=0)  # Operation menu
        self.main_frame.grid_rowconfigure(3, weight=1)  # Input and output
        self.main_frame.grid_rowconfigure(4, weight=0)  # Back button
        self.main_frame.grid_columnconfigure(0, weight=1)  # Input frame

        # Sound Wave title label
        self.title_label = ttk.Label(
            self.main_frame,
            text="Sound Wave Calculator",
            font=("Arial", 60, "bold"),
            anchor="center",
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20), sticky="n")

        # Description label
        self.description_label = ttk.Label(
            self.main_frame,
            text="Focuses on the calculation of properties of sound waves like frequency, wavelength, and speed.",
            font=("Arial", 13),
            anchor="center",
            justify="center",
        )
        self.description_label.grid(row=1, column=0, columnspan=2, pady=(5, 10), sticky="n")

        # Operation label and dropdown menu
        self.operation_label = ttk.Label(self.main_frame, text="Select Operation:", font=("Arial", 15, "bold"))
        self.operation_label.grid(row=2, column=0, padx=20, pady=20, sticky="w")  # Align label to the left

        # Map of operations and corresponding methods and required inputs
        self.operations = {
            "Frequency": (self.calculate_frequency, ["period"], "f = 1 / T"),
            "Wavelength": (self.calculate_wavelength, ["speed_of_sound", "frequency"], "λ = v / f"),
            "Speed of Sound": (self.calculate_speed_of_sound, ["frequency", "wavelength"], "v = f * λ"),
            "Period": (self.calculate_period, ["frequency"], "T = 1 / f"),
        }

        # Custom style for ComboBox
        style = ttk.Style()
        style.configure("TCombobox", font=("Arial", 16), padding=5)

        self.operation_var = tk.StringVar()
        self.operation_menu = ttk.Combobox(
            self.main_frame,
            textvariable=self.operation_var,
            values=list(self.operations.keys()),
            state="readonly",
            height=9,  # Set the drop-down height to show fewer options
            style="TCombobox",  # Apply the custom style
        )
        self.operation_menu.grid(row=2, column=0, padx=200, pady=20, sticky="w")  # Keep dropdown on the right side
        self.operation_menu.bind("<<ComboboxSelected>>", self.update_input_fields)

        # Input fields
        self.input_frame = ttk.LabelFrame(self.main_frame, text="Inputs", padding=(5, 5))
        self.input_frame.grid(row=3, column=0, columnspan=2, padx=200, pady=10, sticky="nsew")
        self.input_frame.grid_propagate(False)  # Prevent resizing of frame
        self.inputs = {}
        self.create_input_fields()

        # Formula inside the Input frame
        self.formula_label = ttk.Label(self.input_frame, text="", font=("Arial", 14), justify="center")
        self.formula_label.grid(row=0, column=0, padx=10, pady=(10, 20), sticky="nsew")

        # Output label and calculate button
        self.output_label = ttk.Label(self.input_frame, text="Result: ", font=("Arial", 18), anchor="center")
        self.output_label.grid(row=len(self.inputs) + 3, column=0, padx=10, pady=10, sticky="nsew")
        self.output_label.grid_remove()  # Initially hidden

        self.calculate_button = ttk.Button(self.input_frame, text="Calculate", command=self.calculate, style="TButton", width=20, padding=10)
        self.calculate_button.grid(row=len(self.inputs) + 4, column=1, pady=10, sticky="nsew")
        self.calculate_button.grid_remove()  # Initially hidden

        self.back_button = ttk.Button(self.main_frame, text="Back", command=self.back, style="TButton", width=20, padding=10)
        self.back_button.grid(row=4, column=0, columnspan=2, pady=20, sticky="nsew")

        style.configure("TButton", font=("Arial", 16), padding=10, width=20)

    def create_input_fields(self):
        fields = [
            "period", "frequency", "wavelength", "speed_of_sound"
        ]

        for idx, field in enumerate(fields):
            label = ttk.Label(self.input_frame, font=("Arial", 15), text=f"{field.capitalize()}:")
            entry = ttk.Entry(self.input_frame, font=("Arial", 15), width=20)
        
            label.grid(row=idx + 1, column=0, sticky="ew", padx=10, pady=5)  # Ensure label is centered
            entry.grid(row=idx + 1, column=1, sticky="ew", padx=10, pady=5)  # Ensure entry is centered

            self.input_frame.grid_columnconfigure(0, weight=1)
            self.input_frame.grid_columnconfigure(1, weight=3)

            self.inputs[field] = (label, entry)
            label.grid_remove()
            entry.grid_remove()

    def update_input_fields(self, event=None):
        for label, entry in self.inputs.values():
            label.grid_remove()
            entry.grid_remove()

        operation = self.operation_var.get()
        if operation in self.operations:
            func, required_fields, formula = self.operations[operation]
            self.formula_label.config(text=f"Formula: {formula}")
            for idx, field in enumerate(required_fields):
                if field in self.inputs:
                    label, entry = self.inputs[field]
                    label.grid(row=idx + 1, column=0, sticky="w", padx=5, pady=5)
                    entry.grid(row=idx + 1, column=1, sticky="ew", padx=5, pady=5)

            self.calculate_button.grid(row=len(required_fields) + 4, column=1, pady=10, sticky="nsew")
            self.calculate_button.grid()

    def calculate(self):
        operation = self.operation_var.get()
        if operation in self.operations:
            func, required_fields, formula = self.operations[operation]
            try:
                values = {field: float(self.inputs[field][1].get()) for field in required_fields}
                result = func(**values)
                self.output_label.config(text=f"Result: {result:.2f}")
                self.output_label.grid()
            except ValueError as e:
                messagebox.showerror("Error", "Enter valid values")  # Shows the error message
            except Exception as e:
                messagebox.showerror("Notice", "Please select operation first!")

    def back(self):
        self.root.destroy()
        from Main import Main
        Main()
    
    def calculate_frequency(self, period):
        return 1 / period

    def calculate_wavelength(self, speed_of_sound, frequency):
        return speed_of_sound / frequency

    def calculate_speed_of_sound(self, frequency, wavelength):
        return frequency * wavelength

    def calculate_period(self, frequency):
        return 1 / frequency
    
if __name__ == "__main__":
    root = tk.Tk()
    app = SoundWaveCalculator(root)
    root.mainloop()