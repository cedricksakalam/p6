import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import PhotoImage

class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Physics Solver")
        self.geometry("1920x1080")
        self.config(bg="white")
        self.iconbitmap('C:/Users/ced/ACP FINAL PROJ/PeriodicTableUI/src/Icon.ico')
        self.state('zoomed')

        # Initialize widgets
        self.create_widgets()

        # Handle close event
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.quit()  # Close the Main window
        self.master.deiconify()  # Show the previous (calculator) window again

    def create_widgets(self):
        """This function is responsible for setting up all UI components."""
        # Label for "Solve Physics Problems" with font size 40
        self.label = tk.Label(self, text="Solve Physics Problems", font=("Papyrus", 40, "bold"))
        # Place the label at the center of the window
        self.label.place(relx=0.5, rely=0.1, anchor="center")  # Positioned at the top center

        # Define the style for the buttons
        self.setup_button_style()

        # Frame to hold the boxes
        self.box_frame = ttk.Frame(self)
        self.box_frame.place(relx=0.5, rely=0.7, anchor="center")

        # Configure rows and columns in the grid to be equally sized
        for i in range(5):
            self.box_frame.grid_columnconfigure(i, weight=1, uniform="equal")
        
        # Create the boxes (with text and buttons)
        self.create_boxes()

    def setup_button_style(self):
        """Define the style of the buttons to remove the default white background."""
        style = ttk.Style(self)
        style.configure("TButton",
                        background="lightgray",  # Set background color for the button
                        relief="flat",           # Make the button flat to avoid 3D effect
                        padding=(3, 5),          # Reduced padding to make the button smaller
                        width=25,                # Adjust width of the button
                        font=("Arial", 8))       # Make the font smaller for the button

        # Ensure button's background remains lightgray when pressed or active
        style.map("TButton",
                  foreground=[('pressed', 'black'), ('active', 'black')],
                  background=[('pressed', 'lightgray'), ('active', 'lightgray')])

    def create_boxes(self):
        """Create 5 boxes with a description and button."""
        box_width = 30  # Increased width for more space
        box_height = 8  # Increased height for better readability

        # Custom descriptions for each box
        descriptions = [
            "Mechanics\n\n\n\n\n\n",
            "Thermodynamics\n\n\n\n\n\n",
            "Unit Conversion\n\n\n\n\n\n",
            "Vectors\n\n\n\n\n\n",
            "Electricity.\n\n\n\n\n\n"
        ]

        # Create the boxes, each with text and a button
        for i in range(5):
            self.create_box(i, descriptions[i])

    def create_box(self, index, description_text):
        """Create a box with a description and a button."""
        # Create a gray background for the box (a Label widget)
        box = tk.Label(self.box_frame, bg="lightgray", relief="solid")
        box.grid(row=0, column=index, padx=10, pady=10, sticky="nsew")  # Adjusted to fill cell

        # Add the custom description or text at the top part of the box
        description = tk.Label(box, text=description_text, bg="lightgray", font=("Arial", 10, "bold"), wraplength=200)
        description.pack(padx=10, pady=100)  # Adjusted padding for better readability

        # Optionally, you can add an image here (ensure the image path is correct)
        try:
            img = PhotoImage(file="path_to_image.png")  # Replace with actual image path
            image_label = tk.Label(box, image=img, bg="lightgray")
            image_label.image = img  # Keep reference to image to prevent garbage collection
            image_label.pack()  # Add the image below the description
        except Exception as e:
            print(f"Error loading image: {e}")

        # Modify the button text for specific boxes
        if index == 0:
            button_text = "Solve for Mechanics"
            button_command = self.solve_mechanics
        elif index == 1:
            button_text = "Solve for Thermodynamics"
            button_command = self.solve_thermodynamics
        elif index == 2:
            button_text = "Converting Units"
            button_command = self.unit_conversion
        elif index == 3:
            button_text = "Solve for Vectors"
            button_command = self.solve_vectors
        elif index == 4:
            button_text = "Solving Electricity"
            button_command = self.solve_electricity
        else:
            button_text = f"Box {index + 1}"
            button_command = None

        # Create the button below the description and image
        button = ttk.Button(box, text=button_text, command=button_command, style="TButton")
        button.pack(pady=5)  # Reduced padding for the button placement

    def solve_mechanics(self):
        from mechanics import MechanicsCalculator
        self.withdraw()  # Hide the main window
        self.mechanics_calculator = MechanicsCalculator(self)  # Pass the current root (self) to MechanicsCalculator
        self.mechanics_calculator.root.mainloop()  # Run the mechanics calculator loop
        self.deiconify()  # Show the main window again once the mechanics calculator is closed

    def solve_thermodynamics(self):
        from Thermodynamics import ThermodynamicsCalculator
        self.withdraw()  # Hide the main window
        self.thermodynamics = ThermodynamicsCalculator(self)  # Pass the current root (self) to MechanicsCalculator
        self.unit_converter.root.mainloop()  # Run the mechanics calculator loop
        self.deiconify()  # Show the main window again once the mechanics calculator is closed

    def unit_conversion(self):
        from units import UnitConverter
        self.withdraw()  # Hide the main window
        self.unit_converter = UnitConverter(self)  # Pass the current root (self) to MechanicsCalculator
        self.unit_converter.root.mainloop()  # Run the mechanics calculator loop
        self.deiconify()  # Show the main window again once the mechanics calculator is closed

    def solve_vectors(self):
        """Function to solve vector-related problems."""
        messagebox.showinfo("Vectors", "Vector calculations are being processed...")

    def solve_electricity(self):
        from Electricty import ElectricityCalculator
        self.withdraw()  # Hide the main window
        self.unit_converter = ElectricityCalculator(self)  # Pass the current root (self) to MechanicsCalculator
        self.unit_converter.root.mainloop()  # Run the mechanics calculator loop
        self.deiconify()  # Show the main window again once the mechanics calculator is closed


if __name__ == "__main__":
    app = Main()
    app.mainloop()
