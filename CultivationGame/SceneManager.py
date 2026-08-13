# SceneManager.py
class SceneManager:
    """管理目前場景、場景生命週期與畫面轉換。"""

    def __init__(self):
        self.scenes = {}
        self.current = None
        self.current_name = None

    def add_scene(self, name, scene):
        if not name:
            raise ValueError("場景名稱不可為空。")

        self.scenes[name] = scene

    def has_scene(self, name):
        return name in self.scenes

    def get_scene(self, name):
        return self.scenes.get(name)

    def change_scene(self, name):
        if name not in self.scenes:
            raise KeyError(f"尚未註冊場景：{name}")

        if self.current is not None:
            exit_method = getattr(self.current, "exit", None)
            if callable(exit_method):
                exit_method()

        self.current = self.scenes[name]
        self.current_name = name

        enter_method = getattr(self.current, "enter", None)
        if callable(enter_method):
            enter_method()

    def handle_event(self, event):
        if self.current is None:
            return None

        handle_method = getattr(self.current, "handle_event", None)
        if callable(handle_method):
            return handle_method(event)

        return None

    def update(self):
        if self.current is None:
            return

        update_method = getattr(self.current, "update", None)
        if callable(update_method):
            update_method()

    def draw(self, screen):
        if self.current is None:
            return

        draw_method = getattr(self.current, "draw", None)
        if callable(draw_method):
            draw_method(screen)
