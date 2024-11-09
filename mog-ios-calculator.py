import tkinter as tk
import math
import re

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to Calculator App")
        self.root.geometry("300x200")
        self.root.resizable(False, False)
        
        # Initial Launch Screen
        welcome_label = tk.Label(self.root, text="Welcome to iOS Style Calculator", font=("Helvetica", 14), pady=20)
        welcome_label.pack()
        
        open_button = tk.Button(self.root, text="Open Calculator", font=("Helvetica", 14), bg="#FF9500", fg="white", 
                                command=self.open_calculator)
        open_button.pack(expand=True, fill="both", padx=20, pady=20)

    def open_calculator(self):
        # Destroy the welcome screen and open the main calculator
        self.root.destroy()
        root = tk.Tk()
        Calculator(root)
        root.mainloop()

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("iOS Style Calculator")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        self.memory = 0

        # iOS Color Scheme
        self.colors = {
            "display": "#000000",
            "function": "#A5A5A5",
            "operation": "#FF9500",
            "number": "#333333",
            "text": "#FFFFFF",
            "background": "#000000"
        }

        # Display variables
        self.display_text = tk.StringVar()
        self.display_text.set("0")
        self.font_size = 40  # Initial font size for display text
        self.max_display_length = 12  # Maximum number of characters on display

        # Create display and buttons
        self.create_display()
        self.create_buttons([
            ['AC', '%', '±', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ])

        # Menu for Credits
        self.create_menu()

    def create_display(self):
        # Display Frame
        display_frame = tk.Frame(self.root, bg=self.colors["display"])
        display_frame.pack(expand=True, fill="both")

        # Display Label with adjustable font
        self.display_label = tk.Label(
            display_frame, textvariable=self.display_text, anchor="e",
            bg=self.colors["display"], fg=self.colors["text"], padx=24,
            font=("Helvetica", self.font_size, "bold")
        )
        self.display_label.pack(expand=True, fill="both")

    def create_buttons(self, buttons):
        # Button Frame
        button_frame = tk.Frame(self.root, bg=self.colors["background"])
        button_frame.pack(expand=True, fill="both")

        for row in buttons:
            row_frame = tk.Frame(button_frame, bg=self.colors["background"])
            row_frame.pack(expand=True, fill="both")
            for btn_text in row:
                if btn_text in ["AC", "%", "±"]:
                    button_color = self.colors["function"]
                elif btn_text in ["/", "*", "-", "+", "="]:
                    button_color = self.colors["operation"]
                else:
                    button_color = self.colors["number"]

                button = tk.Button(
                    row_frame, text=btn_text, font=("Helvetica", 24), fg=self.colors["text"],
                    bg=button_color, activebackground="#5A5A5A", borderwidth=0,
                    command=lambda x=btn_text: self.button_click(x)
                )
                button.pack(side="left", expand=True, fill="both", padx=5, pady=5)

                if btn_text == '0':
                    button.pack_configure(expand=True, fill="both", ipadx=70)

    def create_menu(self):
        # Create a menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Add "Help" menu with "Credits" option
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Credits", command=self.show_credits)

    def show_credits(self):
        # Create a new window for credits
        credits_window = tk.Toplevel(self.root)
        credits_window.title("Credits")
        credits_window.geometry("300x200")
        credits_window.resizable(False, False)

        # Credits message
        credits_text = (
            "Made by @misterofgames_yt on YouTube\n"
            "GitHub: https://github.com/MOG-Developing"
        )
        
        # Display credits information
        credits_label = tk.Label(
            credits_window, text=credits_text, font=("Helvetica", 12), fg=self.colors["text"],
            bg=self.colors["display"], padx=10, pady=10, justify="center"
        )
        credits_label.pack(expand=True, fill="both")

        # Close button
        close_button = tk.Button(
            credits_window, text="Close", font=("Helvetica", 14), bg="#FF9500", fg="white", 
            command=credits_window.destroy
        )
        close_button.pack(pady=20, ipadx=10)

    def button_click(self, key):
        try:
            if key == "=":
                self.calculate()
            elif key == "AC":
                self.clear()
            elif key == "%":
                self.insert_percentage()
            elif key == "±":
                self.plus_minus()
            else:
                self.insert_value(key)
        except Exception:
            self.display_text.set("Error")

    def insert_value(self, value):
        current = self.display_text.get()

        if value in "+-*/":
            # Prevent consecutive operators
            if current[-1] in "+-*/":
                current = current[:-1]  # Replace the last operator with the new one
            new_text = current + value
        elif value == ".":
            # Allow only one decimal point in the current number segment
            if "." in current.split(" ")[-1]:  # Check if current number already has a decimal
                return  # Ignore if decimal already exists
            new_text = current + value
        else:
            # Handle normal digit input
            if current == "0" or current == "Error":
                new_text = value  # Replace "0" or "Error" with the new number
            else:
                new_text = current + value

        if len(new_text) > self.max_display_length:
            self.adjust_font_size(len(new_text))

        self.display_text.set(new_text)

    def insert_percentage(self):
        try:
            expression = self.display_text.get()
            
            if expression[-1] in "0123456789":  # Only apply if the last character is a number
                value = float(expression) / 100
                self.display_text.set(str(value))
            else:
                self.display_text.set("Error")  # Invalid usage of %
        except:
            self.display_text.set("Error")

    def adjust_font_size(self, length):
        if length <= 10:
            self.font_size = 40
        elif length <= 12:
            self.font_size = 36
        elif length <= 14:
            self.font_size = 32
        else:
            self.font_size = 28
        self.display_label.config(font=("Helvetica", self.font_size, "bold"))

    def calculate(self):
        try:
            expression = self.display_text.get()

            # Remove trailing operator if it exists
            if expression[-1] in "+-*/":
                expression = expression[:-1]

            # Convert percentages in expressions like "50+20%" to "50+0.2*50"
            expression = re.sub(r'(\d+(\.\d+)?)%', r'(\1/100)', expression)
            
            result = eval(expression)

            if isinstance(result, float) and (result > 1e10 or result < 1e-10):
                result_str = f"{result:.6e}"  # Scientific notation
            else:
                result_str = f"{result:.10g}"  # Max 10 significant digits

            if len(result_str) > self.max_display_length:
                self.adjust_font_size(len(result_str))
            self.display_text.set(result_str[:self.max_display_length])
        except:
            self.display_text.set("Error")

    def clear(self):
        self.display_text.set("0")
        self.font_size = 40
        self.display_label.config(font=("Helvetica", self.font_size, "bold"))

    def plus_minus(self):
        try:
            value = float(self.display_text.get())
            self.display_text.set(str(-value)[:self.max_display_length])
        except:
            self.display_text.set("Error")

# Main code to run the initial screen
if __name__ == "__main__":
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()
