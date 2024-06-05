import tkinter
from PIL import Image, ImageTk
import random
import numpy as np
from tkinter import Tk, Label, Button, scrolledtext, filedialog, StringVar
from os import path
from tkinter.ttk import Radiobutton
from tkinter import ttk

def clicked():
    global file
    file = filedialog.askopenfilename(filetypes = (("Image files","*.bmp"),("all files","*.*")), initialdir= path.dirname(__file__))
    if file:
        lbl11.configure(text=file.split('/')[-1])
        #file = file.split('/')[-1]
        lbl04 = Label(window, text='Пустой контейнер', font=('Times New Roman', 14))
        lbl04.grid(column=0, row=4, pady=10, padx=10, sticky='W')

        emp_con = Image.open(file)
        emp_con = emp_con.resize((300, 200))
        global tk_emp_con
        tk_emp_con = ImageTk.PhotoImage(emp_con)
        lbl05 = Label(window, image=tk_emp_con)
        lbl05.grid(column=0, row=5, padx=10, pady=10, sticky='W')

def enable_raid():
    rad2_1.configure(state='enable')
    rad2_2.configure(state='enable')
    rad2_3.configure(state='enable')
    rad2_4.configure(state='enable')
    rad2_5.configure(state='enable')
    rad2_6.configure(state='enable')
    rad2_7.configure(state='enable')
    rad2_8.configure(state='enable')
def disable_raid():
    rad2_1.configure(state='disable')
    rad2_2.configure(state='disable')
    rad2_3.configure(state='disable')
    rad2_4.configure(state='disable')
    rad2_5.configure(state='disable')
    rad2_6.configure(state='disable')
    rad2_7.configure(state='disable')
    rad2_8.configure(state='disable')
