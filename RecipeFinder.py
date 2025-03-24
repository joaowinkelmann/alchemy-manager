import tkinter as tk
from tkinter import ttk, messagebox
import itertools
import threading
import time

class RecipeFinder:
    def __init__(self, parent, game_data):
        self.parent = parent
        self.game_data = game_data
        self.search_in_progress = False
        self.search_thread = None
        self.search_cancel = False
        
        # Create main layout
        self.create_layout()
        
    def create_layout(self):
        # Main frame divided into top (controls) and bottom (results)
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Top - Controls
        controls_frame = ttk.LabelFrame(main_frame, text="Search Parameters")
        controls_frame.pack(fill="x", expand=False, padx=10, pady=10)
        
        self.create_controls(controls_frame)
        
        # Bottom - Results
        results_frame = ttk.LabelFrame(main_frame, text="Search Results")
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.create_results_area(results_frame)
    
    def create_controls(self, parent):
        # Create grid layout for controls
        controls_grid = ttk.Frame(parent)
        controls_grid.pack(fill="x", expand=False, padx=10, pady=10)
        
        # Target potion selection
        ttk.Label(controls_grid, text="Target Potion:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.potion_var = tk.StringVar(value=list(self.game_data.potions.keys())[0])
        # Store a reference to the combobox
        self.potion_combobox = ttk.Combobox(
            controls_grid, 
            textvariable=self.potion_var,
            values=list(self.game_data.potions.keys()),
            state="readonly",
            width=15
        )
        self.potion_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Max moves
        ttk.Label(controls_grid, text="Maximum Moves:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.max_moves_var = tk.IntVar(value=3)
        max_moves_spinbox = ttk.Spinbox(
            controls_grid,
            from_=1,
            to=5,
            textvariable=self.max_moves_var,
            width=5
        )
        max_moves_spinbox.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        # Ingredients to include/exclude
        ttk.Label(controls_grid, text="Filter by Ingredients:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        # Create frame for the ingredient selectors
        ingredients_frame = ttk.Frame(controls_grid)
        ingredients_frame.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="ew")
        
        # Available ingredients list
        avail_frame = ttk.LabelFrame(ingredients_frame, text="Available Ingredients")
        avail_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        self.ingredient_listbox = tk.Listbox(avail_frame, selectmode="multiple", exportselection=0, height=5)
        self.ingredient_listbox.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(avail_frame, orient="vertical", command=self.ingredient_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.ingredient_listbox.config(yscrollcommand=scrollbar.set)
        
        # Populate available ingredients
        for ingredient in sorted(self.game_data.ingredients.keys()):
            self.ingredient_listbox.insert(tk.END, ingredient)
        
        # Required ingredients list
        req_frame = ttk.LabelFrame(ingredients_frame, text="Required Ingredients")
        req_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        self.required_listbox = tk.Listbox(req_frame, selectmode="multiple", exportselection=0, height=5)
        self.required_listbox.pack(side="left", fill="both", expand=True)
        
        req_scrollbar = ttk.Scrollbar(req_frame, orient="vertical", command=self.required_listbox.yview)
        req_scrollbar.pack(side="right", fill="y")
        self.required_listbox.config(yscrollcommand=req_scrollbar.set)
        
        # Move buttons
        btn_frame = ttk.Frame(ingredients_frame)
        btn_frame.pack(side="left", fill="y", padx=5)
        
        add_btn = ttk.Button(btn_frame, text="→", width=3, command=self.add_required_ingredient)
        add_btn.pack(side="top", pady=5)
        
        remove_btn = ttk.Button(btn_frame, text="←", width=3, command=self.remove_required_ingredient)
        remove_btn.pack(side="top", pady=5)
        
        # Search button and progress indicator
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill="x", expand=False, padx=10, pady=10)
        
        self.search_btn = ttk.Button(button_frame, text="Find Valid Combinations", command=self.start_search)
        self.search_btn.pack(side="left", padx=5, pady=5)
        
        self.cancel_btn = ttk.Button(button_frame, text="Cancel Search", command=self.cancel_search, state="disabled")
        self.cancel_btn.pack(side="left", padx=5, pady=5)
        
        self.progress_bar = ttk.Progressbar(button_frame, mode="indeterminate", length=200)
        self.progress_bar.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        
        self.status_label = ttk.Label(button_frame, text="Ready")
        self.status_label.pack(side="right", padx=5, pady=5)
    
    def create_results_area(self, parent):
        # Create frame for results with a search summary and detailed results
        results_frame = ttk.Frame(parent)
        results_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Results summary
        summary_frame = ttk.LabelFrame(results_frame, text="Summary")
        summary_frame.pack(fill="x", expand=False, padx=5, pady=5)
        
        self.summary_text = tk.Text(summary_frame, height=3, width=30, wrap="word")
        self.summary_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Results notebook for different lengths
        self.results_notebook = ttk.Notebook(results_frame)
        self.results_notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create tabs for 1-5 moves
        self.result_texts = {}
        for i in range(1, 6):
            frame = ttk.Frame(self.results_notebook)
            self.results_notebook.add(frame, text=f"{i} Move(s)")
            
            # Add text widget with scrollbar
            result_text = tk.Text(frame, wrap="word")
            result_text.pack(side="left", fill="both", expand=True)
            
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=result_text.yview)
            scrollbar.pack(side="right", fill="y")
            result_text.config(yscrollcommand=scrollbar.set)
            
            self.result_texts[i] = result_text
        
        # Add controls for the results
        controls_frame = ttk.Frame(results_frame)
        controls_frame.pack(fill="x", expand=False, padx=5, pady=5)
        
        # Copy button
        copy_btn = ttk.Button(controls_frame, text="Copy Selected Results", command=self.copy_results)
        copy_btn.pack(side="left", padx=5, pady=5)
        
        # Testing button
        test_btn = ttk.Button(controls_frame, text="Test Selected Combination", command=self.test_selected)
        test_btn.pack(side="left", padx=5, pady=5)
        
        # Clear button
        clear_btn = ttk.Button(controls_frame, text="Clear Results", command=self.clear_results)
        clear_btn.pack(side="right", padx=5, pady=5)
    
    def add_required_ingredient(self):
        # Get selected ingredients from available list
        selected_indices = self.ingredient_listbox.curselection()
        if not selected_indices:
            return
        
        # Add to required list
        for idx in selected_indices:
            ingredient = self.ingredient_listbox.get(idx)
            if ingredient not in self.required_listbox.get(0, tk.END):
                self.required_listbox.insert(tk.END, ingredient)
    
    def remove_required_ingredient(self):
        # Get selected ingredients from required list
        selected_indices = self.required_listbox.curselection()
        if not selected_indices:
            return
        
        # Remove from required list (in reverse order to avoid index shifting)
        for idx in sorted(selected_indices, reverse=True):
            self.required_listbox.delete(idx)
    
    def start_search(self):
        if self.search_in_progress:
            return
        
        # Get search parameters
        target_potion = self.potion_var.get()
        max_moves = self.max_moves_var.get()
        required_ingredients = list(self.required_listbox.get(0, tk.END))
        
        # Validation
        if not target_potion:
            messagebox.showerror("Error", "Please select a target potion")
            return
        
        # Clear previous results
        self.clear_results()
        
        # Start search in a background thread
        self.search_in_progress = True
        self.search_cancel = False
        
        # Update UI
        self.search_btn.config(state="disabled")
        self.cancel_btn.config(state="normal")
        self.progress_bar.start(20)
        self.status_label.config(text="Searching...")
        
        # Start search thread
        self.search_thread = threading.Thread(
            target=self.find_combinations, 
            args=(target_potion, max_moves, required_ingredients)
        )
        self.search_thread.daemon = True
        self.search_thread.start()
    
    def cancel_search(self):
        if not self.search_in_progress:
            return
        
        self.search_cancel = True
        self.status_label.config(text="Cancelling...")
    
    def find_combinations(self, target_potion, max_moves, required_ingredients):
        """Find all valid ingredient combinations for a target potion"""
        try:
            target_pos = self.game_data.potions[target_potion]["position"]
            all_ingredients = list(self.game_data.ingredients.keys())
            
            # If there are required ingredients, ensure they're used
            if required_ingredients:
                search_space = required_ingredients.copy()
                # Add other ingredients
                for ing in all_ingredients:
                    if ing not in search_space:
                        search_space.append(ing)
            else:
                search_space = all_ingredients
            
            # Track results by number of moves
            valid_combinations = {i: [] for i in range(1, max_moves + 1)}
            total_combinations = 0
            valid_count = 0
            
            # Try combinations of 1 to max_moves ingredients
            for num_moves in range(1, max_moves + 1):
                # Generate all possible combinations
                for combo in itertools.permutations(search_space, num_moves):
                    # Check if search was cancelled
                    if self.search_cancel:
                        # Update UI on main thread
                        self.parent.after(0, self.update_ui_after_search, 
                                          total_combinations, valid_count, True)
                        return
                    
                    # Check if all required ingredients are included
                    if required_ingredients and not all(ing in combo for ing in required_ingredients):
                        continue
                    
                    total_combinations += 1
                    
                    # Get patterns for this combination
                    patterns = [self.game_data.ingredients[ing]["pattern"] for ing in combo]
                    
                    # Create a temp AlchemyChart for validation
                    temp_chart = AlchemyChartHelper(self.game_data)
                    
                    # Validate path
                    result = temp_chart.validate_path(patterns, target_pos, num_moves)
                    
                    # Update the path validation logic in find_combinations:
                    if result["valid"]:
                        # Extract the path steps from the result
                        # Path format is like "(6,6) → (6,8) → (3,9)" 
                        # For a target hit at the last move
                        
                        # Count the number of arrows (→) in the path to determine move count
                        # For a valid path, there should be exactly num_moves arrows 
                        # (one fewer than the total positions)
                        path_transitions = result["path"].count("→")
                        
                        # We need exactly num_moves transitions to reach the target
                        if path_transitions == num_moves:
                            valid_count += 1
                            valid_combinations[num_moves].append({
                                "ingredients": combo,
                                "path": result["path"]
                            })
            
            # Update UI on main thread
            self.parent.after(0, self.update_ui_after_search, 
                             total_combinations, valid_count, False)
            
            # Display results on main thread
            self.parent.after(0, self.display_results, valid_combinations, target_potion)
            
        except Exception as e:
            # Handle any exceptions
            self.parent.after(0, self.show_error, str(e))
    
    def update_ui_after_search(self, total_combinations, valid_count, was_cancelled):
        self.search_in_progress = False
        self.progress_bar.stop()
        self.search_btn.config(state="normal")
        self.cancel_btn.config(state="disabled")
        
        if was_cancelled:
            self.status_label.config(text="Search cancelled")
        else:
            self.status_label.config(text="Search complete")
        
        # Update summary
        self.summary_text.config(state="normal")
        self.summary_text.delete("1.0", tk.END)
        
        self.summary_text.insert(tk.END, f"Total combinations checked: {total_combinations}\n")
        self.summary_text.insert(tk.END, f"Valid combinations found: {valid_count}\n")
        
        if was_cancelled:
            self.summary_text.insert(tk.END, "Search was cancelled before completion.\n")
            
        self.summary_text.config(state="disabled")
    
    def display_results(self, valid_combinations, target_potion):
        # Display results in each tab
        for num_moves, combinations in valid_combinations.items():
            text_widget = self.result_texts[num_moves]
            text_widget.config(state="normal")
            text_widget.delete("1.0", tk.END)
            
            if not combinations:
                text_widget.insert(tk.END, f"No valid {num_moves}-move combinations found for {target_potion}.\n")
            else:
                text_widget.insert(tk.END, f"Found {len(combinations)} valid {num_moves}-move combinations for {target_potion}:\n\n")
                
                for i, combo in enumerate(combinations):
                    ingredients = " → ".join(combo["ingredients"])
                    text_widget.insert(tk.END, f"{i+1}. {ingredients}\n")
                    text_widget.insert(tk.END, f"   Path: {combo['path']}\n\n")
            
            text_widget.config(state="disabled")
        
        # Switch to the tab with results
        for i in range(1, 6):
            if valid_combinations.get(i):  # Use .get() to avoid KeyError
                self.results_notebook.select(i-1)
                break
    
    def show_error(self, error_message):
        self.search_in_progress = False
        self.progress_bar.stop()
        self.search_btn.config(state="normal")
        self.cancel_btn.config(state="disabled")
        self.status_label.config(text="Error")
        
        messagebox.showerror("Error", f"An error occurred during search: {error_message}")
    
    def copy_results(self):
        # Get the current tab
        current_tab = self.results_notebook.index("current")
        current_text = self.result_texts[current_tab + 1]
        
        # Copy text to clipboard
        self.parent.clipboard_clear()
        self.parent.clipboard_append(current_text.get("1.0", tk.END))
        
        messagebox.showinfo("Success", "Results copied to clipboard")
    
    def test_selected(self):
        # Get the current tab
        current_tab = self.results_notebook.index("current")
        current_text = self.result_texts[current_tab + 1]
        
        # Get current text selection
        try:
            selected_text = current_text.get("sel.first", "sel.last")
        except tk.TclError:
            messagebox.showerror("Error", "Please select a combination to test")
            return
        
        # Parse the selected text to extract ingredients
        if "→" not in selected_text:
            messagebox.showerror("Error", "Invalid selection. Please select a complete ingredient combination.")
            return
        
        # Extract ingredients
        ingredients = []
        for part in selected_text.split("→"):
            ing = part.strip()
            if ing in self.game_data.ingredients:
                ingredients.append(ing)
        
        if not ingredients:
            messagebox.showerror("Error", "No valid ingredients found in selection")
            return
        
        # Send to AlchemyChart for verification
        # This will require integration with the main application
        messagebox.showinfo("Test Combination", 
                           f"Would test: {' → '.join(ingredients)}\n\n"
                           "This feature requires integration with the AlchemyChart tab.")
    
    def clear_results(self):
        # Clear summary
        self.summary_text.config(state="normal")
        self.summary_text.delete("1.0", tk.END)
        self.summary_text.config(state="disabled")
        
        # Clear all result tabs
        for text_widget in self.result_texts.values():
            text_widget.config(state="normal")
            text_widget.delete("1.0", tk.END)
            text_widget.config(state="disabled")

    def refresh(self):
        """Refresh the finder with the latest data"""
        print("refreshing recipe finder")
        # Update potion dropdown using the stored reference
        potion_values = list(self.game_data.potions.keys())
        
        if len(potion_values) > 0:
            # Debug: print all potions
            for potion in potion_values:
                print(potion)
            if self.potion_var.get() not in potion_values:
                self.potion_var.set(potion_values[0])
        else:
            self.potion_var.set("")
        
        # Update combobox directly using the stored reference
        if hasattr(self, 'potion_combobox'):
            self.potion_combobox['values'] = potion_values
        
        # Update ingredient list
        self.ingredient_listbox.delete(0, tk.END)
        for ingredient in sorted(self.game_data.ingredients.keys()):
            self.ingredient_listbox.insert(tk.END, ingredient)

# Helper class to use AlchemyChart's validation without UI elements
class AlchemyChartHelper:
    def __init__(self, game_data):
        self.game_data = game_data
    
    def validate_path(self, patterns, target_pos, max_moves):
        """
        Validates if a path can reach the target potion using the given patterns
        This is copied from AlchemyChart.validate_path
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
        
        # Calculate where the end point will land on the board
        end_pos_i = current_pos[0] + (end_i - start_i)
        end_pos_j = current_pos[1] + (end_j - start_j)
        
        # Check if pattern endpoint is out of bounds
        if (end_pos_i < 0 or end_pos_i >= self.game_data.TAB or 
            end_pos_j < 0 or end_pos_j >= self.game_data.TAB):
            return {
                "valid": False,
                "reason": f"Pattern {pattern_idx+1} endpoint goes out of bounds",
                "path": path
            }
        
        # CRITICAL FIX: First check if the endpoint of this pattern reaches the target position
        # This is the only valid way to reach a target - with the endpoint of a pattern
        if [end_pos_i, end_pos_j] == list(target_pos):
            # Add the endpoint to the path
            path.append(f"({end_pos_i},{end_pos_j})")
            
            # If we've reached the target with this pattern, the path is valid
            return {
                "valid": True,
                "reason": "Path is valid (endpoint reaches target)",
                "path": " → ".join(path)
            }
        
        # Apply pattern to board and check for obstacles
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
        
        # Calculate next position
        next_pos = [end_pos_i, end_pos_j]
        
        # Add to path
        path.append(f"({next_pos[0]},{next_pos[1]})")
        
        # Continue with next pattern
        return self._recursive_validate(table, patterns, pattern_idx + 1, next_pos, target_pos, path)