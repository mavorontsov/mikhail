# Data Preview GUI

A Python-based GUI application for previewing and analyzing PIB/PIF data with background subtraction capabilities.

## Features

- Load and display PIB/PIF data files
- Background subtraction functionality
- Data normalization
- Interactive plotting with adjustable window size and start index
- Multiple plot types:
  - Normalized data
  - Original data
  - Background data
  - Original-Background data
- Statistical information display (mean and standard deviation)
- Data saving capabilities:
  - Save normalized data
  - Save data segments

## Requirements

- Python 3.x
- Required packages:
  - tkinter
  - numpy
  - matplotlib

## Usage

1. Run the application:
   ```bash
   python data_preview_gui.py
   ```

2. Select PIBPIF and background files using the dropdown menus

3. Use the buttons to:
   - Load Data
   - Plot Normalized
   - Plot Original
   - Save Normalized Data
   - Save Data Segments

4. Adjust the display using:
   - Start Index slider
   - Window Size slider
   - Data Type radio buttons (PIB/PIF, PIB, PIF)
   - Plot Type checkboxes (Bg, Orig, Orig-Bg)

## Data Format

The application expects data files in the following format:
- PIBPIF files: CSV format with PIB and PIF data columns
- Background files: CSV format with background data columns

## Development

This project uses Git for version control. To contribute:

1. Check the current status:
   ```bash
   git status
   ```

2. Make your changes

3. Commit your changes:
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

## Author

Mikhail Vorontsov (mvorontsov1@udayton.edu) 