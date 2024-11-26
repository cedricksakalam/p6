from tkinter import *

def bt_draw(key, col, lin):
    bt = Button(window, text=key, command=lambda: bt_press(key), width=5, height=2, font=("Arial", 14))
    bt.grid(column=col, row=lin+2, padx=0, pady=0, sticky="nsew")  # Remove padding and use sticky to fill the grid space
    return bt

def bt_press(key):
    if key == 'C': 
        disp['text'] = ''
    elif key == '<': 
        disp['text'] = disp['text'][:-1]
    elif key == '=':
        try:
            disp['text'] = str(round(eval(disp['text']), 6))
        except:
            disp['text'] = "Error"
    else:
        disp['text'] += key

def key_event(event):
    key = event.char
    if key in '0123456789+-*/().':
        bt_press(key)
    elif event.keysym == 'Return':
        bt_press('=')
    elif event.keysym == 'BackSpace':
        bt_press('<')
    elif event.keysym == 'Escape':
        bt_press('C')

def main_menu():
    window.destroy()
    from Operations import Operations
    Operations()

window = Tk()
window.title('Calculator')
window.resizable(False, False)
window.config(bg='tan')

# Main Menu Button
menu_button = Button(window, text="Main Menu", command=main_menu, font=("Arial", 14), bg="lightgray", width=15)
menu_button.grid(column=0, row=0, columnspan=4, padx=10, pady=5, sticky="w")  # Top-left, spans 4 columns

# Display configuration
disp = Label(window, text='', anchor='e', font=("Arial", 24), bg="white", relief="ridge", height=2, width=20)
disp.grid(column=0, row=1, columnspan=4, padx=5, pady=5)  # Positioned underneath "Main Menu", spans 4 columns

# Button creation (numbers, operators, and special buttons)
keys = '()C<789/456*123-.0=+'
bt_list = [bt_draw(keys[n], n % 4, n // 4) for n in range(len(keys))]  # Buttons aligned with 4 columns

# Adjusting the columns and rows for no gaps
for i in range(4):
    window.grid_columnconfigure(i, weight=1, uniform="equal")  # Uniform column sizes with no extra space

# Adjust row configuration to allow for flexible row heights and no gaps
for i in range(7):  # Number of rows (from the button grid and display)
    window.grid_rowconfigure(i, weight=1)

# Key bindings for keyboard support
window.bind("<Key>", key_event)

window.mainloop()
