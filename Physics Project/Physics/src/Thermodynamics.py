import tkinter as tk
from tkinter import ttk, messagebox
from thermo import Thermodynamics  # Ensure Thermodynamics class is saved in thermodynamics.py

class ThermodynamicsCalculator:
    def __init__(self, root):
        self.thermo = Thermodynamics()
        self.root = root
        self.root.title("Thermodynamics Calculator")

        # Make the window full-screen
        self.root.state('zoomed')
        self.root.resizable(False, False)

        # Center the main frame
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.main_frame = ttk.Frame(root)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Make the grid responsive and center content
        self.main_frame.grid_rowconfigure(0, weight=0)  # Title
        self.main_frame.grid_rowconfigure(1, weight=0)  # Description
        self.main_frame.grid_rowconfigure(2, weight=0)  # Operation menu
        self.main_frame.grid_rowconfigure(3, weight=1)  # Input and output
        self.main_frame.grid_rowconfigure(4, weight=0)  # Back button
        self.main_frame.grid_columnconfigure(0, weight=1)  # Input frame

        # Thermodynamics title label
        self.title_label = ttk.Label(
            self.main_frame,
            text="Thermodynamics Calculator",
            font=("Arial", 60, "bold"),
            anchor="center",
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20), sticky="n")

        # Description label
        self.description_label = ttk.Label(
            self.main_frame,
            text="Calculate thermodynamics properties and laws like ideal gas law, heat transfer, and more.",
            font=("Arial", 13),
            anchor="center",
            justify="center",
        )
        self.description_label.grid(row=1, column=0, columnspan=2, pady=(5, 10), sticky="n")

        # Operation label and combo box
        self.operation_label = ttk.Label(self.main_frame, text="Select Operation:", font=("Arial", 15, "bold"))
        self.operation_label.grid(row=2, column=0, padx=10, pady=20, sticky="e")

        self.operations = {
            "Convert Celsius to Kelvin": (self.convert_celsius_to_kelvin, ["celsius"], "T(K) = T(°C) + 273.15"),
            "Convert Kelvin to Celsius": (self.convert_kelvin_to_celsius, ["kelvin"], "T(°C) = T(K) - 273.15"),
            "Ideal Gas Law": (self.ideal_gas_law, ["pressure", "volume", "temperature"], "PV = nRT"),
            "Thermal Expansion Coefficient": (self.thermal_expansion_coefficient, ["change_in_length", "original_length", "change_in_temperature"], "α = ΔL / (L0 * ΔT)"),
            "Heat Transfer (Conduction)": (self.heat_transfer_conduction, ["thermal_conductivity", "area", "temperature_difference", "thickness"], "Q = (k * A * ΔT) / d"),
            "Heat Transfer (Convection)": (self.heat_transfer_convection, ["heat_transfer", "temperature_change"], "Q = h * A * ΔT"),
            "Heat Transfer (Radiation)": (self.heat_transfer_radiation, ["emissivity", "temperature_hot", "temperature_cold"], "Q = ε * σ * A * (T_hot^4 - T_cold^4)"),
            "First Law of Thermodynamics": (self.first_law_thermodynamics, ["heat_transfer", "work_done"], "ΔU = Q - W"),
            "Carnot Efficiency": (self.efficiency_carnot, ["temperature_hot", "temperature_cold"], "η = 1 - (T_cold / T_hot)"),
            "Entropy Change": (self.entropy_change, ["heat_transfer", "temperature"], "ΔS = Q / T"),
        }

        self.operation_var = tk.StringVar()
        self.operation_menu = ttk.Combobox(
            self.main_frame,
            textvariable=self.operation_var,
            values=list(self.operations.keys()),
            state="readonly",
            height=9,  # Set the drop-down height to show fewer options
            font=("Arial", 16),  # Apply custom font
        )
        self.operation_menu.grid(row=2, column=1, padx=20, pady=20, sticky="ew")
        self.operation_menu.bind("<<ComboboxSelected>>", self.update_input_fields)

        # Input fields container
        self.input_frame = ttk.LabelFrame(self.main_frame, text="Inputs", padding=(5, 5))
        self.input_frame.grid(row=3, column=0, padx=200, pady=10, sticky="nsew")
        self.input_frame.grid_propagate(False)  # Prevent resizing
        self.inputs = {}
        self.create_input_fields()

        # Formula label in input frame
        self.formula_label = ttk.Label(self.input_frame, text="", font=("Arial", 14), justify="center")
        self.formula_label.grid(row=0, column=0, padx=10, pady=(10, 20), sticky="nsew")

        # Initially hide the result and calculate button
        self.output_label = ttk.Label(self.input_frame, text="Result: ", font=("Arial", 18), anchor="center")
        self.output_label.grid(row=len(self.inputs) + 3, column=0, padx=10, pady=10, sticky="nsew")
        self.output_label.grid_remove()  # Hide initially

        self.calculate_button = ttk.Button(self.input_frame, text="Calculate", command=self.calculate, style="TButton")
        self.calculate_button.grid(row=len(self.inputs) + 4, column=1, pady=10, sticky="nsew")
        self.calculate_button.grid_remove()  # Initially hidden

        # Back button
        self.back_button = ttk.Button(self.main_frame, text="Back", command=self.back, style="TButton")
        self.back_button.grid(row=4, column=0, columnspan=2, pady=20, sticky="nsew")

        # Custom button style
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 16), padding=10, width=15)

    def create_input_fields(self):
        fields = [
            "celsius", "kelvin", "pressure", "volume", "temperature", 
            "change_in_length", "original_length", "change_in_temperature",
            "thermal_conductivity", "area", "temperature_difference", "thickness",
            "heat_transfer", "temperature_change", "temperature_hot", "temperature_cold",
            "emissivity", "work_done",
        ]

        for idx, field in enumerate(fields):
            label = ttk.Label(self.input_frame, font=("Arial", 15), text=f"{field.replace('_', ' ').capitalize()}:")
            entry = ttk.Entry(self.input_frame, font=("Arial", 15))

            label.grid(row=idx + 1, column=0, sticky="ew", padx=10, pady=5)
            entry.grid(row=idx + 1, column=1, sticky="ew", padx=10, pady=5)

            self.input_frame.grid_columnconfigure(0, weight=1)
            self.input_frame.grid_columnconfigure(1, weight=3)

            self.inputs[field] = (label, entry)
            label.grid_remove()
            entry.grid_remove()

    def update_input_fields(self, event=None):
        """Show only the relevant input fields for the selected operation."""
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
                    entry.grid(row=idx + 1, column=1, padx=5, pady=5, sticky="ew")

            self.calculate_button.grid()  # Show the calculate button
        else:
            self.formula_label.config(text="")
            self.calculate_button.grid_remove()  # Hide the button if no operation is selected

    def calculate(self):
        """Perform the selected operation."""
        try:
            for key, (label, entry) in self.inputs.items():
                value = entry.get()
                if value:
                    setattr(self.thermo, key, float(value))
                elif key in self.operations[self.operation_var.get()][1]:
                    raise ValueError(f"Please enter a value for {label.cget('text').split(':')[0]}")

            operation = self.operation_var.get()
            if not operation:
                raise ValueError("No operation selected.")

            func, _ = self.operations[operation]
            result = func()

            # Show the result after calculation
            self.output_label.config(text=f"Result: {result:.4f}")
            self.output_label.grid()  # Make the result visible

        except ValueError as e:
            messagebox.showerror("Error", "Enter valid values")  # Shows the error message
        except Exception as e:
            messagebox.showerror("Notice", "Please select operation first!")

    def back(self):
        """Go back to the main screen."""
        self.root.withdraw()
        from Main import Main
        Main()  

    def convert_celsius_to_kelvin(self):
        return self.thermo.convert_celsius_to_kelvin()

    def convert_kelvin_to_celsius(self):
        return self.thermo.convert_kelvin_to_celsius()

    def ideal_gas_law(self):
        return self.thermo.ideal_gas_law()

    def thermal_expansion_coefficient(self):
        return self.thermo.thermal_expansion_coefficient()

    def heat_transfer_conduction(self):
        return self.thermo.heat_transfer_conduction()

    def heat_transfer_convection(self):
        return self.thermo.heat_transfer_convection()

    def heat_transfer_radiation(self):
        return self.thermo.heat_transfer_radiation()

    def first_law_thermodynamics(self):
        return self.thermo.first_law_thermodynamics()

    def efficiency_carnot(self):
        return self.thermo.efficiency_carnot()

    def entropy_change(self):
        return self.thermo.entropy_change()


# Main Application window setup
root = tk.Tk()
app = ThermodynamicsCalculator(root)
root.mainloop()
