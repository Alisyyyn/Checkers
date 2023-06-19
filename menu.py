from tkinter import *
import numpy # через numpy и массив будем передавать данные второму скрипту
import os

#Создание окна
root = Tk()
root.geometry("800x600")
root.title('Игра Шашки')
#Свернуть окно
root.minsize(800, 600)
root.state('zoomed')
a = []
w = None
msg = None
# Загрузка изображения фона
background_image = PhotoImage(file=r".\images\main_menu.png")
background_label = Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

text = '''• При игре имеется отмена хода нажатием клавиш Ctrl+Z;
• Во время игрового процесса можно выйти в главное меню с помощью клавиши Esc;

• Игра ведётся на доске 8х8 клеток, только на коричневых ячейках; 
• Шашки в начале игры занимают первые три ряда с каждый стороны; 
• Бить можно произвольное количество шашек в любых направлениях; 
• Простые шашки ходят только вперёд; 
• Простая шашка может срубить назад; 
• Дамка ходит на любое число полей в любую сторону; 
• Проигрывает тот, у кого не остается фигур, либо ходов; 
• Шашка снимается с поля после боя (одну шашку нельзя срубить дважды за один ход); 
• Бить обязательно; 
• Шашка превращается в дамку, достигнув восьмой (для белых) или первой (для черных) линии доски; 
• Если шашка во время боя проходит через дамочное поле, то она превращается в дамку и следующие бои (если они возможны) совершает уже как дамка. '''

def help(): #кнопка помощи
    global background_label
    global msg
    global w
    background_label.config(image='') #убираем фоновое изображение
    background_label.config(bg='#F5F6BC') #делаем цвет фото
    w = Label(background_label, text ='Правила', font = "50",pady = '70', bg='#F5F6BC') #создаём название окна
    msg = Message(background_label, text = text, font = "12", bg='#F5F6BC') #текст окна
    w.pack() # показываем заголовок
    msg.pack() # текст

    #скрываем кнопки
    play_button.place_forget()
    exit_button.place_forget()
    help_button.place_forget()

    #делаем кнопку назад
    back0_button.place(relx=.5, rely=.9, anchor="c")

def mode():
    vs_computer_button.place_forget()
    vs_player_button.place_forget()
    back_button.place_forget()

    easy_button.place(relx=.5, rely=.3, anchor="c")
    norm_button.place(relx=.5, rely=.4, anchor="c")
    hard_button.place(relx=.5, rely=.5, anchor="c")

    back2_button.place(relx=.5, rely=.7, anchor="c")


# Функция для создания новых кнопок и скрытия старых
def create_new_buttons():
    global a

    # Скрытие старых кнопок
    play_button.place_forget()
    exit_button.place_forget()
    easy_button.place_forget()
    norm_button.place_forget()
    hard_button.place_forget()
    back2_button.place_forget()

    help_button.place_forget()

    # Создание новых кнопок
    vs_computer_button.place(relx=.5, rely=.3, anchor="c")
    vs_player_button.place(relx=.5, rely=.5, anchor="c")

    # Создание кнопки "Назад"
    back_button.place(relx=.5, rely=.7, anchor="c")
    a = a[:-1]

# Функция для отображения кнопок "Начать игру" и "Выход"
def show_play_button():
    global msg
    global w
    global background_label
    global background_image

    try:
        #если есть сообщение с правилами - убираем, и делаем фоновое изображение, убираем цвет фона
        w.destroy()
        msg.destroy()
        background_label.config(image = background_image)
        background_label.config(bg = 'white')
    except:
        pass

    # Отображение кнопок "Начать игру", "Правила" и "Выход"
    play_button.place(relx=.5, rely=.3, anchor="c")
    exit_button.place(relx=.5, rely=.7, anchor="c")

    help_button.place(relx=.5, rely=.5, anchor="c")

    # Скрытие кнопок "Игрок vs компьютер" и "Игрок vs игрок"
    vs_computer_button.place_forget()
    vs_player_button.place_forget()
    back0_button.place_forget()

    # Скрытие кнопки "Назад"
    back_button.place_forget()

