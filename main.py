import tkinter as tk
from tkinter import messagebox
import math
import fractions

class CasioFX991EX:
    def __init__(self, root):
        self.root = root
        self.root.title("Casio fx-991EX ClassWiz - Tkinter")
        self.root.geometry("480x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#d9d9d9")

        # Variables
        self.expression = ""
        self.ans = "0"
        self.memory = 0
        self.shift = False
        self.alpha = False

        # Display Frame
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        self.display = tk.Entry(root, textvariable=self.display_var, font=("Consolas", 24), bd=5, relief=tk.RIDGE,
                                justify='right', bg="#e6e6e6", fg="black", insertbackground='black')
        self.display.grid(row=0, column=0, columnspan=8, sticky="nsew", padx=5, pady=5, ipady=10)

        # Configure grid weights for responsiveness
        for i in range(9):
            root.grid_columnconfigure(i, weight=1)
        for i in range(8):
            root.grid_rowconfigure(i, weight=1)

        # Button colors
        self.colors = {
            "number": "#f0f0f0",
            "basic_op": "#d9d9d9",
            "func": "#b3c6ff",
            "mode": "#ffcc99",
            "memory": "#99cc99",
            "special": "#ff9999",
            "ans": "#ffffb3",
        }

        # Button layout (text, row, col, colspan, color category)
        buttons = [
            # Row 1: Mode buttons
            ("SHIFT", 1, 0, 1, "mode"), ("ALPHA", 1, 1, 1, "mode"), ("OPTN", 1, 2, 1, "mode"),
            ("CALC", 1, 3, 1, "mode"), ("ENG", 1, 4, 1, "mode"), ("DEL", 1, 5, 1, "special"),
            ("AC", 1, 6, 1, "special"), ("(", 1, 7, 1, "basic_op"),

            # Row 2
            ("STO", 2, 0, 1, "memory"), ("RCL", 2, 1, 1, "memory"), ("M+", 2, 2, 1, "memory"),
            ("M-", 2, 3, 1, "memory"), ("MR", 2, 4, 1, "memory"), ("MC", 2, 5, 1, "memory"),
            (")", 2, 6, 1, "basic_op"), ("÷", 2, 7, 1, "basic_op"),

            # Row 3
            ("sin", 3, 0, 1, "func"), ("cos", 3, 1, 1, "func"), ("tan", 3, 2, 1, "func"),
            ("ln", 3, 3, 1, "func"), ("log", 3, 4, 1, "func"), ("√", 3, 5, 1, "func"),
            ("x²", 3, 6, 1, "func"), ("×", 3, 7, 1, "basic_op"),

            # Row 4
            ("x³", 4, 0, 1, "func"), ("xʸ", 4, 1, 1, "func"), ("10ˣ", 4, 2, 1, "func"),
            ("eˣ", 4, 3, 1, "func"), ("nPr", 4, 4, 1, "func"), ("nCr", 4, 5, 1, "func"),
            ("!", 4, 6, 1, "func"), ("−", 4, 7, 1, "basic_op"),

            # Row 5
            ("π", 5, 0, 1, "func"), ("Ans", 5, 1, 1, "ans"), ("±", 5, 2, 1, "basic_op"),
            ("7", 5, 3, 1, "number"), ("8", 5, 4, 1, "number"), ("9", 5, 5, 1, "number"),
            ("Frac", 5, 6, 1, "func"), ("+", 5, 7, 1, "basic_op"),

            # Row 6
            ("abs", 6, 0, 1, "func"), ("∛", 6, 1, 1, "func"), ("EXP", 6, 2, 1, "func"),
            ("4", 6, 3, 1, "number"), ("5", 6, 4, 1, "number"), ("6", 6, 5, 1, "number"),
            ("", 6, 6, 1, "basic_op"), ("=", 6, 7, 2, "special"),

            # Row 7
            ("", 7, 0, 1, "basic_op"), ("", 7, 1, 1, "basic_op"), ("", 7, 2, 1, "basic_op"),
            ("1", 7, 3, 1, "number"), ("2", 7, 4, 1, "number"), ("3", 7, 5, 1, "number"),
            ("", 7, 6, 1, "basic_op"),

            # Row 8
            ("", 8, 0, 1, "basic_op"), ("", 8, 1, 1, "basic_op"), ("", 8, 2, 1, "basic_op"),
            ("0", 8, 3, 2, "number"), (".", 8, 5, 1, "number"),
            ("", 8, 6, 1, "basic_op"), ("", 8, 7, 1, "basic_op"),
        ]

        # Create buttons
        for (text, row, col, colspan, cat) in buttons:
            if text == "":
                continue  # skip empty placeholders

            btn = tk.Button(root, text=text, font=("Consolas", 14, "bold"),
                            bg=self.colors.get(cat, "#f0f0f0"),
                            fg="black", bd=1, relief=tk.RAISED,
                            command=lambda t=text: self.on_button_click(t))
            btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=2, pady=2, ipady=10)

        # Bind keyboard input (optional)
        root.bind("<Return>", lambda event: self.on_button_click("="))
        root.bind("<BackSpace>", lambda event: self.on_button_click("DEL"))

    def on_button_click(self, char):
        try:
            if char == "AC":
                self.expression = ""
                self.display_var.set("0")
            elif char == "DEL":
                self.expression = self.expression[:-1]
                self.display_var.set(self.expression if self.expression else "0")
            elif char == "=":
                self.evaluate_expression()
            elif char == "Ans":
                self.expression += self.ans
                self.display_var.set(self.expression)
            elif char == "±":
                self.toggle_sign()
            elif char == "π":
                self.expression += str(math.pi)
                self.display_var.set(self.expression)
            elif char == "STO":
                self.memory = self.safe_eval(self.expression)
                self.display_var.set("Stored")
                self.expression = ""
            elif char == "RCL":
                self.expression += str(self.memory)
                self.display_var.set(self.expression)
            elif char == "M+":
                self.memory += self.safe_eval(self.expression)
                self.display_var.set("M+")
                self.expression = ""
            elif char == "M-":
                self.memory -= self.safe_eval(self.expression)
                self.display_var.set("M-")
                self.expression = ""
            elif char == "MR":
                self.expression += str(self.memory)
                self.display_var.set(self.expression)
            elif char == "MC":
                self.memory = 0
                self.display_var.set("Memory Cleared")
                self.expression = ""
            elif char == "x²":
                self.expression += "**2"
                self.display_var.set(self.expression)
            elif char == "x³":
                self.expression += "**3"
                self.display_var.set(self.expression)
            elif char == "xʸ":
                self.expression += "**"
                self.display_var.set(self.expression)
            elif char == "√":
                self.expression += "sqrt("
                self.display_var.set(self.expression)
            elif char == "∛":
                self.expression += "cbrt("
                self.display_var.set(self.expression)
            elif char == "10ˣ":
                self.expression += "10**"
                self.display_var.set(self.expression)
            elif char == "eˣ":
                self.expression += "exp("
                self.display_var.set(self.expression)
            elif char == "log":
                self.expression += "log10("
                self.display_var.set(self.expression)
            elif char == "ln":
                self.expression += "log("
                self.display_var.set(self.expression)
            elif char == "sin":
                self.expression += "sin("
                self.display_var.set(self.expression)
            elif char == "cos":
                self.expression += "cos("
                self.display_var.set(self.expression)
            elif char == "tan":
                self.expression += "tan("
                self.display_var.set(self.expression)
            elif char == "!":
                self.expression += "!"
                self.display_var.set(self.expression)
            elif char == "nPr":
                self.expression += "nPr("
                self.display_var.set(self.expression)
            elif char == "nCr":
                self.expression += "nCr("
                self.display_var.set(self.expression)
            elif char == "abs":
                self.expression += "abs("
                self.display_var.set(self.expression)
            elif char == "EXP":
                self.expression += "e"
                self.display_var.set(self.expression)
            elif char == "Frac":
                self.convert_fraction()
            elif char in "0123456789.":
                self.expression += char
                self.display_var.set(self.expression)
            elif char in "+−×÷()":
                # Map to python operators
                mapping = {'−': '-', '×': '*', '÷': '/'}
                self.expression += mapping.get(char, char)
                self.display_var.set(self.expression)
            else:
                # For mode buttons and placeholders, just show a message
                self.display_var.set(f"{char} pressed (not implemented)")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")
            self.expression = ""
            self.display_var.set("0")

    def toggle_sign(self):
        # Toggle sign of current number at the end of expression
        import re
        # Find last number in expression
        matches = list(re.finditer(r"(\d+\.?\d*|\.\d+)$", self.expression))
        if matches:
            last_num = matches[-1]
            start, end = last_num.span()
            num_str = self.expression[start:end]
            if num_str.startswith("-"):
                new_num = num_str[1:]
            else:
                new_num = "-" + num_str
            self.expression = self.expression[:start] + new_num
            self.display_var.set(self.expression)
        else:
            # If no number found, just prepend '-'
            if self.expression.startswith("-"):
                self.expression = self.expression[1:]
            else:
                self.expression = "-" + self.expression
            self.display_var.set(self.expression)

    def convert_fraction(self):
        # Convert current expression to fraction if possible
        try:
            val = self.safe_eval(self.expression)
            frac = fractions.Fraction(val).limit_denominator()
            self.expression = str(frac)
            self.display_var.set(self.expression)
        except Exception:
            messagebox.showerror("Error", "Cannot convert to fraction")

    def evaluate_expression(self):
        try:
            expr = self.expression

            # Replace factorials
            expr = self.replace_factorials(expr)

            # Replace nPr and nCr
            expr = self.replace_nPr_nCr(expr)

            # Replace cbrt with power 1/3
            expr = expr.replace("cbrt(", "pow(")
            # Replace pow(x, 1/3) for cube root
            # We'll handle cbrt(x) as pow(x, 1/3) by adding ,1/3) after argument
            # But since cbrt( is replaced by pow(, we need to add ,1/3) at the end of argument
            # For simplicity, user must enter cbrt(x) as cbrt(x) only, so we replace cbrt(x) with pow(x,1/3)
            # We'll do a regex replacement:
            import re
            def cbrt_repl(match):
                inner = match.group(1)
                return f"pow({inner},1/3)"
            expr = re.sub(r"pow\(([^()]+)\)", cbrt_repl, expr)

            # Allowed names for eval
            allowed_names = {
                'sin': lambda x: math.sin(math.radians(x)),
                'cos': lambda x: math.cos(math.radians(x)),
                'tan': lambda x: math.tan(math.radians(x)),
                'log': math.log,
                'log10': math.log10,
                'sqrt': math.sqrt,
                'pow': pow,
                'exp': math.exp,
                'abs': abs,
                'pi': math.pi,
                'e': math.e,
                'factorial': math.factorial,
                'nPr': self.nPr,
                'nCr': self.nCr,
            }

            # Evaluate safely
            result = eval(expr, {"__builtins__": None}, allowed_names)

            # Store answer
            self.ans = str(result)
            self.display_var.set(self.ans)
            self.expression = self.ans
        except ZeroDivisionError:
            messagebox.showerror("Error", "Division by zero")
            self.expression = ""
            self.display_var.set("0")
        except ValueError as ve:
            messagebox.showerror("Error", f"Math domain error: {ve}")
            self.expression = ""
            self.display_var.set("0")
        except SyntaxError:
            messagebox.showerror("Error", "Syntax error")
            self.expression = ""
            self.display_var.set("0")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")
            self.expression = ""
            self.display_var.set("0")

    def replace_factorials(self, expr):
        import re
        # Replace n! with factorial(n)
        pattern = r'(\d+|\([^()]*\))!'
        while re.search(pattern, expr):
            match = re.search(pattern, expr)
            span = match.span()
            token = match.group(1)
            expr = expr[:span[0]] + f'factorial({token})' + expr[span[1]:]
        return expr

    def replace_nPr_nCr(self, expr):
        import re
        # Replace nPr(a,b) with nPr(a,b)
        # Replace nCr(a,b) with nCr(a,b)
        # We just keep as is because nPr and nCr are in allowed_names
        # But user might enter nPr(5,3) or nCr(5,3)
        # So no replacement needed here
        return expr

    def safe_eval(self, expr):
        # Evaluate expression safely for memory functions
        expr = self.replace_factorials(expr)
        expr = self.replace_nPr_nCr(expr)
        allowed_names = {
            'sin': lambda x: math.sin(math.radians(x)),
            'cos': lambda x: math.cos(math.radians(x)),
            'tan': lambda x: math.tan(math.radians(x)),
            'log': math.log,
            'log10': math.log10,
            'sqrt': math.sqrt,
            'pow': pow,
            'exp': math.exp,
            'abs': abs,
            'pi': math.pi,
            'e': math.e,
            'factorial': math.factorial,
            'nPr': self.nPr,
            'nCr': self.nCr,
        }
        return eval(expr, {"__builtins__": None}, allowed_names)

    def nPr(self, n, r):
        # Permutations nPr = n! / (n-r)!
        try:
            n = int(n)
            r = int(r)
            if r > n or n < 0 or r < 0:
                raise ValueError("Invalid nPr values")
            return math.factorial(n) // math.factorial(n - r)
        except Exception:
            raise ValueError("Invalid nPr values")

    def nCr(self, n, r):
        # Combinations nCr = n! / (r! * (n-r)!)
        try:
            n = int(n)
            r = int(r)
            if r > n or n < 0 or r < 0:
                raise ValueError("Invalid nCr values")
            return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))
        except Exception:
            raise ValueError("Invalid nCr values")

if __name__ == "__main__":
    root = tk.Tk()
    app = CasioFX991EX(root)
    root.mainloop()
