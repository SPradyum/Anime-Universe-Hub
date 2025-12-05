import customtkinter as ctk
import json


JSON_PATH = r"E:\Documents\Projects\Python\Anime Project\data\quiz_questions.json"


class QuizWindow(ctk.CTkToplevel):
    def __init__(self, master, category: str):
        super().__init__(master)

        self.category = category
        self.title(f"Anime Quiz — {category} 🎭")
        self.geometry("950x600")
        self.resizable(False, False)

        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        if self.category == "ALL-ROUND":
            self.questions = data["all_rounder"]
        else:
            self.questions = data["categories"][self.category]

        self.index = 0
        self.score = {}

        self.build_ui()

    def theme_for_category(self, cat: str):
        themes = {
            "ONE PIECE":  ("#FACC15", "#022C22"),
            "ONE PUNCH MAN": ("#F97316", "#111827"),
            "DRAGON BALL Z": ("#FB923C", "#020617"),
            "DEATH NOTE": ("#E5E7EB", "#020617"),
            "INITIAL D": ("#38BDF8", "#020617"),
            "BLEACH": ("#F97316", "#0B1120"),
            "BERSERK": ("#F87171", "#111827"),
            "ALL-ROUND": ("#A855F7", "#020617"),
        }
        return themes.get(cat, ("#FBBF24", "#020617"))

    def build_ui(self):
        accent, bg = self.theme_for_category(self.category)

        self.main_frame = ctk.CTkFrame(self, corner_radius=20, fg_color=bg)
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        header = ctk.CTkLabel(
            self.main_frame,
            text=f"{self.category} QUIZ",
            font=("Consolas", 28, "bold"),
            text_color=accent,
        )
        header.pack(pady=(20, 10))

        self.question_label = ctk.CTkLabel(
            self.main_frame,
            text=self.questions[self.index]["question"],
            font=("Consolas", 20, "bold"),
            wraplength=820,
            text_color="#E5E7EB",
        )
        self.question_label.pack(pady=(15, 20))

        self.options_frame = ctk.CTkFrame(self.main_frame, corner_radius=18, fg_color="#020617")
        self.options_frame.pack(pady=10)

        self.buttons = []
        for opt in self.questions[self.index]["options"]:
            btn = ctk.CTkButton(
                self.options_frame,
                text=opt["text"],
                width=600,
                height=50,
                font=("Consolas", 16),
                fg_color=accent,
                hover_color="#F97316",
                command=lambda c=opt["character"]: self.next_question(c),
            )
            btn.pack(pady=8)
            self.buttons.append(btn)

        self.progress_label = ctk.CTkLabel(
            self.main_frame,
            text=f"Question {self.index + 1} / {len(self.questions)}",
            font=("Consolas", 14),
            text_color="#9CA3AF",
        )
        self.progress_label.pack(pady=(10, 5))

    def next_question(self, character_key: str):
        self.score[character_key] = self.score.get(character_key, 0) + 1
        self.index += 1

        if self.index >= len(self.questions):
            self.show_result()
            return

        q = self.questions[self.index]
        self.question_label.configure(text=q["question"])
        self.progress_label.configure(
            text=f"Question {self.index + 1} / {len(self.questions)}"
        )

        for i, opt in enumerate(q["options"]):
            self.buttons[i].configure(
                text=opt["text"],
                command=lambda c=opt["character"]: self.next_question(c),
            )

    def show_result(self):
        winner = max(self.score, key=self.score.get)
        accent, bg = self.theme_for_category(self.category)

        for w in self.main_frame.winfo_children():
            w.destroy()

        self.main_frame.configure(fg_color=bg)

        ctk.CTkLabel(
            self.main_frame,
            text="QUIZ COMPLETE!",
            font=("Consolas", 28, "bold"),
            text_color=accent,
        ).pack(pady=(60, 20))

        ctk.CTkLabel(
            self.main_frame,
            text=f"You match the vibes of: {winner.upper()} 🔥",
            font=("Consolas", 24, "bold"),
            text_color="#E5E7EB",
        ).pack(pady=20)