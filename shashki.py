from tkinter import *
from tkinter import messagebox
import random
import time
import copy
import numpy

a = numpy.load('a.npy') # загружаем массив из прошлого скрипта
gl_okno=Tk()#создаём окно
gl_okno.title('Игра Шашки')#заголовок окна
gl_okno.minsize(800, 800)
gl_okno.state('zoomed')
doska=Canvas(gl_okno, width=800,height=800,bg='#F5F6BC')
doska.pack()
pole2 = []
n2_spisok=()#конечный список ходов компьютера

x = 0
y = 0
x2 = 0
y2 = 0


if a[0] == 'e':
    ur=1#количество предсказываемых компьютером ходов
elif a[0] == 'n':
    ur = 2
else:
    ur = 3
k_rez=0#!!!
o_rez=0
poz1_x=-1#клетка не задана
if a[1] == 'b':
    f_hi=False#определение хода игрока(no)
else:
    f_hi = True

def izobrazheniya_peshek():#загружаем изображения шашек
    global peshki
    global a
    if a[1] == 'w': # в зависимости от выбранного цвета ставим изображения пешек (1 - может быть как белым так и чёрным)
        i1=PhotoImage(file=r".\images\checker_white.png")
        i2=PhotoImage(file=r".\images\white crown.png")
        i3=PhotoImage(file=r".\images\checker_black.png")
        i5=PhotoImage(file=r".\images\checker.png")
        i4=PhotoImage(file=r".\images\black crown.png")
    else:
        i1=PhotoImage(file=r".\images\checker_black.png")
        i2=PhotoImage(file=r".\images\black crown.png")
        i3=PhotoImage(file=r".\images\checker_white.png")
        i4=PhotoImage(file=r".\images\white crown.png")
        i5=PhotoImage(file=r".\images\checker.png")

    peshki=[0,i1,i2,i3,i4,i5] # массив со всеми видами шашек, в том числе и отсутствующая шашка

def novaya_igra():#начинаем новую игру
    global pole
    global pole2

    pole=[[0,3,0,3,0,3,0,3], # создаём массив с данными о поле при новой игре 0-ничего, 3 - компьютер, 1 - игрок
          [3,0,3,0,3,0,3,0],
          [0,3,0,3,0,3,0,3],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [1,0,1,0,1,0,1,0],
          [0,1,0,1,0,1,0,1],
          [1,0,1,0,1,0,1,0]]


    pole2.append(copy.deepcopy(pole)) # deepcopy нужно, чтобы элементы массива не были зависимы от переменной pole


def vivod(x_poz_1,y_poz_1,x_poz_2,y_poz_2):#рисуем игровое поле
    global peshki
    global pole
    global kr_ramka,zel_ramka
    k=100
    x=0
    doska.delete('all') # стираем прошлую доску
    kr_ramka=doska.create_rectangle(-5, -5, -5, -5,outline="red",width=5) # создаём красную рамку за полем(-5 это значение по x,y начала и конца координат рамки)
    zel_ramka=doska.create_rectangle(-5, -5, -5, -5,outline="green",width=5) # создаём красную рамку за полем(-5 это значение по x,y начала и конца координат рамки)

    while x<8*k:#рисуем доску: нечётные чёрные клетки
        y=1*k # перемещаем координаты клетки, которую будем рисовать, начиная с y = 1, координаты клетки это коорднаты окна * 100
        while y<8*k:
            doska.create_rectangle(x, y, x+k, y+k,fill="#7A4848") # рисуем чёрный квадрат
            y+=2*k #прибавляем 2 к координатам, т.е рисуем через клетки
        x+=2*k #когда нарисовали одну линию, прибавляем к кординатам x 2, чтобы перейти на следующую линию
    x=1*k # сбрасываем x в конце цикла, чтобы рисовать дальше чётные клетки
    while x<8*k:#рисуем доску: чётные чёрные клетки
        y=0 # тут всё тоже самое, только начинаем с координат: x = 1 y = 0
        while y<8*k:
            doska.create_rectangle(x, y, x+k, y+k,fill="#7A4848")
            y+=2*k
        x+=2*k

    for y in range(8):#рисуем стоячие пешки
        for x in range(8): # здесь перебираем x, y в пределах 8, т.е весь массив поля
            a=pole[y][x] # выбираем конкретную позицию в массиве
            if a: # если по позиции в массиве что-то было
                if (x_poz_1,y_poz_1)!=(x,y):#стоячие пешки ? если эту пешку не выбирали то
                    doska.create_image(x*k + 6,y*k +6, anchor=NW, image=peshki[a]) # то просто её рисуем (+6 это чтобы поставить её ровно)
    #рисуем активную пешку
    a=pole[y_poz_1][x_poz_1] # выбираеи активную пешку по нажатым координатам
    if a:#???
        doska.create_image(x_poz_1*k,y_poz_1*k, anchor=NW, image=peshki[a])

