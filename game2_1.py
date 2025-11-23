import pygame as pg, sys, math
pg.init()
screen = pg.display.set_mode((800,600))

trapimg = pg.image.load("game1.ori/dotpict_21.png") #boss
trapimg = pg.transform.scale(trapimg,(70,70))
boss_1_body = pg.image.load("game1.ori/dotpict_13.png")
boss_1_body = pg.transform.scale(boss_1_body,(490,490))
boss_1_body_rect = pg.Rect(310,5,490,490)
boss_1_head = pg.image.load("game1.ori/dotpict_22.png")
boss_1_head = pg.transform.scale(boss_1_head,(120,120))
boss_1_head_small = pg.transform.scale(boss_1_head,(40,35))
boss_1_head_rect = pg.Rect(500,195,120,120)
boss_1_head_damage = pg.image.load("game1.ori/dotpict_23.png")
boss_1_head_damage = pg.transform.scale(boss_1_head_damage,(120,120))
boss_all_1_rect = pg.Rect(750,0,100,500)

HPimg = pg.image.load("game1.ori/dotpict_28.png") #能力
HPimg = pg.transform.scale(HPimg,(40,40))
speedimg = pg.image.load("game1.ori/dotpict_31.png")
speedimg = pg.transform.scale(speedimg,(45,45))
enemyHPimg = pg.image.load("game1.ori/dotpict_27.png")
enemyHPimg = pg.transform.scale(enemyHPimg,(40,40))

chara_1 = pg.image.load("game1.ori/dotpict_12.png") #プレイヤー
chara_1 = pg.transform.scale(chara_1,(80,80))
chara_2 = pg.image.load("game1.ori/dotpict_18.png")
chara_2 = pg.transform.scale(chara_2,(80,80))
chara_3 = pg.image.load("game1.ori/dotpict_14.png")
chara_3 = pg.transform.scale(chara_3,(80,80))
transparent_chara_1 = pg.image.load("game1.ori/dotpict_30.png")
transparent_chara_1 = pg.transform.scale(transparent_chara_1,(80,80))
transparent_chara_2 = pg.image.load("game1.ori/dotpict_29.png")
transparent_chara_2 = pg.transform.scale(transparent_chara_2,(80,80))
transparent_chara_3 = pg.image.load("game1.ori/dotpict_32.png")
transparent_chara_3 = pg.transform.scale(transparent_chara_3,(80,80))

startimg = pg.image.load("game1.ori/dotpict_25.png") #ボタン
startimg = pg.transform.scale(startimg,(150,150))
hardimg = pg.image.load("game1.ori/dotpict_24.png")
hardimg = pg.transform.scale(hardimg,(150,150))
replay_img = pg.image.load("game1.ori/dotpict_34.png")

walls = [pg.Rect(0,0,800,20), #行動範囲
         pg.Rect(0,0,20,600),
         pg.Rect(780,0,20,600),
         pg.Rect(0,580,800,20),
         pg.Rect(0,480,800,20)]

goalrect = pg.Rect(750,200,30,100) #ゴール
statesrect = pg.Rect(20,500,760,80) #ステータス

page = 0 #最初のページ
victory = 0 #normalクリア判定(0:未クリア、1:クリア済)

chara_1_Hp = 1 #各プレイヤーの能力
chara_1_speed = 4
chara_2_Hp = 2
chara_2_speed = 3
chara_3_Hp = 3
chara_3_speed = 2

button_cooling_time = 0 #ボタン誤作動防止