def colors():

    #убираем кнопки сложности
    easy_button.place_forget()
    norm_button.place_forget()
    hard_button.place_forget()
    back2_button.place_forget()

    # Создание новых кнопок
    white_button.place(relx=.5, rely=.3, anchor="c")
    black_button.place(relx=.5, rely=.4, anchor="c")

    # Создание кнопки "Назад"
    back3_button.place(relx=.5, rely=.6, anchor="c")

def back3():
    global a

    white_button.place_forget()
    black_button.place_forget()
    back3_button.place_forget()
    
    easy_button.place(relx=.5, rely=.3, anchor="c")
    norm_button.place(relx=.5, rely=.4, anchor="c")
    hard_button.place(relx=.5, rely=.5, anchor="c")

    back2_button.place(relx=.5, rely=.7, anchor="c")
    a = a[:-1]

def PvsP():
    root.destroy() # уничтожение старого окна
    import time
    time.sleep(0.5)
    os.system("shashkiPvP.py 1")
    print('test')
def PvsC():
    numpy.save('a',a) #сохраняем массив в файл
    root.destroy()
    os.system("shashki.py 1")
def E():
    global a
    a.append('e') #добавление данных в массив сложность e - easym, n - normal, h - hard
def N():
    global a
    a.append('n')
def H():
    global a
    a.append('h')
def W():
    global a
    a.append('w') # добавляем в массив цвет: w - белый b - чёрный
def B():
    global a
    a.append('b')

# Создание кнопок
play_button = Button(root, text="Начать игру", height = 1, width = 17, bg="#B55F5F", fg="white", font=("Helvetica", 24), command=create_new_buttons)
exit_button = Button(root, text="Выход",  height = 1, width = 17, bg="#B55F5F", fg="white", font=("Helvetica", 24), command=root.quit)
help_button = Button(root, text="Правила",  height = 1, width = 17, bg="#B55F5F", fg="white", font=("Helvetica", 24), command=help)

back0_button = Button(root, text="Назад",  height = 1, width = 17, bg="#B55F5F", fg="white", font=("Helvetica", 24), command=show_play_button) 

vs_computer_button = Button(root, text="Игрок vs компьютер", height = 1, width = 17, bg="#B55F5F", fg="white", font=("Helvetica", 24), command = mode)
vs_player_button = Button(root, text="Игрок vs игрок", height = 1, width = 17, bg="#B55F5F", fg="white", font=("Helvetica", 24), command = PvsP)

back_button = Button(root, text="Назад",  bg="#B55F5F", height = 1, width = 17, fg="white", font=("Helvetica", 24), command=show_play_button)

easy_button = Button(root,text="Легко", bg="#B55F5F", height = 1, width = 17, fg="white", font=("Helvetica", 24), command= lambda:[colors(),E()])
norm_button = Button(root,text="Нормально", bg="#B55F5F", height = 1, width = 17, fg="white", font=("Helvetica", 24), command= lambda:[colors(),N()])
hard_button = Button(root,text="Сложно", bg="#B55F5F", height = 1, width = 17, fg="white", font=("Helvetica", 24), command= lambda:[colors(),H()])
back2_button = Button(root,text="Назад", bg="#B55F5F", height = 1, width = 17, fg="white", font=("Helvetica", 24), command= create_new_buttons)

white_button = Button(root,text="Белые", bg="#B55F5F", height = 1, width = 17, fg="white", font=("Helvetica", 24), command = lambda:[W(),PvsC()])
black_button = Button(root,text="Чёрные", bg="#B55F5F", height = 1, width = 17, fg="white", font=("Helvetica", 24), command = lambda:[B(),PvsC()])
back3_button = Button(root,text="Назад", bg="#B55F5F", height = 1, width = 17, fg="white", font=("Helvetica", 24), command = back3)

# Отображение кнопок "Начать игру" и "Выход" при запуске
show_play_button()

root.mainloop()