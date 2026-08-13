# Systems/Level_system.py

class LevelSystem:
    BREAKTHROUGH_PILLS = {
        "練氣期第9層": ("foundation_pill", "築基丹", "築基期第1層"),
        "築基期第9層": ("golden_core_pill", "結金丹", "金丹期第1層"),
        "金丹期第9層": ("nascent_soul_pill", "結嬰丹", "元嬰期第1層"),
        "元嬰期第9層": ("spirit_transformation_pill", "化神丹", "化神期第1層"),
        "化神期第9層": ("void_refinement_pill", "煉虛丹", "煉虛期第1層"),
        "練虛期第9層": ("body_integration_pill", "合體丹", "合體期第1層"),
        "合體期第9層": ("tribulation_pill", "渡劫丹", "渡劫期第1層"),
        "渡劫期第9層": ("mahayana_pill", "大乘丹", "大乘期第1層"),
    }

    def __init__(self):
        # 1. 動態建立所有修仙境界階梯
        self.realms = []
        
        # 初始起點
        self.realms.append({"name": "凡人境界", "max_cultivation": 100})
        
        # 九大境界；每個大境界均包含一至九層。
        major_realms = [
            {"name": "練氣", "base_exp": 120, "growth": 30},
            {"name": "築基", "base_exp": 1000, "growth": 200},
            {"name": "金丹", "base_exp": 5000, "growth": 1000},
            {"name": "元嬰", "base_exp": 20000, "growth": 4000},
            {"name": "化神", "base_exp": 80000, "growth": 16000},
            {"name": "練虛", "base_exp": 300000, "growth": 60000},
            {"name": "合體", "base_exp": 1000000, "growth": 200000},
            {"name": "渡劫", "base_exp": 3000000, "growth": 600000},
            {"name": "大乘", "base_exp": 10000000, "growth": 2000000},
        ]
        
        # 利用雙重迴圈，自動生成 1 到 9 層的境界資料
        for major in major_realms:
            for layer in range(1, 10): # 1 到 9 层
                realm_name = f"{major['name']}期第{layer}層"
                # 隨著層級提高，需要的修為（靈氣）越來越多
                max_cult = major["base_exp"] + (layer - 1) * major["growth"]
                self.realms.append({"name": realm_name, "max_cultivation": max_cult})
                
    def get_max_cultivation(self, current_realm):
        """根據當前境界名稱，取得升級所需的修為上限"""
        realm_index = self._get_realm_index(current_realm)
        if realm_index is None:
            return 0
        return self.realms[realm_index]["max_cultivation"]

    def _get_realm_index(self, current_realm):
        for index, realm_data in enumerate(self.realms):
            if realm_data["name"] == current_realm:
                return index
        return None

    def add_cultivation(self, current_realm, current_cultivation, amount):
        """Add cultivation and handle realm advancement safely."""
        if amount <= 0:
            message = "\u4fee\u70ba\u6c92\u6709\u8b8a\u5316\u3002"
            return current_realm, current_cultivation, message

        realm_index = self._get_realm_index(current_realm)
        if realm_index is None:
            message = "境界資料異常，修為沒有變化。"
            return current_realm, current_cultivation, message

        current_cultivation += amount
        (
            current_realm,
            current_cultivation,
            outcome,
            levels_gained,
        ) = self._advance_realms(realm_index, current_cultivation)

        if outcome == "major_bottleneck":
            pill_name = self.BREAKTHROUGH_PILLS[current_realm][1]
            log_message = f"已達九層圓滿，需服用{pill_name}方可破境。"
        elif outcome == "maximum":
            log_message = "你已達目前天道開放的最高修為！"
        elif levels_gained > 1:
            log_message = (
                f"連續突破 {levels_gained} 層至【{current_realm}】！"
            )
        elif levels_gained == 1:
            log_message = f"成功突破至【{current_realm}】！"
        else:
            log_message = f"修為增加 {amount} 點。"

        return current_realm, current_cultivation, log_message

    def _advance_realms(self, realm_index, current_cultivation):
        levels_gained = 0
        outcome = "gained"

        while True:
            realm_data = self.realms[realm_index]
            current_realm = realm_data["name"]
            max_val = realm_data["max_cultivation"]

            if current_cultivation < max_val:
                break

            if realm_index >= len(self.realms) - 1:
                current_cultivation = max_val
                outcome = "maximum"
                break

            next_realm_name = self.realms[realm_index + 1]["name"]

            requirement = self.BREAKTHROUGH_PILLS.get(current_realm)
            if requirement and next_realm_name == requirement[2]:
                current_cultivation = max_val
                outcome = "major_bottleneck"
                break

            current_cultivation -= max_val
            realm_index += 1
            levels_gained += 1
            outcome = "advanced"

        current_realm = self.realms[realm_index]["name"]
        return current_realm, current_cultivation, outcome, levels_gained

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

        # 2. 尋找當前境界在天梯清單中的索引位置
        realm_index = self._get_realm_index(current_realm)
        if realm_index is None:
            log_message = "【修煉失敗】境界資料異常，修為沒有變化。"
            return current_realm, current_cultivation, log_message

        current_cultivation += final_gain

        (
            current_realm,
            current_cultivation,
            outcome,
            levels_gained,
        ) = self._advance_realms(realm_index, current_cultivation)

        if outcome == "major_bottleneck":
            pill_name = self.BREAKTHROUGH_PILLS[current_realm][1]
            log_message = (
                f"💥【天道屏障】你已達{current_realm}大圓滿！"
                f"需尋得「{pill_name}」方可破境！"
            )
        elif outcome == "maximum":
            log_message = "【功德圓滿】你已達目前天道開放的最高修為！"
        elif levels_gained > 1:
            log_message = (
                f"🎉【連續突破】一舉突破 {levels_gained} 層，"
                f"目前境界為【{current_realm}】！"
            )
        elif levels_gained == 1:
            log_message = (
                f"🎉【破境升仙】恭喜道友！成功突破至【{current_realm}】！"
            )
        else:
            log_message = (
                "【天道酬勤】你運轉功法，吸收天地靈氣，"
                f"修為增加 {final_gain} 點。"
            )

        return current_realm, current_cultivation, log_message

    def attempt_major_breakthrough(self, player, item_system):
        requirement = self.BREAKTHROUGH_PILLS.get(player.realm)
        if requirement is None:
            return False, False, ""

        max_cultivation = self.get_max_cultivation(player.realm)
        if player.cultivation < max_cultivation:
            return False, False, ""

        item_id, pill_name, next_realm = requirement
        if item_system is None:
            return True, False, "【突破失敗】背包系統尚未連接。"
        if item_system.get_item_count(item_id) <= 0:
            return True, False, f"【突破失敗】缺少{pill_name}。"
        if not item_system.remove_item(item_id, 1):
            return True, False, "【突破失敗】丹藥消耗失敗。"

        player.realm = next_realm
        player.realm_index = player._get_realm_index(next_realm)
        player.cultivation = 0
        player.inventory = item_system.get_save_data()
        return True, True, f"【突破成功】服下{pill_name}，晉升{next_realm}！"
