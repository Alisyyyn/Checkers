from tkinter import *
from tkinter import messagebox
import random
import time
import copy
from PIL import ImageTk, Image
import copy

gl_okno=Tk()#создаём окно
gl_okno.title('Игра Шашки')#заголовок окна
gl_okno.minsize(800, 800)
gl_okno.state('zoomed')
doska=Canvas(gl_okno, width=800,height=800,bg='#F5F6BC')
doska.pack()
pole2 = []
x=0
y=0
x2 = 0
y2 = 0

n2_spisok=()#конечный список ходов компьютера
k_rez=0#!!!
o_rez=0
poz1_x=-1#клетка не задана
f_hi=True#определение хода игрока(да)
motion = '1p'

def izobrazheniya_peshek():#загружаем изображения шашек
    global peshki
    i1=PhotoImage(file=r".\images\checker_white.png")
    i2=PhotoImage(file=r".\images\white crown.png")
    i3=PhotoImage(file=r".\images\checker_black.png")
    i5=PhotoImage(file=r".\images\checker.png")
    i4=PhotoImage(file=r".\images\black crown.png")
    peshki=[0,i1,i2,i3,i4,i5]

def novaya_igra():#начинаем новую игру
    global pole
    global motion

    motion = '1p'
    pole=[[0,3,0,3,0,3,0,3],
          [3,0,3,0,3,0,3,0],
          [0,3,0,3,0,3,0,3],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [1,0,1,0,1,0,1,0],
          [0,1,0,1,0,1,0,1],
          [1,0,1,0,1,0,1,0]]
def vivod(x_poz_1,y_poz_1,x_poz_2,y_poz_2):#рисуем игровое поле
    global peshki
    global pole
    global kr_ramka,zel_ramka
    k=100
    x=0
    try:
        doska.delete('all')
    except:
        pass
    kr_ramka=doska.create_rectangle(-5, -5, -5, -5,outline="red",width=5)
    zel_ramka=doska.create_rectangle(-5, -5, -5, -5,outline="green",width=5)

    while x<8*k:#рисуем доску
        y=1*k
        while y<8*k:
            doska.create_rectangle(x, y, x+k, y+k,fill="#7A4848")
            y+=2*k
        x+=2*k
    x=1*k
    while x<8*k:#рисуем доску
        y=0
        while y<8*k:
            doska.create_rectangle(x, y, x+k, y+k,fill="#7A4848")
            y+=2*k
        x+=2*k
    
    for y in range(8):#рисуем стоячие шашки
        for x in range(8):
            z=pole[y][x]
            if z:  
                if (x_poz_1,y_poz_1)!=(x,y):#стоячие шашки?
                    doska.create_image(x*k + 8,y*k + 8, anchor=NW, image=peshki[z])
    #рисуем активную шашку
    z=pole[y_poz_1][x_poz_1]
    if z:#???
        doska.create_image(x_poz_1*k,y_poz_1*k, anchor=NW, image=peshki[z])

def soobsenie(s):
    global f_hi
    z='Игра завершена'
    if s==1:
        i=messagebox.askyesno(title=z, message='Белые победили!\nНажми "Да", чтобы начать заново.',icon='info')
    if s==2:
        i=messagebox.askyesno(title=z, message='Чёрные победили!\nНажми "Да", чтобы начать заново.',icon='info')
    if i:
        novaya_igra()
        vivod(-1,-1,-1,-1)#рисуем игровое поле
        f_hi=True#ход игрока доступен
    else:
        gl_okno.destroy()
        import menu
        exit()

def pozici_1(event):#выбор клетки для хода 1
    x,y=(event.x)//100,(event.y)//100#вычисляем координаты клетки
    doska.coords(zel_ramka,x*100,y*100,x*100+100,y*100+100)#рамка в выбранной клетке

