#小遊戲
import pandas as pd
import random

players=[]
realms=["練氣期","築基期","金丹期","元嬰期","化神期"]
weapons=["木劍","鐵劍","精鋼劍","玄鐵劍"]
armors=["布衣","銅衣","鐵衣","金蟬衣"]

def boss_reward(player):    #掉寶
  drop = random.randint(1,100)
  if drop <= 30:
    item = "丹藥"
  elif drop <= 60:
    item = random.choice(weapons)
  else:
    item = random.choice(armors)
  player["bag"].append(item)
  player["exp"] += 100
  player["spirit_stone"] += 80

  print("獲得道具",item)
  print("獲得經驗+100")
  print("獲得靈石+80")
  level_up(player)

def show_bag():   #背包系統
  player = get_player()
  if player == None:
    return
  
  print("=====背包=====")

  if len(player["bag"]) == 0:
    print("背包是空的")
    return
  for i, item in enumerate(player["bag"],1):
    print(i, item)

  bag_choice = input("請輸入要裝備的物品編號,輸入Q離開")
  if bag_choice.upper() == "Q":
    print("離開背包")
    return
  if not bag_choice.isdigit():
    print("請輸入數字")
    return
  
  index = int(bag_choice) - 1
  if index < 0 or index >= len(player["bag"]):
    print("沒有這個物品")
    return
  
  item = player["bag"][index]
  if item == "鐵劍":
    player["weapon"] = "鐵劍"
    player["weapon_ATK"] = 25
    print("以裝備鐵劍")

  elif item == "精鋼劍":
    player["weapon"] = "精鋼劍"
    player["weapon_ATK"] = 50
    print("已裝備精鋼劍")

  elif item == "玄鐵劍":
    player["weapon"] = "玄鐵劍"
    player["weapon_ATK"] = 100
    print("已裝備玄鐵劍")

  elif item == "銅衣":
    player["armor"] = "銅衣"
    player["armor_DEF"] = 10
    print("已裝備銅衣")

  elif item == "鐵衣":
    player["armor"] = "鐵衣"
    player["armor_DEF"] = 20
    print("已裝備鐵衣")

  elif item == "金蟬衣":
    player["armor"] = "金蟬衣"
    player["armor_DEF"] = 30
    print("已裝備金蟬衣")

  else:
    print("這個物品不能裝備")
    return
  player["bag"].pop(index)
  show_player_info(player)

def meditate():   #打坐
  player = get_player()
  if player == None:
    return
  
  mp_gain = random.randint(20,50)
  
  player["mp"] += mp_gain

  if player["mp"] > 100:
    player["mp"] =100

  print("打坐成功")
  print("恢復魔力:", mp_gain, "點")

  show_player_info(player)

def calc_damage_taken(player, boss_damage):   #BOSS傷害計算
  damage = boss_damage - player["armor_DEF"]
  if damage < 1:
    damage = 1
  return damage

def get_player():
  if not players:
    print("目前沒有角色")
    return None
  
  print("當前角色數量:", len(players))
  print("角色列表:", ",".join(player["name"] for player in players))
  player = find_player()

  if player == None:
    print("查無角色")
    return None
  return player

def show_player_info(player):   #角色資訊
  print("目前血量:", player["hp"])
  print("目前魔力:", player["mp"])
  print("目前靈石:", player["spirit_stone"])
  print("目前丹藥:", player["pill"])
  print("目前經驗:", player["exp"],"/100")
  print("目前等級:", player["level"])
  print("目前境界:", player["realm"])
  print("裝備武器:", player["weapon"])
  print("裝備防具:", player["armor"])
  print("裝備技能:", player["skill"])
  print("當前攻擊力:", player["weapon_ATK"])
  print("當前防禦力", player["armor_DEF"])
  print("技能傷害:", player["skill_power"])
  print("背包:", player["bag"])

