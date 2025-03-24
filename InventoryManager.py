import tkinter as tk
from tkinter import ttk, messagebox

class InventoryManager:
    def __init__(self, parent, game_data):
        self.parent = parent
        self.game_data = game_data
        
        # Create main layout
        self.create_layout()
        
    def create_layout(self):
        # Main frame divided into left (inventory list) and right (details/controls)
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left side - Inventory list
        list_frame = ttk.LabelFrame(main_frame, text="Inventory")
        list_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Create the inventory list
        self.create_inventory_list(list_frame)
        
        # Right side - Details and controls
        details_frame = ttk.LabelFrame(main_frame, text="Item Details")
        details_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Create the details view
        self.create_details_view(details_frame)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=2)
        main_frame.rowconfigure(0, weight=1)
    
    def create_inventory_list(self, parent):
        # Create a frame for the list and controls
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create inventory list with columns for name and quantity
        columns = ("name", "quantity", "rarity")
        self.inventory_tree = ttk.Treeview(frame, columns=columns, show="headings")
        
        # Define headings
        self.inventory_tree.heading("name", text="Ingredient")
        self.inventory_tree.heading("quantity", text="Qty")
        self.inventory_tree.heading("rarity", text="Rarity")
        
        # Configure column widths
        self.inventory_tree.column("name", width=150, minwidth=100)
        self.inventory_tree.column("quantity", width=50, minwidth=50, anchor=tk.CENTER)
        self.inventory_tree.column("rarity", width=100, minwidth=80)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.inventory_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.inventory_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the tree
        self.inventory_tree.pack(side="left", fill="both", expand=True)
        
        # Bind selection event
        self.inventory_tree.bind("<<TreeviewSelect>>", self.on_inventory_select)
        
        # Add control buttons
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill="x", padx=5, pady=5)
        
        add_btn = ttk.Button(btn_frame, text="Add Item", command=self.show_add_dialog)
        add_btn.pack(side="left", padx=5, pady=5)
        
        remove_btn = ttk.Button(btn_frame, text="Remove Item", command=self.remove_item)
        remove_btn.pack(side="left", padx=5, pady=5)
        
        refresh_btn = ttk.Button(btn_frame, text="Refresh List", command=self.refresh_inventory)
        refresh_btn.pack(side="right", padx=5, pady=5)
        
        # Search field
        search_frame = ttk.Frame(parent)
        search_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.filter_inventory())
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Populate the inventory
        self.refresh_inventory()
    
    def create_details_view(self, parent):
        # Create frame for details and controls
        details_frame = ttk.Frame(parent)
        details_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Selected item details
        details_info = ttk.LabelFrame(details_frame, text="Information")
        details_info.pack(fill="x", expand=False, padx=5, pady=5)
        
        # Name
        name_frame = ttk.Frame(details_info)
        name_frame.pack(fill="x", padx=5, pady=2)
        ttk.Label(name_frame, text="Name:", width=10).pack(side="left")
        self.name_label = ttk.Label(name_frame, text="")
        self.name_label.pack(side="left", fill="x", expand=True)
        
        # Quantity
        qty_frame = ttk.Frame(details_info)
        qty_frame.pack(fill="x", padx=5, pady=2)
        ttk.Label(qty_frame, text="Quantity:", width=10).pack(side="left")
        
        # Create spin box for quantity
        self.qty_var = tk.IntVar(value=0)
        self.qty_spinbox = ttk.Spinbox(
            qty_frame, 
            from_=0, 
            to=99, 
            textvariable=self.qty_var,
            width=5,
            state="readonly"
        )
        self.qty_spinbox.pack(side="left")
        
        update_qty_btn = ttk.Button(qty_frame, text="Update", command=self.update_quantity)
        update_qty_btn.pack(side="left", padx=5)
        
        # Rarity
        rarity_frame = ttk.Frame(details_info)
        rarity_frame.pack(fill="x", padx=5, pady=2)
        ttk.Label(rarity_frame, text="Rarity:", width=10).pack(side="left")
        self.rarity_label = ttk.Label(rarity_frame, text="")
        self.rarity_label.pack(side="left", fill="x", expand=True)
        
        # Location
        location_frame = ttk.Frame(details_info)
        location_frame.pack(fill="x", padx=5, pady=2)
        ttk.Label(location_frame, text="Location:", width=10).pack(side="left")
        self.location_label = ttk.Label(location_frame, text="")
        self.location_label.pack(side="left", fill="x", expand=True)
        
        # Pattern preview
        pattern_frame = ttk.LabelFrame(details_frame, text="Pattern")
        pattern_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.pattern_canvas = tk.Canvas(pattern_frame, width=150, height=150, bg="white")
        self.pattern_canvas.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Recipe recommendations
        recipes_frame = ttk.LabelFrame(details_frame, text="Possible Recipes")
        recipes_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.recipe_text = tk.Text(recipes_frame, height=8, width=30, wrap="word", state="disabled")
        self.recipe_text.pack(fill="both", expand=True, padx=5, pady=5)
    
    def on_inventory_select(self, event):
        # Get selected item
        selection = self.inventory_tree.selection()
        if not selection:
            return
            
        item = self.inventory_tree.item(selection[0])
        name = item["values"][0]
        
        # Update details view
        self.update_details(name)
    
    def update_details(self, ingredient_name):
        # Update the details panel with information about the selected ingredient
        if ingredient_name not in self.game_data.ingredients:
            return
            
        ingredient = self.game_data.ingredients[ingredient_name]
        quantity = self.game_data.inventory.get(ingredient_name, 0)
        
        # Update labels
        self.name_label.config(text=ingredient_name)
        self.qty_var.set(quantity)
        self.rarity_label.config(text=ingredient.get("rarity", "Unknown"))
        self.location_label.config(text=ingredient.get("location", "Unknown"))
        
        # Draw pattern
        self.draw_pattern(ingredient.get("pattern", []))
        
        # Update recipe recommendations
        self.update_recipe_recommendations()
    
    def draw_pattern(self, pattern):
        # Clear canvas
        self.pattern_canvas.delete("all")
        
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
                self.pattern_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
                
                # Draw text
                if text:
                    self.pattern_canvas.create_text(
                        x1 + cell_size/2, 
                        y1 + cell_size/2, 
                        text=text, 
                        font=("Arial", 10, "bold")
                    )
    
    def update_recipe_recommendations(self):
        # Find recipes that can be crafted with current inventory
        craftable_recipes = []
        missing_one_recipes = []
        
        for recipe in self.game_data.recipes:
            can_craft = True
            missing_count = 0
            missing_ingredients = []
            
            for ingredient in recipe["ingredients"]:
                if ingredient not in self.game_data.inventory or self.game_data.inventory[ingredient] <= 0:
                    can_craft = False
                    missing_count += 1
                    missing_ingredients.append(ingredient)
            
            if can_craft:
                craftable_recipes.append(recipe)
            elif missing_count == 1:
                missing_one_recipes.append((recipe, missing_ingredients[0]))
        
        # Update the recommendations text
        self.recipe_text.config(state="normal")
        self.recipe_text.delete("1.0", tk.END)
        
        if craftable_recipes:
            self.recipe_text.insert(tk.END, "Ready to craft:\n")
            for recipe in craftable_recipes:
                self.recipe_text.insert(tk.END, f"• {recipe['name']} ({recipe['potion']} Potion)\n")
        
        if missing_one_recipes:
            if craftable_recipes:
                self.recipe_text.insert(tk.END, "\n")
            self.recipe_text.insert(tk.END, "Missing just one ingredient:\n")
            for recipe, missing in missing_one_recipes:
                self.recipe_text.insert(tk.END, f"• {recipe['name']} (need {missing})\n")
        
        if not craftable_recipes and not missing_one_recipes:
            self.recipe_text.insert(tk.END, "No recipes available with current inventory.\n\nCollect more ingredients!")
        
        self.recipe_text.config(state="disabled")
    
    def refresh_inventory(self):
        # Clear existing items
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        
        # Add all inventory items
        for name, qty in self.game_data.inventory.items():
            if qty > 0 or self.show_zero_qty:
                # Get rarity if available
                rarity = "Unknown"
                if name in self.game_data.ingredients:
                    rarity = self.game_data.ingredients[name].get("rarity", "Unknown")
                
                self.inventory_tree.insert("", "end", values=(name, qty, rarity))
    
    def filter_inventory(self):
        # Get search text
        search = self.search_var.get().lower()
        
        # Clear existing items
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        
        # Add filtered items
        for name, qty in self.game_data.inventory.items():
            if search in name.lower() and (qty > 0 or self.show_zero_qty):
                # Get rarity if available
                rarity = "Unknown"
                if name in self.game_data.ingredients:
                    rarity = self.game_data.ingredients[name].get("rarity", "Unknown")
                
                self.inventory_tree.insert("", "end", values=(name, qty, rarity))
    
    def show_add_dialog(self):
        # Create a dialog to add an ingredient to inventory
        add_dialog = tk.Toplevel(self.parent)
        add_dialog.title("Add Ingredient")
        add_dialog.geometry("300x150")
        add_dialog.resizable(False, False)
        add_dialog.transient(self.parent)
        add_dialog.grab_set()
        
        # Ingredient selection
        ttk.Label(add_dialog, text="Ingredient:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        ingredient_var = tk.StringVar()
        ingredient_combo = ttk.Combobox(
            add_dialog, 
            textvariable=ingredient_var, 
            values=sorted(self.game_data.ingredients.keys()),
            state="readonly",
            width=20
        )
        ingredient_combo.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Quantity
        ttk.Label(add_dialog, text="Quantity:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        qty_var = tk.IntVar(value=1)
        qty_spinbox = ttk.Spinbox(
            add_dialog, 
            from_=1, 
            to=99, 
            textvariable=qty_var,
            width=5
        )
        qty_spinbox.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # Buttons
        btn_frame = ttk.Frame(add_dialog)
        btn_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        def add_to_inventory():
            ingredient = ingredient_var.get()
            qty = qty_var.get()
            
            if not ingredient:
                messagebox.showerror("Error", "Please select an ingredient")
                return
                
            if qty <= 0:
                messagebox.showerror("Error", "Quantity must be positive")
                return
            
            # Add to inventory
            self.game_data.add_to_inventory(ingredient, qty)
            
            # Refresh the display
            self.refresh_inventory()
            
            # Update recipe recommendations
            self.update_recipe_recommendations()
            
            # Close dialog
            add_dialog.destroy()
        
        ttk.Button(btn_frame, text="Add", command=add_to_inventory).pack(side="right", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=add_dialog.destroy).pack(side="right", padx=5)
    
    def remove_item(self):
        # Get selected item
        selection = self.inventory_tree.selection()
        if not selection:
            messagebox.showerror("Error", "No item selected")
            return
            
        item = self.inventory_tree.item(selection[0])
        name = item["values"][0]
        
        # Confirm removal
        confirm = messagebox.askyesno(
            "Confirm Remove", 
            f"Remove 1 {name} from inventory?"
        )
        if not confirm:
            return
        
        # Remove from inventory
        self.game_data.remove_from_inventory(name, 1)
        
        # Refresh the display
        self.refresh_inventory()
        
        # Update recipe recommendations
        self.update_recipe_recommendations()
    
    def update_quantity(self):
        # Get selected item
        selection = self.inventory_tree.selection()
        if not selection:
            messagebox.showerror("Error", "No item selected")
            return
            
        item = self.inventory_tree.item(selection[0])
        name = item["values"][0]
        current_qty = self.game_data.inventory.get(name, 0)
        new_qty = self.qty_var.get()
        
        # Update inventory
        if new_qty > current_qty:
            # Adding items
            self.game_data.add_to_inventory(name, new_qty - current_qty)
        elif new_qty < current_qty:
            # Removing items
            self.game_data.remove_from_inventory(name, current_qty - new_qty)
        
        # Refresh the display
        self.refresh_inventory()
        
        # Update recipe recommendations
        self.update_recipe_recommendations()
    
    # Property to control visibility of zero quantity items
    @property
    def show_zero_qty(self):
        return True  # Could be made configurable with a checkbox in the UI