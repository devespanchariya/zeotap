import React from 'react';

const Footer = ({ sheetsArray, setSheetsArray, setActiveSheetIndex }) => {
  const createNewSheet = () => {
    const newSheet = { name: `Sheet ${sheetsArray.length + 1}`, data: {} }; // Assign a default sheet name
    setSheetsArray([...sheetsArray, newSheet]); // Add the new sheet to the sheets array
    setActiveSheetIndex(sheetsArray.length); // Set the newly created sheet as active
  };

  const handleSheetClick = (index) => {
    setActiveSheetIndex(index);
  };

  return (
    <div className="footer">
      {/* Button to add a new sheet */}
      <button className="new-sheet" onClick={createNewSheet}>New Sheet</button>

      {/* Display the list of sheets as tabs */}
      <div className="sheets-list">
        {sheetsArray.map((sheet, index) => (
          <div
            key={index}
            className={`sheet-tab ${index === sheetsArray.indexOf(sheet) ? "active-sheet" : ""}`}
            onClick={() => handleSheetClick(index)}
          >
            {sheet.name}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Footer;