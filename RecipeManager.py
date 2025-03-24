import tkinter as tk
from tkinter import ttk, messagebox

class RecipeManager:
    def __init__(self, parent, game_data):
        self.parent = parent
        self.game_data = game_data
        
        # Create main layout
        self.create_layout()
        
    def create_layout(self):
        # Main frame divided into left (recipe list) and right (details/editor)
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left side - Recipe list
        list_frame = ttk.LabelFrame(main_frame, text="Recipes")
        list_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Create the recipe list
        self.create_recipe_list(list_frame)
        
        # Right side - Recipe details and editor
        editor_frame = ttk.LabelFrame(main_frame, text="Recipe Editor")
        editor_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Create the recipe editor
        self.create_recipe_editor(editor_frame)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=3)
        main_frame.rowconfigure(0, weight=1)
    
    def create_recipe_list(self, parent):
        # Create a frame for the list and controls
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create scrollable list of recipes
        self.recipe_listbox = tk.Listbox(frame, exportselection=0)
        self.recipe_listbox.pack(side="left", fill="both", expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.recipe_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.recipe_listbox.config(yscrollcommand=scrollbar.set)
        
        # Populate list
        self.update_recipe_list()
        
        # Bind selection event
        self.recipe_listbox.bind('<<ListboxSelect>>', self.on_recipe_select)
        
        # Buttons for add/delete
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill="x", padx=5, pady=5)
        
        add_btn = ttk.Button(btn_frame, text="Add New", command=self.add_recipe)
        add_btn.pack(side="left", padx=5, pady=5)
        
        delete_btn = ttk.Button(btn_frame, text="Delete", command=self.delete_recipe)
        delete_btn.pack(side="left", padx=5, pady=5)
        
        craft_btn = ttk.Button(btn_frame, text="Craft Recipe", command=self.craft_recipe)
        craft_btn.pack(side="right", padx=5, pady=5)
    
    def create_recipe_editor(self, parent):
        # Create frame with controls
        editor_frame = ttk.Frame(parent)
        editor_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Name field
        name_frame = ttk.Frame(editor_frame)
        name_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(name_frame, text="Name:").pack(side="left", padx=5)
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(name_frame, textvariable=self.name_var)
        name_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Potion selection
        potion_frame = ttk.Frame(editor_frame)
        potion_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(potion_frame, text="Potion:").pack(side="left", padx=5)
        self.potion_var = tk.StringVar()
        potion_combo = ttk.Combobox(
            potion_frame, 
            textvariable=self.potion_var,
            values=sorted(list(self.game_data.potions.keys())),
            state="readonly"
        )
        potion_combo.pack(side="left", fill="x", expand=True, padx=5)
        
        # Difficulty selection
        difficulty_frame = ttk.Frame(editor_frame)
        difficulty_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(difficulty_frame, text="Difficulty:").pack(side="left", padx=5)
        self.difficulty_var = tk.StringVar(value="Medium")
        difficulty_combo = ttk.Combobox(
            difficulty_frame, 
            textvariable=self.difficulty_var,
            values=["Easy", "Medium", "Hard", "Very Hard"],
            state="readonly"
        )
        difficulty_combo.pack(side="left", fill="x", expand=True, padx=5)
        
        # Ingredients selection
        ingredients_frame = ttk.LabelFrame(editor_frame, text="Ingredients")
        ingredients_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.create_ingredients_selector(ingredients_frame)
        
        # Preview section
        preview_frame = ttk.LabelFrame(editor_frame, text="Recipe Preview")
        preview_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.preview_text = tk.Text(preview_frame, height=6, width=30, wrap="word", state="disabled")
        self.preview_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Save button
        save_btn = ttk.Button(editor_frame, text="Save Recipe", command=self.save_recipe)
        save_btn.pack(side="right", padx=5, pady=5)
        
        # Preview button
        preview_btn = ttk.Button(editor_frame, text="Update Preview", command=self.update_preview)
        preview_btn.pack(side="right", padx=5, pady=5)
    
    def create_ingredients_selector(self, parent):
        # Create a frame for available ingredients and selected ingredients
        selector_frame = ttk.Frame(parent)
        selector_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Available ingredients
        available_frame = ttk.LabelFrame(selector_frame, text="Available Ingredients")
        available_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        self.available_listbox = tk.Listbox(available_frame, exportselection=0)
        self.available_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Selected ingredients
        selected_frame = ttk.LabelFrame(selector_frame, text="Selected Ingredients")
        selected_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        self.selected_listbox = tk.Listbox(selected_frame, exportselection=0)
        self.selected_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Buttons for adding/removing ingredients
        btn_frame = ttk.Frame(selector_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        
        add_btn = ttk.Button(btn_frame, text="Add →", command=self.add_ingredient_to_recipe)
        add_btn.pack(side="left", padx=5, pady=5, expand=True)
        
        remove_btn = ttk.Button(btn_frame, text="← Remove", command=self.remove_ingredient_from_recipe)
        remove_btn.pack(side="left", padx=5, pady=5, expand=True)
        
        # Configure grid weights
        selector_frame.columnconfigure(0, weight=1)
        selector_frame.columnconfigure(1, weight=1)
        selector_frame.rowconfigure(0, weight=1)
        
        # Populate available ingredients
        self.update_available_ingredients()
    
    def update_available_ingredients(self):
        # Clear and populate the available ingredients list
        self.available_listbox.delete(0, tk.END)
        for ingredient in sorted(self.game_data.ingredients.keys()):
            self.available_listbox.insert(tk.END, ingredient)
    
    def update_recipe_list(self):
        # Clear and populate the recipe list
        self.recipe_listbox.delete(0, tk.END)
        for recipe in self.game_data.recipes:
            self.recipe_listbox.insert(tk.END, recipe["name"])
    
    def on_recipe_select(self, event):
        # Get selected recipe
        selection = self.recipe_listbox.curselection()
        if not selection:
            return
            
        recipe_name = self.recipe_listbox.get(selection[0])
        
        # Find the recipe
        recipe = None
        for r in self.game_data.recipes:
            if r["name"] == recipe_name:
                recipe = r
                break
        
        if not recipe:
            return
            
        # Update editor fields
        self.name_var.set(recipe["name"])
        self.potion_var.set(recipe["potion"])
        self.difficulty_var.set(recipe.get("difficulty", "Medium"))
        
        # Update selected ingredients
        self.selected_listbox.delete(0, tk.END)
        for ingredient in recipe["ingredients"]:
            self.selected_listbox.insert(tk.END, ingredient)
        
        # Update preview
        self.update_preview()
    
    def add_ingredient_to_recipe(self):
        # Get selected available ingredient
        selection = self.available_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select an ingredient to add")
            return
            
        ingredient = self.available_listbox.get(selection[0])
        
        # Check if already in selected list
        selected_ingredients = self.selected_listbox.get(0, tk.END)
        if ingredient in selected_ingredients:
            messagebox.showerror("Error", f"Ingredient '{ingredient}' is already in the recipe")
            return
            
        # Add to selected list
        self.selected_listbox.insert(tk.END, ingredient)
    
    def remove_ingredient_from_recipe(self):
        # Get selected ingredient
        selection = self.selected_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select an ingredient to remove")
            return
            
        # Remove from selected list
        self.selected_listbox.delete(selection[0])
    
    def update_preview(self):
        # Get current recipe data
        name = self.name_var.get().strip()
        potion = self.potion_var.get()
        difficulty = self.difficulty_var.get()
        ingredients = list(self.selected_listbox.get(0, tk.END))
        
        # Enable text widget for editing
        self.preview_text.config(state="normal")
        
        # Clear preview
        self.preview_text.delete("1.0", tk.END)
        
        # Add recipe preview
        if name:
            self.preview_text.insert(tk.END, f"Recipe: {name}\n")
        else:
            self.preview_text.insert(tk.END, "Recipe: [Unnamed Recipe]\n")
            
        if potion:
            self.preview_text.insert(tk.END, f"Creates: {potion} Potion\n")
            
            # Add potion effect if available
            if potion in self.game_data.potions:
                effect = self.game_data.potions[potion].get("effect", "")
                if effect:
                    self.preview_text.insert(tk.END, f"Effect: {effect}\n")
                    
        self.preview_text.insert(tk.END, f"Difficulty: {difficulty}\n\n")
        
        if ingredients:
            self.preview_text.insert(tk.END, "Ingredients:\n")
            for ing in ingredients:
                rarity = self.game_data.ingredients.get(ing, {}).get("rarity", "Unknown")
                self.preview_text.insert(tk.END, f"- {ing} ({rarity})\n")
        else:
            self.preview_text.insert(tk.END, "Ingredients: None")
        
        # Disable text widget after editing
        self.preview_text.config(state="disabled")
    
    def save_recipe(self):
        # Get values from UI
        name = self.name_var.get().strip()
        potion = self.potion_var.get()
        difficulty = self.difficulty_var.get()
        ingredients = list(self.selected_listbox.get(0, tk.END))
        
        # Validation
        if not name:
            messagebox.showerror("Error", "Recipe name cannot be empty")
            return
            
        if not potion:
            messagebox.showerror("Error", "Please select a potion for this recipe")
            return
            
        if not ingredients:
            messagebox.showerror("Error", "Please add at least one ingredient to the recipe")
            return
        
        # Get original name if we're editing
        selection = self.recipe_listbox.curselection()
        original_name = ""
        if selection:
            original_name = self.recipe_listbox.get(selection[0])
        
        # Check if name already exists (for new recipes)
        if not original_name or original_name != name:
            for recipe in self.game_data.recipes:
                if recipe["name"] == name:
                    messagebox.showerror("Error", f"Recipe name '{name}' already exists")
                    return
        
        # Create new recipe or update existing
        new_recipe = {
            "name": name,
            "potion": potion,
            "ingredients": ingredients,
            "difficulty": difficulty
        }
        
        if original_name:
            # Update existing recipe
            for i, recipe in enumerate(self.game_data.recipes):
                if recipe["name"] == original_name:
                    self.game_data.recipes[i] = new_recipe
                    break
        else:
            # Add new recipe
            self.game_data.recipes.append(new_recipe)
        
        # Update the recipe list
        self.update_recipe_list()
        
        # Select the saved recipe
        for i in range(self.recipe_listbox.size()):
            if self.recipe_listbox.get(i) == name:
                self.recipe_listbox.selection_set(i)
                break
        
        messagebox.showinfo("Success", f"Recipe '{name}' saved successfully")
    
    def add_recipe(self):
        # Clear editor fields
        self.name_var.set("")
        self.potion_var.set("")
        self.difficulty_var.set("Medium")
        
        # Clear selected ingredients
        self.selected_listbox.delete(0, tk.END)
        
        # Clear selection in recipe list
        self.recipe_listbox.selection_clear(0, tk.END)
        
        # Update preview
        self.update_preview()
    
    def delete_recipe(self):
        # Get selected recipe
        selection = self.recipe_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "No recipe selected")
            return
            
        recipe_name = self.recipe_listbox.get(selection[0])
        
        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Delete", 
            f"Are you sure you want to delete the recipe '{recipe_name}'?"
        )
        if not confirm:
            return
        
        # Delete the recipe
        for i, recipe in enumerate(self.game_data.recipes):
            if recipe["name"] == recipe_name:
                del self.game_data.recipes[i]
                break
                
        # Update the list
        self.update_recipe_list()
        
        # Clear editor fields
        self.add_recipe()
        
        messagebox.showinfo("Success", f"Recipe '{recipe_name}' deleted successfully")
    
    def craft_recipe(self):
        # Get selected recipe
        selection = self.recipe_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "No recipe selected")
            return
            
        recipe_name = self.recipe_listbox.get(selection[0])
        
        # Check if we can craft it
        can_craft = self.game_data.can_craft_recipe(recipe_name)
        
        if not can_craft:
            # Find which ingredients are missing
            missing = []
            for recipe in self.game_data.recipes:
                if recipe["name"] == recipe_name:
                    for ingredient in recipe["ingredients"]:
                        if ingredient not in self.game_data.inventory or self.game_data.inventory[ingredient] <= 0:
                            missing.append(ingredient)
                    break
            
            messagebox.showerror(
                "Cannot Craft Recipe", 
                f"Missing ingredients: {', '.join(missing)}\n\nCheck your inventory!"
            )
            return
        
        # Confirm crafting
        confirm = messagebox.askyesno(
            "Confirm Crafting", 
            f"Craft '{recipe_name}'? This will consume the required ingredients."
        )
        if not confirm:
            return
        
        # Craft recipe
        success = self.game_data.craft_recipe(recipe_name)
        
        if success:
            # Find the potion
            potion_name = ""
            for recipe in self.game_data.recipes:
                if recipe["name"] == recipe_name:
                    potion_name = recipe["potion"]
                    break
                    
            messagebox.showinfo(
                "Success", 
                f"Successfully crafted '{recipe_name}'!\n\nYou created a {potion_name} potion."
            )