def gamereset():
    global time,cooling_time_1,fires,fires_vec,fires_time,boss_1_head_rect,boss_Hp,cooling_time_2
    global boss_attack_2_check,bomb,bomb_ready,boss_KO_check,damage_time,bomb_col,rightFlag,transparent_time,boss_KO_time,button_cooling_time
    time = 0 #時間
    cooling_time_1 = 100 #fireのクーリングタイム
    cooling_time_2 = -200 #bombのクーリングタイム
    damage_time = 0 #bossがダメージを受けた後のクーリングタイム
    fires = [] #各fireの位置
    fires_vec = [] #各fireのベクトル
    fires_time = [] #各fireの出現時間
    boss_1_head_rect = pg.Rect(640,195,120,120) #bossの頭の位置
    boss_attack_2_check = 0 #bombを一つだけ発動
    boss_KO_check = 0 #bossが倒れた瞬間1になる
    bomb = [] #各bombの位置
    bomb_ready = [] #各bombの予告
    bomb_col = [] #各bombの当たり判定
    rightFlag = True #プレイヤーの向き(Trueが左)
    transparent_time = 0 #プレイヤーが攻撃を受けたときの無敵時間測定
    boss_KO_time = -1 #bossが消えるモーション測定


def button_to_jump(btn,newpage,select): #ボタン操作
    global myimgR,myrect,myimgL,speed,Hp,transparent_myimgR,transparent_myimgL,myimgR_small,boss_Hp,boss_Hp_angry
    global page,hard,button_cooling_time
    mdown = pg.mouse.get_pressed()
    (mx,my) = pg.mouse.get_pos()
    if mdown[0] and button_cooling_time <= 0:
        if btn.collidepoint(mx,my):
            if select == 1:
                if newpage == 1: #normalモード
                    hard = 1
                    boss_Hp = 15
                    boss_Hp_angry = 10
                else: #chara_1
                    myimgR = chara_1
                    myimgR_small = pg.transform.scale(myimgR,(55,55))
                    myimgL = pg.transform.flip(myimgR,True,False)
                    transparent_myimgR = transparent_chara_1
                    transparent_myimgL = pg.transform.flip(transparent_myimgR,True,False)
                    myrect = pg.Rect(70,200,80,80)
                    speed = chara_1_speed
                    Hp = chara_1_Hp
            if select == 2: 
                if newpage == 1: #hardモード
                    hard = 2
                    boss_Hp = 20
                    boss_Hp_angry = 15
                else: #chara_2
                    myimgR = chara_2
                    myimgR_small = pg.transform.scale(myimgR,(55,55))
                    myimgL = pg.transform.flip(myimgR,True,False)
                    transparent_myimgR = transparent_chara_2
                    transparent_myimgL = pg.transform.flip(transparent_myimgR,True,False)
                    myrect = pg.Rect(70,200,80,80)
                    speed = chara_2_speed
                    Hp = chara_2_Hp
            if select == 3:
                if newpage == 2 or newpage == 3: #chara_3
                    myimgR = chara_3
                    myimgR_small = pg.transform.scale(myimgR,(55,55))
                    myimgL = pg.transform.flip(myimgR,True,False)
                    transparent_myimgR = transparent_chara_3
                    transparent_myimgL = pg.transform.flip(transparent_myimgR,True,False)
                    myrect = pg.Rect(70,200,80,80)
                    speed = chara_3_speed
                    Hp = chara_3_Hp
            page = newpage
            button_cooling_time = 20





def gamestage(): #基本ステージ
    global rightFlag
    global page
    screen.fill(pg.Color("gold"))

    #ステータス画面
    pg.draw.rect(screen,pg.Color("black"),statesrect)
    screen.blit(myimgR_small,(25,490))
    screen.blit(boss_1_head_small,(32,542))
    for i in range(Hp):
        screen.blit(HPimg,(80 + 34*i,500))  
    for i in range(boss_Hp):
        screen.blit(enemyHPimg,(80 + 34*i,540))

    #壁の描画
    for wall in walls:
        pg.draw.rect(screen,pg.Color("gold4"),wall)
    pg.draw.rect(screen,pg.Color("green3"),goalrect)

    #ゴール判定
    if myrect.colliderect(goalrect):
        page = 4
        myrect.x = 70
        myrect.y = 200

