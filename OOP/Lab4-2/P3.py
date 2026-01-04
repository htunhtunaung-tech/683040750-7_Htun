from videogame import VideoGame

# Create players
player1 = VideoGame("Hero01", "Ninja")
player2 = VideoGame("Mage99", "Wizard")

# Gameplay
player1.collect_coins(50)
player1.fight_monster("Goblin", 3)
player1.fight_monster("Dragon", 10)

# Party creation
party = VideoGame.create_party(["Alpha", "Beta", "Gamma"], "Doctor")

# Stats
print(player1.get_stats())
print(player2.get_stats())

# Leaderboard
print(VideoGame.get_leaderboard())

# Server stats
print(VideoGame.get_server_stats())
