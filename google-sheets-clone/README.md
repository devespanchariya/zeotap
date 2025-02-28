# Google Sheets Mimicking Web Application

## Overview
This web application closely mimics the user interface and core functionalities of Google Sheets. It allows users to perform mathematical calculations, data entry, and data quality functions in a spreadsheet-like environment. The application is built using React and Vite, ensuring a responsive and interactive user experience.

## Features

### 1. Spreadsheet Interface
- **Mimicked UI**: The application replicates the visual design and layout of Google Sheets, including a toolbar, formula bar, and cell structure.
- **Drag Functions**: Users can drag cell content, formulas, and selections, mirroring Google Sheets' behavior.
- **Cell Dependencies**: Formulas and functions accurately reflect cell dependencies and update automatically when related cells change.
- **Basic Cell Formatting**: Supports formatting options such as bold, italics, font size, and color.
- **Row and Column Management**: Users can add, delete, and resize rows and columns.

### 2. Mathematical Functions
Implemented mathematical functions include:
- **SUM**: Calculates the sum of a range of cells.
- **AVERAGE**: Calculates the average of a range of cells.
- **MAX**: Returns the maximum value from a range of cells.
- **MIN**: Returns the minimum value from a range of cells.
- **COUNT**: Counts the number of cells containing numerical values in a range.

### 3. Data Quality Functions
Implemented data quality functions include:
- **TRIM**: Removes leading and trailing whitespace from a cell.
- **UPPER**: Converts the text in a cell to uppercase.
- **LOWER**: Converts the text in a cell to lowercase.
- **REMOVE_DUPLICATES**: Removes duplicate rows from a selected range.
- **FIND_AND_REPLACE**: Allows users to find and replace specific text within a range of cells.

### 4. Data Entry and Validation
- Users can input various data types, including numbers, text, and dates.
- Basic data validation checks ensure that numeric cells only contain numbers.

### 5. Testing
- Users can test the implemented functions with their own data.
- Results of function execution are displayed clearly.

## Bonus Features
- Additional mathematical and data quality functions implemented.
- Support for complex formulas and cell referencing (relative and absolute references).
- Users can save and load their spreadsheets.
- Data visualization capabilities, including charts and graphs.

## Tech Stack
- **Frontend**: React, Vite
- **State Management**: React Hooks
- **Styling**: CSS for UI design
- **Routing**: React Router (HashRouter for GitHub Pages compatibility)

## Data Structures
- **State Management**: Utilizes React's `useState` and `useEffect` hooks to manage application state and side effects.
- **Spreadsheet Model**: A 2D array structure to represent the grid of cells, allowing for easy manipulation of cell data and dependencies.

## Installation
To run the application locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/devespanchariya/zeotap.git
   cd zeotap
