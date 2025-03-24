class GameData:
    def __init__(self):
        # Constants
        self.TAB = 13
        self.CENTER = self.TAB // 2
        
        # Initialize game data
        self.init_blocked_cells()
        self.init_potions()
        self.init_ingredients()
        self.init_recipes()
        self.init_inventory()
    
    def init_blocked_cells(self):
        # Define blocked cells (based on C code)
        self.blocked_cells = [
            (1, 2),
            (1, 6),
            (2, 9),
            (6, 3),
            (7, 4),
            (8, 3),
            (9, 7),
            (9, 8),
            (12, 6)
        ]
    
    def init_potions(self):
        # Define potions (based on C code)
        self.potions = {
            "Dispel": {
                "position": (7, 10),
                "effect": "Removes magical effects",
                "rarity": "Common"
            },
            "Healing": {
                "position": (3, 9),
                "effect": "Restores health",
                "rarity": "Common"
            },
            "Regen": {
                "position": (0, 6),
                "effect": "Regenerates health over time",
                "rarity": "Uncommon"
            },
            "Defense": {
                "position": (2, 1),
                "effect": "Increases physical defense",
                "rarity": "Uncommon"
            },
            "Strength": {
                "position": (6, 2),
                "effect": "Increases physical attack power",
                "rarity": "Uncommon"
            },
            "Haste": {
                "position": (10, 2),
                "effect": "Increases speed",
                "rarity": "Rare"
            },
            "Poison": {
                "position": (10, 7),
                "effect": "Causes damage over time",
                "rarity": "Rare"
            },
            "Acid": {
                "position": (12, 9),
                "effect": "Causes severe damage",
                "rarity": "Very Rare"
            }
        }
    
    def init_ingredients(self):
        # Define ingredients with patterns (based on C code)
        # 0 = Empty, 1 = Path, 2 = Start, 3 = End
        self.ingredients = {
            "Argosia": {
                "pattern": [
                    [0, 2, 0, 0],
                    [1, 1, 0, 0],
                    [1, 1, 0, 0],
                    [0, 3, 0, 0]
                ],
                "rarity": "Common",
                "location": "Forest"
            },
            "Cinderbloom": {
                "pattern": [
                    [1, 0, 0, 0],
                    [1, 1, 0, 0],
                    [2, 0, 3, 0],
                    [0, 0, 0, 0]
                ],
                "rarity": "Common",
                "location": "Volcanic regions"
            },
            "Coronarium": {
                "pattern": [
                    [0, 2, 0, 0],
                    [0, 1, 1, 1],
                    [3, 0, 1, 0],
                    [0, 1, 0, 0]
                ],
                "rarity": "Uncommon",
                "location": "Highlands"
            },
            "Howlbane": {
                "pattern": [
                    [1, 1, 0, 0],
                    [1, 1, 0, 0],
                    [3, 1, 0, 0],
                    [0, 0, 2, 0]
                ],
                "rarity": "Uncommon",
                "location": "Swamps"
            },
            "Miriagreen": {
                "pattern": [
                    [0, 1, 1, 0],
                    [2, 1, 3, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]
                ],
                "rarity": "Uncommon",
                "location": "Plains"
            },
            "Paleroot": {
                "pattern": [
                    [0, 1, 3, 0],
                    [1, 0, 0, 0],
                    [0, 1, 2, 0],
                    [0, 0, 0, 0]
                ],
                "rarity": "Rare",
                "location": "Caves"
            },
            "Sageleaf": {
                "pattern": [
                    [0, 0, 2, 0],
                    [1, 1, 1, 0],
                    [1, 3, 0, 0],
                    [0, 0, 0, 0]
                ],
                "rarity": "Rare",
                "location": "Desert"
            },
            "Thickweed": {
                "pattern": [
                    [3, 1, 1, 2],
                    [0, 0, 0, 1],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]
                ],
                "rarity": "Rare",
                "location": "Ocean shores"
            },
            "Widow's Tear": {
                "pattern": [
                    [0, 3, 0, 0],
                    [0, 1, 0, 0],
                    [1, 0, 0, 0],
                    [2, 0, 0, 0]
                ],
                "rarity": "Very Rare",
                "location": "Dark forests"
            }
        }
    
    def init_recipes(self):
        # Define recipes based on the provided list
        self.recipes = [
            {
                "name": "Simple Healing Draught",
                "potion": "Healing",
                "ingredients": ["Widow's Tear", "Cinderbloom"],
                "difficulty": "Easy"
            },
            {
                "name": "Alternative Healing",
                "potion": "Healing",
                "ingredients": ["Miriagreen", "Widow's Tear"],
                "difficulty": "Easy"
            },
            {
                "name": "Basic Dispel Elixir",
                "potion": "Dispel",
                "ingredients": ["Howlbane", "Cinderbloom"],
                "difficulty": "Easy"
            },
            {
                "name": "Strength Concoction",
                "potion": "Strength",
                "ingredients": ["Paleroot", "Thickweed", "Sageleaf"],
                "difficulty": "Medium"
            },
            {
                "name": "Complex Defense Brew",
                "potion": "Defense",
                "ingredients": ["Miriagreen", "Thickweed", "Howlbane", "Widow's Tear", "Thickweed"],
                "difficulty": "Very Hard"
            },
            {
                "name": "Advanced Defense Potion",
                "potion": "Defense",
                "ingredients": ["Paleroot", "Thickweed", "Sageleaf", "Howlbane", "Widow's Tear"],
                "difficulty": "Very Hard"
            },
            {
                "name": "Triple Regeneration",
                "potion": "Regen",
                "ingredients": ["Paleroot", "Paleroot", "Paleroot"],
                "difficulty": "Medium"
            },
            {
                "name": "Complex Haste Brew",
                "potion": "Haste",
                "ingredients": ["Miriagreen", "Howlbane", "Argosia", "Sageleaf", "Thickweed"],
                "difficulty": "Very Hard"
            },
            {
                "name": "Alternative Haste Elixir",
                "potion": "Haste",
                "ingredients": ["Howlbane", "Howlbane", "Argosia", "Argosia"],
                "difficulty": "Hard"
            },
            {
                "name": "Deadly Poison Brew",
                "potion": "Poison",
                "ingredients": ["Miriagreen", "Howlbane", "Argosia", "Sageleaf", "Cinderbloom"],
                "difficulty": "Very Hard"
            },
            {
                "name": "Corrosive Acid Mixture",
                "potion": "Acid",
                "ingredients": ["Howlbane", "Cinderbloom", "Coronarium", "Argosia"],
                "difficulty": "Hard"
            }
        ]

    def init_inventory(self):
        # Initialize player's inventory
        self.inventory = {
            "Argosia": 5,
            "Cinderbloom": 3,
            "Coronarium": 2,
            "Howlbane": 1,
            "Miriagreen": 2,
            "Paleroot": 0,
            "Sageleaf": 1,
            "Thickweed": 0,
            "Widow's Tear": 0
        }
    
    def get_table(self):
        """
        Creates and returns a 2D grid representing the game board
        """
        # Initialize empty table
        table = [[0 for _ in range(self.TAB)] for _ in range(self.TAB)]
        
        # Set blocked cells
        for pos in self.blocked_cells:
            table[pos[0]][pos[1]] = -1
        
        # Set potion cells
        for name, potion in self.potions.items():
            pos = potion["position"]
            table[pos[0]][pos[1]] = 4
        
        return table
    
    def add_to_inventory(self, ingredient, amount=1):
        """Add an ingredient to the inventory"""
        if ingredient in self.inventory:
            self.inventory[ingredient] += amount
        else:
            self.inventory[ingredient] = amount
    
    def remove_from_inventory(self, ingredient, amount=1):
        """Remove an ingredient from the inventory"""
        if ingredient in self.inventory:
            self.inventory[ingredient] -= amount
            if self.inventory[ingredient] < 0:
                self.inventory[ingredient] = 0
            return True
        return False
    
    def can_craft_recipe(self, recipe_name):
        """Check if player has enough ingredients to craft a recipe"""
        recipe = None
        for r in self.recipes:
            if r["name"] == recipe_name:
                recipe = r
                break
        
        if not recipe:
            return False
        
        # Check ingredient availability
        for ingredient in recipe["ingredients"]:
            if ingredient not in self.inventory or self.inventory[ingredient] <= 0:
                return False
        
        return True
    
    def craft_recipe(self, recipe_name):
        """Attempt to craft a recipe"""
        if not self.can_craft_recipe(recipe_name):
            return False
        
        # Find the recipe
        recipe = None
        for r in self.recipes:
            if r["name"] == recipe_name:
                recipe = r
                break
        
        # Consume ingredients
        for ingredient in recipe["ingredients"]:
            self.remove_from_inventory(ingredient, 1)
        
        return True
    
    def add_recipe(self, name, potion, ingredients, difficulty="Medium"):
        """Add a new recipe to the game"""
        self.recipes.append({
            "name": name,
            "potion": potion,
            "ingredients": ingredients,
            "difficulty": difficulty
        })