def MainCharacter(): #プレイヤー操作
    global rightFlag
    vx = 0
    vy = 0
    key = pg.key.get_pressed()
    if key[pg.K_RIGHT] or key[pg.K_d]:
        vx = speed
        rightFlag = True
    if key[pg.K_LEFT] or key[pg.K_a]:
        vx = -speed
        rightFlag = False
    if key[pg.K_UP] or key[pg.K_w]:
        vy = -speed
    if key[pg.K_DOWN] or key[pg.K_s]:
        vy = speed
    
    myrect.x += vx
    myrect.y += vy

    #壁や敵との衝突
    if myrect.collidelist(walls) != -1 or (boss_Hp > 0 and myrect.x > 570):
        myrect.x -= vx
        myrect.y -= vy

    #プレイヤーの描画
    if rightFlag and transparent_time < 2:
        screen.blit(myimgR,myrect)
    elif not rightFlag and transparent_time < 2:
        screen.blit(myimgL,myrect)
    elif rightFlag:
        screen.blit(transparent_myimgR,myrect)
    else:
        screen.blit(transparent_myimgL,myrect)



def startpage(): #タイトル画面
    gamereset()
    screen.fill(pg.Color("skyblue"))
    font = pg.font.Font(None,150)
    text = font.render("TREASURE",True,pg.Color("red"))
    screen.blit(text,(60,100))
    text = font.render("HUNTERS",True,pg.Color("red"))
    screen.blit(text,(60,200))
    btn1 = screen.blit(startimg,(160,380))
    button_to_jump(btn1,1,1)
    if victory == 1: #normalモードをクリアすると出現
        btn2 = screen.blit(hardimg,(480,380))
        button_to_jump(btn2,1,2)

def selectpage(): #プレイヤー選択画面
    screen.fill(pg.Color("blue"))
    font = pg.font.Font(None,80)
    text = font.render("CHOOSE A CHARACTER",True,pg.Color("white"))
    font = pg.font.Font(None,40)
    screen.blit(text,(55,50))

    #chara_1
    btn1 = pg.draw.rect(screen,pg.Color("white"),pg.Rect(200,150,400,100))
    screen.blit(chara_1,(220,160))
    text = font.render("HP",True,pg.Color("black"))
    screen.blit(text,(318,170))
    text = font.render("SPEED",True,pg.Color("black"))
    screen.blit(text,(320,210))
    for i in range(chara_1_Hp):
        screen.blit(HPimg,(420+38*i,160))
    for i in range(chara_1_speed):
        screen.blit(speedimg,(415+38*i,200))
    if hard == 1:
        button_to_jump(btn1,2,1)
    elif hard == 2:
        button_to_jump(btn1,3,1)

    #chara_2
    btn2 = pg.draw.rect(screen,pg.Color("white"),pg.Rect(200,300,400,100))
    screen.blit(chara_2,(220,310))
    text = font.render("HP",True,pg.Color("black"))
    screen.blit(text,(318,320))
    text = font.render("SPEED",True,pg.Color("black"))
    screen.blit(text,(320,360))
    for i in range(chara_2_Hp):
        screen.blit(HPimg,(420+38*i,310))
    for i in range(chara_2_speed):
        screen.blit(speedimg,(415+38*i,350))
    if hard == 1:
        button_to_jump(btn2,2,2)
    elif hard == 2:
        button_to_jump(btn2,3,2)

    #chara_3
    btn3 = pg.draw.rect(screen,pg.Color("white"),pg.Rect(200,450,400,100))
    screen.blit(chara_3,(220,460))
    text = font.render("HP",True,pg.Color("black"))
    screen.blit(text,(318,470))
    text = font.render("SPEED",True,pg.Color("black"))
    screen.blit(text,(320,510))
    for i in range(chara_3_Hp):
        screen.blit(HPimg,(420+38*i,460))
    for i in range(chara_3_speed):
        screen.blit(speedimg,(415+38*i,500))
    if hard == 1:
        button_to_jump(btn3,2,3)
    elif hard == 2:
        button_to_jump(btn3,3,3)
    

