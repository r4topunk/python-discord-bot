summary = """\
=== Status ===
Name: {player_name}
Health: {player_health}
Level: {player_level}
Silver: {player_silver}
Monsters Defeated: {player_monster_defeated}
"""

class Player():
    def __init__(self, discord_id, name) -> None:
        self.discord_id = discord_id
        self.name = name
        self.experience = 0
        self.level = 1
        self.silver = 0
        self.health = 250
        self.max_health = 250
        self.power = 5
        self.monsters_defeated = 0

    def attack(self, target):
        target.defend(self.get_level() * self.power)

    def defend(self, damage):
        self.health -= damage

    def get_level(self):
        return self.level

    def exp_up(self, qtd):
        self.experience += qtd
        if self.experience % 100 == 0:
            self.level_up()

    def level_up(self):
        self.level += 1
        print(f"Player {self.name} level up to {self.level}!")

    def earn_silver(self, qtd):
        self.silver += qtd

    def increase_monsters_defeated(self):
        self.monsters_defeated += 1

    def get_summary(self):
        return summary.format(
                    player_name=self.name,
                    player_health=self.health,
                    player_level=self.level,
                    player_silver=self.silver,
                    player_monster_defeated=self.monsters_defeated,
                )

    def is_alive(self):
        return self.health > 0
    
    def reset(self):
        self.health = self.max_health