def soobsenie(s):
    global f_hi
    global a
    z='Игра завершена'
    if s==1:
        i=messagebox.askyesno(title=z, message='Вы победили!\nНажми "Да", чтобы начать заново.',icon='info')
    if s==2:
        i=messagebox.askyesno(title=z, message='Вы проиграли!\nНажми "Да", чтобы начать заново.',icon='info')
    if s==3:
        i=messagebox.askyesno(title=z, message='Ходов больше нет.\nНажми "Да", чтобы начать заново.',icon='info')
    if i: # Если нажато да в диалоговом окне
        if a[1] == 'b':
            f_hi = False
            novaya_igra()
            hod_kompjutera()
        else:
            f_hi = True
            novaya_igra()
            hod_igroka()
        vivod(-1,-1,-1,-1)#рисуем игровое поле
        f_hi=True#ход игрока доступен
    else: # Если нажато нет
        gl_okno.destroy()
        import menu
        exit() # выключаем скрипт, чтобы не было ошибок

def pozici_1(event):#выбор клетки для хода 1
    x,y=(event.x)//100,(event.y)//100#вычисляем координаты клетки
    doska.coords(zel_ramka,x*100,y*100,x*100+100,y*100+100)#рамка в выбранной клетке

def pozici_2(event):#выбор клетки для хода 2
    global poz1_x,poz1_y,poz2_x,poz2_y
    global f_hi
    x,y=(event.x)//100,(event.y)//100#вычисляем координаты клетки
    if pole[y][x]==1 or pole[y][x]==2:#проверяем шашку игрока в выбранной клетке
        doska.coords(kr_ramka,x*100,y*100,x*100+100,y*100+100)#рамка в выбранной клетке
        poz1_x,poz1_y=x,y
    else:
        if poz1_x!=-1:#клетка выбрана
            poz2_x,poz2_y=x,y
            if f_hi:#ход игрока?
                hod_igroka()
                if not(f_hi):
                    time.sleep(0.5)
                    hod_kompjutera()#передаём ход компьютеру
            poz1_x=-1#клетка не выбрана
            doska.coords(kr_ramka,-5,-5,-5,-5)#рамка вне поля

def hod_kompjutera():#ход компьютера
    global f_hi
    global n2_spisok
    proverka_hk(1,(),[])
    if n2_spisok:#проверяем наличие доступных ходов
        kh=len(n2_spisok)#количество ходов
        th=random.randint(0,kh-1)#случайный ход
        dh=len(n2_spisok[th])#длина хода
        for i in range(dh-1):
            #выполняем ход
            if f_hi == False:
                spisok=hod(1,n2_spisok[th][i][0],n2_spisok[th][i][1],n2_spisok[th][1+i][0],n2_spisok[th][1+i][1])
        n2_spisok=[]#очищаем список ходов
        for n1 in range(8):
            for n2 in range(8):
                if pole[n1][n2] ==5:
                    pole[n1][n2] = 0
        f_hi=True#ход игрока доступен

    #определяем победителя
    s_k,s_i=skan()
    if not(s_i):
            soobsenie(2)
    elif not(s_k):
            soobsenie(1)
    elif f_hi and not(spisok_hi()):
            soobsenie(3)
    elif not(f_hi) and not(spisok_hk()):
            soobsenie(3)

