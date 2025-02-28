import React, { useState } from 'react';
import Header from './components/Header';
import Grid from './components/Grid';
import Footer from './components/Footer';
import './styles/App.css'; // Import your CSS styles

const App = () => {
  // State to manage the sheets, active sheet index, active cell, and active sheet object
  const [sheetsArray, setSheetsArray] = useState([]); // Array of sheets
  const [activeSheetIndex, setActiveSheetIndex] = useState(-1); // Index of the currently active sheet
  const [activeCell, setActiveCell] = useState(null); // Currently selected cell
  const [activeSheetObject, setActiveSheetObject] = useState({}); // Object representing the active sheet's data

  return (
    <div className="main">
      {/* Header component for toolbar and cell formatting options */}
      <Header 
        activeCell={activeCell} 
        setActiveCell={setActiveCell} 
        activeSheetObject={activeSheetObject} 
        setActiveSheetObject={setActiveSheetObject} 
        sheetsArray={sheetsArray} 
        setSheetsArray={setSheetsArray} 
        setActiveSheetIndex={setActiveSheetIndex} 
      />
      
      {/* Grid component for displaying and editing the spreadsheet */}
      <Grid 
        activeCell={activeCell} 
        setActiveCell={setActiveCell} 
        activeSheetObject={activeSheetObject} 
        setActiveSheetObject={setActiveSheetObject} 
      />
      
      {/* Footer component for managing sheets */}
      <Footer 
        sheetsArray={sheetsArray} 
        setSheetsArray={setSheetsArray} 
        setActiveSheetIndex={setActiveSheetIndex} 
      />
    </div>
  );
};

export default App;