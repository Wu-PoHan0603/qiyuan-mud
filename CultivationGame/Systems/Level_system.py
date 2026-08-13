# Systems/Level_system.py

class LevelSystem:
    def __init__(self):
        # 1. 動態建立所有修仙境界階梯
        self.realms = []
        
        # 初始起點
        self.realms.append({"name": "凡人境界", "max_cultivation": 100})
        
        # 定義大境界與其每層所需的基礎修為
        # 練氣期每升一層，上限增加；築基期則需要更多靈氣
        major_realms = [
            {"name": "練氣", "base_exp": 120, "growth": 30},  # 一層 120, 二層 150... 九層 360
            {"name": "築基", "base_exp": 1000, "growth": 200}, # 一層 1000, 二層 1200...
            {"name": "金丹", "base_exp": 5000, "growth": 1000}
        ]
        
        # 利用雙重迴圈，自動生成 1 到 9 層的境界資料
        for major in major_realms:
            for layer in range(1, 10): # 1 到 9 层
                realm_name = f"{major['name']}期第{layer}層"
                # 隨著層級提高，需要的修為（靈氣）越來越多
                max_cult = major["base_exp"] + (layer - 1) * major["growth"]
                self.realms.append({"name": realm_name, "max_cultivation": max_cult})
                
        # 頂點設定（九層之後的最高境界預留）
        self.realms.append({"name": "元嬰大能", "max_cultivation": 999999})

    def get_max_cultivation(self, current_realm):
        """根據當前境界名稱，取得升級所需的修為上限"""
        for r in self.realms:
            if r["name"] == current_realm:
                return r["max_cultivation"]
        return 100  # 預設防錯

    def train(self, current_realm, current_cultivation, spiritual_root):
        """
        核心方法：計算閉關修煉後的數值變更與突破 (支援九層階梯)
        """
        # 1. 根據創角畫面的五行靈根，賦予不同的修煉特性
        base_gain = 10
        if spiritual_root == "木":
            final_gain = int(base_gain * 1.5)  # 木靈根修煉速度 +50%
        elif spiritual_root == "火":
            final_gain = int(base_gain * 1.2)  # 火靈根修煉速度 +20%
        else:
            final_gain = base_gain             # 金、水、土為正常速度

        current_cultivation += final_gain
        
        # 2. 尋找當前境界在天梯清單中的索引位置
        realm_index = 0
        for i, r in enumerate(self.realms):
            if r["name"] == current_realm:
                realm_index = i
                break
                
        max_val = self.realms[realm_index]["max_cultivation"]
        log_message = f"【天道酬勤】你運轉功法，吸收天地靈氣，修為增加 {final_gain} 點。"

        # 3. 處理突破與卡大境界瓶頸邏輯
        if current_cultivation >= max_val:
            # 如果還有下一個境界可以突破
            if realm_index < len(self.realms) - 1:
                next_realm_name = self.realms[realm_index + 1]["name"]
                
                # 🌟 特殊大境界瓶頸：從練氣期第9層要突破到築基期第1層時卡住
                if "練氣期第9層" in current_realm and "築基期" in next_realm_name:
                    current_cultivation = max_val  # 修為卡在滿值瓶頸
                    log_message = "💥【天道屏障】你已達練氣期九層大圓滿！前方築基屏障堅不可摧，需尋得「築基丹」方可破境！"
                
                # 🌟 特殊大境界瓶頸：從築基期第9層要突破到金丹期第1層時卡住
                elif "築基期第9層" in current_realm and "金丹期" in next_realm_name:
                    current_cultivation = max_val
                    log_message = "⚡【金丹雷劫】你已達築基期九層大圓滿！若要凝結金丹，需做好抗衡九九天劫之準備！"
                
                else:
                    # 一般小層級（例如一層升二層，二層升三層）直接順利突破
                    current_cultivation -= max_val
                    current_realm = next_realm_name
                    log_message = f"🎉【破境升仙】恭喜道友！你福至心靈，成功突破至【{current_realm}】！"
            else:
                # 已達最高境界
                current_cultivation = max_val
                log_message = "【功德圓滿】你已達目前天道開放的最高修為！"

        return current_realm, current_cultivation, log_message
