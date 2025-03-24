import tkinter as tk
from tkinter import ttk, messagebox

class IngredientsManager:
    def __init__(self, parent, game_data):
        self.parent = parent
        self.game_data = game_data
        
        # Create main layout
        self.create_layout()
        
    def create_layout(self):
        # Main frame divided into left (ingredient list) and right (details/editor)
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left side - Ingredient list
        list_frame = ttk.LabelFrame(main_frame, text="Ingredients")
        list_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Create the ingredient list
        self.create_ingredient_list(list_frame)
        
        # Right side - Ingredient details and editor
        editor_frame = ttk.LabelFrame(main_frame, text="Ingredient Editor")
        editor_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Create the ingredient editor
        self.create_ingredient_editor(editor_frame)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=3)
        main_frame.rowconfigure(0, weight=1)
    
    def create_ingredient_list(self, parent):
        # Create a frame for the list and controls
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create scrollable list of ingredients
        self.ingredient_listbox = tk.Listbox(frame, exportselection=0)
        self.ingredient_listbox.pack(side="left", fill="both", expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.ingredient_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.ingredient_listbox.config(yscrollcommand=scrollbar.set)
        
        # Populate list
        self.update_ingredient_list()
        
        # Bind selection event
        self.ingredient_listbox.bind('<<ListboxSelect>>', self.on_ingredient_select)
        
        # Buttons for add/delete
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill="x", padx=5, pady=5)
        
        add_btn = ttk.Button(btn_frame, text="Add New", command=self.add_ingredient)
        add_btn.pack(side="left", padx=5, pady=5)
        
        delete_btn = ttk.Button(btn_frame, text="Delete", command=self.delete_ingredient)
        delete_btn.pack(side="left", padx=5, pady=5)
    
    def create_ingredient_editor(self, parent):
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
        
        # Rarity field
        rarity_frame = ttk.Frame(editor_frame)
        rarity_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(rarity_frame, text="Rarity:").pack(side="left", padx=5)
        self.rarity_var = tk.StringVar()
        rarity_combo = ttk.Combobox(
            rarity_frame, 
            textvariable=self.rarity_var,
            values=["Common", "Uncommon", "Rare", "Very Rare"],
            state="readonly"
        )
        rarity_combo.pack(side="left", fill="x", expand=True, padx=5)
        
        # Location field
        location_frame = ttk.Frame(editor_frame)
        location_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(location_frame, text="Location:").pack(side="left", padx=5)
        self.location_var = tk.StringVar()
        location_entry = ttk.Entry(location_frame, textvariable=self.location_var)
        location_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Pattern editor
        pattern_frame = ttk.LabelFrame(editor_frame, text="Pattern Editor")
        pattern_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.create_pattern_editor(pattern_frame)
        
        # Save button
        save_btn = ttk.Button(editor_frame, text="Save Changes", command=self.save_changes)
        save_btn.pack(side="right", padx=5, pady=5)
    
    def create_pattern_editor(self, parent):
        # Create frame for pattern grid
        grid_frame = ttk.Frame(parent)
        grid_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create 4x4 grid of buttons for pattern editing
        self.pattern_btns = []
        for i in range(4):
            row_btns = []
            for j in range(4):
                btn = ttk.Button(
                    grid_frame, 
                    text="0", 
                    width=3,
                    command=lambda r=i, c=j: self.toggle_pattern_cell(r, c)
                )
                btn.grid(row=i, column=j, padx=2, pady=2)
                row_btns.append(btn)
            self.pattern_btns.append(row_btns)
        
        # Create legend
        legend_frame = ttk.Frame(parent)
        legend_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(legend_frame, text="Legend:").grid(row=0, column=0, sticky="w")
        ttk.Label(legend_frame, text="0 = Empty").grid(row=0, column=1, sticky="w")
        ttk.Label(legend_frame, text="1 = Path").grid(row=1, column=1, sticky="w")
        ttk.Label(legend_frame, text="2 = Start").grid(row=0, column=2, sticky="w")
        ttk.Label(legend_frame, text="3 = End").grid(row=1, column=2, sticky="w")
        
        # Preview canvas to show pattern
        preview_frame = ttk.LabelFrame(parent, text="Preview")
        preview_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.preview_canvas = tk.Canvas(preview_frame, width=150, height=150, bg="white")
        self.preview_canvas.pack(fill="both", expand=True)
    
    def update_ingredient_list(self):
        # Clear existing items
        self.ingredient_listbox.delete(0, tk.END)
        
        # Add all ingredients sorted by name
        for name in sorted(self.game_data.ingredients.keys()):
            self.ingredient_listbox.insert(tk.END, name)
    
    def on_ingredient_select(self, event):
        # Get selected ingredient
        selection = self.ingredient_listbox.curselection()
        if not selection:
            return
            
        ingredient_name = self.ingredient_listbox.get(selection[0])
        ingredient = self.game_data.ingredients.get(ingredient_name)
        
        if not ingredient:
            return
            
        # Update editor fields
        self.name_var.set(ingredient_name)
        self.rarity_var.set(ingredient.get("rarity", "Common"))
        self.location_var.set(ingredient.get("location", ""))
        
        # Update pattern grid
        pattern = ingredient.get("pattern", [[0 for _ in range(4)] for _ in range(4)])
        for i in range(4):
            for j in range(4):
                value = pattern[i][j] if i < len(pattern) and j < len(pattern[i]) else 0
                self.pattern_btns[i][j].config(text=str(value))
        
        # Update preview
        self.update_preview()
    
    def toggle_pattern_cell(self, row, col):
        # Toggle between 0-3 for the pattern cell value
        current_value = int(self.pattern_btns[row][col]["text"])
        new_value = (current_value + 1) % 4
        self.pattern_btns[row][col].config(text=str(new_value))
        
        # Update preview
        self.update_preview()
    
    def update_preview(self):
        # Clear canvas
        self.preview_canvas.delete("all")
        
        # Get pattern from UI
        pattern = self.get_pattern_from_ui()
        
        # Draw the pattern
        cell_size = 30
        offset_x = 15
        offset_y = 15
        
        # Draw grid and pattern
        for i in range(len(pattern)):
            for j in range(len(pattern[i])):
                x1 = offset_x + j * cell_size
                y1 = offset_y + i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                
                # Determine cell color and text based on value
                color = "white"
                text = ""
                
                if pattern[i][j] == 0:
                    # Empty
                    color = "white"
                    text = ""
                elif pattern[i][j] == 1:
                    # Path
                    color = "lightgray"
                    text = ""
                elif pattern[i][j] == 2:
                    # Start
                    color = "lightgreen"
                    text = "S"
                elif pattern[i][j] == 3:
                    # End
                    color = "lightblue"
                    text = "E"
                
                # Draw cell
                self.preview_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
                
                # Draw text
                if text:
                    self.preview_canvas.create_text(
                        x1 + cell_size/2, 
                        y1 + cell_size/2, 
                        text=text, 
                        font=("Arial", 10, "bold")
                    )
    
    def get_pattern_from_ui(self):
        # Get pattern from the UI grid
        pattern = []
        for i in range(4):
            row = []
            for j in range(4):
                row.append(int(self.pattern_btns[i][j]["text"]))
            pattern.append(row)
        return pattern
    
    def save_changes(self):
        # Get values from UI
        name = self.name_var.get().strip()
        rarity = self.rarity_var.get()
        location = self.location_var.get().strip()
        pattern = self.get_pattern_from_ui()
        
        # Validation
        if not name:
            messagebox.showerror("Error", "Ingredient name cannot be empty")
            return
            
        # Check if pattern has a start (2) and end (3)
        has_start = False
        has_end = False
        for row in pattern:
            for cell in row:
                if cell == 2:
                    has_start = True
                elif cell == 3:
                    has_end = True
        
        if not has_start or not has_end:
            messagebox.showerror("Error", "Pattern must have both a start (2) and end (3) point")
            return
        
        # Get original name if we're editing
        selection = self.ingredient_listbox.curselection()
        original_name = ""
        if selection:
            original_name = self.ingredient_listbox.get(selection[0])
        
        # If name changed but already exists
        if name != original_name and name in self.game_data.ingredients:
            messagebox.showerror("Error", f"Ingredient '{name}' already exists")
            return
        
        # Save the ingredient
        if original_name and original_name != name:
            # Remove old name if renamed
            del self.game_data.ingredients[original_name]
        
        # Add or update ingredient
        self.game_data.ingredients[name] = {
            "pattern": pattern,
            "rarity": rarity,
            "location": location
        }
        
        # Update the list
        self.update_ingredient_list()
        
        # Select the saved ingredient
        for i in range(self.ingredient_listbox.size()):
            if self.ingredient_listbox.get(i) == name:
                self.ingredient_listbox.selection_set(i)
                break
        
        messagebox.showinfo("Success", f"Ingredient '{name}' saved successfully")
    
    def add_ingredient(self):
        # Clear editor fields
        self.name_var.set("")
        self.rarity_var.set("Common")
        self.location_var.set("")
        
        # Reset pattern grid
        for i in range(4):
            for j in range(4):
                self.pattern_btns[i][j].config(text="0")
        
        # Clear selection in list
        self.ingredient_listbox.selection_clear(0, tk.END)
        
        # Update preview
        self.update_preview()
    
    def delete_ingredient(self):
        # Get selected ingredient
        selection = self.ingredient_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "No ingredient selected")
            return
            
        ingredient_name = self.ingredient_listbox.get(selection[0])
        
        # Check if ingredient is used in any recipes
        used_in_recipes = []
        for recipe in self.game_data.recipes:
            if ingredient_name in recipe["ingredients"]:
                used_in_recipes.append(recipe["name"])
        
        # Warn if used in recipes
        if used_in_recipes:
            warning = f"Warning: '{ingredient_name}' is used in these recipes:\n"
            warning += "\n".join(used_in_recipes)
            warning += "\n\nDeleting this ingredient may break these recipes. Continue?"
            
            confirm = messagebox.askyesno("Warning", warning)
            if not confirm:
                return
        else:
            # Normal confirmation
            confirm = messagebox.askyesno(
                "Confirm Delete", 
                f"Are you sure you want to delete '{ingredient_name}'?"
            )
            if not confirm:
                return
        
        # Delete the ingredient
        if ingredient_name in self.game_data.ingredients:
            del self.game_data.ingredients[ingredient_name]
            
            # Update the list
            self.update_ingredient_list()
            
            # Clear editor fields
            self.add_ingredient()
            
            messagebox.showinfo("Success", f"Ingredient '{ingredient_name}' deleted successfully")