def pozici_2(event):#выбор клетки для хода 2
    global poz1_x,poz1_y,poz2_x,poz2_y
    global f_hi
    global motion
    x,y=(event.x)//100,(event.y)//100#вычисляем координаты клетки
    if motion == '1p':
        if pole[y][x]==1 or pole[y][x]==2:#проверяем шашку игрока в выбранной клетке
            doska.coords(kr_ramka,x*100,y*100,x*100+100,y*100+100)#рамка в выбранной клетке
            poz1_x,poz1_y=x,y
        else:
            if poz1_x!=-1:#клетка выбрана
                poz2_x,poz2_y=x,y
                hod_igroka()
                if not(f_hi):
                    time.sleep(0.5)
                    motion = '2p'
                poz1_x=-1#клетка не выбрана
                doska.coords(kr_ramka,-5,-5,-5,-5)#рамка вне поля
    if motion == '2p':
        if pole[y][x]==3 or pole[y][x]==4:#проверяем шашку игрока в выбранной клетке
            doska.coords(kr_ramka,x*100,y*100,x*100+100,y*100+100)#рамка в выбранной клетке
            poz1_x,poz1_y=x,y
        else:
            if poz1_x!=-1:#клетка выбрана
                poz2_x,poz2_y=x,y
                hod_igroka()
                if not(f_hi):
                    time.sleep(0.5)
                    motion = '1p'
                poz1_x=-1#клетка не выбрана
                doska.coords(kr_ramka,-5,-5,-5,-5)#рамка вне поля


def spisok_hi():#составляем список ходов игрока
    spisok=prosmotr_hodov_i1([])#здесь проверяем обязательные ходы
    if not(spisok):
        spisok=prosmotr_hodov_i2([])#здесь проверяем оставшиеся ходы
    return spisok
    
def proverka_hi(tur,spisok):
    global pole,k_rez,o_rez
    global ur
    if not(spisok):
        spisok=spisok_hi()

    if spisok:#проверяем наличие доступных ходов
        k_pole=copy.deepcopy(pole)#копируем поле
        if motion == '1p':
            for ((poz1_x,poz1_y),(poz2_x,poz2_y)) in spisok:
                t_spisok=hod(0,poz1_x,poz1_y,poz2_x,poz2_y)
                if t_spisok:#если существует ещё ход
                    proverka_hi(tur,t_spisok)
                else:
                    s_k,s_i=skan()#подсчёт результата хода
                    o_rez+=(s_k-s_i)
                    k_rez+=1

                pole=copy.deepcopy(k_pole)#возвращаем поле
        else:
            for ((poz1_x,poz3_y),(poz2_x,poz4_y)) in spisok:
                t_spisok=hod(0,poz1_x,7 - poz1_y,poz2_x,7 - poz2_y)
                if t_spisok:#если существует ещё ход
                    proverka_hi(tur,t_spisok)
                else:
                    s_k,s_i=skan()#подсчёт результата хода
                    o_rez+=(s_k-s_i)
                    k_rez+=1
                pole=copy.deepcopy(k_pole)#возвращаем поле
    else:#доступных ходов нет
        s_k,s_i=skan()#подсчёт результата хода
        o_rez+=(s_k-s_i)
        k_rez+=1

def skan():#подсчёт шашек на поле
    global pole
    s_i=0
    s_k=0
    for i in range(8):
        for ii in pole[i]:
            if ii==1:s_i+=1
            if ii==2:s_i+=3
            if ii==3:s_k+=1
            if ii==4:s_k+=3
    return s_k,s_i

def hod_igroka():
    global poz1_x,poz1_y,poz2_x,poz2_y
    global f_hi
    global pole
    global x 
    global y
    global x2
    global y2

    spisok=spisok_hi()
    if spisok:
        if ((poz1_x,poz1_y),(poz2_x,poz2_y)) in spisok: #проверяем ход на соответствие правилам игры
            if x != 0 and y!=0:
                if poz1_y == y and poz1_x == x:

                    f_hi=False#считаем ход игрока выполненным
                    t_spisok=hod(1,poz1_x,poz1_y,poz2_x,poz2_y)#если всё хорошо, делаем ход
                    if t_spisok:#если есть ещё ход той же шашкой
                        x2 = x #записываем координаты предыдущей активной шашки
                        y2 = y
                        x = poz2_x
                        y = poz2_y
                        f_hi=True#считаем ход игрока невыполненным
                    else:
                        x = 0
                        y = 0
                        for n1 in range(8):
                            for n2 in range(8):
                                if pole[n1][n2] == 5:
                                    pole[n1][n2] = 0
            else:
                t_spisok=hod(1,poz1_x,poz1_y,poz2_x,poz2_y)#если всё хорошо, делаем ход

                f_hi=False#считаем ход игрока выполненным
                if t_spisok:#если есть ещё ход той же шашкой
                    x = poz2_x
                    y = poz2_y
                    f_hi=True#считаем ход игрока невыполненным
                else:
                    for n1 in range(8):
                        for n2 in range(8):
                            if pole[n1][n2] == 5:
                                pole[n1][n2] = 0
        else:
            f_hi=True#считаем ход игрока невыполненным

    doska.update()#!!!обновление

