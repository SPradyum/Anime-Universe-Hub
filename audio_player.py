import customtkinter as ctk
import pygame
import os
import random
import ffmpeg


class MusicPlayer(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("Anime OST Player 🎵")
        self.geometry("800x520")
        self.resizable(False, False)
        self.attributes("-alpha", 0.0)
        self.fade_in()

        pygame.mixer.init()

        # Correct path to your OST folder
        self.folder = r"E:\Documents\Projects\Python\Anime Project\assets\ost"
        print("Looking for music in:", self.folder)

        # Collect raw files
        if os.path.exists(self.folder):
            raw_files = os.listdir(self.folder)
            print("Files detected:", raw_files)
        else:
            print("⚠ Folder not found!")
            raw_files = []

        # Auto convert unsupported formats
        self.playlist = self.prepare_playlist(raw_files)
        print("Playlist ready:", self.playlist)

        self.index = 0

        # UI Layout
        main_frame = ctk.CTkFrame(self, corner_radius=20)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        header = ctk.CTkLabel(main_frame, text="Anime OST Player",
                              font=("Consolas", 24, "bold"), text_color="#34D399")
        header.pack(pady=15)

        self.song_label = ctk.CTkLabel(
            main_frame,
            text=self.playlist[self.index].replace(".wav", "").replace(".mp3", "").replace(".ogg", "")
            if self.playlist else "No audio found",
            font=("Consolas", 18), text_color="#FBBF24"
        )
        self.song_label.pack(pady=10)

        control_frame = ctk.CTkFrame(main_frame, corner_radius=16)
        control_frame.pack(pady=10)

        self.btn_play = ctk.CTkButton(control_frame, text="▶ Play", width=120, command=self.play_music)
        self.btn_play.grid(row=0, column=0, padx=10, pady=10)

        self.btn_pause = ctk.CTkButton(control_frame, text="⏸ Pause", width=120, command=self.pause_music)
        self.btn_pause.grid(row=0, column=1, padx=10, pady=10)

        self.btn_resume = ctk.CTkButton(control_frame, text="▶ Resume", width=120, command=self.resume_music)
        self.btn_resume.grid(row=0, column=2, padx=10, pady=10)

        self.btn_prev = ctk.CTkButton(control_frame, text="⏮ Prev", width=120, command=self.prev_song)
        self.btn_prev.grid(row=1, column=0, padx=10, pady=10)

        self.btn_next = ctk.CTkButton(control_frame, text="⏭ Next", width=120, command=self.next_song)
        self.btn_next.grid(row=1, column=2, padx=10, pady=10)

        # Visualizer fake bars
        self.visual_frame = ctk.CTkFrame(main_frame, corner_radius=16)
        self.visual_frame.pack(pady=20, fill="x", padx=60)

        self.bars = []
        for i in range(12):
            bar = ctk.CTkFrame(self.visual_frame, width=10, height=20, corner_radius=4)
            bar.grid(row=0, column=i, padx=4, pady=10, sticky="s")
            self.bars.append(bar)

        self.animate_visualizer()

    # Fade effect
    def fade_in(self):
        alpha = self.attributes("-alpha")
        if alpha < 1.0:
            alpha += 0.06
            self.attributes("-alpha", alpha)
            self.after(20, self.fade_in)

    # Prepare playlist with auto-conversion
    def prepare_playlist(self, file_list):
        supported = [".mp3", ".wav", ".ogg"]
        final_list = []

        for file in file_list:
            ext = os.path.splitext(file)[1].lower()

            if ext in supported:
                final_list.append(file)
            else:
                print(f"⚠ Unsupported file detected: {file} → Converting to WAV...")
                input_path = os.path.join(self.folder, file)
                output_name = os.path.splitext(file)[0] + ".wav"
                output_path = os.path.join(self.folder, output_name)

                try:
                    ffmpeg.input(input_path).output(output_path).run(overwrite_output=True)
                    print("✔ Converted:", output_name)
                    final_list.append(output_name)
                except Exception as e:
                    print("❌ AutoConvert failed:", e)

        return final_list

    # Play with retry conversion if MP3 crashes
    def play_music(self):
        if not self.playlist:
            print("⚠ No music available")
            return

        path = os.path.join(self.folder, self.playlist[self.index])
        print("Now playing:", path)

        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(loops=0)
        except Exception as e:
            print("❌ Load failed, converting to WAV:", e)

            new_name = os.path.splitext(self.playlist[self.index])[0] + "_fixed.wav"
            new_path = os.path.join(self.folder, new_name)

            try:
                ffmpeg.input(path).output(new_path).run(overwrite_output=True)
                print("🎵 Converted OK:", new_path)

                self.playlist[self.index] = new_name  # Replace entry
                pygame.mixer.music.load(new_path)
                pygame.mixer.music.play(loops=0)
            except Exception as error:
                print("💥 Conversion failure:", error)

    def pause_music(self):
        pygame.mixer.music.pause()

    def resume_music(self):
        pygame.mixer.music.unpause()

    def next_song(self):
        if not self.playlist:
            return
        self.index = (self.index + 1) % len(self.playlist)
        self.song_label.configure(text=self.playlist[self.index].replace(".wav", "").replace(".mp3", ""))
        self.play_music()

    def prev_song(self):
        if not self.playlist:
            return
        self.index = (self.index - 1) % len(self.playlist)
        self.song_label.configure(text=self.playlist[self.index].replace(".wav", "").replace(".mp3", ""))
        self.play_music()

    def animate_visualizer(self):
        for bar in self.bars:
            bar.configure(height=random.randint(15, 70))
        self.after(120, self.animate_visualizer)
