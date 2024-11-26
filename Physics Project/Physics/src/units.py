import tkinter as tk
from tkinter import ttk, messagebox

class UnitConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Unit Converter")

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

        # Title label
        self.title_label = ttk.Label(
            self.main_frame,
            text="Unit Converter",
            font=("Arial", 60, "bold"),
            anchor="center",
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20), sticky="n")

        # Description label
        self.description_label = ttk.Label(
            self.main_frame,
            text="Provides tools to convert between different measurement units for length, mass, volume, time, and temperature,\nensuring accuracy and consistency in calculations across various systems of measurement.",
            font=("Arial", 13),
            anchor="center",
            justify="center",
        )
        self.description_label.grid(row=1, column=0, columnspan=2, pady=(5, 10), sticky="n")

        # Operation selection label
        self.operation_label = ttk.Label(self.main_frame, text="Select Conversion:", font=("Arial", 15, "bold"))
        self.operation_label.grid(row=2, column=0, padx=10, pady=20, sticky="e")

        # Map of operations and corresponding methods
        self.operations = {
            "Celsius to Fahrenheit": (self.convert_celsius_to_fahrenheit, ["value"], "(Celsius * 9/5) + 32"),
            "Fahrenheit to Celsius": (self.convert_fahrenheit_to_celsius, ["value"], "(Fahrenheit - 32) * 5/9"),
            "Kilometers to Miles": (self.convert_km_to_miles, ["value"], "Kilometers * 0.621371"),
            "Miles to Kilometers": (self.convert_miles_to_km, ["value"], "Miles / 0.621371"),
            "Kilograms to Pounds": (self.convert_kg_to_pounds, ["value"], "Kilograms * 2.20462"),
            "Pounds to Kilograms": (self.convert_pounds_to_kg, ["value"], "Pounds / 2.20462"),
            "Centimeters to Meters": (self.convert_cm_to_meters, ["value"], "Centimeters / 100"),
            "Centimeters to Inches": (self.convert_cm_to_inches, ["value"], "Centimeters / 2.54"),
            "Meters to Yards": (self.convert_meter_to_yards, ["value"], "Meters * 1.09361")
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
        self.operation_menu.grid(row=2, column=1, padx=20, pady=20, sticky="ew")
        self.operation_menu.bind("<<ComboboxSelected>>", self.update_input_fields)

        # Input fields
        self.input_frame = ttk.LabelFrame(self.main_frame, text="Inputs", padding=(5, 5))
        self.input_frame.grid(row=3, column=0, padx=200, pady=10, sticky="nsew")
        self.input_frame.grid_propagate(False)  # Prevent the frame from resizing
        self.inputs = {}
        self.create_input_fields()

        # Formula inside the Input frame
        self.formula_label = ttk.Label(self.input_frame, text="", font=("Arial", 14), justify="center")
        self.formula_label.grid(row=0, column=0, padx=10, pady=(10, 20), sticky="nsew")

        # Initially hide the result and calculate button
        self.output_label = ttk.Label(self.input_frame, text="Result: ", font=("Arial", 18), anchor="center")
        self.output_label.grid(row=len(self.inputs) + 3, column=0, padx=10, pady=10, sticky="nsew")
        self.output_label.grid_remove()  # Hide initially

        self.convert_button = ttk.Button(self.input_frame, text="Convert", command=self.convert, style="TButton")
        self.convert_button.grid(row=len(self.inputs) + 4, column=1, pady=10, sticky="nsew")
        self.convert_button.grid_remove()  # Initially hidden

        self.back_button = ttk.Button(self.main_frame, text="Back", command=self.back, style="TButton")
        self.back_button.grid(row=4, column=0, columnspan=2, pady=20, sticky="nsew")

        style.configure("TButton", font=("Arial", 16), padding=10, width=15)

    def create_input_fields(self):
        """Create the input fields for the converter."""
        for field in ["value"]:
            label = ttk.Label(self.input_frame, font=("Arial", 15), text=f"{field.capitalize()}:")
            entry = ttk.Entry(self.input_frame, font=("Arial", 15))
            
            label.grid(row=1, column=0, sticky="ew", padx=10, pady=5)  # Ensure label is centered
            entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)  # Ensure entry is centered

            self.inputs[field] = (label, entry)
            label.grid_remove()
            entry.grid_remove()

    def update_input_fields(self, event=None):
        """Update input fields based on selected operation."""
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

            # Show the "Convert" button when an operation is selected
            self.convert_button.grid()  # Make the calculate button visible
        else:
            self.formula_label.config(text="")
            self.convert_button.grid_remove()  # Hide the "Convert" button if no operation is selected

    def convert(self):
        """Perform the selected conversion."""
        try:
            value = self.inputs["value"][1].get()
            if not value:
                raise ValueError("No value entered.")

            value = float(value)

            operation = self.operation_var.get()
            if operation:
                # Perform the calculation
                func, _, _ = self.operations[operation]
                result = func(value)

                # Show the result only after calculation
                self.output_label.config(text=f"Result: {result:.4f}")
                self.output_label.grid()  # Make the result visible
            else:
                raise ValueError("No operation selected.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Conversion Methods
    def convert_celsius_to_fahrenheit(self, celsius):
        """Formula: (Celsius * 9/5) + 32"""
        return (celsius * 9/5) + 32

    def convert_fahrenheit_to_celsius(self, fahrenheit):
        """Formula: (Fahrenheit - 32) * 5/9"""
        return (fahrenheit - 32) * 5/9

    def convert_km_to_miles(self, kilometers):
        """Formula: Kilometers * 0.621371"""
        return kilometers * 0.621371

    def convert_miles_to_km(self, miles):
        """Formula: Miles / 0.621371"""
        return miles / 0.621371

    def convert_kg_to_pounds(self, kilograms):
        """Formula: Kilograms * 2.20462"""
        return kilograms * 2.20462

    def convert_pounds_to_kg(self, pounds):
        """Formula: Pounds / 2.20462"""
        return pounds / 2.20462

    def convert_cm_to_meters(self, centimeters):
        """Formula: Centimeters / 100"""
        return centimeters / 100

    def convert_cm_to_inches(self, centimeters):
        """Formula: Centimeters / 2.54"""
        return centimeters / 2.54

    def convert_meter_to_yards(self, meters):
        """Formula: Meters * 1.09361"""
        return meters * 1.09361

    def back(self):
        """Go back to the main screen."""
        self.root.withdraw()
        from Main import Main
        Main()  

def main():
    root = tk.Tk()
    app = UnitConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
