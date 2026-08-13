class Boss:
    def __init__(self, name="練氣妖狼", hp=100, attack=40, reward=None):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.reward = dict(reward or {})

    @property
    def is_dead(self):
        return self.hp <= 0
