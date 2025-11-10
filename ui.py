import tkinter as tk
from tkinter import scrolledtext, messagebox
from oglexer import Lexer

class LexerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Lexer Analyzer")
        root.configure(bg="#1e1e1e")
        self.root.attributes("-fullscreen", True)
        root.bind("<Escape>", lambda e: root.destroy())


        # Create main frame
        main_frame = tk.Frame(root, bg="#1e1e1e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Input section
        input_label = tk.Label(
            main_frame, 
            text="Source Code Input:", 
            font=("Segoe UI", 20, "bold"),
            bg="#1e1e1e",
            fg="#9CDCFE"
            )
        input_label.pack(anchor=tk.W, pady=(0, 8))


        self.input_text = scrolledtext.ScrolledText(
            main_frame,
            height=10,
            wrap=tk.WORD,
            font=("Consolas", 12),
            fg="#FFFFFF",
            bg="#252526",          # slightly lighter than background
            insertbackground="white",  # white blinking cursor
            borderwidth=0,
            relief="flat"
        )
        self.input_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # ===== Button Frame =====
        button_frame = tk.Frame(main_frame, bg="#1e1e1e")
        button_frame.pack(fill=tk.X, pady=(0, 15))

        tokenize_button = tk.Button(
            button_frame, text="Tokenize", command=self.tokenize_code,
            bg="#0E639C", fg="white",
            activebackground="#1177BB", activeforeground="white",
            font=("Segoe UI", 11, "bold"), relief="flat", padx=15, pady=6
        )
        tokenize_button.pack(side=tk.LEFT, padx=(0, 10))

        clear_button = tk.Button(
            button_frame, text="Clear All", command=self.clear_all,
            bg="#C33C3C", fg="white",
            activebackground="#E65050", activeforeground="white",
            font=("Segoe UI", 11, "bold"), relief="flat", padx=15, pady=6
        )
        clear_button.pack(side=tk.LEFT)

        # Output section
        output_frame = tk.Frame(main_frame, bg="#1e1e1e")
        output_frame.pack(fill=tk.BOTH, expand=True)

        # Tokens output
        tokens_label = tk.Label(
            output_frame, text="Tokens:",
            font=("Segoe UI", 14, "bold"),
            bg="#1e1e1e", fg="#CE9178"
        )
        tokens_label.pack(anchor=tk.W, pady=(5, 5))

        self.tokens_text = scrolledtext.ScrolledText(
            output_frame,
            height=8,
            wrap=tk.WORD,
            font=("Consolas", 12),
            fg="#DCDCAA", bg="#252526",
            insertbackground="white", borderwidth=0, relief="flat"
        )
        self.tokens_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Errors output
        errors_label = tk.Label(
            output_frame, text="Errors:",
            font=("Segoe UI", 14, "bold"),
            bg="#1e1e1e", fg="#F44747"
        )
        errors_label.pack(anchor=tk.W, pady=(5, 5))

        self.errors_text = scrolledtext.ScrolledText(
            output_frame,
            height=8,
            wrap=tk.WORD,
            font=("Consolas", 12),
            fg="#FFFFFF", bg="#2D1E1E",
            insertbackground="white", borderwidth=0, relief="flat"
        )
        self.errors_text.pack(fill=tk.BOTH, expand=True)

        # Load sample code
        self.load_sample_code()

    def tokenize_code(self):
        source_code = self.input_text.get("1.0", tk.END).strip()

        if not source_code:
            messagebox.showwarning("Warning", "Please enter some source code to tokenize.")
            return

        try:
            lexer = Lexer(source_code)
            tokens, errors = lexer.tokenize()

            # Clear previous output
            self.tokens_text.delete("1.0", tk.END)
            self.errors_text.delete("1.0", tk.END)

            # Display tokens
            if tokens:
                for token in tokens:
                    self.tokens_text.insert(tk.END, f"{token}\n")
            else:
                self.tokens_text.insert(tk.END, "No tokens generated.\n")

            # Display errors
            if errors:
                for error in errors:
                    self.errors_text.insert(tk.END, f"{error}\n")
            else:
                self.errors_text.insert(tk.END, "No errors found.\n")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during tokenization:\n{str(e)}")

    def clear_all(self):
        self.input_text.delete("1.0", tk.END)
        self.tokens_text.delete("1.0", tk.END)
        self.errors_text.delete("1.0", tk.END)

    def load_sample_code(self):
        sample_code = '''numero A = 123;
lutang B = 4.5;
teksto Message = "Hello, world!";
kung A >= 10:
    print("A is greater than or equal to 10");
ediwow'''
        self.input_text.insert(tk.END, sample_code)

def main():
    root = tk.Tk()
    app = LexerUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
