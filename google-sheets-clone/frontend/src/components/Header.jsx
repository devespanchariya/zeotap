import React, { useState } from "react";
import {
  setFont,
  setSize,
  toggleBold,
  toggleItalic,
  toggleUnderline,
  textColor,
  backgroundColor,
  sum,
  average,
  max,
  min,
  count,
  trim,
  upper,
  lower,
  removeDuplicates,
  findAndReplace,
} from "../utils";

const Header = ({
  activeCell,
  activeSheetObject,
  setActiveSheetObject,
}) => {
  const [selectedFunction, setSelectedFunction] = useState("");

  // Event Handlers
  const handleFontChange = (e) => {
    const updatedSheet = setFont(e.target.value, activeCell, activeSheetObject);
    if (updatedSheet) setActiveSheetObject({ ...updatedSheet });
  };

  const handleSizeChange = (e) => {
    const updatedSheet = setSize(e.target.value, activeCell, activeSheetObject);
    if (updatedSheet) setActiveSheetObject({ ...updatedSheet });
  };

  const handleBoldClick = () => {
    const updatedSheet = toggleBold(activeCell, activeSheetObject);
    if (updatedSheet) setActiveSheetObject({ ...updatedSheet });
  };

  const handleItalicClick = () => {
    const updatedSheet = toggleItalic(activeCell, activeSheetObject);
    if (updatedSheet) setActiveSheetObject({ ...updatedSheet });
  };

  const handleUnderlineClick = () => {
    const updatedSheet = toggleUnderline(activeCell, activeSheetObject);
    if (updatedSheet) setActiveSheetObject({ ...updatedSheet });
  };

  const handleTextColorChange = (e) => {
    const updatedSheet = textColor(e.target.value, activeCell, activeSheetObject);
    if (updatedSheet) setActiveSheetObject({ ...updatedSheet });
  };

  const handleBackgroundColorChange = (e) => {
    const updatedSheet = backgroundColor(e.target.value, activeCell, activeSheetObject);
    if (updatedSheet) setActiveSheetObject({ ...updatedSheet });
  };

  const handleFunctionChange = (e) => {
    setSelectedFunction(e.target.value);
  };

  const executeFunction = () => {
    if (activeCell && activeSheetObject) {
      const range = Object.keys(activeSheetObject); // Example: Get all cells
      let result;

      switch (selectedFunction) {
        case "SUM":
          result = sum(range, activeSheetObject);
          break;
        case "AVERAGE":
          result = average(range, activeSheetObject);
          break;
        case "MAX":
          result = max(range, activeSheetObject);
          break;
        case "MIN":
          result = min(range, activeSheetObject);
          break;
        case "COUNT":
          result = count(range, activeSheetObject);
          break;
        case "TRIM":
          trim(activeCell, activeSheetObject);
          break;
        case "UPPER":
          upper(activeCell, activeSheetObject);
          break;
        case "LOWER":
          lower(activeCell, activeSheetObject);
          break;
        case "REMOVE_DUPLICATES":
          removeDuplicates(activeSheetObject);
          break;
        case "FIND_AND_REPLACE":
          // Implement find and replace logic here
          break;
        default:
          break;
      }

      if (result !== undefined) {
        alert(`Result: ${result}`);
      }
    }
  };

  return (
    <div className="header">
      {/* Navigation Menu */}
      <div className="nav-content">
        <div className="nav-menu">File</div>
        <div className="nav-menu nav-active">Home</div>
        <div className="nav-menu">Insert</div>
        <div className="nav-menu">Layout</div>
        <div className="nav-menu">Help</div>
      </div>

      {/* Cell Styles */}
      <div className="cell-styles">
        <span className="material-icons copy" onClick={() => console.log("Copy clicked!")}>
          content_copy
        </span>
        <span className="material-icons cut" onClick={() => console.log("Cut clicked!")}>
          content_cut
        </span>
        <span className="material-icons paste" onClick={() => console.log("Paste clicked!")}>
          content_paste
        </span>

        {/* Font Selection */}
        <select onChange={handleFontChange} className="font-family-selection font-family">
          <option value="monospace">MonoSpace</option>
          <option value="sans-serif">Sans-serif</option>
          <option value="fantasy">Fantasy</option>
          <option value="cursive">Cursive</option>
        </select>

        {/* Font Size Selection */}
        <select onChange={handleSizeChange} className="font-size-selection font-size">
          <option value="14">14</option>
          <option value="16">16</option>
          <option value="18">18</option>
          <option value="20">20</option>
        </select>

        {/* Text Formatting */}
        <span className="material-icons bold" onClick={handleBoldClick}>
          format_bold
        </span>
        <span className="material-icons italic" onClick={handleItalicClick}>
          format_italic
        </span>
        <span className="material-icons underline" onClick={handleUnderlineClick}>
          format_underlined
        </span>

        {/* Alignment */}
        <span className="material-icons alignment" onClick={() => console.log("Align Left")}>
          format_align_left
        </span>
        <span className="material-icons alignment" onClick={() => console.log("Align Center")}>
          format_align_center
        </span>
        <span className="material-icons alignment" onClick={() => console.log("Align Right")}>
          format_align_right
        </span>

        {/* Colors */}
        <div className="color-prop">
          <label htmlFor="color" className="material-icons">
            format_color_text
          </label>
          <input
            id="color"
            type="color"
            onChange={handleTextColorChange}
          />
        </div>

        <div className="color-prop">
          <label htmlFor="bgcolor" className="material-icons">
            format_color_fill
          </label>
          <input
            id="bgcolor"
            type="color"
            onChange={handleBackgroundColorChange}
          />
        </div>
      </div>

      {/* Function Selection */}
      <div className="function-selection">
        <select onChange={handleFunctionChange} className="function-dropdown">
          <option value="">Select Function</option>
          <option value="SUM">SUM</option>
          <option value="AVERAGE">AVERAGE</option>
          <option value="MAX">MAX</option>
          <option value="MIN">MIN</option>
          <option value="COUNT">COUNT</option>
          <option value="TRIM">TRIM</option>
          <option value="UPPER">UPPER</option>
          <option value="LOWER">LOWER</option>
          <option value="REMOVE_DUPLICATES">REMOVE_DUPLICATES</option>
          <option value="FIND_AND_REPLACE">FIND_AND_REPLACE</option>
        </select>
        <button onClick={executeFunction}>Execute</button>
      </div>

      {/* Active Cell and Formula */}
      <div className="active-cell-data">
        <b className="address-bar">{activeCell || "Null"}</b>
        <img
          className="formula-icon"
          src="https://img.icons8.com/ios/50/000000/formula-fx.png"
          alt="Formula Icon"
        />
        <input
          className="formula-bar"
          type="text"
          onChange={(e) => console.log("Formula:", e.target.value)}
        />
      </div>
    </div>
  );
};

export default Header;