import React, { useState } from 'react';
import { HashRouter as Router } from 'react-router-dom'; // Change here
import Header from './components/Header';
import Grid from './components/Grid';
import Footer from './components/Footer';
import './styles/App.css'; // Import your CSS styles

const App = () => {
  const [sheetsArray, setSheetsArray] = useState([]);
  const [activeSheetIndex, setActiveSheetIndex] = useState(-1);
  const [activeCell, setActiveCell] = useState(null);
  const [activeSheetObject, setActiveSheetObject] = useState({});

  return (
    <Router>
      <div className="main">
        <Header 
          activeCell={activeCell} 
          setActiveCell={setActiveCell} 
          activeSheetObject={activeSheetObject} 
          setActiveSheetObject={setActiveSheetObject} 
          sheetsArray={sheetsArray} 
          setSheetsArray={setSheetsArray} 
          setActiveSheetIndex={setActiveSheetIndex} 
        />
        <Grid 
          activeCell={activeCell} 
          setActiveCell={setActiveCell} 
          activeSheetObject={activeSheetObject} 
          setActiveSheetObject={setActiveSheetObject} 
        />
        <Footer 
          sheetsArray={sheetsArray} 
          setSheetsArray={setSheetsArray} 
          setActiveSheetIndex={setActiveSheetIndex} 
        />
      </div>
    </Router>
  );
};

export default App;