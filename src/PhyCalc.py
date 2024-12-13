import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Physics Solver")
        self.geometry("1920x1080")
        self.config(bg="#03254c") 
        self.state('zoomed')  # Start window maximized
        self.create_widgets()
        
        # Bottom GIF
        self.bottom_frames = self.load_gif("C:/Users/ced/Physics Project/Physics/src/mechanics.gif")
        self.bottom_current_frame_index = 0
        self.bottom_canvas = tk.Canvas(self, bg='#03254c', highlightthickness=0)
        self.bottom_canvas.pack(side="bottom", fill="x")
        self.bottom_label = tk.Label(self.bottom_canvas, bg='#03254c')
        self.bottom_label.pack()
        
        # Side GIFs
        self.left_frames = self.load_gif("C:/Users/ced/Physics Project/Physics/src/electricity.gif")
        self.left_current_frame_index = 0
        self.left_canvas = tk.Canvas(self, bg='#03254c', highlightthickness=0)
        self.left_canvas.place(relx=0.2, rely=0.82, anchor="center")
        self.left_label = tk.Label(self.left_canvas, bg='#03254c')
        self.left_label.pack()

        self.right_frames = self.load_gif("C:/Users/ced/Physics Project/Physics/src/waves.gif")
        self.right_current_frame_index = 0
        self.right_canvas = tk.Canvas(self, bg='#03254c', highlightthickness=0)
        self.right_canvas.place(relx=0.8, rely=0.82, anchor="center")
        self.right_label = tk.Label(self.right_canvas, bg='#03254c')
        self.right_label.pack()

        self.update_backgrounds()
    
    def load_gif(self, filepath):
        gif = Image.open(filepath)
        frames = []
        bg_color = (3, 37, 76)

        try:
            while True:
                frame = gif.convert("RGBA")
                background = Image.new("RGBA", frame.size, bg_color)
                composite = Image.alpha_composite(background, frame)
                frames.append(ImageTk.PhotoImage(composite))
                gif.seek(len(frames))
        except EOFError:
            pass
        return frames

    def update_backgrounds(self):
        # Update bottom GIF
        bottom_frame = self.bottom_frames[self.bottom_current_frame_index]
        self.bottom_label.config(image=bottom_frame)
        self.bottom_current_frame_index = (self.bottom_current_frame_index + 1) % len(self.bottom_frames)

        # Update left GIF
        left_frame = self.left_frames[self.left_current_frame_index]
        self.left_label.config(image=left_frame)
        self.left_current_frame_index = (self.left_current_frame_index + 1) % len(self.left_frames)

        # Update right GIF
        right_frame = self.right_frames[self.right_current_frame_index]
        self.right_label.config(image=right_frame)
        self.right_current_frame_index = (self.right_current_frame_index + 1) % len(self.right_frames)

        self.after(100, self.update_backgrounds)

    def create_widgets(self):
        """This function is responsible for setting up all UI components."""
        # Header label for "Solve Physics Problems"
        self.label = tk.Label(self, text="PhyCalc: Your Physics Partner", bg='#03254c', font=("Arial", 80, "bold"), fg='#d0efff')
        self.label.pack(pady=100)

        self.label = tk.Label(self, text="Power up your physics with a calculator that tackles electricity mechanics and sound waves, delivering fast, accurate results every time!", bg='#03254c', font=("Papyrus", 20, "bold"), fg='#d0efff')
        self.label.pack(pady=50)
        
        button_frame = tk.Frame(self, bg='#03254c')
        button_frame.pack(pady=40)
        
        self.electricity = tk.Button(button_frame, text="Solve for Electricity", font=("Georgia", 30), bg='#40B7FF', command=self.solve_electricity)
        self.electricity.pack(side="left", padx=60)

        self.mechanics = tk.Button(button_frame, text="Solve for Mechanics", bg='#40B7FF', font=("Georgia", 30), command=self.solve_mechanics)
        self.mechanics.pack(side="left", padx=60)
        
        self.soundwaves = tk.Button(button_frame, text="Solve for Sound Waves", bg='#40B7FF', font=("Georgia", 30), command=self.solve_Waves)
        self.soundwaves.pack(side="left", padx=60)

    def solve_mechanics(self):
        from mechanics import MechanicsCalculator
        self.withdraw()  # Hide the main window
        self.mechanics = MechanicsCalculator(self)  # Pass the main window as parent
        self.mechanics.grab_set()  # Block interaction with the main window until this window is closed

    def solve_Waves(self):
        from Waves import SoundWaveCalculator
        self.withdraw()  # Hide the main window
        self.waves = SoundWaveCalculator(self)  # Pass the main window as parent
        self.waves.grab_set()  # Block interaction with the main window until this window is closed

    def solve_electricity(self):
        from Electricity import ElectricityCalculator
        self.withdraw()  # Hide the main window
        self.electricity = ElectricityCalculator(self)  # Pass the main window as parent
        self.electricity.grab_set()  # Block interaction with the main window until this window is closed

if __name__ == "__main__":
    app = Main()
    app.mainloop()

