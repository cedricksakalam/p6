import tkinter as tk
from tkinter import ttk, messagebox
import math


class VectorOperations:
    def __init__(self):
        self.vector_a = [0, 0, 0]
        self.vector_b = [0, 0, 0]

    def set_vectors(self, vector_a, vector_b=None):
        self.vector_a = vector_a
        if vector_b is not None:
            self.vector_b = vector_b

    def vector_addition(self):
        return [self.vector_a[i] + self.vector_b[i] for i in range(3)]

    def vector_subtraction(self):
        return [self.vector_a[i] - self.vector_b[i] for i in range(3)]

    def dot_product(self):
        return sum(self.vector_a[i] * self.vector_b[i] for i in range(3))

    def cross_product(self):
        return [
            self.vector_a[1] * self.vector_b[2] - self.vector_a[2] * self.vector_b[1],
            self.vector_a[2] * self.vector_b[0] - self.vector_a[0] * self.vector_b[2],
            self.vector_a[0] * self.vector_b[1] - self.vector_a[1] * self.vector_b[0]
        ]

    def magnitude(self, vector=None):
        if vector is None:
            vector = self.vector_a
        return math.sqrt(sum(v**2 for v in vector))

    def scalar_multiplication(self, scalar):
        return [scalar * v for v in self.vector_a]


class VectorCalculator:
    def __init__(self, root):
        self.vector_ops = VectorOperations()
        self.root = root
        self.root.title("Vector Operations")

        # Full-screen window and resizable
        self.root.geometry('1000x700')
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Main frame (fills the screen)
        self.main_frame = ttk.Frame(root)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Title
        self.title_label = ttk.Label(self.main_frame, text="Vector Operations", font=("Arial", 60, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20), sticky="nsew")

        # Description
        self.description_label = ttk.Label(
            self.main_frame,
            text="Perform vector operations such as addition, subtraction, dot product, and more.",
            font=("Arial", 15),
            anchor="center",
            justify="center"
        )
        self.description_label.grid(row=1, column=0, columnspan=2, pady=(5, 10), sticky="nsew")

        # Operation selector
        self.operation_label = ttk.Label(self.main_frame, text="Select Operation:", font=("Arial", 15, "bold"))
        self.operation_label.grid(row=2, column=0, padx=10, pady=20, sticky="e")

        self.operations = {
            "Vector Addition (A + B)": "both_vectors",
            "Vector Subtraction (A - B)": "both_vectors",
            "Dot Product (A . B)": "both_vectors",
            "Cross Product (A x B)": "both_vectors",
            "Magnitude of A (|A|)": "single_vector",
            "Magnitude of B (|B|)": "single_vector",
            "Scalar Multiplication (k * A)": "scalar_and_vector",
        }

        self.operation_var = tk.StringVar()
        self.operation_menu = ttk.Combobox(self.main_frame, textvariable=self.operation_var, values=list(self.operations.keys()), state="readonly", height=9)
        self.operation_menu.grid(row=2, column=1, padx=20, pady=20, sticky="ew")
        self.operation_menu.bind("<<ComboboxSelected>>", self.update_input_fields)

        # Input frame
        self.input_frame = ttk.LabelFrame(self.main_frame, text="Inputs", padding=(10, 10))
        self.input_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="nsew")
        self.inputs = {}
        self.create_input_fields()

        # Formula display
        self.formula_label = ttk.Label(self.input_frame, text="", font=("Arial", 14), justify="center")
        self.formula_label.grid(row=0, column=0, padx=10, pady=(10, 20), sticky="nsew")

        # Calculate button
        self.calculate_button = ttk.Button(self.input_frame, text="Calculate", command=self.calculate)
        self.calculate_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Output label
        self.output_label = ttk.Label(self.input_frame, text="Result: ", font=("Arial", 18), anchor="center")
        self.output_label.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.output_label.grid_remove()  # Hide initially

        # Back button
        self.back_button = ttk.Button(self.main_frame, text="Back", command=self.back)
        self.back_button.grid(row=4, column=0, columnspan=2, pady=20, sticky="nsew")

    def create_input_fields(self):
        fields = [
            "vector_a_x", "vector_a_y", "vector_a_z", "vector_b_x", "vector_b_y", "vector_b_z", "scalar"
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
        for label, entry in self.inputs.values():
            label.grid_remove()
            entry.grid_remove()

        operation = self.operation_var.get()
        if operation in self.operations:
            field_type = self.operations[operation]
            if field_type == "both_vectors":
                self.create_vector_fields("A", 0)
                self.create_vector_fields("B", 3)
            elif field_type == "single_vector":
                self.create_vector_fields("A", 0)
            elif field_type == "scalar_and_vector":
                self.create_scalar_field()
                self.create_vector_fields("A", 1)

            self.calculate_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
            self.output_label.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        else:
            self.formula_label.config(text="")
            self.calculate_button.grid_remove()
            self.output_label.grid_remove()

    def create_vector_fields(self, label, row_offset):
        ttk.Label(self.input_frame, text=f"Vector {label} x:").grid(row=row_offset, column=0, sticky=tk.W, padx=5, pady=2)
        self.inputs[f"vector_{label.lower()}_x"][1].grid(row=row_offset, column=1, padx=5, pady=2)

        ttk.Label(self.input_frame, text=f"Vector {label} y:").grid(row=row_offset + 1, column=0, sticky=tk.W, padx=5, pady=2)
        self.inputs[f"vector_{label.lower()}_y"][1].grid(row=row_offset + 1, column=1, padx=5, pady=2)

        ttk.Label(self.input_frame, text=f"Vector {label} z:").grid(row=row_offset + 2, column=0, sticky=tk.W, padx=5, pady=2)
        self.inputs[f"vector_{label.lower()}_z"][1].grid(row=row_offset + 2, column=1, padx=5, pady=2)

    def create_scalar_field(self):
        ttk.Label(self.input_frame, text="Scalar k:").grid(row=4, column=0, padx=10, pady=5)
        self.inputs["scalar"][1].grid(row=4, column=1, padx=10, pady=5)

    def calculate(self):
        operation = self.operation_var.get()
        try:
            vector_a = [float(self.inputs["vector_a_x"][1].get()), float(self.inputs["vector_a_y"][1].get()), float(self.inputs["vector_a_z"][1].get())]
            vector_b = [float(self.inputs["vector_b_x"][1].get()), float(self.inputs["vector_b_y"][1].get()), float(self.inputs["vector_b_z"][1].get())] if "B" in operation else None
            self.vector_ops.set_vectors(vector_a, vector_b)
            
            result = ""
            if operation == "Vector Addition (A + B)":
                result = self.vector_ops.vector_addition()
            elif operation == "Vector Subtraction (A - B)":
                result = self.vector_ops.vector_subtraction()
            elif operation == "Dot Product (A . B)":
                result = self.vector_ops.dot_product()
            elif operation == "Cross Product (A x B)":
                result = self.vector_ops.cross_product()
            elif operation == "Magnitude of A (|A|)":
                result = self.vector_ops.magnitude(vector_a)
            elif operation == "Magnitude of B (|B|)":
                result = self.vector_ops.magnitude(vector_b)
            elif operation == "Scalar Multiplication (k * A)":
                scalar = float(self.inputs["scalar"][1].get())
                result = self.vector_ops.scalar_multiplication(scalar)

            self.output_label.config(text=f"Result: {result}")
            self.output_label.grid()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numerical values.")
  
    def back(self):
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = VectorCalculator(root)
    root.mainloop()