def spisok_hk():#составляем список ходов компьютера
    spisok=prosmotr_hodov_k1([])#здесь проверяем обязательные ходы
    if not(spisok):
        spisok=prosmotr_hodov_k2([])#здесь проверяем оставшиеся ходы
    return spisok

def proverka_hk(tur,n_spisok,spisok):#!!!
    global pole
    global n2_spisok
    global l_rez,k_rez,o_rez
    if not(spisok):#если список ходов пустой...
        spisok=spisok_hk()#заполняем

    if spisok:
        k_pole=copy.deepcopy(pole)#копируем поле
        for ((poz1_x,poz1_y),(poz2_x,poz2_y)) in spisok:#проходим все ходы по списку
            t_spisok=hod(0,poz1_x,poz1_y,poz2_x,poz2_y)
            if t_spisok:#если существует ещё ход
                proverka_hk(tur,(n_spisok+((poz1_x,poz1_y),)),t_spisok)
            else:
                proverka_hi(tur,[])
                if tur==1:
                    t_rez=o_rez/k_rez
                    if not(n2_spisok):#записываем, если пустой
                        n2_spisok=(n_spisok+((poz1_x,poz1_y),(poz2_x,poz2_y)),)
                        l_rez=t_rez#сохряняем наилучший результат
                    else:
                        if t_rez==l_rez:
                            n2_spisok=n2_spisok+(n_spisok+((poz1_x,poz1_y),(poz2_x,poz2_y)),)
                        if t_rez>l_rez:
                            n2_spisok=()
                            n2_spisok=(n_spisok+((poz1_x,poz1_y),(poz2_x,poz2_y)),)
                            l_rez=t_rez#сохряняем наилучший результат
                    o_rez=0
                    k_rez=0

            pole=copy.deepcopy(k_pole)#возвращаем поле
    else:#???
        s_k,s_i=skan()#подсчёт результата хода
        o_rez+=(s_k-s_i)
        k_rez+=1

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
        for ((poz1_x,poz1_y),(poz2_x,poz2_y)) in spisok:
            t_spisok=hod(0,poz1_x,poz1_y,poz2_x,poz2_y)
            if t_spisok:#если существует ещё ход
                proverka_hi(tur,t_spisok)
            else:
                if tur<ur:
                    proverka_hk(tur+1,(),[])
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
    global pole2
    global x,x2,y,y2
    f_hi=False#считаем ход игрока выполненным
    spisok=spisok_hi()
    if spisok:
        if ((poz1_x,poz1_y),(poz2_x,poz2_y)) in spisok:#проверяем ход на соответствие в правилам игры
            if x != 0 and y!=0:
                if poz1_y == y and poz1_x == x:
                    if f_hi == False:
                        pole2.append(copy.deepcopy(pole)) #каждый раз при ходе игрока записывай состояние поля до этого хода
                        t_spisok=hod(1,poz1_x,poz1_y,poz2_x,poz2_y)#если всё хорошо, делаем ход
                    if t_spisok:#если есть ещё, ход той же пешкой
                        x2 = poz1_x #записывай координа предыдущей активной пешки
                        y2 = poz1_y
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
                    f_hi = True
            else:
                pole2.append(copy.deepcopy(pole)) #каждый раз при ходе игрока записывай состояние поля до этого хода
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
    global spisok
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

    #рубим пешку игрока
    kx=ky=1
    if poz1_x<poz2_x:kx=-1
    if poz1_y<poz2_y:ky=-1
    x_poz,y_poz=poz2_x,poz2_y
    while (poz1_x!=x_poz) or (poz1_y!=y_poz):
        x_poz+=kx
        y_poz+=ky
        if pole[y_poz][x_poz]!=0:
            pole[y_poz][x_poz]=5
            if f:vivod(-1,-1,-1,-1)#рисуем игровое поле
            #проверяем ход той же пешкой...
            if pole[poz2_y][poz2_x]==3 or pole[poz2_y][poz2_x]==4:#...компьютера
                return prosmotr_hodov_k1p([],poz2_x,poz2_y)#возвращаем список доступных ходов
            elif pole[poz2_y][poz2_x]==1 or pole[poz2_y][poz2_x]==2:#...игрока
                return prosmotr_hodov_i1p([],poz2_x,poz2_y)#возвращаем список доступных ходов
    if f:vivod(poz1_x,poz1_y,poz2_x,poz2_y)#рисуем игровое поле

