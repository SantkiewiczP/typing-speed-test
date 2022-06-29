import random
from tkinter import *

BACKGROUND_COLOR = "#FFEBC9"
TEXT_COLOR = "#B05B3B"
BUTTON_COLOR = "#D79771"
TIMER_COLOR = "#753422"
FONT_NAME = "Montserrat Black"
timer = None


class TypingSpeed:

    def __init__(self):
        self.window = Tk()
        self.window.title("Typing Speed Test")
        self.window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)

        # Placing the window in the centre of the screen.
        width = 1100
        height = 700
        ws = self.window.winfo_screenwidth()
        hs = self.window.winfo_screenheight()

        x = (ws / 2) - (width / 2)
        y = (hs / 2) - (height / 2)
        self.window.geometry('%dx%d+%d+%d' % (width, height, x, y))

        self.user_list = []
        self.prompt_list = []

        # Text Label
        self.prompt = Label(text="Click Start to start and press Enter after each completed sentence.",
                            font=(FONT_NAME, 20, "bold"),
                            wraplength=800, justify="center", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, padx=25, pady=50)
        self.prompt.pack()

        # Timer/Result Label
        self.seconds = 90
        self.timer_label = Label(text=f"TIMER: {self.seconds}", bg=BACKGROUND_COLOR, fg=TIMER_COLOR,
                                 font=(FONT_NAME, 40, "bold"), padx=50, pady=10)
        self.timer_label.pack()

        # User input field
        self.user_input = Text(width=100, height=4, font=(FONT_NAME, 15), bg=BACKGROUND_COLOR, fg=TIMER_COLOR)
        self.user_input.config(state="disabled", bg=BACKGROUND_COLOR)
        self.user_input.pack(padx=20, pady=50)
        self.user_input.bind("<Return>", self.new_sentence)

        # Start button
        self.start_button = Button(text="Start", font=(FONT_NAME, 15, "bold"), bg=BUTTON_COLOR, fg=TIMER_COLOR,
                                   command=self.start_countdown)
        self.start_button.pack(pady=10)

        # Reset button
        self.reset_button = Button(text="Reset", font=(FONT_NAME, 15, "bold"), bg=BUTTON_COLOR, fg=TIMER_COLOR,
                                   command=self.reset, state="disabled")
        self.reset_button.pack(padx=10, pady=10)

    # Reset the test
    def reset(self):
        self.window.after_cancel(timer)
        self.user_input.delete("1.0", END)
        self.start_button.config(state="active", bg=BUTTON_COLOR, fg=TEXT_COLOR)
        self.reset_button.config(state="disabled", bg=BUTTON_COLOR, fg=TEXT_COLOR)
        self.user_input.config(state="disabled", bg=BACKGROUND_COLOR)
        self.prompt.config(text="Click Start to start and press Enter after each completed sentence.",
                           font=(FONT_NAME, 20, "bold"))
        self.timer_label.config(text=self.seconds)

    # Timer and displaying the result
    def countdown(self, count):
        self.timer_label.config(text=f"TIMER: {count}")
        if count > 0:
            global timer
            # call countdown again after 1000ms (1s)
            timer = self.window.after(1000, self.countdown, count - 1)
        else:
            self.collect_data()

            self.start_button.config(state="active")
            self.reset_button.config(state="disabled")
            self.user_input.config(state="disabled")

    # Start timer and disable/enable buttons
    def start_countdown(self):
        self.user_input.config(state="normal", bg="white")
        self.user_input.focus()
        self.countdown(self.seconds)
        self.new_sentence(self)
        self.start_button['state'] = 'disabled'
        self.reset_button['state'] = 'active'

    # Choose a random sentence from the text file
    def random_sentence(self):
        with open('paragraphs.txt') as file:
            lines = file.readlines()
            random_line = random.choice(lines)
        n = [sentence for sentence in lines if sentence != random_line]
        return random_line

    # Display new random sentence
    def new_sentence(self, event):
        self.prompt.config(text=self.random_sentence())
        self.collect_data()
        self.user_input.delete("1.0", END)

    def collect_data(self):
        prompt_words = self.prompt.cget("text").split()
        for word in prompt_words:
            self.prompt_list.append(word)
        user_words = self.user_input.get("1.0", END).split()
        for words in user_words:
            self.user_list.append(words)

    # Calculate the result
    def results(self):
        result = 0
        for word in self.user_list:
            if word in self.prompt_list:
                result += 1
        self.timer_label.config(text=f"Your result is: {round((result / 1.5), 2)} words per minute.",
                                font=(FONT_NAME, 40, "bold"), bg=BACKGROUND_COLOR, fg=TIMER_COLOR)


app = TypingSpeed()
app.window.mainloop()