def gameclear(): #ゲームクリア画面
    global victory
    screen.fill(pg.Color("Gold"))
    font = pg.font.Font(None,150)
    text = font.render("GAMECLEAR",True,pg.Color("red"))
    screen.blit(text,(60,200))
    font = pg.font.Font(None,50)
    if hard == 1: #normalモードクリア時
        text = font.render("Hard mode is unlocked!",True,pg.Color("red"))
        screen.blit(text,(200,340))
    if hard == 2: #hardモードクリア時
        text = font.render("Amazing!!",True,pg.Color("red"))
        screen.blit(text,(305,340))
    btn1 = screen.blit(replay_img,(330,420))
    victory = 1 #normalモードクリア判定
    button_to_jump(btn1,0,0)
    

def gameover(): #ゲームオーバー画面
    screen.fill(pg.Color("navy"))
    font = pg.font.Font(None,150)
    text = font.render("GAMEOVER",True,pg.Color("red"))
    screen.blit(text,(100,200))
    btn1 = screen.blit(replay_img,(330,420))
    button_to_jump(btn1,0,0)

def is_circle_collision(x1,y1,r1,x2,y2,r2): #円同士の当たり判定
    dx = x1 - x2
    dy = y1 - y2
    distance = dx**2+dy**2
    return distance < (r1 + r2)**2

def fire_ref(i): #fireの壁反射
    global fires_vec
    if (fires[i].x < 25 and fires_vec[i][0] <= 0) or (fires[i].x > 730 and fires_vec[i][0] >= 0): #fire壁貫通バグ防止
        fires_vec[i][0] = -fires_vec[i][0]
    if (fires[i].y < 25 and fires_vec[i][1] <= 0) or (fires[i].y > 410 and fires_vec[i][1] >= 0):
        fires_vec[i][1] = -fires_vec[i][1]


def fire_draw(i): #fireの位置と描画
    global fires,fires_vec
    fires[i].x += fires_vec[i][0]
    fires[i].y += fires_vec[i][1]
    screen.blit(trapimg,fires[i])
    fire_ref(i)


def boss_attack_1(n): #fire攻撃(fireは最大n個)
    global fires,fires_vec,cooling_time_1

    #fire決定
    if len(fires) < n and damage_time < -30:
        if cooling_time_1 <= 0:
            fires.append(pg.Rect(560,boss_1_head_rect.y+20,70,70))
            x = myrect.x - 590
            y = myrect.y - 185
            r = math.isqrt(x**2+y**2)
            x = (x/r)*5
            y = (y/r)*5
            fires_vec.append([x,y])
            cooling_time_1 = 125
            fires_time.append(0)

    #fire描画
    for i in range(len(fires)):
        fire_draw(i)

def boss_attack_2(n): #bomb攻撃(n=1で縦、n=2で十字)
    global cooling_time_2,bomb,bomb_ready,boss_attack_2_check,bomb_col

    #bomb決定
    if cooling_time_2 <= 0 and boss_Hp <= boss_Hp_angry and boss_attack_2_check == 0:
        bomb.append(pg.Rect(myrect.x-10,20,100,460))
        bomb_ready.append(pg.Rect(myrect.x,30,80,440))
        bomb_col.append(pg.Rect(myrect.x-2,20,84,460))
        if n == 2:
            bomb.append(pg.Rect(20,myrect.y-10,760,100))
            bomb_ready.append(pg.Rect(30,myrect.y,740,80))
            bomb_col.append(pg.Rect(30,myrect.y-2,760,84))
        boss_attack_2_check = 1
        cooling_time_2 = 0

    #bomb予告
    if -99 <= cooling_time_2 <= -80 or -59 <= cooling_time_2 <= -40 or -19 <= cooling_time_2 <= 0:
        for i in range(len(bomb)):
            pg.draw.rect(screen,pg.Color("coral1"),bomb[i])
        for i in range(len(bomb)):
            pg.draw.rect(screen,pg.Color("gold"),bomb_ready[i])

    #bomb爆発
    if -130 <= cooling_time_2 <= -120:
        for i in range(len(bomb)):
            pg.draw.rect(screen,pg.Color("Red"),bomb[i])

    #bomb初期化
    if cooling_time_2 == -140:
        cooling_time_2 = 480
        bomb = []
        bomb_ready = []
        bomb_col = []
        boss_attack_2_check = 0




