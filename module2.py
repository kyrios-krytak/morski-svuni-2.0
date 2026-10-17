import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Морські свині!!!")
root.geometry("534x600")
root.minsize(300, 340)          # мінімальний розмір вікна
root.resizable(True, True)      # тепер вікно можна розтягувати

original = Image.open("background.jpg").convert("RGB")  # завантажуємо один раз

canvas = tk.Canvas(root, bg="black", highlightthickness=0)
canvas.pack(fill="both", expand=True)

refs = []          # тримаємо посилання на картинки
resize_job = None  # для "затримки" перемальовування

def play():
    print("Гру розпочато!")

def make_rgba_image(w, h, color):
    photo = ImageTk.PhotoImage(Image.new("RGBA", (max(w, 1), max(h, 1)), color))
    refs.append(photo)
    return photo

def make_button(x, y, w, h, text, command, font_size):
    normal = make_rgba_image(w, h, (255, 255, 255, 70))
    hover = make_rgba_image(w, h, (255, 255, 255, 140))
    bg = canvas.create_image(x, y, image=normal)
    label = canvas.create_text(x, y, text=text,
                               font=("Arial", font_size, "bold"), fill="#222222")

    def on_enter(e):
        canvas.itemconfig(bg, image=hover)
        canvas.config(cursor="hand2")

    def on_leave(e):
        canvas.itemconfig(bg, image=normal)
        canvas.config(cursor="")

    for item in (bg, label):
        canvas.tag_bind(item, "<Button-1>", lambda e: command())
        canvas.tag_bind(item, "<Enter>", on_enter)
        canvas.tag_bind(item, "<Leave>", on_leave)

def redraw():
    W = canvas.winfo_width()
    H = canvas.winfo_height()
    if W < 10 or H < 10:
        return

    canvas.delete("all")
    refs.clear()

    # Картинка вписується у вікно без спотворень
    scale = min(W / original.width, H / original.height)
    IMG_W = int(original.width * scale)
    IMG_H = int(original.height * scale)
    OFFSET_X = (W - IMG_W) // 2
    OFFSET_Y = (H - IMG_H) // 2

    bg_img = ImageTk.PhotoImage(original.resize((IMG_W, IMG_H), Image.LANCZOS))
    refs.append(bg_img)
    canvas.create_image(OFFSET_X, OFFSET_Y, image=bg_img, anchor="nw")

    k = IMG_H / 600  # коефіцієнт масштабу

    canvas.create_text(
        OFFSET_X + IMG_W * 0.5, OFFSET_Y + IMG_H * 0.07,
        text="Морські свині!!!", font=("Arial", max(int(36 * k), 8), "bold"), fill="#222222"
    )

    make_button(OFFSET_X + IMG_W * 0.37, OFFSET_Y + IMG_H * 0.77,
                int(120 * k), int(55 * k), "ГРАТИ", play, max(int(14 * k), 6))
    make_button(OFFSET_X + IMG_W * 0.84, OFFSET_Y + IMG_H * 0.92,
                int(110 * k), int(45 * k), "ВИЙТИ", root.destroy, max(int(12 * k), 6))

def on_resize(event):
    # перемальовуємо не частіше, ніж раз на ~50 мс, щоб не лагало
    global resize_job
    if resize_job:
        root.after_cancel(resize_job)
    resize_job = root.after(50, redraw)

canvas.bind("<Configure>", on_resize)

# Повноекранний режим
def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))

def exit_fullscreen(event=None):
    root.attributes("-fullscreen", False)

root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", exit_fullscreen)

root.mainloop()