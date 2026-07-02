#登入
import pandas as pd
players = []
jobs = ["warrior","mage","shooter"]

def add_player(name,job,level):
    players.append({
        "name":name,
        "job":job,
        "level":level
  })


while True:
    print("1.新增")
    print("2.顯示")
    print("3.查詢")
    print("4.刪除角色")
    print("5.修改角色等級")
    print("6.儲存")
    print("7.讀取")
    print("8.職業統計")
    print("9.最高等級玩家")
    print("10.離開")

    choice = input("請輸入代碼")
    if choice == "1":     #新增
        while True:
            name = input("請輸入要建立的玩家名稱")
            if " " in name:
                print("不可輸入空白")
            elif len(name) < 3:
                print("不可輸入少於三個字元")
            elif not name.isalpha():
                print("不可輸入英文以外的字元")
            else:
                duplicate = False

                for player in players:
                    if player["name"] == name:
                        duplicate = True
                        break

                if duplicate:
                    print("不可重複輸入")
                else:
                    print("名稱可用")
                    break

        job = input("請輸入職業名稱:warrior,mage,shooter")
        if job not in jobs:
            print("輸入錯誤")
            continue

        while True:
            try:
                level = int(input("請輸入等級"))
                break
            except ValueError:
                print("輸入值錯誤只能輸入數字")
        add_player(name,job,level)

        print("新增成功")

    elif choice == "2":   #顯示
        print(players)

    elif choice == "3":   #查詢
        keyword = input("請輸入查詢玩家名稱")

        found = False

        for player in players:
            if player["name"] == keyword:
                print(player)
                found = True
                break

        if found == False:
            print("查無資料")

    elif choice == "4":   #刪除
        keyword = input("請輸入要刪除的角色名子")

        found = False

        for player in players:
            if player["name"] == keyword:
                players.remove(player)
                print("刪除成功")
                found = True
                break

        if found == False:
            print("查無資料")


    elif choice == "5":   #修改
        keyword = input("請輸入要修改的角色名稱")

        found = False

        for player in players:
            if player["name"] == keyword:
                while True:
                    try:
                        new_level = int(input("請輸入修改後的等級:"))
                        break
                    except ValueError:
                        print("只能輸入數字")

                player["level"] = new_level
                print("修改成功")
                found = True
                break
        if found == False:
            print("查無資料")


    elif choice == "6": #儲存
        if players:
            df = pd.DataFrame(players)
            df.to_csv("players.csv", index=False, encoding="utf-8")
            print("儲存成功")
        else:
            print("沒有玩家資料可儲存")


    elif choice == "7":   #讀取
        try:
            df = pd.read_csv("players.csv", encoding="utf-8")
            df["level"] = df["level"].astype(int)
            players = df.to_dict(orient="records")
            print("讀取成功")
        except FileNotFoundError:
            print("players.csv 檔案不存在")
        except Exception as e:
            print("讀取失敗：", e)

    elif choice == "8":   #職業統計
      if players:
        df = pd.DataFrame(players)
        print(df.groupby("job")["name"].count())
      else:
        print("查無資料")

    elif choice == "9":   #最高等級玩家
      if players:
        df = pd.DataFrame(players)
        print(df[df["level"] == df["level"].max()].to_string(index=False))
        index = False
      else:
        print("查無資料")


    elif choice == "10":
        print("離開")
        break

    else:
        print("輸入錯誤")