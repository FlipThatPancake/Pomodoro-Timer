import sys, os, math
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from plyer import notification

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None
egg_offset = 0
reset_flag = False


# ---------------------------- OTHER -------------------------------- #
# TODO Force window on top
def focus_window(option):
    if option == 'on':
        # Restore if window is minimized
        window.state('normal')

        # Bring to top level above all windows and back normal
        window.attributes('-topmost', 1)
        window.attributes('-topmost', 0)


def wind_mechanical_egg_clock(minutes):
    clicks = 24

    def move_dial(clicks_remaining):
        global egg_offset
        if clicks_remaining > 0:
            egg_canvas.move(egg_top, (183 / 25) * minutes / 24, 0)
            egg_offset += minutes / 100
            window.after(42, move_dial, clicks_remaining - 1)

    move_dial(clicks)


# TODO Display a notificaiton upon completing a cycle
def popup_notification():
    notification.notify(
        title="Break Time",
        message="Take a well-deserved break!",
        timeout=5
    )


# ---------------------------- CREATE LOG -------------------------------- #
# TODO Create Log Func
def write_log():
    with open("pomodoro_log.dat", 'a') as logfile:
        now = datetime.now()
        date_string = now.strftime("%d/%m/%Y %H:%M\n")
        log_text = f"Time Spent Studying: {WORK_MIN} minutes. Study Session Time: {date_string}"
        logfile.write(log_text)


# ---------------------------- TIMER RESET ------------------------------- #


# TODO Reset Timer
def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")


# TODO Erase checkmarks
def erase_checkmarks():
    for checkmark in frame.winfo_children():
        checkmark.destroy()


# TODO Egg clock back in position
def egg_clock_reset():
    global egg_offset
    egg_canvas.move(egg_top, -(183 / 25) * egg_offset, 0)
    egg_offset -= egg_offset


# TODO Reset reps count
def reset_reps():
    global reps
    reps = 0


# TODO Reset func
def reset_all():
    start_button.config(state=NORMAL)
    erase_checkmarks()
    heading_text.config(text="Timer", fg="GREEN")
    egg_clock_reset()
    reset_timer()
    reset_reps()


# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    start_button.config(state=DISABLED)
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    global reps
    reps += 1

    if reps % 8 == 0:
        focus_window('on')
        wind_mechanical_egg_clock(LONG_BREAK_MIN)
        count_down(long_break_sec)
        heading_text.config(text="Long Break", fg=RED)
        popup_notification()

    elif reps % 2 == 0:
        focus_window('on')
        wind_mechanical_egg_clock(SHORT_BREAK_MIN)
        count_down(short_break_sec)
        heading_text.config(text="Short Break", fg=PINK)
        popup_notification()
        print("\a")


    else:
        focus_window('on')
        wind_mechanical_egg_clock(WORK_MIN)
        count_down(work_sec)
        heading_text.config(text="Work", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

def count_down(count):
    global reps
    global egg_offset

    count_min = math.floor(count / 60)  # count // 60
    count_sec = count % 60
    canvas.itemconfig(timer_text, text=f"{count_min:02}:{count_sec:02}")

    egg_canvas.move(egg_top, -(183 / 25) / 60, 0)
    egg_offset -= 1 / 60

    if count > 0:
        # gets triggered as soon as TIME is loaded to the count
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        # gets triggered when timer shows "00:00"/runs out

        col = 0
        for _ in range(math.floor(reps / 2)):
            check_mark = Label(frame, text="✔", bg=YELLOW, fg=GREEN)
            check_mark.grid(column=col, row=0)
            col += 1

        if reps == 8 or (reps > 8 and reps % 8 == 0):
            # force on top even if minimized
            focus_window('on')
            # force on top
            window.attributes('-topmost', 1)
            heading_text.config(text="Complete", fg=GREEN)
            messagebox.showinfo('End', 'Timer Cycle Complete')
            # turn of force on top
            window.attributes('-topmost', 0)
            print("Completed!")
            start_button.config(state=NORMAL)
            write_log()

        else:
            start_timer()


# ---------------------------- UI SETUP ------------------------------- #

# TODO import image path to pack into exe
# 1. run "pyinstaller --onefile --windowed --add-data "tomato.png;." main.py" in the console
# 2. add "a.datas += [('tomato.png','D:\CODING\100 Days of Python\Pomodoro Timer\tomato.png', "DATA")]" in main.spec
# 3. run "pyinstaller main.spec" in the console
def resource_path(relative_path):
    try:
        # "cannot find reference '_MEIPASS' in 'sys.pyi' is OK, because it only gets accessed when the code is 'frozen'
        # by Pyinstaller; meaning in code compiler it cannot be accessed
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# TODO Initialize window
window = Tk()
window.title("Pomodoro Timer")
window.geometry("550x500")
window.config(padx=60, pady=40, bg=YELLOW)
tomato_img = PhotoImage(file=resource_path("tomato.png"))
window.iconphoto(False, tomato_img)
window.resizable(0, 0)

# TODO Local Frame
frame = Frame(bg=YELLOW)
frame.grid(column=1, row=3)

# TODO Tomato picture
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
canvas.create_image(100, 112, image=tomato_img)

# TODO Timer
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 32, "bold"))
canvas.grid(column=1, row=1)

# TODO Egg clock
egg_canvas = Canvas(width=400, height=100, bg=YELLOW, highlightthickness=0)
egg_top_image = PhotoImage(file="./Pomodoro_super/resources/Top_marks.png")
egg_bottom_image = PhotoImage(file="./Pomodoro_super/resources/Bottom_marks.png")
egg_top = egg_canvas.create_image(200, 25, image=egg_top_image)
egg_bottom = egg_canvas.create_image(200, 73, image=egg_bottom_image)
egg_canvas.grid(column=1, row=4)

# TODO Heading Title
heading_text = Label(text="Timer", font=(FONT_NAME, 40, "normal"), bg=YELLOW, fg=GREEN)
heading_text.grid(column=0, row=0, columnspan=3, sticky="nsew")
# Set the width of columns, middle column 4x wider than sides
window.grid_columnconfigure(0, weight=1, uniform='pomodoro')
window.grid_columnconfigure(1, weight=4, uniform='pomodoro')
window.grid_columnconfigure(2, weight=1, uniform='pomodoro')

# TODO Start Button
start_button = Button(text="Start", bg=RED, fg=YELLOW, command=start_timer)
start_button.grid(column=0, row=2)

# TODO Reset Button
reset_button = Button(text="Reset", bg=RED, fg=YELLOW, command=reset_all)
reset_button.grid(column=2, row=2)

# WORK_MIN = simpledialog.askinteger(title="Study Session Times", prompt="How long are the study sessions?", parent=window)


window.mainloop()
