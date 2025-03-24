import tkinter as tk
from tkinter import ttk, messagebox, colorchooser

class PotionManager:
    def __init__(self, parent, game_data):
        self.parent = parent
        self.game_data = game_data
        
        # Create main layout
        self.create_layout()
        
    def create_layout(self):
        # Main frame divided into left (potion list) and right (details/editor)
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left side - Potion list
        list_frame = ttk.LabelFrame(main_frame, text="Potions")
        list_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Create the potion list
        self.create_potion_list(list_frame)
        
        # Right side - Potion details and editor
        editor_frame = ttk.LabelFrame(main_frame, text="Potion Editor")
        editor_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Create the potion editor
        self.create_potion_editor(editor_frame)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=3)
        main_frame.rowconfigure(0, weight=1)
    
    def create_potion_list(self, parent):
        # Create a frame for the list and controls
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create scrollable list of potions
        columns = ("name", "rarity")
        self.potion_tree = ttk.Treeview(frame, columns=columns, show="headings")
        
        # Define headings
        self.potion_tree.heading("name", text="Potion")
        self.potion_tree.heading("rarity", text="Rarity")
        
        # Configure column widths
        self.potion_tree.column("name", width=120, minwidth=100)
        self.potion_tree.column("rarity", width=80, minwidth=80)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.potion_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.potion_tree.config(yscrollcommand=scrollbar.set)
        
        # Pack the tree
        self.potion_tree.pack(side="left", fill="both", expand=True)
        
        # Bind selection event
        self.potion_tree.bind("<<TreeviewSelect>>", self.on_potion_select)
        
        # Buttons for add/delete
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill="x", padx=5, pady=5)
        
        add_btn = ttk.Button(btn_frame, text="Add New", command=self.add_potion)
        add_btn.pack(side="left", padx=5, pady=5)
        
        delete_btn = ttk.Button(btn_frame, text="Delete", command=self.delete_potion)
        delete_btn.pack(side="left", padx=5, pady=5)
        
        # Populate the potion list
        self.update_potion_list()
    
    def create_potion_editor(self, parent):
        # Create scrollable frame for editor
        editor_frame = ttk.Frame(parent)
        editor_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Basic information
        info_frame = ttk.LabelFrame(editor_frame, text="Potion Information")
        info_frame.pack(fill="x", expand=False, padx=5, pady=5)
        
        # Name field
        name_frame = ttk.Frame(info_frame)
        name_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(name_frame, text="Name:").pack(side="left", padx=5)
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(name_frame, textvariable=self.name_var)
        name_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Effect field
        effect_frame = ttk.Frame(info_frame)
        effect_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(effect_frame, text="Effect:").pack(side="left", padx=5)
        self.effect_var = tk.StringVar()
        effect_entry = ttk.Entry(effect_frame, textvariable=self.effect_var)
        effect_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Rarity field
        rarity_frame = ttk.Frame(info_frame)
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
        
        # Position frame
        position_frame = ttk.LabelFrame(editor_frame, text="Position on Chart")
        position_frame.pack(fill="x", expand=False, padx=5, pady=5)
        
        # X position
        x_frame = ttk.Frame(position_frame)
        x_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(x_frame, text="X Position:").pack(side="left", padx=5)
        self.x_var = tk.IntVar()
        x_spinbox = ttk.Spinbox(
            x_frame,
            from_=0,
            to=self.game_data.TAB-1,
            textvariable=self.x_var,
            width=5
        )
        x_spinbox.pack(side="left", padx=5)
        
        # Y position
        y_frame = ttk.Frame(position_frame)
        y_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(y_frame, text="Y Position:").pack(side="left", padx=5)
        self.y_var = tk.IntVar()
        y_spinbox = ttk.Spinbox(
            y_frame,
            from_=0,
            to=self.game_data.TAB-1,
            textvariable=self.y_var,
            width=5
        )
        y_spinbox.pack(side="left", padx=5)
        
        # Visual preview
        preview_frame = ttk.LabelFrame(editor_frame, text="Appearance")
        preview_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Color selector
        color_frame = ttk.Frame(preview_frame)
        color_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(color_frame, text="Color:").pack(side="left", padx=5)
        self.color_var = tk.StringVar(value="lightblue")
        
        # Color preview and button
        self.color_preview = tk.Canvas(color_frame, width=30, height=20, bg=self.color_var.get())
        self.color_preview.pack(side="left", padx=5)
        
        color_btn = ttk.Button(color_frame, text="Choose Color", command=self.choose_color)
        color_btn.pack(side="left", padx=5)
        
        # Position visualization
        self.preview_canvas = tk.Canvas(preview_frame, width=390, height=390, bg="white")
        self.preview_canvas.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Save button
        save_btn = ttk.Button(editor_frame, text="Save Changes", command=self.save_changes)
        save_btn.pack(side="right", padx=5, pady=10)
        
        # Update preview button
        preview_btn = ttk.Button(editor_frame, text="Update Preview", command=self.update_position_preview)
        preview_btn.pack(side="right", padx=5, pady=10)
    
    def update_potion_list(self):
        # Clear existing items
        for item in self.potion_tree.get_children():
            self.potion_tree.delete(item)
        
        # Add all potions
        for name, potion in sorted(self.game_data.potions.items()):
            self.potion_tree.insert("", "end", values=(name, potion.get("rarity", "Unknown")))
    
    def on_potion_select(self, event):
        # Get selected potion
        selection = self.potion_tree.selection()
        if not selection:
            return
            
        item = self.potion_tree.item(selection[0])
        name = item["values"][0]
        
        # Get potion data
        potion = self.game_data.potions.get(name)
        if not potion:
            return
            
        # Update editor fields
        self.name_var.set(name)
        self.effect_var.set(potion.get("effect", ""))
        self.rarity_var.set(potion.get("rarity", "Common"))
        
        # Update position
        position = potion.get("position", (0, 0))
        self.x_var.set(position[1])
        self.y_var.set(position[0])
        
        # Update color
        self.color_var.set(potion.get("color", "lightblue"))
        self.color_preview.config(bg=self.color_var.get())
        
        # Update preview
        self.update_position_preview()
    
    def choose_color(self):
        color = colorchooser.askcolor(initialcolor=self.color_var.get())
        if color[1]:  # If a color was chosen (not canceled)
            self.color_var.set(color[1])
            self.color_preview.config(bg=color[1])
    
    def update_position_preview(self):
        # Clear canvas
        self.preview_canvas.delete("all")
        
        # Get board dimensions
        tab_size = self.game_data.TAB
        
        # Calculate cell size
        cell_size = min(self.preview_canvas.winfo_width(), self.preview_canvas.winfo_height()) // tab_size
        if cell_size < 10:  # Fallback if canvas not yet sized properly
            cell_size = 30
        
        # Draw grid
        for i in range(tab_size):
            for j in range(tab_size):
                x1 = j * cell_size
                y1 = i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                
                # Determine cell color
                color = "white"
                
                # Center point
                if i == self.game_data.CENTER and j == self.game_data.CENTER:
                    color = "lightgreen"
                
                # Currently selected position
                elif i == self.y_var.get() and j == self.x_var.get():
                    color = self.color_var.get()
                
                # Blocked cells
                elif (i, j) in self.game_data.blocked_cells:
                    color = "black"
                
                # Other potions
                else:
                    for potion_name, potion_data in self.game_data.potions.items():
                        pos = potion_data.get("position")
                        if pos and pos[0] == i and pos[1] == j:
                            # Skip if this is the current potion being edited
                            if potion_name != self.name_var.get():
                                color = potion_data.get("color", "lightblue")
                                break
                
                # Draw cell
                self.preview_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
                
                # Add coordinate labels
                self.preview_canvas.create_text(
                    x1 + 5, y1 + 5,
                    text=f"{i},{j}",
                    font=("Arial", 6),
                    fill="gray",
                    anchor="nw"
                )
                
                # Add potion letter for potion positions
                if color != "white" and color != "black":
                    letter = ""
                    if i == self.y_var.get() and j == self.x_var.get():
                        letter = self.name_var.get()[0] if self.name_var.get() else "?"
                    else:
                        for potion_name, potion_data in self.game_data.potions.items():
                            pos = potion_data.get("position")
                            if pos and pos[0] == i and pos[1] == j:
                                letter = potion_name[0]
                                break
                    
                    if letter:
                        self.preview_canvas.create_text(
                            x1 + cell_size/2, y1 + cell_size/2,
                            text=letter,
                            font=("Arial", 12, "bold")
                        )
    
    def save_changes(self):
        # Get values from UI
        name = self.name_var.get().strip()
        effect = self.effect_var.get().strip()
        rarity = self.rarity_var.get()
        position = (self.x_var.get(), self.y_var.get())
        color = self.color_var.get()
        
        # Validation
        if not name:
            messagebox.showerror("Error", "Potion name cannot be empty")
            return
        
        # Check for position conflict with existing potions
        position_conflicts = []
        for potion_name, potion_data in self.game_data.potions.items():
            if potion_name != name and potion_data.get("position") == position:
                position_conflicts.append(potion_name)
        
        # Position conflict with block
        if position in self.game_data.blocked_cells:
            messagebox.showerror("Error", f"Position {position} conflicts with a blocked cell")
            return
        
        # Position conflict with another potion
        if position_conflicts:
            messagebox.showerror("Error", f"Position {position} conflicts with potions: {', '.join(position_conflicts)}")
            return
        
        # Get original name if we're editing
        selection = self.potion_tree.selection()
        original_name = ""
        if selection:
            item = self.potion_tree.item(selection[0])
            original_name = item["values"][0]
        
        # If name changed but already exists
        if name != original_name and name in self.game_data.potions:
            messagebox.showerror("Error", f"Potion '{name}' already exists")
            return
        
        # Create new potion data
        potion_data = {
            "position": position,
            "effect": effect,
            "rarity": rarity,
            "color": color
        }
        
        # Save the potion
        if original_name and original_name != name:
            # Remove old name if renamed
            del self.game_data.potions[original_name]
            
            # Update recipes that use this potion
            for recipe in self.game_data.recipes:
                if recipe["potion"] == original_name:
                    recipe["potion"] = name
        
        # Add or update potion
        self.game_data.potions[name] = potion_data
        
        # Update the list
        self.update_potion_list()
        
        # Update preview
        self.update_position_preview()
        
        # Select the saved potion
        for item in self.potion_tree.get_children():
            if self.potion_tree.item(item)["values"][0] == name:
                self.potion_tree.selection_set(item)
                break
        
        messagebox.showinfo("Success", f"Potion '{name}' saved successfully")
    
    def add_potion(self):
        # Clear editor fields
        self.name_var.set("")
        self.effect_var.set("")
        self.rarity_var.set("Common")
        
        # Set default position
        self.x_var.set(0)
        self.y_var.set(0)
        
        # Set default color
        self.color_var.set("lightblue")
        self.color_preview.config(bg="lightblue")
        
        # Clear selection in list
        for item in self.potion_tree.selection():
            self.potion_tree.selection_remove(item)
        
        # Update preview
        self.update_position_preview()
    
    def delete_potion(self):
        # Get selected potion
        selection = self.potion_tree.selection()
        if not selection:
            messagebox.showerror("Error", "No potion selected")
            return
            
        item = self.potion_tree.item(selection[0])
        potion_name = item["values"][0]
        
        # Check if potion is used in any recipes
        used_in_recipes = []
        for recipe in self.game_data.recipes:
            if recipe["potion"] == potion_name:
                used_in_recipes.append(recipe["name"])
        
        # Warn if used in recipes
        if used_in_recipes:
            warning = f"Warning: '{potion_name}' is used in these recipes:\n"
            warning += "\n".join(used_in_recipes)
            warning += "\n\nDeleting this potion will break these recipes. Continue?"
            
            confirm = messagebox.askyesno("Warning", warning)
            if not confirm:
                return
        else:
            # Normal confirmation
            confirm = messagebox.askyesno(
                "Confirm Delete", 
                f"Are you sure you want to delete the potion '{potion_name}'?"
            )
            if not confirm:
                return
        
        # Delete the potion
        if potion_name in self.game_data.potions:
            del self.game_data.potions[potion_name]
            
            # Update the list
            self.update_potion_list()
            
            # Clear editor fields
            self.add_potion()
            
            # Update recipes that use this potion
            for recipe in self.game_data.recipes:
                if recipe["potion"] == potion_name:
                    recipe["potion"] = ""
            
            messagebox.showinfo("Success", f"Potion '{potion_name}' deleted successfully")

    def refresh(self):
        """Refresh the potion manager with the latest data"""
        # Update the potion list
        self.update_potion_list()
        
        # Update preview if a potion is selected
        if self.potion_tree.selection():
            self.update_position_preview()