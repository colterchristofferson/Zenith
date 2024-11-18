import random
import time

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

    def print_status(self):
        print(f"\nTurn {self.turn}:")
        print(f"Population: {self.population}")
        print(f"Morale: {self.morale}")
        print(f"Resources: {self.resources}")
        print(f"Water: {self.water}%")
        print(f"Food: {self.food}%")
        if self.alien_deal_active:
            print("Alien Deal: -10 resources per turn (active)")
        print()

    def check_game_over(self):
        if self.population <= 0:
            print("Game Over: The colony's population has reached zero.")
            return True
        elif self.morale <= 0:
            print("Game Over: Morale has dropped to zero, and the colony has collapsed.")
            return True
        return False

    def handle_consequence(self, action, success):
        if action == "negotiate" and not success:
            print("Negotiation failed. The aliens refused to provide water and captured the negotiators.")
            self.population -= 2
            self.morale -= 3
            self.water -= 10
            print("\n-2 Population, -3 Morale, -10% Water")

        elif action == "explore" and not success:
            print("Exploration failed. The team encountered harsh conditions and returned empty-handed.")
            self.population -= 1
            self.morale -= 2
            print("\n-1 Population, -2 Morale")

        elif action == "farm" and not success:
            print("Farm construction failed. The colony lacks sufficient resources to complete the project.")
            self.morale -= 5
            self.resources -= 10
            print("\n-5 Morale, -10 Resources")

        elif action == "recycle" and not success:
            print("Water recycling research failed. Technical setbacks have delayed progress.")
            self.morale -= 4
            print("\n-4 Morale")

    def handle_water_crisis(self):
        if self.water < 50:
            print("Water Crisis: The colony's water supply is dangerously low!")
            print("What will you do?")
            print("1. Explore for a Water Source (Takes 1 turn)")
            print("2. Negotiate with Aliens for Water (Takes 1 turn)")
            print("3. Research Water Recycling Technology (Takes 2 turns)")

            choice = input("Choose an option (1/2/3): ")

            if choice == '1':  # Explore for water
                print("Exploring for water...")
                self.water_action = "explore"

            elif choice == '2':  # Negotiate with Aliens
                print("Negotiating with aliens for water...")
                self.water_action = "negotiate"

            elif choice == '3':  # Research water recycling
                print("Innovating water recycling technology...")
                self.water_action = "recycle"

            else:
                print("Invalid choice!")

            print()

    def handle_food_crisis(self):
        if self.food <= 20:
            print("Food Crisis: The colony's food supply is critically low!")
            print("What will you do?")
            print("1. Build a Farm (Takes 2 turns)")
            print("2. Ration Food (Takes 1 turn)")
            print("3. Do Nothing and Let the Colony Suffer")

            choice = input("Choose an option (1/2/3): ")

            if choice == '1':  # Build a farm
                print("Building a farm...")
                self.food_action = "farm"

            elif choice == '2':  # Ration food
                print("Starting food rationing...")
                self.food += 5
                self.morale -= 2
                self.food_action = "rationing"

            elif choice == '3':  # Do nothing
                print("Doing nothing... The colony suffers.")
                self.food -= 10
                self.morale -= 5
                self.food_action = "do_nothing"

            else:
                print("Invalid choice!")

            print()

    def next_turn(self):
        # Decrease food and resources daily
        self.food -= 5
        if self.food < 0:
            self.food = 0

        # Deduct resources for active alien deal
        if self.alien_deal_active:
            self.resources -= 10
            print("-10 Resources due to alien deal.")
            if self.resources < 0:
                self.resources = 0

        self.resources += 20
        if self.resources > 100:
            self.resources = 100

        # Process water actions
        if self.water_action == "explore":
            exploration_success = random.choice([True, False])
            if exploration_success:
                print("Exploration successful! Water levels have increased.")
                self.water += 10
            else:
                self.handle_consequence("explore", False)
            self.water_action = None

        elif self.water_action == "negotiate":
            negotiation_success = random.choice([True, False])
            if negotiation_success:
                print("Success! The aliens have agreed to provide water to the colony.")
                self.water = 100
                self.alien_deal_active = True  # Activate the deal
            else:
                self.handle_consequence("negotiate", False)
            self.water_action = None

        elif self.water_action == "recycle":
            research_success = random.choice([True, False])
            if research_success:
                self.water_recycling_turns = 2
            else:
                self.handle_consequence("recycle", False)

        # Process food actions
        if self.food_action == "farm":
            farm_success = random.choice([True, False])
            if farm_success:
                self.farm_turns = 2
            else:
                self.handle_consequence("farm", False)

        elif self.food_action == "rationing":
            print("Food rationing complete. Food supply stabilized.")
            self.food += 5
            self.morale -= 2

        elif self.food_action == "do_nothing":
            print("The colony suffers due to food shortages.")
            self.food -= 10
            self.morale -= 5

        self.food_action = None

        # Handle ongoing actions
        if self.water_recycling_turns > 0:
            self.water_recycling_turns -= 1
            if self.water_recycling_turns == 0:
                print("Water Recycling Technology complete! The colony now has infinite water.")
                self.water = 100

        if self.farm_turns > 0:
            self.farm_turns -= 1
            if self.farm_turns == 0:
                print("Farm complete! The colony now has a sustainable food source.")
                self.food = 50

        # Adjust population and check for game over
        if self.morale > 80:
            self.population += 1
        if self.morale < 3:
            self.population -= 1
        elif self.morale == 0:
            self.population -= 2

        if self.check_game_over():
            return False
        return True

    def start_game(self):
        print("Welcome to Zenith!")
        print("You are the leader of a Martian colony, and your survival is at stake.")
        while True:
            print("\n>>> Starting the next turn... <<<")
            self.print_status()

            if self.water < 50:
                self.handle_water_crisis()

            if self.food <= 20:
                self.handle_food_crisis()

            if not self.next_turn():
                break

            time.sleep(1)

game = ZenithGame()
game.start_game()
