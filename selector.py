import customtkinter as ctk
from PIL import Image, ImageOps
import os

POSTER_DIR = r"E:\Documents\Projects\Python\Anime Project\assets\posters"


class AnimeSelector(ctk.CTkToplevel):
    def __init__(self, master, on_select):
        super().__init__(master)

        self.title("Select Anime World 🎌")
        self.geometry("1100x700")
        self.resizable(False, False)
        self.on_select = on_select

        self.categories = [
            "ONE PIECE", "ONE PUNCH MAN", "DRAGON BALL Z", "DEATH NOTE", "JJk",
            "INITIAL D", "BLEACH", "BERSERK", "Demon Slayer","MyHeroAcademia",
            "Solo Leveling", "ALL-ROUND"
        ]
        self.index = 0

        self.bg_label = ctk.CTkLabel(self, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.main_frame = ctk.CTkFrame(self, corner_radius=20, width=900, height=550, fg_color="#020617")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.heading = ctk.CTkLabel(self.main_frame, text="Choose Your Anime World",
                                   font=("Consolas", 30, "bold"), text_color="#FBBF24")
        self.heading.pack(pady=(20, 10))

        self.name_label = ctk.CTkLabel(self.main_frame, text="", font=("Consolas", 38, "bold"))
        self.name_label.pack(pady=(10, 15))

        self.poster_label = ctk.CTkLabel(self.main_frame, text="")
        self.poster_label.pack(pady=10)

        btn_frame = ctk.CTkFrame(self.main_frame, corner_radius=18)
        btn_frame.pack(pady=20)

        self.prev_btn = ctk.CTkButton(btn_frame, text="◀", font=("Consolas", 26, "bold"),
                                      width=120, height=50, command=self.prev_category)
        self.prev_btn.grid(row=0, column=0, padx=15)

        self.start_btn = ctk.CTkButton(btn_frame, text="Start Quiz 🚀", width=220, height=55,
                                       font=("Consolas", 22, "bold"),
                                       fg_color="#DC2626", hover_color="#F87171",
                                       command=self.start_quiz)
        self.start_btn.grid(row=0, column=1, padx=15)

        self.next_btn = ctk.CTkButton(btn_frame, text="▶", font=("Consolas", 26, "bold"),
                                      width=120, height=50, command=self.next_category)
        self.next_btn.grid(row=0, column=2, padx=15)

        self.update_display()


    def find_poster_file(self, base_name):
        search_key = base_name.lower().replace(" ", "").replace("-", "").replace("_", "")

        for file in os.listdir(POSTER_DIR):
            normalized = file.lower().replace(" ", "").replace("-", "").replace("_", "")
            if normalized.startswith(search_key):
                return os.path.join(POSTER_DIR, file)

        print(f"❌ Poster not found for: {base_name}")
        return None


    def update_display(self):
        cat = self.categories[self.index]

        self.name_label.configure(text=cat, text_color="#FFFFFF")

        full_path = self.find_poster_file(cat)

        if full_path:
            poster = Image.open(full_path)
            poster = ImageOps.contain(poster, (520, 380))
            self.poster_img = ctk.CTkImage(light_image=poster, size=poster.size)
            self.poster_label.configure(image=self.poster_img, text="")
        else:
            self.poster_label.configure(image=None, text="❌ Poster Not Found")


    def next_category(self):
        self.index = (self.index + 1) % len(self.categories)
        self.update_display()

    def prev_category(self):
        self.index = (self.index - 1) % len(self.categories)
        self.update_display()

    def start_quiz(self):
        self.on_select(self.categories[self.index])
        self.destroy()