def create():   #創建
  while True:
    name = input("請輸入名稱,輸入 Q 回主選單:").strip()
                  
    if name.upper() == "Q":
      print("返回主選單")
      break

    if " " in name:
      print("不可輸入空格")
    elif len(name) < 3:
      print("不可小於三個字元")
    elif not name.isalpha():
      print("不可輸入英文以外的字元")
    else:
      duplicate = False
      for player in players:
        if player["name"] == name:
          duplicate = True
          break
      if duplicate:
          print("不可重複")
      else:
        players.append({
            "name":name,
            "realm_index":0,
            "realm":"練氣期",
            "level":1,
            "exp":0,
            "hp":100,
            "mp":100,
            "spirit_stone":50,
            "pill":3,
            "weapon":"木劍",
            "weapon_ATK": 5,
            "armor":"布衣",
            "armor_DEF":5,
            "skill":"火球術",
            "skill_power": 20,
            "bag":[]
        })
        print("創建成功")
        break

def cultivate():    #修練
  player = get_player()
  if player == None:
    return

  event = random.randint(1,100)

  if event <= 60:
    exp_gain = random.randint(10,30)
    print("一般修練+",exp_gain)
  elif event <= 90:
    exp_gain = random.randint(40,80)
    print("爆擊修練+",exp_gain)
  else:
    exp_gain = random.randint(120,200)
    print("天道頓悟+",exp_gain)

  player["exp"] += exp_gain
  print("修練成功,經驗增加:",exp_gain)

  level_up(player)
  show_player_info(player)

def find_player():    #找玩家
  keyword = input("請輸入角色名稱")

  for player in players:
    if player["name"] == keyword:
      return player
  
  return None

def alchemy():   #煉丹
  player = get_player()
  if player == None:
    return
  
  event = random.randint(1,100)

  if player["spirit_stone"] >= 30:
    print("可以煉丹")

    if event <= 60:
      player["spirit_stone"] -= 30
      player["pill"] += 1
      print("丹藥數量+1")
      print("煉丹成功")

    else:
      player["spirit_stone"] -= 30
      print("煉丹失敗")

  else:
    print("靈石不足,無法煉丹")

  show_player_info(player)

def level_up(player):   #經驗升級
  while player["exp"] >= 100:
    player["level"] += 1
    player["exp"] -= 100
    print("突破成功")

    realm_index = (player["level"] - 1) // 10
    if realm_index >= len(realms):
      realm_index = len(realms) - 1

    if realm_index != player["realm_index"]:
      player["realm_index"] = realm_index
      player["realm"] = realms[player["realm_index"]]
      print("境界突破")
      print(player["realm"])

def explore():   #探索秘境
  player = get_player()
  if player == None:
    return
  
  event = random.randint(1,100)

  if event >= 96:
    player["exp"] += 200
    print("上古傳承,經驗加200")
  elif event >= 86:
    player["hp"] -= 20
    print("遭遇妖獸,血量-20")

    if player["hp"] <= 0:
      player["hp"] = 0
      print("GameOver")

  elif event >= 71:
    player["pill"] += 1
    print("找到丹藥,丹藥+1")
  elif event >= 41:
    player["exp"] +=50
    print("領悟天地靈氣,經驗+50")
  else:
    player["spirit_stone"] += 50
    print("發現靈石礦脈,靈石+50")

  level_up(player)

  show_player_info(player)

def use_pill():   #4.使用丹藥
  player = get_player()
  if player == None:
    return
  
  if player["pill"] >= 1:
    player["pill"] -= 1
    player["hp"] += 50
    print("使用成功")

    if player["hp"] > 100:
        player["hp"] = 100
        print("血量已達上限")

  else:
    print("丹藥不足")

  show_player_info(player)

def show_status():    #5.查看狀態
  player = get_player()
  if player == None:
    return
  
  show_player_info(player)