def hod(f,poz1_x,poz1_y,poz2_x,poz2_y):
    global pole
    global pole2
    global motion
    pole2.append([copy.deepcopy(pole), motion])
    if f:vivod(poz1_x,poz1_y,poz2_x,poz2_y)#рисуем игровое поле
    #превращение
    if poz2_y==0 and pole[poz1_y][poz1_x]==1:
        pole[poz1_y][poz1_x]=2
    #превращение
    if poz2_y==7 and pole[poz1_y][poz1_x]==3:
        pole[poz1_y][poz1_x]=4
    #делаем ход
    pole[poz2_y][poz2_x]=pole[poz1_y][poz1_x]
    pole[poz1_y][poz1_x]=0

    #рубим шашку игрока
    kx=ky=1
    if poz1_x<poz2_x:kx=-1
    if poz1_y<poz2_y:ky=-1
    x_poz,y_poz=poz2_x,poz2_y
    while (poz1_x!=x_poz) or (poz1_y!=y_poz):
        x_poz+=kx #блок 1
        y_poz+=ky #блок 1
        if pole[y_poz][x_poz]!=0:
            pole[y_poz][x_poz]=5
            if f:vivod(-1,-1,-1,-1)#рисуем игровое поле
            s_k,s_i=skan()
            if not(s_i):
                    soobsenie(2)
            elif not(s_k):
                    soobsenie(1)
            elif f_hi and not (spisok_hi()):
                soobsenie(3)
            if f:vivod(poz1_x,poz1_y,poz2_x,poz2_y)#рисуем игровое поле
            return prosmotr_hodov_i1p([],poz2_x,poz2_y)#возвращаем список доступных ходов

    s_k,s_i=skan()
    if not(s_i):
            soobsenie(2)
    elif not(s_k):
            soobsenie(1)
    elif f_hi and not (spisok_hi()):
        soobsenie(3)
    if f:vivod(poz1_x,poz1_y,poz2_x,poz2_y)#рисуем игровое поле

def prosmotr_hodov_i1(spisok):#проверка наличия обязательных ходов
    spisok=[]#список ходов
    for y in range(8):#сканируем всё поле
        for x in range(8):
            spisok=prosmotr_hodov_i1p(spisok,x,y)
    return spisok

def prosmotr_hodov_i1p(spisok,x,y):
    if motion =='1p':
        if pole[y][x]==1:#шашка
            for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                if 0<=y+iy+iy<=7 and 0<=x+ix+ix<=7:
                    if pole[y+iy][x+ix]==3 or pole[y+iy][x+ix]==4:
                        if pole[y+iy+iy][x+ix+ix]==0:
                            spisok.append(((x,y),(x+ix+ix,y+iy+iy)))#запись хода в конец списка
        if pole[y][x]==2:
            for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                osh=0#определение правильности хода
                for i in  range(1,8):
                    if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                        if osh==1:
                            spisok.append(((x,y),(x+ix*i,y+iy*i)))#запись хода в конец списка
                        if pole[y+iy*i][x+ix*i]==3 or pole[y+iy*i][x+ix*i]==4:
                            osh+=1
                        if pole[y+iy*i][x+ix*i]==1 or pole[y+iy*i][x+ix*i]==2 or osh==2 or pole[y+iy*i][x+ix*i]==5:
                            if osh>0:spisok.pop()#удаление хода из списка
                            break
    else:
        if pole[y][x]==3:#шашка
            for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                if 0<=y+iy+iy<=7 and 0<=x+ix+ix<=7:
                    if pole[y+iy][x+ix]==1 or pole[y+iy][x+ix]==2:
                        if pole[y+iy+iy][x+ix+ix]==0:
                            spisok.append(((x,y),(x+ix+ix,y+iy+iy)))#запись хода в конец списка
        if pole[y][x]==4:
            for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                osh=0#определение правильности хода
                for i in  range(1,8):
                    if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                        if osh==1:
                            spisok.append(((x,y),(x+ix*i,y+iy*i)))#запись хода в конец списка
                        if pole[y+iy*i][x+ix*i]==1 or pole[y+iy*i][x+ix*i]==2:
                            osh+=1
                        if pole[y+iy*i][x+ix*i]==3 or pole[y+iy*i][x+ix*i]==4 or osh==2 or pole[y+iy*i][x+ix*i]==5:
                            if osh>0:spisok.pop()#удаление хода из списка
                            break
    return spisok

