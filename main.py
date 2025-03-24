# main.py
import tkinter as tk
from tkinter import ttk

from AlchemyChart import AlchemyChart
from IngredientsManager import IngredientsManager
from InventoryManager import InventoryManager
from RecipeManager import RecipeManager
from RecipeFinder import RecipeFinder
from PotionManager import PotionManager
from data.GameData import GameData

class AlchemyApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Alchemy System")
        self.root.geometry("1024x768")
        
        # Initialize game data (shared across modules)
        self.game_data = GameData()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_alchemy_chart_tab()
        self.create_ingredients_editor_tab()
        self.create_inventory_manager_tab()
        self.create_recipes_manager_tab()
        self.create_recipe_finder_tab()
        self.create_potion_manager_tab()

        # Bind tab change event
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def on_tab_changed(self, event):
        """Handle tab change events by refreshing the selected tab"""
        current_tab = self.notebook.index("current")
        
        # Refresh the appropriate component based on the selected tab
        if current_tab == 0:  # Alchemy Chart
            self.alchemy_chart.refresh()
        elif current_tab == 1:  # Ingredients Editor
            if hasattr(self.ingredients_manager, 'refresh'):
                self.ingredients_manager.refresh()
        elif current_tab == 2:  # Inventory Manager
            if hasattr(self.inventory_manager, 'refresh'):
                self.inventory_manager.refresh()
        elif current_tab == 3:  # Recipes Manager
            if hasattr(self.recipe_manager, 'refresh'):
                self.recipe_manager.refresh()
        elif current_tab == 4:  # Recipe Finder
            if hasattr(self.recipe_finder, 'refresh'):
                self.recipe_finder.refresh()
        elif current_tab == 5:  # Potion Manager
            if hasattr(self.potion_manager, 'refresh'):
                self.potion_manager.refresh()
    
    def create_alchemy_chart_tab(self):
        chart_frame = ttk.Frame(self.notebook)
        self.notebook.add(chart_frame, text="Alchemy Chart")
        
        # Initialize the alchemy chart
        self.alchemy_chart = AlchemyChart(chart_frame, self.game_data)
        
    def create_ingredients_editor_tab(self):
        ingredients_frame = ttk.Frame(self.notebook)
        self.notebook.add(ingredients_frame, text="Ingredients Editor")
        
        # Initialize the ingredients manager
        self.ingredients_manager = IngredientsManager(ingredients_frame, self.game_data)
        
    def create_inventory_manager_tab(self):
        inventory_frame = ttk.Frame(self.notebook)
        self.notebook.add(inventory_frame, text="Inventory Manager")
        
        # Initialize the inventory manager
        self.inventory_manager = InventoryManager(inventory_frame, self.game_data)
        
    def create_recipes_manager_tab(self):
        recipes_frame = ttk.Frame(self.notebook)
        self.notebook.add(recipes_frame, text="Recipes Manager")
        
        # Initialize the recipe manager
        self.recipe_manager = RecipeManager(recipes_frame, self.game_data)

    def create_recipe_finder_tab(self):
        finder_frame = ttk.Frame(self.notebook)
        self.notebook.add(finder_frame, text="Potion Finder")
        
        # Initialize the recipe finder
        self.recipe_finder = RecipeFinder(finder_frame, self.game_data)
    
    def create_potion_manager_tab(self):
        potion_frame = ttk.Frame(self.notebook)
        self.notebook.add(potion_frame, text="Potion Manager")
        
        # Initialize the potion manager
        self.potion_manager = PotionManager(potion_frame, self.game_data)

def main():
    root = tk.Tk()
    app = AlchemyApplication(root)
    root.mainloop()

if __name__ == "__main__":
    main()