def hiding():
    def ext_pix(image):
        pixels = list(image.getdata())
        print('Пиксели:', pixels[:10])
        for i in range(len(pixels)):
            pixels[i] = list(pixels[i])
            for j in range(len(pixels[i])):
                pixels[i][j] = bin(pixels[i][j])[2:].zfill(8)
        return pixels

    if var1.get() == '1':
        print('Метод LSB-R\n_Скрытие сообщения_')
        image = Image.open(file)
        width, height = image.size
        pixels = ext_pix(image)
        print('Пиксели в двоичном виде:', pixels[:10])

        secmes = scr.get("1.0", "end-1c")
        print('Сообщение:', secmes)
        global lenmes
        lenmes = len(secmes)
        binary_secmes = ''.join(format(ord(x), '08b') for x in secmes)
        print('Сообщение в двоичном виде:', binary_secmes)

        raid = int(var2.get())
        for i in range(len(pixels)):
            for j in range(len(pixels[i])):
                r = list(pixels[i][j][-raid:])
                for k in range(len(r)):
                    if binary_secmes == '':
                        break
                    elif r[k] != binary_secmes[0]:
                        r[k] = binary_secmes[0]
                    binary_secmes = binary_secmes[1:]
                pixels[i][j] = pixels[i][j][:-raid] + ''.join(r)
        print('Пиксели с сообщением:', pixels[:10])

        for i in range(len(pixels)):
            for j in range(len(pixels[i])):
                pixels[i][j] = int(pixels[i][j], 2)
            pixels[i] = tuple(pixels[i])
        print('Пиксели в десятичном виде с сообщением:', pixels[:10])

        image_LSB_R = Image.new('RGB', (width, height))
        image_LSB_R.putdata(pixels)
        save_path = filedialog.asksaveasfilename(defaultextension=".bmp")
        if save_path:
            image_LSB_R.save(save_path)

        global image_for_ext
        image_for_ext = image_LSB_R

        lbl14 = Label(window, text='Заполненный контейнер', font=('Times New Roman', 14))
        lbl14.place(x=340, y=235)

        image_LSB_R = image_LSB_R.resize((300, 200))
        global tk_image
        tk_image = ImageTk.PhotoImage(image_LSB_R)
        lbl15 = Label(window, image=tk_image)
        lbl15.place(x=340, y=282)

    elif var1.get() == '2':
        print('Метод LSB-M\n_Скрытие сообщения_')
        image = Image.open(file)
        width, height = image.size
        pixels = ext_pix(image)
        print('Пиксели в двоичном виде:', pixels[:10])

        secmes = scr.get("1.0", "end-1c")
        print('Сообщение:', secmes)
        #global lenmes
        lenmes = len(secmes)
        binary_secmes = ''.join(format(ord(x), '08b') for x in secmes)
        print('Сообщение в двоичном виде:', binary_secmes)

        raid = int(var2.get())
        for i in range(len(pixels)):
            for j in range(len(pixels[i])):
                if binary_secmes == '':
                    break
                l = int(binary_secmes[:raid], 2)
                r = pixels[i][j]
                if l != int(r[-raid:], 2):
                    if raid != 1:
                        k1 = 0
                        while l != int(r[-raid:], 2):
                            r = bin(int(r, 2) + 1)[2:]
                            k1 += 1
                        r1 = r
                        r = pixels[i][j]
                        k2 = 0
                        while l != int(r[-raid:], 2) and not (bin(int(r, 2) - 1).startswith('-')):
                            r = bin(int(r, 2) - 1)[2:]
                            k2 += 1
                        r2 = r
                        R = [r1, r2]
                        if k1 > k2:
                            pixels[i][j] = r1
                        elif k1 < k2:
                            pixels[i][j] = r2
                        else:
                            pixels[i][j] = random.choice(R)
                    else:
                        pixels[i][j] = bin(int(pixels[i][j], 2) + random.choice([-1, 1]))[2:]
                binary_secmes = binary_secmes[raid:]

        print('Пиксели с сообщением:', pixels[:10])

        for i in range(len(pixels)):
            for j in range(len(pixels[i])):
                pixels[i][j] = int(pixels[i][j], 2)
            pixels[i] = tuple(pixels[i])
        print('Пиксели в десятичном виде с сообщением:', pixels[:10])

        image_LSB_M = Image.new('RGB', (width, height))
        image_LSB_M.putdata(pixels)
        save_path = filedialog.asksaveasfilename(defaultextension=".bmp")
        if save_path:
            image_LSB_M.save(save_path)

        #global image_for_ext
        image_for_ext = image_LSB_M

        lbl14 = Label(window, text='Заполненный контейнер', font=('Times New Roman', 14))
        lbl14.place(x=340, y=235)

        image_LSB_L = image_LSB_M.resize((300, 200))
        #global tk_image
        tk_image = ImageTk.PhotoImage(image_LSB_L)
        lbl15 = Label(window, image=tk_image)
        lbl15.place(x=340, y=282)

    elif var1.get() == '3':
        print('Код Хемминга\n_Скрытие сообщения_')
        image = Image.open(file)
        width, height = image.size
        pixels = ext_pix(image)
        print('Пиксели в двоичном виде:', pixels[:10])

        secmes = scr.get("1.0", "end-1c")
        print('Сообщение:', secmes)
        # global lenmes
        lenmes = len(secmes)
        binary_secmes = ''.join(format(ord(x), '08b') for x in secmes)
        print('Сообщение в двоичном виде:', binary_secmes)

        global H
        H = np.array([list(format(i, '04b')) for i in range(1, 16)], dtype=int).T
        print('Проверочная матрица H:\n', H)

        pr = False
        for i in range(len(pixels)):
            c = np.array(list(pixels[i][0][-5:] + pixels[i][1][-5:] + pixels[i][2][-5:]))
            c = np.array(list(map(int, c)))
            m = np.array(list(binary_secmes[:4]))
            m = np.array(list(map(int, m)))
            binary_secmes = binary_secmes[4:]
            while len(binary_secmes) < 4:
                binary_secmes += '0'
                pr = True
            if pr:
                break

            s = (H @ c + m) % 2

            I = 8 * s[0] + 4 * s[1] + 2 * s[2] + s[3]
            if I == 0:
                continue

            c_mod = c
            c_mod[I - 1] = not c_mod[I - 1]
            c_mod = ''.join(str(x) for x in c_mod)

            pixels[i][0] = pixels[i][0][:-5] + c_mod[:5]
            c_mod = c_mod[5:]
            pixels[i][1] = pixels[i][1][:-5] + c_mod[:5]
            c_mod = c_mod[5:]
            pixels[i][2] = pixels[i][2][:-5] + c_mod[:5]
            c_mod = c_mod[5:]
        print('Пиксели в двоичном виде с сообщением:', pixels)

        for i in range(len(pixels)):
            for j in range(len(pixels[i])):
                pixels[i][j] = int(pixels[i][j], 2)
            pixels[i] = tuple(pixels[i])
        print('Пиксели в десятичном виде с сообщением:', pixels[:10])

        image_Hem = Image.new('RGB', (width, height))
        image_Hem.putdata(pixels)
        save_path = filedialog.asksaveasfilename(defaultextension=".bmp")
        if save_path:
            image_Hem.save(save_path)

        # global image_for_ext
        image_for_ext = image_Hem

        lbl14 = Label(window, text='Заполненный контейнер', font=('Times New Roman', 14))
        lbl14.place(x=340, y=235)

        image_Hem = image_Hem.resize((300, 200))
        # global tk_image
        tk_image = ImageTk.PhotoImage(image_Hem)
        lbl15 = Label(window, image=tk_image)
        lbl15.place(x=340, y=282)