def shop():   #6.商店
  player = get_player()
  if player == None:
    return

  while True:
    print("1.買丹藥:30靈石")
    print("2.賣丹藥:15靈石")
    print("3.升級武器")
    print("4.升級防具")
    print("5.升級技能")
    print("6.離開商店")

    shop_choice = input("請輸入商店功能")

    if shop_choice == "1":
      if player["spirit_stone"] >= 30:
        player["spirit_stone"] -= 30
        player["pill"] += 1
        print("購買成功,獲得丹藥+1")
      else:
        print("靈石不足,無法購買")

    elif shop_choice == "2":
      if player["pill"] >= 1:
        player["pill"] -= 1
        player["spirit_stone"] += 15
        print("賣出成功,獲得:15 塊靈石")
      else:
        print("物品不足,無法賣出")

    elif shop_choice == "3":

      print("1.升級鐵劍,消耗100靈石,獲得25攻擊力")
      print("2.升級精鋼劍,消耗300靈石,獲得50攻擊力")
      print("3.升級玄鐵劍,消耗800靈石,獲得100攻擊力")
      weapon_choice = input("請輸入升級選項")

      if weapon_choice == "1":
        if player["spirit_stone"] >= 100:
            player["spirit_stone"] -= 100
            player["weapon"] = "鐵劍"
            player["weapon_ATK"] = 25
            print("升級成功,以升級成鐵劍")
        else:
          print("靈石不足,無法升級")
      elif weapon_choice == "2":
        if player["spirit_stone"] >= 300:
            player["spirit_stone"] -= 300
            player["weapon"] = "精鋼劍"
            player["weapon_ATK"] = 50
            print("升級成功,已升級為精鋼劍")
        else:
          print("靈石不足,無法升級")
      elif weapon_choice == "3":
        if player["spirit_stone"] >= 800:
            player["spirit_stone"] -= 800
            player["weapon"] = "玄鐵劍"
            player["weapon_ATK"] = 100
            print("升級成功,已升級為玄鐵劍")
        else:
          print("靈石不足,無法升級")
      else:
        print("輸入錯誤")

    elif shop_choice == "4":
      print("1.升級銅衣,消耗100靈石,獲得10防禦力")
      print("2.升級鐵衣,消耗300靈石,獲得20防禦力")
      print("3.升級金蟬衣,消耗800靈石,獲得30防禦力")
      armor_choice = input("請輸入升級選項")

      if armor_choice == "1":
        if player["spirit_stone"] >= 100:
            player["spirit_stone"] -= 100
            player["armor"] = "銅衣"
            player["armor_DEF"] = 10
            print("升級成功,已升級成銅衣")
        else:
          print("靈石不足,無法升級")
      elif armor_choice == "2":
        if player["spirit_stone"] >= 300:
            player["spirit_stone"] -= 300
            player["armor"] = "鐵衣"
            player["armor_DEF"] = 20
            print("升級成功.已升級為鐵衣")
        else:
          print("靈石不足,無法升級")
      elif armor_choice == "3":
        if player["spirit_stone"] >= 800:
            player["spirit_stone"] -= 800
            player["armor"] = "金蟬衣"
            player["armor_DEF"] = 30
            print("升級成功,已升級為金蟬衣")
        else:
          print("靈石不足,無法升級")
      else:
        print("輸入錯誤")

    elif shop_choice == "5":

      print("1.升級土刺術,消耗100靈石,獲得50技能傷害")
      print("2.升級冰箭術,消耗300靈石,獲得80技能傷害")
      print("3.升級雷擊術,消耗800靈石,獲得100技能傷害")

      skill_choice = input("請輸入升級選項")

      if skill_choice == "1":
        if player["spirit_stone"] >= 100:
          player["spirit_stone"] -= 100
          player["skill"] = "土刺術"
          player["skill_power"] = 50
          print("升級成功,已升級為土刺術")
        else:
          print("靈石不足,無法升級")
        
      elif skill_choice == "2":
        if player["spirit_stone"] >= 300:
          player["spirit_stone"] -= 300
          player["skill"] = "冰箭術"
          player["skill_power"] = 80
          print("升級成功,已升級為冰箭術")
        else:
          print("靈石不足,無法升級")
      
      elif skill_choice == "3":
        if player["spirit_stone"] >= 800:
          player["spirit_stone"] -= 800
          player["skill"] = "雷擊術"
          player["skill_power"] = 100
          print("升級成功,已升級為雷擊術")
        else:
          print("靈石不足,無法升級")
      else:
        print("輸入錯誤")

    elif shop_choice == "6":
      print("離開商店")
      break
    
    else:
      print("輸入錯誤")

    show_player_info(player)