def stage_boss(n,m): #fireがn個,bombがm
    global time,Hp,boss_1_head_rect,fires,fires_vec,fires_time,cooling_time_1,page,boss_Hp
    global cooling_time_2,bomb,boss_KO_check,damage_time,bomb_col,transparent_time,boss_KO_time

    time = (time+1)%480
    if cooling_time_1 >= -12000:
        cooling_time_1 -= 1
    if cooling_time_2 >= -12000:
        cooling_time_2 -= 1
    if damage_time >= -12000:
        damage_time -= 1
    if transparent_time >= -12000:
        transparent_time -= 1
    if boss_KO_time >= -12000:
        boss_KO_time -= 1
    for i in range(len(fires)):
        fires_time[i] += 1

    #bossの頭の動き
    if 80 <= time < 240:
        boss_1_head_rect.y = 205
    elif 320 <= time:
        boss_1_head_rect.y = 185
    else:
        boss_1_head_rect.y = 195
    
    #bossの行動と描画
    if boss_Hp > 0:
        boss_attack_2(m)
        boss_attack_1(n)
        screen.blit(boss_1_body,boss_1_body_rect)
        if damage_time < 0:
            screen.blit(boss_1_head,boss_1_head_rect)
        else:
            screen.blit(boss_1_head_damage,boss_1_head_rect)

    #プレイヤーの当たり判定
    mydamage_check = 0
    for i in range(len(fires)):
        if is_circle_collision(myrect.x+40,myrect.y+40,31,fires[i].x+35,fires[i].y+35,26) and transparent_time < 0:
            Hp -= 1
            print("fire")
            mydamage_check = 1
            transparent_time = 120
            break
    if myrect.collidelist(bomb_col) != -1 and -130 <= cooling_time_2 <= -122 and mydamage_check == 0 and transparent_time < 0:
        Hp -= 1
        mydamage_check = 1
        transparent_time = 120
        print("bomb")
    if Hp == 0:
        page = 5
        pg.time.Clock().tick(3)
    elif mydamage_check == 1:
        pg.time.Clock().tick(3)

    #bossとの衝突や時間経過によるfireの消滅
    vanish = []
    for i in range(len(fires)):
        if boss_1_head_rect.colliderect(fires[i]):
            vanish.append(i)
            boss_Hp -= 1
            damage_time = 10
    for i in range(len(fires)):
        if fires_time[i] > 3600 and (not i in vanish):
            vanish.append(i)
    vanish.sort()
    for i in range(len(vanish)):
        fires.pop(vanish[-i-1])
        fires_vec.pop(vanish[-i-1])
        fires_time.pop(vanish[-i-1])
    
    #bossが倒れたとき
    if boss_Hp == 0 and boss_KO_check == 0:
        boss_KO_check = 1
        fires = []
        bomb_col = []
        boss_KO_time = 120
    if 0 <= boss_KO_time <= 29 or 60<= boss_KO_time <= 89:
        screen.blit(boss_1_body,boss_1_body_rect)
        screen.blit(boss_1_head,boss_1_head_rect)
        time -= 1
    


    
while True:
    if button_cooling_time >= 0:
        button_cooling_time -= 1
    if page == 0:
        startpage()
    if page == 1:
        selectpage()
    if page == 2:
        gamestage()
        font = pg.font.Font(None,40)
        text = font.render("NORMAL",True,pg.Color("white"))
        screen.blit(text,(600,510))
        stage_boss(2,1)
        MainCharacter()
    if page == 3:
        gamestage()
        font = pg.font.Font(None,40)
        text = font.render("HARD",True,pg.Color("white"))
        screen.blit(text,(600,510))
        stage_boss(4,2)
        MainCharacter()
    if page == 4:
        gameclear()
    if page == 5:
        gameover()
    
    pg.display.update()
    pg.time.Clock().tick(120)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()