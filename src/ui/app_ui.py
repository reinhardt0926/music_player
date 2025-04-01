import os
import sys
import pygame
import time
import threading
from tkinter import *
from tkinter import filedialog, ttk

class MusicPlayer():
    def __init__(self, root):
        # self.root = Toplevel(root)
        self.root = root
        self.root.geometry("500x220")
        self.root.title("Play a Music")
        self.skip_speed = 5
        self.loop_start = None
        self.loop_end = None
        self.looping = False

        # 재생 위치 기준 오프셋 변수
        self.offset = 0

        top_frame = Frame(self.root)
        top_frame.grid(row=0, column=0, padx=10, pady=5, sticky="wens")

        # 원하는 파일 찾기
        file_btn = Button(top_frame, text="File Select", command=self.file_select)
        file_btn.config(bg="white", highlightthickness=0, width=15)
        file_btn.grid(row=0, column=0, padx=(5, 10), pady=10, sticky="w")

        # skip speed combobox
        number = StringVar()
        self.speed_combo = ttk.Combobox(
            top_frame, textvariable=number, state="readonly", postcommand=self.adjust_combo
        )
        self.speed_combo['value'] = [num for num in range(50)]
        self.speed_combo.current(self.skip_speed)
        self.speed_combo.bind("<<ComboboxSelected>>", self.select_speed)
        self.speed_combo.config(width=10)
        self.speed_combo.grid(row=0, column=2, padx=1, pady=10, sticky="w")

        # label 만들기
        speed_label = Label(top_frame, text="Skip Speed")
        speed_label.grid(row=0, column=1, padx=5, pady=10, sticky="w")

        explain_label = Label(top_frame, text="Repeated playback of music file")
        explain_label.grid(row=1, column=0, columnspan=3, padx=5, sticky="w")

        button_frame = Frame(self.root)
        button_frame.grid(row=2, column=0, padx=10, pady=(5,2), sticky="wens")

        # 구간 반복 라벨
        self.loop_label = Label(button_frame, text="", fg="blue")
        self.loop_label.grid(row=0, column=0, columnspan=6, padx=5, sticky="w")

        # 재생 버튼
        play_button = Button(button_frame, text="play", command=self.play_music)
        play_button.config(bg='white', highlightthickness=0, width=8)
        play_button.grid(row=1, column=1, padx=1, pady=10, sticky="wens")

        # 일시 정지 버튼
        pause_button = Button(button_frame, text="pause", command=self.pause_music)
        pause_button.config(bg='white', highlightthickness=0, width=8)
        pause_button.grid(row=1, column=2, padx=1, pady=10, sticky="wens")

        # 정지 버튼
        stop_button = Button(button_frame, text="stop", command=self.stop_music)
        stop_button.config(bg='white', highlightthickness=0, width=8)
        stop_button.grid(row=1, column=3, padx=1, pady=10, sticky="wens")

        # 앞으로 이동 버튼
        forward_button = Button(button_frame, text="forward", command=self.forward_music)
        forward_button.config(bg='white', highlightthickness=0, width=8)
        forward_button.grid(row=1, column=4, padx=(1, 15), pady=10, sticky="wens")

        # 뒤로 이동 버튼
        rewind_button = Button(button_frame, text="rewind", command=self.rewind_music)
        rewind_button.config(bg='white', highlightthickness=0, width=10)
        rewind_button.grid(row=1, column=0, padx=(5, 1), pady=10, sticky="wens")

        # 구간 반복 시작 버튼
        loop_start_button = Button(button_frame, text="Loop Start", command=self.set_loop_start)
        loop_start_button.config(bg='white', highlightthickness=0, width=10)
        loop_start_button.grid(row=2, column=0, padx=5, pady=5, sticky="wens")

        # 구간 반복 종료 버튼
        loop_end_button = Button(button_frame, text="Loop End", command=self.set_loop_end)
        loop_end_button.config(bg='white', highlightthickness=0, width=10)
        loop_end_button.grid(row=2, column=1, padx=5, pady=5, sticky="wens")

        # 구간 반복 실행 버튼
        loop_play_button = Button(button_frame, text="Play Loop", command=self.play_loop)
        loop_play_button.config(bg='white', highlightthickness=0, width=10)
        loop_play_button.grid(row=2, column=2, padx=5, pady=5, sticky="wens")

        self.running = True
        self.paused = False
        self.current_pos = 0
        self.track_length = 0
        pygame.init()
        pygame.mixer.init()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # 키 이벤트 바인딩
        self.root.bind("<KeyPress>", self.on_key_press)
        self.file_path = None

        # Pygame 이벤트 처리 스레드 시작
        threading.Thread(target=self.pygame_event_loop, daemon=True).start()

    def file_select(self):
        self.file_path = filedialog.askopenfilename()
        _, ext = os.path.splitext(self.file_path)
        if self.file_path and ext in [".mp3", ".wav", ".ogg", ".midi"]:
            pygame.mixer.music.load(self.file_path)
            self.track_length = pygame.mixer.Sound(self.file_path).get_length()
            self.current_pos = 0
            self.play_music()
        else:
            print("Please select a valid audio file.")

    def on_key_press(self, event):
        if event.keysym == 'q':
            self.running = False
            self.root.destroy()
        elif event.keysym == 'space':
            self.pause_music()
        elif event.keysym == "Return":
            self.play_music()
        elif event.keysym == 'Right':
            self.forward_music()
        elif event.keysym == 'Left':
            self.rewind_music()

    def play_music(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
            # 재개 시 offset을 현재 위치로 유지
            self.offset = self.current_pos
        else:
            if self.looping and self.loop_start is not None:
                self.current_pos = self.loop_start
            self.offset = self.current_pos
            pygame.mixer.music.play(-1, self.current_pos)
            self.paused = False
            self.looping = False
            self.loop_label.config(text="")

    def pause_music(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
            self.offset = self.current_pos
        else:
            pygame.mixer.music.pause()
            self.paused = True

    def stop_music(self):
        pygame.mixer.music.stop()
        self.paused = False
        self.current_pos = 0
        self.offset = 0
        self.loop_label.config(text="")

    def forward_music(self, event=None):
        if self.file_path:
            self.update_current_pos()
            self.current_pos += self.skip_speed
            if self.current_pos >= self.track_length:
                self.current_pos = 0
            self.offset = self.current_pos
            pygame.mixer.music.play(-1, self.current_pos)

    def rewind_music(self, event=None):
        if self.file_path:
            self.update_current_pos()
            self.current_pos = max(0, self.current_pos - self.skip_speed)
            self.offset = self.current_pos
            pygame.mixer.music.play(-1, self.current_pos)

    def update_current_pos(self):
        if pygame.mixer.music.get_busy() and not self.paused:
            # 현재 재생 위치는 offset + 재생 후 경과 시간(ms를 초로 변환)
            self.current_pos = self.offset + (pygame.mixer.music.get_pos() / 1000.0)

    def set_loop_start(self):
        self.loop_start = pygame.mixer.music.get_pos() / 1000.0
        self.loop_label.config(text=f"Loop start: {self.loop_start:.2f}s")
        print(f"Loop start set at: {self.loop_start} seconds")

    def set_loop_end(self):
        self.loop_end = pygame.mixer.music.get_pos() / 1000.0
        self.loop_label.config(text=f"Loop start: {self.loop_start:.2f}s, Loop end: {self.loop_end:.2f}s")
        print(f"Loop end set at: {self.loop_end} seconds")

    def play_loop(self):
        if self.loop_start is not None and self.loop_end is not None:
            self.looping = True
            self.current_pos = self.loop_start
            self.offset = self.loop_start
            pygame.mixer.music.play(-1, self.loop_start)
            print(f"Playing loop from {self.loop_start} to {self.loop_end} seconds")

    def pygame_event_loop(self):
        while self.running:
            if self.looping and self.loop_start is not None and self.loop_end is not None:
                current_pos = self.loop_start + (pygame.mixer.music.get_pos() / 1000.0)
                if current_pos >= self.loop_end:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.play(-1, self.loop_start)
                    self.offset = self.loop_start
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    self.on_key_press(event)
            time.sleep(0.1)
        pygame.mixer.music.stop()
        pygame.quit()
        print("Playback finished.")

    def on_closing(self):
        self.running = False
        self.root.destroy()

    def select_speed(self, event=None):
        if self.speed_combo.get():
            self.skip_speed = int(self.speed_combo.get())
        else:
            self.skip_speed = 5

    def adjust_combo(self):
        self.speed_combo['height'] = 15
        self.speed_combo.update_idletasks()
