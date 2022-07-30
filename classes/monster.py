class Monster:
    def __init__(self, name, level) -> None:
        self.name = name
        self.level = level
        self.max_health = level * 20
        self.health = self.max_health
        self.power = 2

    def attack(self, target):
        target.defend(self.level * self.power)

    def defend(self, damage):
        self.health -= damage