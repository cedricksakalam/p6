import tkinter as tk
from tkinter import ttk, messagebox


class Operations(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Physics Solver")
        self.geometry("450x200")
        self.config(bg="tan")
        self.iconbitmap('C:/Users/ced/ACP FINAL PROJ/PeriodicTableUI/src/Icon.ico')
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        # Title Label
        self.label = tk.Label(self, text="Solve Physics Problems", font=("Papyrus", 15, "bold"))
        self.label.grid(pady=10, column=1)

        # Operation Selection Dropdown
        self.operations = {
            "Mechanics": self.calculate_mechanics,
            "Thermodynamics": self.explore_thermodynamics,
            "Unit Conversion": self.calculate_conversion,
            "Vectors": self.calculate_vector,
            "Electricity": self.calculate_electricity,
            "Newton's Laws": self.apply_newtons_laws,
            "Gravitational Force": self.calculate_gravitational_force,
            "Momentum": self.calculate_momentum,
            "Circular Motion": self.calculate_circular_motion,
            "Wave Dynamics": self.explore_wave_dynamics,
        }

        self.operation_label = ttk.Label(self, text="Select Operation:", font=("Papyrus", 10, "bold"), background="tan")
        self.operation_label.grid(row=1, column=0, pady=10, padx=10)

        self.operation_var = tk.StringVar()
        self.operation_menu = ttk.Combobox(
            self, textvariable=self.operation_var, values=list(self.operations.keys()), state="readonly", width=30
        )
        self.operation_menu.grid(row=1, column=1, pady=5, padx=5)
        self.operation_menu.bind("<<ComboboxSelected>>", self.display_instruction)

        # Instruction Label
        self.instruction_label = ttk.Label(self, text="", background="tan", font=("Papyrus", 10), wraplength=450)
        self.instruction_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Calculate Button
        self.calculate_button = ttk.Button(self, text="Solve", command=self.perform_operation)
        self.calculate_button.grid(row=3, column=0, columnspan=2, pady=20)

        # Output Label
        self.output_label = ttk.Label(self, text="Result: ", font=("Arial", 12), background="tan")
        self.output_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def display_instruction(self, event=None):
        """Update the instruction based on the selected operation."""
        operation = self.operation_var.get()
        instructions = {
            "Mechanics": "Perform calculations for mechanics problems.",
            "Thermodynamics": "Explore thermodynamic concepts and calculations.",
            "Unit Conversion": "Convert units of physical quantities.",
            "Vectors": "Perform vector operations like addition, subtraction, and dot product.",
            "Electricity": "Explore Electricity concepts and calculations.",
            "Newton's Laws": "Review and apply Newton's Laws of Motion.",
            "Gravitational Force": "Calculate gravitational forces using Newton's formula.",
            "Momentum": "Calculate momentum of objects.",
            "Circular Motion": "Solve problems involving centripetal force and circular motion.",
            "Wave Dynamics": "Explore wave properties and dynamics.",
        }
        self.instruction_label.config(text=instructions.get(operation, ""))

    def perform_operation(self):
        operation = self.operation_var.get()
        if operation and operation in self.operations:
            self.operations[operation]()
        else:
            messagebox.showerror("Selection Error", "Please select a valid operation.")

    def calculate_mechanics(self):
        from mechanics import MechanicsCalculator
        new_window = tk.Toplevel(self)
        MechanicsCalculator(new_window)

    def explore_thermodynamics(self):
        from Thermodynamics import ThermodynamicsCalculator
        new_window = tk.Toplevel(self)
        ThermodynamicsCalculator(new_window)

    def calculate_conversion(self):
        from units import UnitConverter
        new_window = tk.Toplevel(self)
        UnitConverter(new_window)

    def calculate_vector(self):
        from vectors import VectorCalculator
        new_window = tk.Toplevel(self)
        VectorCalculator(new_window)

    def calculate_electricity(self):
        from Electricty import ElectricityCalculator
        new_window = tk.Toplevel(self)
        ElectricityCalculator(new_window)

    def apply_newtons_laws(self):
        messagebox.showinfo("Newton's Laws", "Newton's Laws of Motion:\n1. An object at rest stays at rest...\n2. F=ma\n3. Action = Reaction.")

    def calculate_gravitational_force(self):
        G = 6.67430e-11
        m1 = 5.972e24
        m2 = 1
        r = 6371000
        force = G * (m1 * m2) / r**2
        self.output_label.config(text=f"Result: Gravitational Force = {force:.2e} N.")

    def calculate_momentum(self):
        mass = 5
        velocity = 10
        momentum = mass * velocity
        self.output_label.config(text=f"Result: Momentum = {momentum} kg·m/s.")

    def calculate_circular_motion(self):
        mass = 10
        velocity = 15
        radius = 3
        centripetal_force = mass * velocity**2 / radius
        self.output_label.config(text=f"Result: Centripetal Force = {centripetal_force} N.")

    def explore_wave_dynamics(self):
        frequency = 50
        wavelength = 2
        wave_speed = frequency * wavelength
        self.output_label.config(text=f"Result: Wave Speed = {wave_speed} m/s.")


if __name__ == "__main__":
    app = Operations()
    app.mainloop()
