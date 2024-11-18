import random
import pygame

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
        # Decrease food and resources daily
        self.food -= 5
        if self.food < 0:
            self.food = 0

        # Deduct resources for active alien deal
        if self.alien_deal_active:
            self.resources -= 10
            if self.resources < 0:
                self.resources = 0

        self.resources += 20
        if self.resources > 100:
            self.resources = 100

        # Process water actions
        if self.water_action == "explore":
            self.handle_explore()

        elif self.water_action == "negotiate":
            self.handle_negotiate()

        elif self.water_action == "recycle":
            self.handle_recycle()

        # Process food actions
        if self.food_action == "farm":
            self.handle_farm()

        elif self.food_action == "rationing":
            self.handle_rationing()

        elif self.food_action == "do_nothing":
            self.handle_do_nothing()

        # Update ongoing actions
        self.update_ongoing_actions()

        # Check if the game is over
        return not self.check_game_over()

    def handle_explore(self):
        """Handle the outcome of exploring for water."""
        exploration_success = random.choice([True, False])
        if exploration_success:
            self.water += 10
        else:
            self.morale -= 2

    def handle_negotiate(self):
        """Handle the outcome of negotiating with aliens for water."""
        negotiation_success = random.choice([True, False])
        if negotiation_success:
            self.water = 100
            self.alien_deal_active = True  # Activate the alien deal
        else:
            self.morale -= 3
            self.population -= 2
            self.water -= 10

    def handle_recycle(self):
        """Handle the outcome of researching water recycling."""
        research_success = random.choice([True, False])
        if research_success:
            self.water_recycling_turns = 2  # Start water recycling project
        else:
            self.morale -= 4

    def handle_farm(self):
        """Handle the outcome of building a farm."""
        farm_success = random.choice([True, False])
        if farm_success:
            self.farm_turns = 2  # Start farm construction
        else:
            self.morale -= 5
            self.resources -= 10

    def handle_rationing(self):
        """Handle food rationing."""
        self.food += 5
        self.morale -= 2

    def handle_do_nothing(self):
        """Handle doing nothing during a food crisis."""
        self.food -= 10
        self.morale -= 5

    def update_ongoing_actions(self):
        """Handle actions that take multiple turns."""
        if self.water_recycling_turns > 0:
            self.water_recycling_turns -= 1
            if self.water_recycling_turns == 0:
                self.water = 100  # Infinite water due to recycling

        if self.farm_turns > 0:
            self.farm_turns -= 1
            if self.farm_turns == 0:
                self.food = 50  # Sustainable food source from farm

    def check_game_over(self):
        """Check if the game is over."""
        if self.population <= 0:
            print("Game Over: The colony's population has reached zero.")
            return True
        elif self.morale <= 0:
            print("Game Over: Morale has dropped to zero, and the colony has collapsed.")
            return True
        return False

    def draw_status(self, screen):
        """Draw the current game status on the screen."""
        font = pygame.font.Font(None, 36)  # Default font, size 36
        white = (255, 255, 255)

        # Create text surfaces for each status
        population_text = font.render(f"Population: {self.population}", True, white)
        morale_text = font.render(f"Morale: {self.morale}", True, white)
        resources_text = font.render(f"Resources: {self.resources}", True, white)
        water_text = font.render(f"Water: {self.water}%", True, white)
        food_text = font.render(f"Food: {self.food}%", True, white)
        turn_text = font.render(f"Turn: {self.turn}", True, white)

        # Draw text on the screen at specific positions
        screen.blit(population_text, (20, 20))
        screen.blit(morale_text, (20, 60))
        screen.blit(resources_text, (20, 100))
        screen.blit(water_text, (20, 140))
        screen.blit(food_text, (20, 180))
        screen.blit(turn_text, (20, 220))

    def start_game(self):
        """Start the game loop."""
        print("Welcome to Zenith!")
        print("You are the leader of a Martian colony, and your survival is at stake.")
        while True:
            print(f"\n>>> Starting the next turn... <<<")
            self.print_status()

            if self.water < 50:
                self.handle_water_crisis()

            if self.food <= 20:
                self.handle_food_crisis()

            if not self.next_turn():
                break

    def handle_water_crisis(self):
        """Handle a water crisis if water is low."""
        if self.water < 50:
            print("Water Crisis: The colony's water supply is dangerously low!")
            print("What will you do?")
            print("1. Explore for a Water Source (Takes 1 turn)")
            print("2. Negotiate with Aliens for Water (Takes 1 turn)")
            print("3. Research Water Recycling Technology (Takes 2 turns)")

            choice = input("Choose an option (1/2/3): ")

            if choice == '1':  # Explore for water
                self.water_action = "explore"
            elif choice == '2':  # Negotiate with Aliens
                self.water_action = "negotiate"
            elif choice == '3':  # Research water recycling
                self.water_action = "recycle"
            else:
                print("Invalid choice!")

    def handle_food_crisis(self):
        """Handle a food crisis if food is critically low."""
        if self.food <= 20:
            print("Food Crisis: The colony's food supply is critically low!")
            print("What will you do?")
            print("1. Build a Farm (Takes 2 turns)")
            print("2. Ration Food (Takes 1 turn)")
            print("3. Do Nothing and Let the Colony Suffer")

            choice = input("Choose an option (1/2/3): ")

            if choice == '1':  # Build a farm
                self.food_action = "farm"
            elif choice == '2':  # Ration food
                self.food_action = "rationing"
            elif choice == '3':  # Do nothing
                self.food_action = "do_nothing"
            else:
                print("Invalid choice!")

    def print_status(self):
        """Print the current game status to the console."""
        print(f"\nTurn {self.turn}:")
        print(f"Population: {self.population}")
        print(f"Morale: {self.morale}")
        print(f"Resources: {self.resources}")
        print(f"Water: {self.water}%")
        print(f"Food: {self.food}%")
        if self.alien_deal_active:
            print("Alien Deal: -10 resources per turn (active)")
        print()
