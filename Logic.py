import random

class ZenithGame:
    def __init__(self):
        # Initialize game state
        self.population = 10
        self.morale = 10
        self.resources = 0
        self.water = 40  # Water starts at 40%
        self.food = 30  # Food starts at 30%
        self.turn = 1

        # Actions that take multiple turns (initialized to 0 turns left)
        self.water_recycling_turns = 0
        self.farm_turns = 0

        # Track decisions made in the current turn
        self.water_action = None
        self.food_action = None

        # Track alien negotiation effects
        self.alien_deal_active = False

    def next_turn(self):
        # Game logic for progressing to the next turn
        self.food -= 5
        self.resources += 20

        if self.water_action == "explore":
            self.handle_explore()

        if self.food_action == "farm":
            self.handle_farm()

        # Update ongoing actions
        self.update_ongoing_actions()

        return not self.check_game_over()

    def handle_explore(self):
        # Exploration logic
        exploration_success = random.choice([True, False])
        if exploration_success:
            self.water += 10
        else:
            self.morale -= 2

    def handle_farm(self):
        # Farming logic
        farm_success = random.choice([True, False])
        if farm_success:
            self.food += 10
        else:
            self.morale -= 5

    def update_ongoing_actions(self):
        # Update multi-turn actions
        if self.water_recycling_turns > 0:
            self.water_recycling_turns -= 1
            if self.water_recycling_turns == 0:
                self.water = 100

        if self.farm_turns > 0:
            self.farm_turns -= 1
            if self.farm_turns == 0:
                self.food = 50

    def check_game_over(self):
        if self.population <= 0 or self.morale <= 0:
            return True
        return False
