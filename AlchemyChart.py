import tkinter as tk
from tkinter import ttk, messagebox

class AlchemyChart:
    def __init__(self, parent, game_data):
        self.parent = parent
        self.game_data = game_data
        
        # Create main layout
        self.create_layout()
        
    def create_layout(self):
        # Main frame divided into left (chart) and right (controls)
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left side - Chart visualization
        chart_frame = ttk.LabelFrame(main_frame, text="Alchemy Chart")
        chart_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Create the chart visualization
        self.create_chart_visualization(chart_frame)
        
        # Right side - Path verification controls
        controls_frame = ttk.LabelFrame(main_frame, text="Path Verification")
        controls_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Create the controls
        self.create_controls(controls_frame)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=3)
        main_frame.columnconfigure(1, weight=2)
        main_frame.rowconfigure(0, weight=1)
    
    def create_chart_visualization(self, parent):
        # Create canvas for chart
        self.chart_canvas = tk.Canvas(parent, bg="white")
        self.chart_canvas.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Draw the chart
        self.draw_chart()
    
    def draw_chart(self):
        # Clear the canvas
        self.chart_canvas.delete("all")
        
        # Get the table data
        table = self.game_data.get_table()
        
        # Calculate cell size based on canvas size
        canvas_width = self.chart_canvas.winfo_width() or 500
        canvas_height = self.chart_canvas.winfo_height() or 500
        
        cell_size = min(canvas_width, canvas_height) // self.game_data.TAB
        
        # Draw grid
        for i in range(self.game_data.TAB):
            for j in range(self.game_data.TAB):
                x1 = j * cell_size
                y1 = i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                
                # Determine cell color and label
                if i == self.game_data.CENTER and j == self.game_data.CENTER:
                    # Center/starting point
                    color = "lightgreen"
                    text = "◉"
                elif table[i][j] == -1:
                    # Blocked
                    color = "black"
                    text = ""
                elif table[i][j] == 4:
                    # Potion
                    color = "lightblue"
                    text = self.get_potion_at_position(i, j)[0]  # First letter
                else:
                    # Empty
                    color = "white"
                    text = ""
                
                # Draw cell
                self.chart_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
                
                # Draw text
                if text:
                    self.chart_canvas.create_text(
                        x1 + cell_size/2, 
                        y1 + cell_size/2, 
                        text=text, 
                        font=("Arial", 12, "bold")
                    )
        
        # Add potion legend
        y_offset = 10
        self.chart_canvas.create_text(
            canvas_width - 100, 
            y_offset, 
            text="Potions:", 
            font=("Arial", 10, "bold"),
            anchor="nw"
        )
        
        y_offset += 20
        for name, potion in self.game_data.potions.items():
            self.chart_canvas.create_rectangle(
                canvas_width - 100, 
                y_offset, 
                canvas_width - 80, 
                y_offset + 15, 
                fill="lightblue"
            )
            self.chart_canvas.create_text(
                canvas_width - 75, 
                y_offset + 7, 
                text=name, 
                anchor="w",
                font=("Arial", 8)
            )
            y_offset += 20
    
    def get_potion_at_position(self, i, j):
        for name, potion in self.game_data.potions.items():
            position = potion["position"]
            if position[0] == i and position[1] == j:
                return name
        return ""
    
    def create_controls(self, parent):
        # Target potion
        ttk.Label(parent, text="Target Potion:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.potion_var = tk.StringVar(value=list(self.game_data.potions.keys())[0])
        potion_combo = ttk.Combobox(
            parent, 
            textvariable=self.potion_var,
            values=list(self.game_data.potions.keys()),
            state="readonly"
        )
        potion_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Max moves
        ttk.Label(parent, text="Max Moves:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.moves_var = tk.IntVar(value=5)
        moves_spinbox = ttk.Spinbox(
            parent,
            from_=1,
            to=5,
            textvariable=self.moves_var,
            width=5
        )
        moves_spinbox.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Ingredients
        ttk.Label(parent, text="Ingredients:").grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        
        # Create frame for ingredients
        ingredients_frame = ttk.Frame(parent)
        ingredients_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        
        # Create dropdown for each ingredient
        self.ingredient_vars = []
        for i in range(5):  # Max 5 ingredients
            ttk.Label(ingredients_frame, text=f"{i+1}:").grid(row=i, column=0, padx=5, pady=2, sticky="w")
            var = tk.StringVar()
            combo = ttk.Combobox(
                ingredients_frame,
                textvariable=var,
                values=list(self.game_data.ingredients.keys()),
                state="readonly",
                width=15
            )
            combo.grid(row=i, column=1, padx=5, pady=2, sticky="ew")
            self.ingredient_vars.append(var)
        
        # Recipe selection
        ttk.Label(parent, text="Recipe:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.recipe_var = tk.StringVar()
        recipe_combo = ttk.Combobox(
            parent,
            textvariable=self.recipe_var,
            values=[recipe["name"] for recipe in self.game_data.recipes],
            state="readonly"
        )
        recipe_combo.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        recipe_combo.bind("<<ComboboxSelected>>", self.load_recipe)
        
        # Verify button
        verify_button = ttk.Button(parent, text="Verify Path", command=self.verify_path)
        verify_button.grid(row=5, column=0, columnspan=2, padx=5, pady=10, sticky="ew")
        
        # Results
        ttk.Label(parent, text="Results:").grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        self.results_text = tk.Text(parent, height=10, width=30, wrap="word")
        self.results_text.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        
        # Bind resize event to redraw chart
        self.parent.bind("<Configure>", lambda e: self.draw_chart())
        
        # Symbol visualization
        ttk.Label(parent, text="Selected Pattern:").grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        self.symbol_canvas = tk.Canvas(parent, width=150, height=150, bg="white")
        self.symbol_canvas.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        
        # Bind symbol selection
        for i, var in enumerate(self.ingredient_vars):
            var.trace_add("write", lambda *args, idx=i: self.update_symbol_display(idx))
    
    def load_recipe(self, event=None):
        recipe_name = self.recipe_var.get()
        if not recipe_name:
            return
            
        # Find the recipe
        for recipe in self.game_data.recipes:
            if recipe["name"] == recipe_name:
                # Clear existing ingredients
                for var in self.ingredient_vars:
                    var.set("")
                    
                # Set ingredients
                for i, ingredient in enumerate(recipe["ingredients"]):
                    if i < len(self.ingredient_vars):
                        self.ingredient_vars[i].set(ingredient)
                
                # Set potion
                self.potion_var.set(recipe["potion"])
                
                # Set moves
                self.moves_var.set(len(recipe["ingredients"]))
                break
    
    def update_symbol_display(self, idx):
        # Clear canvas
        self.symbol_canvas.delete("all")
        
        if idx >= len(self.ingredient_vars):
            return
            
        ingredient_name = self.ingredient_vars[idx].get()
        if not ingredient_name or ingredient_name not in self.game_data.ingredients:
            return
            
        # Get the pattern
        pattern = self.game_data.ingredients[ingredient_name]["pattern"]
        
        # Draw the pattern
        cell_size = 30
        offset_x = 15
        offset_y = 15
        
        # Draw title
        self.symbol_canvas.create_text(
            75, 10, 
            text=ingredient_name, 
            font=("Arial", 10, "bold")
        )
        
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
                self.symbol_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
                
                # Draw text
                if text:
                    self.symbol_canvas.create_text(
                        x1 + cell_size/2, 
                        y1 + cell_size/2, 
                        text=text, 
                        font=("Arial", 10, "bold")
                    )
    
    def verify_path(self):
        # Clear previous results
        self.results_text.delete("1.0", tk.END)
        
        # Get selected values
        target_potion = self.potion_var.get()
        max_moves = self.moves_var.get()
        
        # Get selected ingredients
        ingredients = []
        for var in self.ingredient_vars:
            if var.get():
                ingredients.append(var.get())
        
        # Validation
        if not target_potion:
            self.results_text.insert(tk.END, "Error: Please select a target potion.\n")
            return
            
        if not ingredients:
            self.results_text.insert(tk.END, "Error: Please select at least one ingredient.\n")
            return
            
        if len(ingredients) > max_moves:
            self.results_text.insert(tk.END, f"Error: You selected {len(ingredients)} ingredients but only allowed {max_moves} moves.\n")
            return
        
        # Get potion position
        potion_pos = self.game_data.potions[target_potion]["position"]
        
        # Get ingredient patterns
        patterns = []
        for ingredient in ingredients:
            patterns.append(self.game_data.ingredients[ingredient]["pattern"])
        
        # Verify path using the game's validation logic
        result = self.validate_path(patterns, potion_pos, max_moves)
        
        if result["valid"]:
            self.results_text.insert(tk.END, f"Success! Path to {target_potion} is valid.\n\n")
            self.results_text.insert(tk.END, f"Ingredients used: {', '.join(ingredients)}\n")
            self.results_text.insert(tk.END, f"Moves required: {len(ingredients)}\n")
            self.results_text.insert(tk.END, f"Path: {result['path']}\n")
        else:
            self.results_text.insert(tk.END, f"Failed! Path to {target_potion} is invalid.\n\n")
            self.results_text.insert(tk.END, f"Reason: {result['reason']}\n")
    
    def validate_path(self, patterns, target_pos, max_moves):
        """
        Validates if a path can reach the target potion using the given patterns
        This is a simplified version of the C algorithm from verifica_validade function
        """
        # Start position is center
        start_pos = [self.game_data.CENTER, self.game_data.CENTER]
        
        # Get table
        table = self.game_data.get_table()
        
        # Remaining attempts
        moves_left = len(patterns)
        
        # Path tracking
        path = [f"({start_pos[0]},{start_pos[1]})"]
        
        # Check if we have enough moves
        if moves_left > max_moves:
            return {
                "valid": False,
                "reason": f"Too many ingredients ({moves_left}). Maximum allowed is {max_moves}.",
                "path": path
            }
        
        # Try to validate path
        result = self._recursive_validate(table, patterns, 0, start_pos, target_pos, path)
        
        if result["valid"]:
            return result
        else:
            return {
                "valid": False,
                "reason": "No valid path found with the given ingredients",
                "path": path
            }
    
    def _recursive_validate(self, table, patterns, pattern_idx, current_pos, target_pos, path):
        # Base case: no more patterns to try
        if pattern_idx >= len(patterns):
            return {
                "valid": False,
                "reason": "Used all patterns but didn't reach target",
                "path": path
            }
        
        # Get current pattern
        pattern = patterns[pattern_idx]
        
        # Find start (2) and end (3) positions in the pattern
        start_i, start_j = -1, -1
        end_i, end_j = -1, -1
        
        for i in range(len(pattern)):
            for j in range(len(pattern[i])):
                if pattern[i][j] == 2:  # Start position
                    start_i, start_j = i, j
                elif pattern[i][j] == 3:  # End position
                    end_i, end_j = i, j
        
        # Validate that pattern has start and end
        if start_i == -1 or end_i == -1:
            return {
                "valid": False,
                "reason": f"Pattern {pattern_idx+1} is missing start or end point",
                "path": path
            }
        
        # Apply pattern to board
        for i in range(len(pattern)):
            for j in range(len(pattern[i])):
                # Skip empty cells
                if pattern[i][j] == 0:
                    continue
                
                # Calculate board position
                board_i = current_pos[0] + (i - start_i)
                board_j = current_pos[1] + (j - start_j)
                
                # Check bounds
                if (board_i < 0 or board_i >= self.game_data.TAB or 
                    board_j < 0 or board_j >= self.game_data.TAB):
                    return {
                        "valid": False,
                        "reason": f"Pattern {pattern_idx+1} goes out of bounds",
                        "path": path
                    }
                
                # Check for blocked cells
                if table[board_i][board_j] == -1:
                    return {
                        "valid": False,
                        "reason": f"Pattern {pattern_idx+1} passes through a blocked cell",
                        "path": path
                    }
                
                # Check if we've reached the target with the endpoint
                if pattern[i][j] == 3 and table[board_i][board_j] == 4:
                    if [board_i, board_j] == target_pos:
                        path.append(f"({board_i},{board_j})")
                        return {
                            "valid": True,
                            "reason": "Path is valid",
                            "path": " → ".join(path)
                        }
        
        # Calculate next position
        next_pos = [
            current_pos[0] + (end_i - start_i),
            current_pos[1] + (end_j - start_j)
        ]
        
        # Add to path
        path.append(f"({next_pos[0]},{next_pos[1]})")
        
        # Continue with next pattern
        return self._recursive_validate(table, patterns, pattern_idx + 1, next_pos, target_pos, path)