import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFont

root = tk.Tk()
root.title("تطبيق تصميم مثل PicsLab")
root.geometry("500x650")

canvas = tk.Canvas(root, bg="white", width=400, height=500)
canvas.pack(pady=10)

image = None
tk_image = None
texts = []
selected = None

# تحميل صورة
def load_image():
    global image, tk_image
    path = filedialog.askopenfilename()
    if not path:
        return
    image = Image.open(path).resize((400, 500))
    tk_image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor="nw", image=tk_image)

# إضافة نص
def add_text():
    text = text_entry.get()
    if not text:
        return

    color = colorchooser.askcolor()[1]
    text_id = canvas.create_text(
        200, 250,
        text=text,
        fill=color,
        font=("Arial", 24)
    )
    texts.append(text_id)

# تحريك النص
def select(event):
    global selected
    selected = canvas.find_closest(event.x, event.y)

def move(event):
    if selected:
        canvas.coords(selected, event.x, event.y)

def release(event):
    global selected
    selected = None

# حفظ الصورة
def save_image():
    result = image.copy()
    draw = ImageDraw.Draw(result)

    for t in texts:
        x, y = canvas.coords(t)
        text = canvas.itemcget(t, "text")
        color = canvas.itemcget(t, "fill")
        font = ImageFont.load_default()
        draw.text((x, y), text, fill=color, font=font)

    result.save("design.png")

# أدوات
toolbar = tk.Frame(root)
toolbar.pack()

tk.Button(toolbar, text="تحميل صورة", command=load_image).grid(row=0, column=0)
tk.Button(toolbar, text="إضافة نص", command=add_text).grid(row=0, column=1)
tk.Button(toolbar, text="حفظ", command=save_image).grid(row=0, column=2)

text_entry = tk.Entry(root)
text_entry.pack(pady=5)

# أحداث الماوس
canvas.bind("<Button-1>", select)
canvas.bind("<B1-Motion>", move)
canvas.bind("<ButtonRelease-1>", release)

root.mainloop()