def prosmotr_hodov_i2(spisok):#проверка наличия остальных ходов
    for y in range(8):#сканируем всё поле
        for x in range(8):
            if motion == '1p':
                for y in range(8):  #сканируем всё поле
                    for x in range(8):
                        if pole[y][x] == 1:  #шашка
                            for ix, iy in (-1, -1), (1, -1):
                                if 0 <= y + iy <= 7 and 0 <= x + ix <= 7:
                                    if pole[y + iy][x + ix] == 0:
                                        spisok.append(((x, y), (x + ix, y + iy)))  #запись хода в конец списка
                                    if pole[y + iy][x + ix] == 3 or pole[y + iy][x + ix] == 4:
                                        if 0 <= y + iy * 2 <= 7 and 0 <= x + ix * 2 <= 7:
                                            if pole[y + iy * 2][x + ix * 2] == 0:
                                                spisok.append(
                                                    ((x, y), (x + ix * 2, y + iy * 2)))  #запись хода в конец списка
                        if pole[y][x] == 2:  #шашка с короной
                            for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                                osh = 0  #определение правильности хода
                                for i in range(1, 8):
                                    if 0 <= y + iy * i <= 7 and 0 <= x + ix * i <= 7:
                                        if pole[y + iy * i][x + ix * i] == 0:
                                            spisok.append(
                                                ((x, y), (x + ix * i, y + iy * i)))  #запись хода в конец списка
                                        if pole[y + iy * i][x + ix * i] == 3 or pole[y + iy * i][x + ix * i] == 4:
                                            osh += 1
                                        if pole[y + iy * i][x + ix * i] == 1 or pole[y + iy * i][
                                            x + ix * i] == 2 or osh == 2:
                                            break
            if motion == '2p':
                for y in range(8):  #сканируем всё поле
                    for x in range(8):
                        if pole[y][x] == 3:  #шашка
                            for ix, iy in (-1, 1), (1, 1):
                                if 0 <= y + iy <= 7 and 0 <= x + ix <= 7:
                                    if pole[y + iy][x + ix] == 0:
                                        spisok.append(((x, y), (x + ix, y + iy)))  #запись хода в конец списка
                                    if pole[y + iy][x + ix] == 1 or pole[y + iy][x + ix] == 2:
                                        if 0 <= y + iy * 2 <= 7 and 0 <= x + ix * 2 <= 7:
                                            if pole[y + iy * 2][x + ix * 2] == 0:
                                                spisok.append(
                                                    ((x, y), (x + ix * 2, y + iy * 2)))  #запись хода в конец списка
                        if pole[y][x] == 4:  #шашка с короной
                            for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                                osh = 0  #определение правильности хода
                                for i in range(1, 8):
                                    if 0 <= y + iy * i <= 7 and 0 <= x + ix * i <= 7:
                                        if pole[y + iy * i][x + ix * i] == 0:
                                            spisok.append(
                                                ((x, y), (x + ix * i, y + iy * i)))  #запись хода в конец списка
                                        if pole[y + iy * i][x + ix * i] == 1 or pole[y + iy * i][x + ix * i] == 2:
                                            osh += 1
                                        if pole[y + iy * i][x + ix * i] == 3 or pole[y + iy * i][
                                            x + ix * i] == 4 or osh == 2:
                                            break
    return spisok

def z(event):
    global pole
    global pole2
    global motion
    global x
    global y
    global x2
    global y2
    try:
        if  pole!=[[0,3,0,3,0,3,0,3], # Если был хотя бы 1 ход
          [3,0,3,0,3,0,3,0],
          [0,3,0,3,0,3,0,3],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [1,0,1,0,1,0,1,0],
          [0,1,0,1,0,1,0,1],
          [1,0,1,0,1,0,1,0]]:
            x = x2
            y = y2
            pole = pole2[-1][0]
            motion = pole2[-1][1]
            pole2 = []
            vivod(-1,-1,-1,-1)
    except:
        pass

def Esc(event):
    global gl_okno
    gl_okno.destroy()
    import menu

izobrazheniya_peshek()#здесь загружаем изображения шашек
novaya_igra()#начинаем новую игру
vivod(-1,-1,-1,-1)#рисуем игровое поле
doska.bind_all('<Escape>', Esc)
doska.bind_all('<Control-z>', z)#если нажали нужное сочетание - откатываем
doska.bind("<Motion>", pozici_1)#движение мышки по полю
doska.bind("<Button-1>", pozici_2)#нажатие левой кнопки

mainloop()