def boss_fight():   #7.世界BOSS
  player = get_player()
  if player == None:
    return

  boss_name = "練氣妖狼"
  boss_hp = 100
  boss_damage = 40

  print("遭遇世界BOSS", boss_name)

  while boss_hp > 0 and player["hp"] > 0:
    print("BOSS血量:", boss_hp)
    print("玩家血量:", player["hp"])
    print("1.攻擊")
    print("2.技能")
    print("3.使用丹藥")
    print("4.逃跑")
    round_choice = input("請輸入行動")

    if round_choice == "1":
      damage_ATK = player["level"] * 10 + player["weapon_ATK"]
      boss_hp -= damage_ATK
      if boss_hp > 0:
        print("你對世界BOSS造成:", damage_ATK, "點傷害")
        print("世界BOSS剩餘血量:", boss_hp)

      if boss_hp <= 0:
        boss_hp = 0
        print("你擊敗了世界BOSS:",boss_name)
        boss_reward(player)
        show_player_info(player)
        break

      damage = calc_damage_taken(player, boss_damage)
      player["hp"] -= damage
      print("世界BOSS反擊,你損失了:",damage,"點血量")

      if player["hp"] <= 0:
        player["hp"] = 0
        print("戰鬥失敗")
        break

    elif round_choice == "2":
      if player["mp"] >= 20:
        player["mp"] -=20
        damage_skill_power = (player["level"] * 10 + player["weapon_ATK"] + player["skill_power"])
        boss_hp -= damage_skill_power
        print("釋放",player["skill"])
        print("消耗20魔力")
        print("剩餘魔力:", player["mp"])
      else:
        print("魔力不足")
        continue
      
      if boss_hp > 0:
        print("你對世界BOSS造成:", damage_skill_power, "點傷害")
        print("世界BOSS剩餘血量:", boss_hp)

      if boss_hp <= 0:
        boss_hp = 0
        print("你擊敗了世界BOSS:",boss_name)
        boss_reward(player)
        show_player_info(player)
        break

      damage = calc_damage_taken(player, boss_damage)
      player["hp"] -= damage
      print("世界BOSS反擊,你損失了:",damage,"點血量")

      if player["hp"] <= 0:
        player["hp"] = 0
        print("戰鬥失敗")
        break

    elif round_choice == "3":
      if player["pill"] >= 1:
        player["pill"] -= 1
        player["hp"] += 50
        if player["hp"] > 100:
          player["hp"] = 100
        print("丹藥使用成功,丹藥-1")
        print("目前丹藥:", player["pill"])
        print("當前玩家血量:", player["hp"])

      else:
        print("丹藥不足,使用失敗")

      damage = calc_damage_taken(player, boss_damage)
      player["hp"] -= damage
      print("世界BOSS反擊,你損失了:",damage,"點血量")

      if player["hp"] <= 0:
        player["hp"] = 0
        print("戰鬥失敗")
        break

    elif round_choice == "4":
      print("逃跑成功")
      break
    
    else:
      print("輸入錯誤")

def save_game():   #儲存
  if not players:
    print("目前沒有角色資料")
    return
  else:
    if players:
      df = pd.DataFrame(players)
      df.to_csv("gamers.csv", index=False, encoding="utf-8")
      print("儲存成功")
    else:
      print("儲存失敗")

def load_game():    #讀取
  global players

  try:
    df = pd.read_csv("gamers.csv", encoding="utf-8")
    df["level"] = df["level"].astype(int)
    players = df.to_dict(orient="records")
    print("讀取成功")
  except FileNotFoundError:
    print("gamers.csv 檔案不存在")
  except Exception as e:
    print("讀取失敗", e)


while True:
  print("0.創建角色")
  print("1.修練")
  print("2.打坐")
  print("3.背包")
  print("4.探索秘境")
  print("5.煉丹")
  print("6.使用丹藥")
  print("7.查看狀態")
  print("8.商店")
  print("9.世界BOSS")
  print("10.儲存")
  print("11.讀取")
  print("12.離開")

  choice = input("請選擇行動")

  if choice == "0":   #創建角色
    create()

  elif choice == "1":   #修練
    cultivate()

  elif choice == "2":   #打坐
    meditate()

  elif choice == "3":   #背包
    show_bag()

  elif choice == "4":   #探索秘境
    explore()

  elif choice == "5":   #煉丹
    alchemy()

  elif choice == "6":   #使用丹藥
    use_pill()
  
  elif choice == "7":   #查看狀態
    show_status()

  elif choice == "8":   #商店
    shop()

  elif choice == "9":   #世界BOSS
    boss_fight()

  elif choice == "10":   #儲存
    save_game()

  elif choice == "11":   #讀取
    load_game()

  elif choice == "12":   #離開
    break

  else:
    print("輸入錯誤,請重新輸入選擇")