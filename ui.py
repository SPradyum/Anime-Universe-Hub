import customtkinter as ctk
from selector import AnimeSelector
from audio_player import MusicPlayer
from PIL import Image
import os

POSTER_DIR = r"E:\Documents\PROJECTS\Python\Anime Project\assets\posters"
BG_NAME = "Anime"

BG_PATH = None
for f in os.listdir(POSTER_DIR):
    if f.lower().startswith(BG_NAME.lower()):
        BG_PATH = os.path.join(POSTER_DIR, f)
        break
if not BG_PATH:
    raise FileNotFoundError("No background poster found for ALL-ROUND. Check posters folder.")



class AppUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Anime Universe Hub 🎌")
        self.geometry("1100x700")
        self.resizable(True, True)

        # fade animation alpha
        self.fade = 0
        self.attributes("-alpha", 0.0)

        # Build UI
        self.build_background()
        self.build_home()

        # Fade in intro animation
        self.fade_in()

        # Apply fullscreen after rendering (important to avoid bg vanish)
        self.after(80, lambda: self.state("zoomed"))


    # ----------------------------------
    # Fade animation
    # ----------------------------------
    def fade_in(self):
        if self.fade < 1:
            self.fade += 0.05
            self.attributes("-alpha", self.fade)
            self.after(30, self.fade_in)


    # ----------------------------------
    # Background + overlay layer
    # ----------------------------------
    def build_background(self):
        # Load raw and resize based on current screen
        self.bg_raw = Image.open(BG_PATH)
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        resized = self.bg_raw.resize((screen_w, screen_h))
        self.bg_img = ctk.CTkImage(light_image=resized, size=(screen_w, screen_h))
        self._bg_keep = self.bg_img  # prevent GC removal

        # Set background label
        self.bg_label = ctk.CTkLabel(self, text="", image=self.bg_img)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Translucent overlay using Canvas stipple
        self.overlay = ctk.CTkCanvas(self, width=screen_w, height=screen_h,
                                     highlightthickness=0)
        self.overlay.place(x=0, y=0)
        self.overlay.create_rectangle(
            0, 0, screen_w, screen_h,
            fill="black", stipple="gray50"
        )


    # ----------------------------------
    # Home screen UI panel
    # ----------------------------------
    def build_home(self):
        self.panel = ctk.CTkFrame(self, width=600, height=450,
                                  corner_radius=22, fg_color="#0F172A")
        self.panel.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        title = ctk.CTkLabel(
            self.panel, text="ANIME UNIVERSE HUB",
            font=("Consolas", 42, "bold"),
            text_color="#FBBF24"
        )
        title.pack(pady=(25, 15))

        subtitle = ctk.CTkLabel(
            self.panel,
            text="🎭 Character Quiz  •  🎵 OST Player",
            font=("Consolas", 20, "bold"),
            text_color="#93C5FD",
        )
        subtitle.pack(pady=(0, 20))

        # Buttons
        quiz_btn = ctk.CTkButton(
            self.panel, text="🎭 Start Anime Quiz",
            width=380, height=55,
            font=("Consolas", 22, "bold"),
            fg_color="#DC2626",
            hover_color="#F87171",
            command=self.open_quiz
        )
        quiz_btn.pack(pady=15)

        music_btn = ctk.CTkButton(
            self.panel, text="🎵 Launch OST Player",
            width=380, height=55,
            font=("Consolas", 22, "bold"),
            fg_color="#2563EB",
            hover_color="#3B82F6",
            command=self.open_music
        )
        music_btn.pack(pady=10)


    # ----------------------------------
    # Navigation
    # ----------------------------------
    def open_quiz(self):
        AnimeSelector(self, self.launch_quiz)

    def launch_quiz(self, anime):
        from quiz import QuizWindow
        QuizWindow(self, anime)

    def open_music(self):
        MusicPlayer(self)
