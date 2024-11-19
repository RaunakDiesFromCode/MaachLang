import tkinter as tk
from tkinter import scrolledtext
import basic  # Your custom module


class IDLEApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MachLang Shell")

        # Add a menu bar (like Python's IDLE)
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

        # Create the main text area for the shell output and input
        self.text_area = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, height=20, width=80, state=tk.NORMAL
        )
        self.text_area.pack(pady=10)

        # Initialize the shell prompt
        self.insert_text("MachLang Shell\nType 'exit' or 'tham' to quit.\n🐟~~~> ")
        self.text_area.bind("<Return>", self.execute_command)  # Bind Return key
        self.text_area.bind(
            "<BackSpace>", self.prevent_prompt_deletion
        )  # Prevent prompt deletion
        self.text_area.focus()  # Focus the text area for typing

    def show_about(self):
        tk.messagebox.showinfo("About", "MachLang Shell IDLE\nCreated by Raunak")

    def insert_text(self, text):
        """Insert text into the shell."""
        self.text_area.insert(tk.END, text)
        self.text_area.see(tk.END)  # Auto-scroll to the bottom

    def execute_command(self, event=None):
        """Execute a command typed into the shell."""
        input_text = self.get_current_line()  # Get the last line of input
        self.text_area.insert(tk.END, "\n")  # Move to a new line after input
        if input_text.strip() in ["exit", "tham"]:
            self.insert_text("Exiting...\n")
            self.root.quit()
            return

        # Evaluate the input using your basic module
        result, error = basic.run("<AjobFile>", input_text)
        if error:
            self.insert_text(f"{error.as_string()}")
        else:
            self.insert_text(f"{result}")
        self.insert_text("\n🐟~~~> ")

        # Stop the default newline behavior
        return "break"

    def get_current_line(self):
        """Get the current line of text where the cursor is located."""
        current_index = self.text_area.index(tk.INSERT)  # Get the cursor position
        line_start = f"{current_index.split('.')[0]}.0"  # Start of the current line
        line_end = f"{current_index.split('.')[0]}.end"  # End of the current line
        return self.text_area.get(line_start, line_end).replace("🐟~~~>", "").strip()

    def prevent_prompt_deletion(self, event=None):
        """Prevent deleting the prompt."""
        cursor_position = self.text_area.index(tk.INSERT)  # Get the cursor position
        line_start = f"{cursor_position.split('.')[0]}.0"  # Start of the current line
        prompt_text = self.text_area.get(
            line_start, line_start + "+6c"
        )  # Get the first 6 characters
        if "🐟~~~>" in prompt_text and cursor_position.split(".")[1] == "6":
            # Stop the BackSpace if it's at the prompt
            return "break"
        return None


# Main loop to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = IDLEApp(root)
    root.mainloop()
