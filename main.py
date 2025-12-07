import tkinter as tk
from time import strftime
from plyer import notification
import random
import threading

# --- Configuration ---
TEXT_COLOR = "#FFFFFF" 
DOCK_COLOR = "#000000"  # The color of the rounded bubble
TRANSPARENT_BG = "#000001" # A color we will make invisible (Don't change this)
OPACITY = 0.60          # Window transparency
FONT_SIZE = 18          
FONT_FAMILY = "DS-Digital" 

# Time in seconds between notifications (8 minutes)
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
        
        # VITAL: This tells Windows that the color #000001 should be 
        # completely invisible, cutting off the square corners.
        self.root.wm_attributes("-transparentcolor", TRANSPARENT_BG)
        self.root.configure(bg=TRANSPARENT_BG)

        # 2. Position (Top Center Dynamic)
        screen_width = self.root.winfo_screenwidth()
        
        # Dimensions of the dock
        window_width = 120
        window_height = 35
        
        # Calculate center x
        x_pos = (screen_width // 2) - (window_width // 2)
        y_pos = 0 # Top of screen
        
        self.root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

        # 3. UI Elements (Canvas instead of Label)
        # We remove the highlightthickness to get rid of the default border
        self.canvas = tk.Canvas(
            self.root, 
            width=window_width, 
            height=window_height, 
            bg=TRANSPARENT_BG, 
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        # Draw the Rounded Dock Background
        # We draw a thick line with rounded caps to simulate a pill shape
        self.round_rect = self.canvas.create_line(
            20, (window_height/2),  # Start Point (x, y)
            window_width - 20, (window_height/2), # End Point
            fill=DOCK_COLOR, 
            width=window_height,    # Thickness
            capstyle=tk.ROUND       # This creates the rounded corners!
        )

        # Draw the Text on top of the dock
        self.text_id = self.canvas.create_text(
            window_width/2, 
            window_height/2 + 2, # +2 for slight vertical adjustment
            text="", 
            font=(FONT_FAMILY, FONT_SIZE), 
            fill=TEXT_COLOR
        )

        # 4. User Interaction
        self.canvas.bind("<Button-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.do_move)
        self.canvas.bind("<Double-Button-1>", self.close_app)
        
        # 5. Start Logic
        self.update_clock()
        self.schedule_notification()
        
        self.root.mainloop()

    def update_clock(self):
        current_time = strftime('%H:%M:%S')
        # Update canvas text item
        self.canvas.itemconfigure(self.text_id, text=current_time)
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