def prosmotr_hodov_k1(spisok):#проверка наличия обязательных ходов
    for y in range(8):#сканируем всё поле
        for x in range(8):
            spisok=prosmotr_hodov_k1p(spisok,x,y)
    return spisok

def prosmotr_hodov_k1p(spisok,x,y):
    if pole[y][x]==3:#пешка
        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
            if 0<=y+iy+iy<=7 and 0<=x+ix+ix<=7:
                if pole[y+iy][x+ix]==1 or pole[y+iy][x+ix]==2:
                    if pole[y+iy+iy][x+ix+ix]==0:
                        spisok.append(((x,y),(x+ix+ix,y+iy+iy)))#запись хода в конец списка
    if pole[y][x]==4:#пешка с короной
        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
            osh=0#определение правильности хода
            for i in  range(1,8):
                if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                    if osh==1:
                        spisok.append(((x,y),(x+ix*i,y+iy*i)))#запись хода в конец списка
                    if pole[y+iy*i][x+ix*i]==1 or pole[y+iy*i][x+ix*i]==2 :
                        osh+=1
                    if pole[y+iy*i][x+ix*i]==3 or pole[y+iy*i][x+ix*i]==4 or osh==2 or pole[y+iy*i][x+ix*i]==5:
                        if osh>0:spisok.pop()#удаление хода из списка
                        break
    return spisok

def prosmotr_hodov_k2(spisok):#проверка наличия остальных ходов
    for y in range(8):#сканируем всё поле
        for x in range(8):
            if pole[y][x]==3:#шашка
                for ix,iy in (-1,1),(1,1):
                    if 0<=y+iy<=7 and 0<=x+ix<=7:
                        if pole[y+iy][x+ix]==0:
                            spisok.append(((x,y),(x+ix,y+iy)))#запись хода в конец списка
                        if pole[y+iy][x+ix]==1 or pole[y+iy][x+ix]==2:
                            if 0<=y+iy*2<=7 and 0<=x+ix*2<=7:
                                if pole[y+iy*2][x+ix*2]==0:
                                    spisok.append(((x,y),(x+ix*2,y+iy*2)))#запись хода в конец списка
            if pole[y][x]==4:#шашка с короной
                for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                    osh=0#определение правильности хода
                    for i in range(1,8):
                        if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                            if pole[y+iy*i][x+ix*i]==0:
                                spisok.append(((x,y),(x+ix*i,y+iy*i)))#запись хода в конец списка
                            if pole[y+iy*i][x+ix*i]==1 or pole[y+iy*i][x+ix*i]==2:
                                osh+=1
                            if pole[y+iy*i][x+ix*i]==3 or pole[y+iy*i][x+ix*i]==4 or osh==2:
                                break
    return spisok

