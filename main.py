# main.py
import tkinter as tk
from tkinter import ttk

from AlchemyChart import AlchemyChart
from IngredientsManager import IngredientsManager
from InventoryManager import InventoryManager
from RecipesManager import RecipesManager
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
        
        # Initialize the recipes manager
        self.recipes_manager = RecipesManager(recipes_frame, self.game_data)

def main():
    root = tk.Tk()
    app = AlchemyApplication(root)
    root.mainloop()

if __name__ == "__main__":
    main()