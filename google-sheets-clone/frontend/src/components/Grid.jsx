import React, { useState, useEffect } from "react";
import {
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

const Grid = ({
  activeSheetObject,
  setActiveSheetObject,
  activeCell,
  setActiveCell,
  setAddressBar,
}) => {
  const initialCellState = {
    fontFamily_data: "monospace",
    fontSize_data: "14",
    isBold: false,
    isItalic: false,
    textAlign: "start",
    isUnderlined: false,
    color: "#000000",
    backgroundColor: "#ffffff",
    content: "",
  };

  // Generates the grid dynamically
  const renderGrid = () => {
    const rows = [];
    for (let i = 1; i <= 100; i++) {
      const cells = [];
      // Add Row Header (SL.NO.)
      cells.push(
        <div key={`row-header-${i}`} className="grid-cell row-header">
          {i}
        </div>
      );

      // Add Columns (A-Z)
      for (let j = 65; j <= 90; j++) {
        const key = String.fromCharCode(j) + i; // E.g., "A1", "B1"
        cells.push(
          <div
            key={key}
            id={key}
            className="grid-cell"
            contentEditable
            draggable
            onDragStart={(e) => handleDragStart(e, key)}
            onDrop={(e) => handleDrop(e, key)}
            onFocus={() => cellFocus(key)}
            onInput={(e) => cellInput(key, e.target.innerText)}
          >
            {activeSheetObject[key]?.content || ""}
          </div>
        );
      }

      rows.push(
        <div key={`row-${i}`} className="row">
          {cells}
        </div>
      );
    }
    return rows;
  };

  // Handles cell focus (when a cell is clicked)
  const cellFocus = (key) => {
    setActiveCell(key);
    setAddressBar(key);

    const currentCell = activeSheetObject[key] || initialCellState;

    // Set UI states based on the current cell's properties
    document.querySelector(".font-family").value = currentCell.fontFamily_data;
    document.querySelector(".font-size").value = currentCell.fontSize_data;
    document.querySelector(".bold").style.backgroundColor = currentCell.isBold
      ? "#c9c8c8"
      : "#ecf0f1";
    document.querySelector(".italic").style.backgroundColor = currentCell.isItalic
      ? "#c9c8c8"
      : "#ecf0f1";
    document.querySelector(".underline").style.backgroundColor = currentCell.isUnderlined
      ? "#c9c8c8"
      : "#ecf0f1";
    document.querySelector("#color").value = currentCell.color;
    document.querySelector("#bgcolor").value = currentCell.backgroundColor;
    document.querySelector(".formula-bar").value = currentCell.content;
  };

  // Handles cell input (when typing inside a cell)
  const cellInput = (key, value) => {
    const updatedSheet = { ...activeSheetObject };
    // Basic validation: Allow only numbers or text
    if (value === "" || !isNaN(value) || /^[a-zA-Z]+$/.test(value)) {
      updatedSheet[key].content = value;
      setActiveSheetObject(updatedSheet);
    } else {
      alert("Please enter a valid number or text.");
    }
  };

  // Drag and Drop functionality
  const handleDragStart = (e, key) => {
    e.dataTransfer.setData("text/plain", key);
  };

  const handleDrop = (e, targetKey) => {
    const sourceKey = e.dataTransfer.getData("text/plain");
    if (sourceKey !== targetKey) {
      const updatedSheet = { ...activeSheetObject };
      updatedSheet[targetKey].content = updatedSheet[sourceKey].content;
      setActiveSheetObject(updatedSheet);
    }
  };

  // Initializes the sheet headers dynamically
  useEffect(() => {
    const gridHeader = document.querySelector(".grid-header");
    const rowHeader = document.createElement("div");
    rowHeader.className = "grid-header-col";
    rowHeader.innerText = "SL. NO.";
    gridHeader.append(rowHeader);

    for (let i = 65; i <= 90; i++) {
      const colHeader = document.createElement("div");
      colHeader.className = "grid-header-col";
      colHeader.innerText = String.fromCharCode(i);
      colHeader.id = String.fromCharCode(i);
      gridHeader.append(colHeader);
    }
  }, []); // Run only on mount

  return (
    <div className="grid">
      <div className="grid-header"></div>
      <div className="grid-body">{renderGrid()}</div>
    </div>
  );
};

export default Grid;