def prosmotr_hodov_i1(spisok):#проверка наличия обязательных ходов
    spisok=[]#список ходов
    for y in range(8):#сканируем всё поле
        for x in range(8):
            spisok=prosmotr_hodov_i1p(spisok,x,y)
    return spisok

def prosmotr_hodov_i1p(spisok,x,y):
    if pole[y][x]==1:#шашка
        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
            if 0<=y+iy+iy<=7 and 0<=x+ix+ix<=7:
                if pole[y+iy][x+ix]==3 or pole[y+iy][x+ix]==4:
                    if pole[y+iy+iy][x+ix+ix]==0:
                        spisok.append(((x,y),(x+ix+ix,y+iy+iy)))#запись хода в конец списка
    if pole[y][x]==2:#шашка с короной
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
    return spisok

def prosmotr_hodov_i2(spisok):#проверка наличия остальных ходов
    for y in range(8):#сканируем всё поле
        for x in range(8):
            if pole[y][x]==1:#шашка
                for ix,iy in (-1,-1),(1,-1):
                    if 0<=y+iy<=7 and 0<=x+ix<=7:
                        if pole[y+iy][x+ix]==0:
                            spisok.append(((x,y),(x+ix,y+iy)))#запись хода в конец списка
                        if pole[y+iy][x+ix]==3 or pole[y+iy][x+ix]==4:
                            if 0<=y+iy*2<=7 and 0<=x+ix*2<=7:
                                if pole[y+iy*2][x+ix*2]==0:
                                    spisok.append(((x,y),(x+ix*2,y+iy*2)))#запись хода в конец списка
            if pole[y][x]==2:#шашка с короной
                for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                    osh=0#определение правильности хода
                    for i in range(1,8):
                        if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                            if pole[y+iy*i][x+ix*i]==0:
                                spisok.append(((x,y),(x+ix*i,y+iy*i)))#запись хода в конец списка
                            if pole[y+iy*i][x+ix*i]==3 or pole[y+iy*i][x+ix*i]==4:
                                osh+=1
                            if pole[y+iy*i][x+ix*i]==1 or pole[y+iy*i][x+ix*i]==2 or osh==2:
                                break
    return spisok

def z(event): #отмена хода
    global pole
    global pole2
    global f_hi
    global x,x2,y,y2
    try:
        if pole != [[0,3,0,3,0,3,0,3],
          [3,0,3,0,3,0,3,0],
          [0,3,0,3,0,3,0,3],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [1,0,1,0,1,0,1,0],
          [0,1,0,1,0,1,0,1],
          [1,0,1,0,1,0,1,0]]:
            pole = pole2[-1]#загружаем последнее состояние поля
            pole2 = []# обнуляем, чтобы нельзя было откатить на 2+ хода
            f_hi = True#ходит игрок
            x = x2
            y = y2
            vivod(-1,-1,-1,-1) #рисуем поле в состоянии без выбранной клетки
    except:
        pass

def Esc(event):
    global gl_okno
    gl_okno.destroy()
    import menu

def l(event): #если первым ходит бот
    if f_hi == False and pole == [[0,3,0,3,0,3,0,3],
          [3,0,3,0,3,0,3,0],
          [0,3,0,3,0,3,0,3],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [1,0,1,0,1,0,1,0],
          [0,1,0,1,0,1,0,1],
          [1,0,1,0,1,0,1,0]]:
          hod_kompjutera()


izobrazheniya_peshek()#здесь загружаем изображения шашек
novaya_igra()#начинаем новую игру
vivod(-1,-1,-1,-1)#рисуем игровое поле
doska.bind_all('<Control-z>', z)#если нажали нужное сочетание - откатываем (происходит отмена хода)
doska.bind_all('<Escape>', Esc)
doska.bind("<Motion>", pozici_1)#движение мышки по полю
doska.bind("<Button-1>", pozici_2)#нажатие левой кнопки
doska.bind("<Enter>", l) #если курсор где-то в окне, проверяем, кто ходит первым

mainloop()