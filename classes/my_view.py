import discord
from discord.ext import tasks, commands
from classes.monster import Monster
from classes.player import Player
from time import sleep

class MyView(discord.ui.View):
    def __init__(self, ctx: commands.Context, player: Player):
        super().__init__(timeout=10)
        self.ctx = ctx
        self.player = player
        self.update_count = 0

    @discord.ui.button(label="Work!", row=0, style=discord.ButtonStyle.primary)
    async def work_button_callback(self, button, interaction):
        self.timeout = None
        button.disabled = True

        self.message = interaction.message
        self.slow_count.start()

        embed = discord.Embed(title="Counter", description=self.update_count)
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="Cancel", row=0, style=discord.ButtonStyle.primary)
    async def cancel_button_callback(self, button, interaction):
        self.slow_count.cancel()
        await interaction.response.send_message("Goodbye")

    @discord.ui.button(label="Start Hunting", row=1, style=discord.ButtonStyle.danger)
    async def start_hunting_button_callback(self, button, interaction):
        self.clear_items()
        self.timeout = None
        await self.fight.start(interaction)
        
    @tasks.loop(hours=1)
    async def fight(self, iteraction: discord.InteractionMessage):
        self.clear_items()
        embed = discord.Embed(title="=== Status ===", description="Starting fight!")
        await iteraction.response.edit_message(embed=embed, view=self)

        monsters = [
            ('Rat', 1),
            ('Boar', 2),
            ('Goblin', 3)
        ]
        player = self.player
        for monster_recipe in monsters:
            while player.get_level() == monster_recipe[1] and player.health > 0:
                monster = Monster(monster_recipe[0], monster_recipe[1])
                while monster.health > 0 and player.health > 0:
                    if player.health > 0:
                        player.attack(monster)
                    else:
                        break
                    if monster.health > 0:
                        monster.attack(player)
                    else:
                        print(f"Player {player.name} defeated a {monster.name}")
                        player.exp_up(10)
                        player.earn_silver(5 * monster.level)
                        player.increase_monsters_defeated()
                    sleep(2)
                embed.description = player.get_summary()
                await iteraction.message.edit(embed=embed)

        if player.is_alive():
            print(f"Player {player.name} won!")
            await self.ctx.message.reply("You won!")
        else:
            print(f"Player {player.name} died!")
            await self.ctx.message.reply("You have died!")
            player.reset()

    async def interaction_check(self, interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("Hey! This message wasn't for you...", ephemeral=True)
            return False
        else:
            return True

    async def on_timeout(self):
        await self.message.delete()
                
    @tasks.loop(seconds=5)
    async def slow_count(self):
        self.update_count += 1
        embed = discord.Embed(title="Counter", description=self.update_count)
        await self.message.edit(embed=embed)