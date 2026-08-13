#主畫面
class BaseScene:

    def enter(self):
        """進入場景"""
        pass

    def exit(self):
        """離開場景"""
        pass

    def handle_event(self, event):
        """事件"""
        return None

    def update(self):
        """更新"""
        pass

    def draw(self, screen):
        """畫面"""
        pass