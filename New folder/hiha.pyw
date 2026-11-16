import os
import random
import subprocess
import tkinter as tk
import winsound

# Force the working directory to where this script is saved
# This ensures music.wav and your .bat file are found immediately when double-clicking
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

memes = [
    "Bro really thought he could code 💀",
    "It's not a bug, it's an undocumented feature 🤡",
    "404: Motivation not found ☕",
    "When the code works on the first try (Suspicious...) 🤨",
    (
        "There are 2 hard things in computer science: cache invalidation &"
        " naming things 📉"
    ),
    "Ctrl+C, Ctrl+V: The backbone of software engineering 💻",
    (
        "Debugging: Being the detective in a movie where you are also the"
        " murderer 🕵️‍♂️"
    ),
    "Segmentation fault (core dumped) 💥",
    "Stack Overflow is down? Guess I'll quit programming 🤷‍♂️",
    "It worked fine in my local environment! 🌍",
    "Have you tried turning it off and on again? 🔌",
]

# Curated high-contrast color themes (Background, Text) for the popups
color_palettes = [
    ("#ff0055", "#ffffff"),  # Hot Pink & White
    ("#00ffcc", "#000000"),  # Neon Cyan & Black
    ("#ffcc00", "#1b1b1b"),  # Electric Yellow & Dark Gray
    ("#9900ff", "#00ffcc"),  # Neon Purple & Cyan
    ("#000000", "#ff0000"),  # Pitch Black & Blood Red
    ("#003366", "#ffffff"),  # Deep Blue & White
    ("#ff3300", "#ffff00"),  # Orange-Red & Yellow
    ("#39ff14", "#000000"),  # Neon Green & Black
]


def play_real_music():
  """Plays music.wav in a continuous loop using absolute pathing."""
  try:
    music_path = os.path.join(script_dir, "music.wav")
    if os.path.exists(music_path):
      winsound.PlaySound(
          music_path,
          winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP,
      )
    else:
      print(f"Warning: Could not find music.wav at {music_path}")
  except Exception as e:
    print(f"Could not play music: {e}")


def stop_music():
  """Stops the background music."""
  try:
    winsound.PlaySound(None, winsound.SND_PURGE)
  except Exception:
    pass


class BatFileMemeBlast:

  def __init__(self, root):
    self.root = root
    self.root.withdraw()

    self.screen_width = self.root.winfo_screenwidth()
    self.screen_height = self.root.winfo_screenheight()

    self.elapsed_time = 0
    self.total_duration = 5000  # Exactly 5 seconds (5,000 ms)
    self.interval = 35  # Ultra-fast window spam

    self.popups = []

    # Start music and begin the 5-second meme blast
    play_real_music()
    self.spawn_loop()

  def spawn_popup(self):
    popup = tk.Toplevel(self.root)
    popup.overrideredirect(True)
    self.popups.append(popup)

    w, h = random.randint(310, 430), random.randint(110, 160)
    x = random.randint(0, max(0, self.screen_width - w))
    y = random.randint(0, max(0, self.screen_height - h))

    popup.geometry(f"{w}x{h}+{x}+{y}")

    # Assign a unique random background and text color to this popup
    bg_color, fg_color = random.choice(color_palettes)
    popup.config(bg=bg_color)

    text = random.choice(memes)
    label = tk.Label(
        popup,
        text=text,
        font=("Arial", 11, "bold"),
        fg=fg_color,
        bg=bg_color,
        wraplength=w - 20,
        justify="center",
    )
    label.pack(expand=True, padx=10, pady=10)

  def spawn_loop(self):
    if self.elapsed_time < self.total_duration:
      for _ in range(3):
        self.spawn_popup()

      self.elapsed_time += self.interval
      self.root.after(self.interval, self.spawn_loop)
    else:
      self.finish_blast()

  def finish_blast(self):
    # 1. OPEN THE .BAT FILE IMMEDIATELY THE MILLISECOND 5 SECONDS ENDS
    # Change "run.bat" below to match the exact name of your batch file
    bat_filename = "exe.bat"
    bat_path = os.path.join(script_dir, bat_filename)

    try:
      if os.name == "nt":
        os.startfile(bat_path)
      else:
        subprocess.Popen(["xdg-open", bat_path])
    except Exception as e:
      print(f"Could not open batch file: {e}")

    # 2. Stop music and destroy popup windows right after
    stop_music()
    for popup in self.popups:
      try:
        popup.destroy()
      except Exception:
        pass

    self.root.destroy()


if __name__ == "__main__":
  root = tk.Tk()
  BatFileMemeBlast(root)
  root.mainloop()