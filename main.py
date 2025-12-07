import tkinter as tk
from time import strftime
from plyer import notification
import random
import threading

# --- Configuration ---
# Color settings
TEXT_COLOR = "#FFFFFF"  # Red (Classic Alarm Clock style)
# TEXT_COLOR = "#00FF00" # Uncomment for Matrix Green
BG_COLOR = "#000000"    # Black background
OPACITY = 0.60          # Slightly less transparent for better contrast
FONT_SIZE = 18         # Bigger for the digital look
FONT_FAMILY = "DS-Digital" # Make sure this font is installed!

# Time in seconds between notifications (8 minutes = 480 seconds)
NOTIFY_INTERVAL = 480 

QUOTES = [
    "Stay hard. Stay focused.",
    "Time is passing. Are you?",
    "Deep work creates value.",
    "One task at a time.",
    "Discipline equals freedom.",
    "Don't stop when you're tired, stop when you're done.",
    "Focus on the process, not the outcome.",
    "What is the most important thing right now?",
]

class FocusOverlay:
    def __init__(self):
        self.root = tk.Tk()
        
        # 1. Window Setup
        self.root.title("Focus Clock")
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-alpha", OPACITY)
        self.root.configure(bg=BG_COLOR)

        # 2. Position (Bottom Right Default)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Adjusted size calculation for the bigger font
        window_width = 90
        window_height = 30
        # x_pos = screen_width - window_width - 20
        x_loc = (screen_width / 2)
        print(x_loc)
        x_pos = 683 
        # y_pos = screen_height - window_height - 50
        y_pos = 0 
        self.root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

        # 3. UI Elements
        self.label = tk.Label(
            self.root, 
            font=(FONT_FAMILY, FONT_SIZE), 
            background=BG_COLOR, 
            foreground=TEXT_COLOR
        )
        self.label.pack(expand=True)

        # 4. User Interaction
        self.root.bind("<Button-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.do_move)
        self.root.bind("<Double-Button-1>", self.close_app)
        
        # 5. Start Logic
        self.update_clock()
        self.schedule_notification()
        
        self.root.mainloop()

    def update_clock(self):
        current_time = strftime('%H:%M:%S')
        self.label.config(text=current_time)
        self.root.after(1000, self.update_clock)

    def schedule_notification(self):
        self.root.after(NOTIFY_INTERVAL * 1000, self.trigger_notification)

    def trigger_notification(self):
        quote = random.choice(QUOTES)
        t = threading.Thread(target=self.show_toast, args=(quote,))
        t.start()
        self.schedule_notification()

    def show_toast(self, quote):
        try:
            notification.notify(
                title='FOCUS TRIGGER',
                message=quote,
                timeout=5,
            )
        except Exception as e:
            print(f"Notification error: {e}")

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def close_app(self, event):
        self.root.destroy()

if __name__ == "__main__":
    app = FocusOverlay()