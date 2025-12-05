import customtkinter as ctk
from ui import AppUI

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def main():
    app = AppUI()
    app.mainloop()


if __name__ == "__main__":
    main()
