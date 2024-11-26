import tkinter as tk
from tkinter import ttk, messagebox
from mecha import Mechanics  # Ensure Mechanics.py is in the same folder

class MechanicsCalculator:
    def __init__(self, root):
        self.mechanics = Mechanics()
        self.root = root
        self.root.title("Mechanics Calculator")

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
        self.main_frame.grid_rowconfigure(2, weight=0)  # Operation menu (modified)
        self.main_frame.grid_rowconfigure(3, weight=1)  # Input and output
        self.main_frame.grid_rowconfigure(4, weight=0)  # Back button
        self.main_frame.grid_columnconfigure(0, weight=1)  # Input frame

        # Mechanics title label
        self.title_label = ttk.Label(
            self.main_frame,
            text="Solving Mechanics",
            font=("Arial", 60, "bold"),
            anchor="center",
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20), sticky="n")

        # New Mechanics description label below the title
        self.description_label = ttk.Label(
            self.main_frame,
            text="Focuses on the motion of objects and the forces that affect them. It includes concepts such as \nNewton's laws, kinematics, dynamics, and statics, applicable in understanding the physical behavior of systems.",
            font=("Arial", 13),
            anchor="center",
            justify="center",
        )
        self.description_label.grid(row=1, column=0, columnspan=2, pady=(5, 10), sticky="n")

        # Adjust the grid and layout so the operation dropdown is placed beneath the description
        self.operation_label = ttk.Label(self.main_frame, text="Select Operation:", font=("Arial", 15, "bold"))
        self.operation_label.grid(row=2, column=0, padx=10, pady=20, sticky="e")

        # Map of operations and corresponding methods and required inputs
        self.operations = {
            "Velocity": (self.calculate_velocity, ["initial_velocity", "acceleration", "time"], "v = u + at"),
            "Displacement": (self.calculate_displacement, ["initial_velocity", "acceleration", "time"], "s = ut + 1/2 * a * t^2"),
            "Acceleration": (self.calculate_acceleration, ["final_velocity", "initial_velocity", "time"], "a = (v - u) / t"),
            "Force": (self.calculate_force, ["mass", "acceleration"], "F = m * a"),
            "Work": (self.calculate_work, ["force", "displacement", "angle"], "W = F * d * cos(θ)"),
            "Kinetic Energy": (self.calculate_kinetic_energy, ["mass", "velocity"], "KE = 1/2 * m * v^2"),
            "Power": (self.calculate_power, ["work", "time"], "P = W / t"),
            "Momentum": (self.calculate_momentum, ["mass", "velocity"], "p = m * v"),
            "Impulse": (self.calculate_impulse, ["force", "time"], "I = F * t"),
            "Circular Velocity": (self.calculate_circular_velocity, ["radius", "period"], "v = 2 * π * r / T"),
            "Centripetal Acceleration": (self.calculate_centripetal_acceleration, ["velocity", "radius"], "a_c = v^2 / r"),
            "Torque": (self.calculate_torque, ["force", "lever_arm"], "τ = F * r * sin(θ)"),
            "Angular Velocity": (self.calculate_angular_velocity, ["angular_displacement", "time"], "ω = θ / t"),
            "Angular Acceleration": (self.calculate_angular_acceleration, ["angular_velocity", "time"], "α = (ω - ω_0) / t"),
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

        self.calculate_button = ttk.Button(self.input_frame, text="Calculate", command=self.calculate, style="TButton")
        self.calculate_button.grid(row=len(self.inputs) + 4, column=1, pady=10, sticky="nsew")
        self.calculate_button.grid_remove()  # Initially hidden

        self.back_button = ttk.Button(self.main_frame, text="Back", command=self.back, style="TButton")
        self.back_button.grid(row=4, column=0, columnspan=2, pady=20, sticky="nsew")

        style.configure("TButton", font=("Arial", 16), padding=10, width=15)

    def create_input_fields(self):
        fields = [
            "initial_velocity", "acceleration", "time", "final_velocity",
            "mass", "velocity", "force", "displacement", "angle", "work",
            "radius", "period", "lever_arm", "angular_displacement", "angular_velocity"
        ]

        for idx, field in enumerate(fields):
            label = ttk.Label(self.input_frame, font=("Arial", 15), text=f"{field.replace('_', ' ').capitalize()}:")
            entry = ttk.Entry(self.input_frame, font=("Arial", 15))
            
            # Center the label and entry within the input frame
            label.grid(row=idx + 1, column=0, sticky="ew", padx=10, pady=5)  # Ensure label is centered
            entry.grid(row=idx + 1, column=1, sticky="ew", padx=10, pady=5)  # Ensure entry is centered

            # Center the labels and entries in the input_frame
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
                    entry.grid(row=idx + 1, column=1, padx=5, pady=5, sticky="ew")

            # Show the "Calculate" button when an operation is selected
            self.calculate_button.grid()  # Make the calculate button visible
        else:
            self.formula_label.config(text="")
            self.calculate_button.grid_remove()  # Hide the "Calculate" button if no operation is selected

    def calculate(self):
        try:
            # Check if any required input fields are empty
            for key, (label, entry) in self.inputs.items():
                value = entry.get()
                if value:
                    setattr(self.mechanics, key, float(value))
                elif key in self.operations[self.operation_var.get()][1]:
                    raise ValueError(f"Please enter a value for {label.cget('text').split(':')[0]}")

            operation = self.operation_var.get()
            if not operation:
                raise ValueError("No operation selected.")

            func, _, _ = self.operations[operation]
            result = func()

            # Show the result only after calculation
            self.output_label.config(text=f"Result: {result:.4f}")
            self.output_label.grid()  # Make the result visible

        except ValueError as e:
            messagebox.showerror("Error", f"Enter valid values")  # Shows the error message
        except Exception as e:
            messagebox.showerror("Notice", f"Please select operation first!")

    def back(self):
        self.root.withdraw()
        from Main import Main
        Main()  

    def calculate_velocity(self):
        return self.mechanics.calculate_velocity()

    def calculate_displacement(self):
        return self.mechanics.calculate_displacement()

    def calculate_acceleration(self):
        return self.mechanics.calculate_acceleration()

    def calculate_force(self):
        return self.mechanics.calculate_force()

    def calculate_work(self):
        return self.mechanics.calculate_work()

    def calculate_kinetic_energy(self):
        return self.mechanics.calculate_kinetic_energy()

    def calculate_power(self):
        return self.mechanics.calculate_power()

    def calculate_momentum(self):
        return self.mechanics.calculate_momentum()

    def calculate_impulse(self):
        return self.mechanics.calculate_impulse()

    def calculate_circular_velocity(self):
        return self.mechanics.calculate_circular_velocity()

    def calculate_centripetal_acceleration(self):
        return self.mechanics.calculate_centripetal_acceleration()

    def calculate_torque(self):
        return self.mechanics.calculate_torque()

    def calculate_angular_velocity(self):
        return self.mechanics.calculate_angular_velocity()

    def calculate_angular_acceleration(self):
        return self.mechanics.calculate_angular_acceleration()
if __name__ == "__main__":
    root = tk.Tk()
    app = MechanicsCalculator(root)
    root.mainloop()
