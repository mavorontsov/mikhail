import tkinter as tk
from tkinter import ttk
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Constants
BASE_DIR = r"C:\\D_MV\\Data_D"

class DataPreviewGUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Data Preview GUI")
        self.window.geometry("1200x800")
        
        # Initialize variables
        self.data_loaded = False
        self.PIB_bg = None
        self.PIF_bg = None
        self.PIB_orig = None
        self.PIF_orig = None
        self.PIB = None
        self.PIF = None
        self.PIB_norm = None
        self.PIF_norm = None
        
        # Create main frame
        self.main_frame = ttk.Frame(window, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(self.main_frame, text="Select PIBPIF and background files", font=('Helvetica', 14))
        title_label.grid(row=0, column=0, columnspan=6, pady=10)
        
        # File selection dropdowns
        self.create_file_selection()
        
        # Buttons
        self.create_buttons()
        
        # Radio buttons for data type selection
        self.create_data_type_radio_buttons()
        
        # Radio buttons for plot type selection
        self.create_plot_type_radio_buttons()
        
        # Sliders
        self.create_sliders()
        
        # Plot area
        self.create_plot_area()
        
    def create_file_selection(self):
        # Get list of files
        pibpif_files = [f for f in os.listdir(BASE_DIR) if f.startswith('PIBPIF') and not f.endswith('background.dat')]
        bg_files = [f for f in os.listdir(BASE_DIR) if f.startswith('PIBPIF') and f.endswith('background.dat')]
        
        # PIBPIF file selection
        ttk.Label(self.main_frame, text="PIBPIF File:").grid(row=1, column=0, padx=5, pady=5)
        self.pibpif_var = tk.StringVar()
        self.pibpif_dropdown = ttk.Combobox(self.main_frame, textvariable=self.pibpif_var, values=pibpif_files, width=40)
        self.pibpif_dropdown.grid(row=1, column=1, padx=5, pady=5)
        
        # Background file selection
        ttk.Label(self.main_frame, text="Background File:").grid(row=1, column=2, padx=5, pady=5)
        self.bg_var = tk.StringVar()
        self.bg_dropdown = ttk.Combobox(self.main_frame, textvariable=self.bg_var, values=bg_files, width=40)
        self.bg_dropdown.grid(row=1, column=3, padx=5, pady=5)
        
    def create_buttons(self):
        button_colors = ["lightblue", "lightgreen", "lightyellow", "lightpink", "lightcyan", "lightgray"]
        button_texts = ["Load Data", "Plot Normalized", "Plot Original", "Save Norm Data", "Save Data Segments", "Exit"]
        
        # Create a frame for buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=2, column=0, columnspan=6, padx=5, pady=5, sticky="ew")
        
        # Set fixed button width
        button_width = 15
        
        # Create all buttons except Exit
        for i, (text, color) in enumerate(zip(button_texts[:-1], button_colors[:-1])):
            btn = tk.Button(button_frame, text=text, bg=color, width=button_width,
                          command=lambda t=text: self.button_click(t))
            btn.pack(side="left", padx=5)
        
        # Create Exit button separately and pack it to the right
        exit_btn = tk.Button(button_frame, text="Exit", bg=button_colors[-1], width=button_width,
                           command=lambda: self.button_click("Exit"))
        exit_btn.pack(side="right", padx=5)
            
    def create_data_type_radio_buttons(self):
        self.data_type_var = tk.StringVar(value="PIB/PIF")
        
        frame = ttk.LabelFrame(self.main_frame, text="Data Type Selection")
        frame.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="w")
        
        for i, text in enumerate(["PIB/PIF", "PIB", "PIF"]):
            rb = ttk.Radiobutton(frame, text=text, variable=self.data_type_var, value=text)
            rb.grid(row=0, column=i, padx=5, pady=5)
            
    def create_plot_type_radio_buttons(self):
        self.plot_type_vars = {
            "Bg": tk.BooleanVar(value=False),
            "Orig": tk.BooleanVar(value=False),
            "Orig-Bg": tk.BooleanVar(value=False)
        }
        
        frame = ttk.LabelFrame(self.main_frame, text="Plot Type Selection")
        frame.grid(row=3, column=3, columnspan=3, padx=5, pady=5, sticky="w")
        
        for i, (text, var) in enumerate(self.plot_type_vars.items()):
            cb = ttk.Checkbutton(frame, text=text, variable=var)
            cb.grid(row=0, column=i, padx=5, pady=5)
            
    def create_sliders(self):
        # Start index slider and entry
        ttk.Label(self.main_frame, text="Start Index:").grid(row=4, column=0, padx=5, pady=5)
        self.start_index_var = tk.IntVar(value=5)  # Changed initial value to 5
        
        # Create a frame for start index controls
        start_frame = ttk.Frame(self.main_frame)
        start_frame.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        
        # Add entry for start index (before slider)
        self.start_index_entry = ttk.Entry(start_frame, textvariable=self.start_index_var, width=8)
        self.start_index_entry.pack(side="left", padx=(0, 5))
        
        # Start index slider
        self.start_index_slider = ttk.Scale(start_frame, from_=0, to=1000, variable=self.start_index_var, 
                                          orient="horizontal", command=self.update_plot)
        self.start_index_slider.pack(side="left", fill="x", expand=True)
        
        # Window size slider and entry
        ttk.Label(self.main_frame, text="Window Size:").grid(row=4, column=3, padx=5, pady=5)
        self.window_size_var = tk.IntVar(value=1000)  # Changed initial value to 1000
        
        # Create a frame for window size controls with same width as start index frame
        window_frame = ttk.Frame(self.main_frame)
        window_frame.grid(row=4, column=4, columnspan=2, padx=5, pady=5, sticky="ew")
        
        # Add entry for window size (before slider)
        self.window_size_entry = ttk.Entry(window_frame, textvariable=self.window_size_var, width=8)
        self.window_size_entry.pack(side="left", padx=(0, 5))
        
        # Window size slider
        self.window_size_slider = ttk.Scale(window_frame, from_=1, to=1000, variable=self.window_size_var, 
                                          orient="horizontal", command=self.update_plot)
        self.window_size_slider.pack(side="left", fill="x", expand=True)
        
        # Make both frames the same width
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(4, weight=1)
        
        # Bind entry changes to update plot and validate integers
        def validate_int(P):
            if P == "": return True
            try:
                int(P)
                return True
            except ValueError:
                return False
        
        vcmd = (self.window.register(validate_int), '%P')
        self.start_index_entry.configure(validate='key', validatecommand=vcmd)
        self.window_size_entry.configure(validate='key', validatecommand=vcmd)
        
        # Bind entry changes to update plot
        self.start_index_entry.bind('<Return>', lambda e: self.update_plot())
        self.window_size_entry.bind('<Return>', lambda e: self.update_plot())
        
    def create_plot_area(self):
        self.fig = Figure(figsize=(10, 6))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.canvas.get_tk_widget().grid(row=5, column=0, columnspan=6, padx=5, pady=5)
        
    def button_click(self, button_text):
        if button_text == "Load Data":
            self.load_data()
        elif button_text == "Plot Normalized":
            self.plot_normalized()
        elif button_text == "Plot Original":
            self.plot_original()
        elif button_text == "Save Norm Data":
            self.save_normalized_data()
        elif button_text == "Save Data Segments":
            self.save_data_segments()
        elif button_text == "Exit":
            self.clear_plots()
            
    def load_data(self):
        try:
            # Load data
            data_pibpif = np.loadtxt(os.path.join(BASE_DIR, self.pibpif_var.get()), skiprows=2, delimiter=',')
            data_bg = np.loadtxt(os.path.join(BASE_DIR, self.bg_var.get()), skiprows=2, delimiter=',')
            
            # Extract arrays
            self.PIB_bg = data_bg[:, 0]
            self.PIF_bg = data_bg[:, 1]
            self.PIB_orig = data_pibpif[:, 0]
            self.PIF_orig = data_pibpif[:, 1]
            
            # Calculate PIB and PIF
            self.PIB = self.PIB_orig - self.PIB_bg
            self.PIF = self.PIF_orig - self.PIF_bg
            
            # Normalize data
            self.PIB_norm = (self.PIB - np.min(self.PIB)) / (np.max(self.PIB) - np.min(self.PIB))
            self.PIF_norm = (self.PIF - np.min(self.PIF)) / (np.max(self.PIF) - np.min(self.PIF))
            
            self.data_loaded = True
            print("Data loaded successfully!")
            
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            
    def update_plot(self, *args):
        """Update the plot when sliders or entries change"""
        if not self.data_loaded:
            return
            
        # Get current values and ensure they are integers
        try:
            start_idx = int(self.start_index_var.get())
            window_size = int(self.window_size_var.get())
            
            # Update the variables to ensure they are integers
            self.start_index_var.set(start_idx)
            self.window_size_var.set(window_size)
        except ValueError:
            return
            
        # Update slider ranges based on data length
        if hasattr(self, 'PIB_norm'):
            max_idx = len(self.PIB_norm)
            self.start_index_slider.configure(to=max(0, max_idx - window_size))
            self.window_size_slider.configure(to=max(1, max_idx - start_idx))
        
        # Update the plot based on which button was last clicked
        if hasattr(self, '_last_plot_type'):
            if self._last_plot_type == "normalized":
                self.plot_normalized()
            elif self._last_plot_type == "original":
                self.plot_original()
                
    def plot_normalized(self):
        if not self.data_loaded:
            print("Please load data first!")
            return
            
        self._last_plot_type = "normalized"  # Store the last plot type
        self.ax.clear()
        start_idx = self.start_index_var.get()
        window_size = self.window_size_var.get()
        end_idx = min(start_idx + window_size, len(self.PIB_norm))
        
        data_type = self.data_type_var.get()
        if data_type in ["PIB/PIF", "PIB"]:
            # Plot PIB data in blue
            mean_pib = np.mean(self.PIB_norm[start_idx:end_idx])
            std_pib = np.std(self.PIB_norm[start_idx:end_idx])
            self.ax.plot(self.PIB_norm[start_idx:end_idx], label=f'PIB Normalized (mean={mean_pib:.3f}, std={std_pib:.3f})', 
                        color='blue')
            
        if data_type in ["PIB/PIF", "PIF"]:
            # Plot PIF data in green
            mean_pif = np.mean(self.PIF_norm[start_idx:end_idx])
            std_pif = np.std(self.PIF_norm[start_idx:end_idx])
            self.ax.plot(self.PIF_norm[start_idx:end_idx], label=f'PIF Normalized (mean={mean_pif:.3f}, std={std_pif:.3f})', 
                        color='green')
            
        self.ax.set_title("Normalized Data Plot")
        self.ax.legend()
        self.canvas.draw()
        
    def plot_original(self):
        if not self.data_loaded:
            print("Please load data first!")
            return
            
        self._last_plot_type = "original"  # Store the last plot type
        self.ax.clear()
        start_idx = self.start_index_var.get()
        window_size = self.window_size_var.get()
        end_idx = min(start_idx + window_size, len(self.PIB_orig))
        
        data_type = self.data_type_var.get()
        plot_types = [k for k, v in self.plot_type_vars.items() if v.get()]
        
        if not plot_types:
            print("Please select at least one plot type!")
            return
            
        # Define colors for different plot types
        colors = {
            'Bg': {'PIB': 'lightblue', 'PIF': 'lightgreen'},
            'Orig': {'PIB': 'blue', 'PIF': 'green'},
            'Orig-Bg': {'PIB': 'darkblue', 'PIF': 'darkgreen'}
        }
            
        for plot_type in plot_types:
            if data_type in ["PIB/PIF", "PIB"]:
                if plot_type == "Bg":
                    data = self.PIB_bg[start_idx:end_idx]
                    mean = np.mean(data)
                    std = np.std(data)
                    self.ax.plot(data, label=f'PIB Background (mean={mean:.3f}, std={std:.3f})', 
                               color=colors['Bg']['PIB'])
                elif plot_type == "Orig":
                    data = self.PIB_orig[start_idx:end_idx]
                    mean = np.mean(data)
                    std = np.std(data)
                    self.ax.plot(data, label=f'PIB Original (mean={mean:.3f}, std={std:.3f})', 
                               color=colors['Orig']['PIB'])
                elif plot_type == "Orig-Bg":
                    data = self.PIB[start_idx:end_idx]
                    mean = np.mean(data)
                    std = np.std(data)
                    self.ax.plot(data, label=f'PIB (Orig-Bg) (mean={mean:.3f}, std={std:.3f})', 
                               color=colors['Orig-Bg']['PIB'])
                    
            if data_type in ["PIB/PIF", "PIF"]:
                if plot_type == "Bg":
                    data = self.PIF_bg[start_idx:end_idx]
                    mean = np.mean(data)
                    std = np.std(data)
                    self.ax.plot(data, label=f'PIF Background (mean={mean:.3f}, std={std:.3f})', 
                               color=colors['Bg']['PIF'])
                elif plot_type == "Orig":
                    data = self.PIF_orig[start_idx:end_idx]
                    mean = np.mean(data)
                    std = np.std(data)
                    self.ax.plot(data, label=f'PIF Original (mean={mean:.3f}, std={std:.3f})', 
                               color=colors['Orig']['PIF'])
                elif plot_type == "Orig-Bg":
                    data = self.PIF[start_idx:end_idx]
                    mean = np.mean(data)
                    std = np.std(data)
                    self.ax.plot(data, label=f'PIF (Orig-Bg) (mean={mean:.3f}, std={std:.3f})', 
                               color=colors['Orig-Bg']['PIF'])
                    
        self.ax.set_title("Original Data Plot")
        self.ax.legend()
        self.canvas.draw()
        
    def save_normalized_data(self):
        if not self.data_loaded:
            print("Please load data first!")
            return
            
        save_dir = os.path.join(BASE_DIR, "Data_norm")
        os.makedirs(save_dir, exist_ok=True)
        
        data_type = self.data_type_var.get()
        if data_type in ["PIB/PIF", "PIB"]:
            np.savetxt(os.path.join(save_dir, "PIB_norm.txt"), self.PIB_norm)
        if data_type in ["PIB/PIF", "PIF"]:
            np.savetxt(os.path.join(save_dir, "PIF_norm.txt"), self.PIF_norm)
            
        print("Normalized data saved successfully!")
        
    def save_data_segments(self):
        if not self.data_loaded:
            print("Please load data first!")
            return
            
        save_dir = os.path.join(BASE_DIR, "Data_seg")
        os.makedirs(save_dir, exist_ok=True)
        
        start_idx = self.start_index_var.get()
        window_size = self.window_size_var.get()
        end_idx = min(start_idx + window_size, len(self.PIB_norm))
        
        data_type = self.data_type_var.get()
        if data_type in ["PIB/PIF", "PIB"]:
            np.savetxt(os.path.join(save_dir, "PIB_norm_seg.txt"), self.PIB_norm[start_idx:end_idx])
        if data_type in ["PIB/PIF", "PIF"]:
            np.savetxt(os.path.join(save_dir, "PIF_norm_seg.txt"), self.PIF_norm[start_idx:end_idx])
            
        print("Data segments saved successfully!")
        
    def clear_plots(self):
        self.ax.clear()
        self.canvas.draw()

# Create and run the GUI
if __name__ == "__main__":
    window = tk.Tk()
    app = DataPreviewGUI(window)
    window.mainloop() 