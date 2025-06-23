from gui.main_app import SimuladorElectoralApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorElectoralApp(root)
    root.mainloop()