def extraction():
    def ext_pix(image):
        pixels = list(image.getdata())
        print('Пиксели:', pixels[:10])
        for i in range(len(pixels)):
            pixels[i] = list(pixels[i])
            for j in range(len(pixels[i])):
                pixels[i][j] = bin(pixels[i][j])[2:].zfill(8)
        return pixels

    if var1.get() == '1' or var1.get() == '2':
        raid = int(var2.get())
        print('\n_Извлечение сообщения_')
        image = image_for_ext
        pixels = ext_pix(image)
        print('Пиксели в двоичном виде:', pixels)
        secmes = ''
        for i in range(len(pixels)):
            for j in range(len(pixels[i])):
                secmes += pixels[i][j][-raid:]
        print('Сообщение в двоичном виде: ', secmes)
        chunks = [secmes[i:i + 8] for i in range(0, len(secmes), 8)]
        mes = ''.join(chr(int(chunk, 2)) for chunk in chunks)
        print('Сообщение:', mes[:lenmes])

        lbl_mes = Label(window, text='Извлеченное сообщение', font = ('Times New Roman', 14))
        lbl_mes.place(x=680, y=235)

        scr_mes = scrolledtext.ScrolledText(window, width=40, height=12)
        scr_mes.insert(tkinter.INSERT, mes[:lenmes])
        scr_mes.place(x=680, y=282)

    elif var1.get() == '3':
        print('\n_Извлечение сообщения_')
        image = image_for_ext
        pixels = ext_pix(image)
        print('Пиксели в двоичном виде:', pixels)
        secmes_err = ''
        for i in range(len(pixels)):
            secmes_err += pixels[i][0][-5:] + pixels[i][1][-5:] + pixels[i][2][-5:]
        print('Сообщение в двоичном виде с ошибкой:', secmes_err)

        secmes = ''
        for i in range(0, len(secmes_err), 15):
            ser_err = (H @ np.array(list(int(x) for x in secmes_err[i: i + 15])).tolist()) % 2
            ser_err = ''.join(str(x) for x in ser_err)
            secmes += str(ser_err)
        print(secmes)
        chunks = [secmes[i:i + 8] for i in range(0, len(secmes), 8)]
        mes = ''.join(chr(int(chunk, 2)) for chunk in chunks)
        print('Сообщение:', mes[:lenmes])

        lbl_mes = Label(window, text='Извлеченное сообщение', font=('Times New Roman', 14))
        lbl_mes.place(x=680, y=235)

        scr_mes = scrolledtext.ScrolledText(window, width=40, height=12)
        scr_mes.insert(tkinter.INSERT, mes[:lenmes])
        scr_mes.place(x=680, y=282)

window = Tk()
window.geometry("300x250")
window.minsize(width=1100, height=1500)
window.title('9 Лабораторная работа')

lbl00 = Label(window, text='Сообщение', font = ('Times New Roman', 14))
lbl00.grid(column=0, row=0, pady=10, padx=10, sticky='W')

scr = scrolledtext.ScrolledText(window, width=60, height=8)
scr.grid(column=0, row=1, padx=10)
scr.focus()

lbl00 = Label(window, text='Контейнер', font = ('Times New Roman', 14))
lbl00.grid(column=1, row=0, pady=10, padx=10, sticky='W')

btn11 = Button(window, text="Выберите изображение", command=clicked)
btn11.grid(column=1, row=1, padx=10, pady=10, sticky='N')

lbl11 = Label(window, text='', font=('Times New Roman', 9))
lbl11.place(x=530, y=90)

lbl02 = Label(window, text='Метод скрытия', font = ('Times New Roman', 14))
lbl02.grid(column=2, row=0, pady=10, padx=10, sticky='W')

var1 = StringVar()
rad1 = Radiobutton(window, text='LSB-R', value=1, variable=var1, command=enable_raid)
rad2 = Radiobutton(window, text='LSB-M', value=2, variable=var1, command=enable_raid)
rad3 = Radiobutton(window, text='Код Хемминга', value=3, variable=var1, command=disable_raid)
rad1.place(x=725, y=55)
rad2.place(x=725, y=75)
rad3.place(x=725, y=95)

lbl03 = Label(window, text='Рейт', font = ('Times New Roman', 14))
lbl03.grid(column=3, row=0, pady=10, padx=30, sticky='W')

var2 = StringVar()
rad2_1 = Radiobutton(window, text='1', value=1, variable=var2, state='disable')
rad2_2 = Radiobutton(window, text='2', value=2, variable=var2, state='disable')
rad2_3 = Radiobutton(window, text='3', value=3, variable=var2, state='disable')
#rad2_4 = Radiobutton(window, text='4', value=4, variable=var2, state='disable')
#rad2_5 = Radiobutton(window, text='5', value=5, variable=var2, state='disable')
#rad2_6 = Radiobutton(window, text='6', value=6, variable=var2, state='disable')
#rad2_7 = Radiobutton(window, text='7', value=7, variable=var2, state='disable')
#rad2_8 = Radiobutton(window, text='8', value=8, variable=var2, state='disable')
rad2_1.place(x=872, y=55)
rad2_2.place(x=872, y=75)
rad2_3.place(x=872, y=95)
#rad2_4.place(x=850, y=115)
#rad2_5.place(x=890, y=55)
#rad2_6.place(x=890, y=75)
#rad2_7.place(x=890, y=95)
#rad2_8.place(x=890, y=115)

btn03 = Button(window, text="Произвести скрытие", width=25, command=hiding)
btn03.grid(column=0, row=3, padx=0, pady=10, columnspan=2)

btn13 = Button(window, text="Извлечь сообщение", width=25, command=extraction)
btn13.grid(column=1, row=3, padx=0, pady=10, columnspan=2)



window.mainloop()