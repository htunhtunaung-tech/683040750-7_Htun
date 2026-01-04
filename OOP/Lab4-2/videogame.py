from datetime import datetime

class VideoGame:
    
    # Class Attributes
    total_players = 0
    difficulty_levels = ["Easy", "Medium", "Hard"]
    max_level = 100
    server_start_time = datetime.now()
    active_players = []
    leaderboard = {}  # {player_name: score}

    # Constructor
    def __init__(self, player_name, character_type):
        if not VideoGame.is_valid_character_name(player_name):
            raise ValueError("Invalid character name.")

        self.player_name = player_name
        self.character_type = character_type
        self.level = 1
        self.health = 100
        self.exp = 0
        self.coins = 0
        self.inventory = []
        self.is_alive = True

        # Update class attributes
        VideoGame.total_players += 1
        VideoGame.active_players.append(player_name)
        VideoGame.leaderboard[player_name] = 0

    # Instance Methods
    def level_up(self):
        if self.level < VideoGame.max_level:
            self.level += 1
            self.health = 100
            VideoGame.leaderboard[self.player_name] = self.level * 100 + self.coins

        print(f"[LEVEL UP] {self.player_name} | Level: {self.level} | "
              f"Health: {self.health} | Score: {VideoGame.leaderboard[self.player_name]}")

    def collect_coins(self, amount):
        self.coins += amount
        VideoGame.leaderboard[self.player_name] = self.level * 100 + self.coins

        print(f"[COINS] {self.player_name} | Coins: {self.coins} | "
              f"Score: {VideoGame.leaderboard[self.player_name]}")

    def take_damage(self, damage):
        self.health -= damage

        if self.health <= 0:
            self.is_alive = False
            self.health = 0
            if self.player_name in VideoGame.active_players:
                VideoGame.active_players.remove(self.player_name)
            print(f"[DEAD] {self.player_name} has died.")
        else:
            print(f"[DAMAGE] {self.player_name} | Health: {self.health}")

    def fight_monster(self, monster_name, monster_level):
        if not self.is_alive:
            print(f"{self.player_name} cannot fight. Character is dead.")
            return

        print(f"\n[FIGHT] {self.player_name} vs {monster_name} (Lv {monster_level})")

        damage = VideoGame.calculate_damage(
            attack_power=10,
            defense=5,
            level=monster_level
        )
        self.take_damage(damage)

        if self.is_alive:
            gained_exp = 10 * monster_level
            self.exp += gained_exp
            self.collect_coins(3 * monster_level)

            print(f"[EXP] Gained {gained_exp} EXP (Total: {self.exp})")

            if self.exp >= VideoGame.calculate_exp_needed(self.level):
                self.exp = 0
                self.level_up()

    def get_stats(self):
        return (
            f"Player: {self.player_name}\n"
            f"Type: {self.character_type}\n"
            f"Level: {self.level}\n"
            f"Health: {self.health}\n"
            f"EXP: {self.exp}\n"
            f"Coins: {self.coins}\n"
            f"Alive: {self.is_alive}\n"
            f"Rank: {VideoGame.get_rank_title(self.level)}"
        )

    # Class Methods
    @classmethod
    def create_party(cls, player_names, character_type):
        party = []
        for name in player_names:
            party.append(cls(name, character_type))
        return party

    @classmethod
    def get_server_stats(cls):
        uptime = datetime.now() - cls.server_start_time
        return (
            f"\n=== SERVER STATS ===\n"
            f"Total Players: {cls.total_players}\n"
            f"Active Players: {cls.active_players}\n"
            f"Leaderboard: {cls.leaderboard}\n"
            f"Server Uptime: {uptime}\n"
        )

    @classmethod
    def get_leaderboard(cls):
        sorted_board = sorted(cls.leaderboard.items(),
                               key=lambda x: x[1],
                               reverse=True)

        result = "\n=== LEADERBOARD ===\n"
        for i, (player, score) in enumerate(sorted_board, start=1):
            result += f"{i}. {player} - {score}\n"
        return result

    @classmethod
    def reset_server(cls):
        cls.total_players = 0
        cls.active_players = []
        cls.leaderboard = {}
        cls.server_start_time = datetime.now()

    # Static Methods
    @staticmethod
    def calculate_damage(attack_power, defense, level):
        damage = (attack_power * level) - defense
        return max(0, damage)

    @staticmethod
    def calculate_exp_needed(level):
        return 100 * level

    @staticmethod
    def is_valid_character_name(name):
        return 3 <= len(name) <= 20 and name.isalnum()

    @staticmethod
    def get_rank_title(level):
        if level < 20:
            return "Beginner"
        elif level < 40:
            return "Warrior"
        elif level < 60:
            return "Elite"
        elif level < 80:
            return "Master"
        else:
            return "Legend"
