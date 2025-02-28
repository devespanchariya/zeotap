// src/utils.js

// Sets the font family of the active cell
export const setFont = (fontInput, activeCell, activeSheetObject) => {
  if (activeCell && activeSheetObject) {
    activeSheetObject[activeCell].fontFamily_data = fontInput;
    return activeSheetObject;
  }
  return null;
};

// Sets the font size of the active cell
export const setSize = (sizeInput, activeCell, activeSheetObject) => {
  if (activeCell && activeSheetObject) {
    activeSheetObject[activeCell].fontSize_data = sizeInput + "px";
    return activeSheetObject;
  }
  return null;
};

// Toggles bold formatting for the active cell
export const toggleBold = (activeCell, activeSheetObject) => {
  if (activeCell && activeSheetObject) {
    const isBold = activeSheetObject[activeCell].isBold;
    activeSheetObject[activeCell].isBold = !isBold;
    return activeSheetObject;
  }
  return null;
};

// Toggles italic formatting for the active cell
export const toggleItalic = (activeCell, activeSheetObject) => {
  if (activeCell && activeSheetObject) {
    const isItalic = activeSheetObject[activeCell].isItalic;
    activeSheetObject[activeCell].isItalic = !isItalic;
    return activeSheetObject;
  }
  return null;
};

// Toggles underline formatting for the active cell
export const toggleUnderline = (activeCell, activeSheetObject) => {
  if (activeCell && activeSheetObject) {
    const isUnderlined = activeSheetObject[activeCell].isUnderlined;
    activeSheetObject[activeCell].isUnderlined = !isUnderlined;
    return activeSheetObject;
  }
  return null;
};

// Sets the text color of the active cell
export const textColor = (colorInput, activeCell, activeSheetObject) => {
  if (activeCell && activeSheetObject) {
    activeSheetObject[activeCell].color = colorInput;
    return activeSheetObject;
  }
  return null;
};

// Sets the background color of the active cell
export const backgroundColor = (colorInput, activeCell, activeSheetObject) => {
  if (activeCell && activeSheetObject) {
    activeSheetObject[activeCell].backgroundColor = colorInput;
    return activeSheetObject;
  }
  return null;
};

// Aligns text within the active cell
export const alignment = (align, activeCell, activeSheetObject) => {
  if (activeCell && activeSheetObject) {
    activeSheetObject[activeCell].textAlign = align;
    return activeSheetObject;
  }
  return null;
};

// Copies the content of the active cell to the clipboard
export const copyToClipboard = (activeCell, activeSheetObject) => {
  if (activeCell && activeSheetObject) {
    navigator.clipboard.writeText(activeSheetObject[activeCell].content || "");
  }
};

// Cuts the content of the active cell (copies and clears the content)
export const cutToClipboard = (activeCell, activeSheetObject) => {
  if (activeCell && activeSheetObject) {
    navigator.clipboard.writeText(activeSheetObject[activeCell].content || "");
    activeSheetObject[activeCell].content = "";
    return activeSheetObject;
  }
  return null;
};

// Pastes clipboard content into the active cell
export const pasteFromClipboard = async (activeCell, activeSheetObject) => {
  if (activeCell && activeSheetObject) {
    const text = await navigator.clipboard.readText();
    activeSheetObject[activeCell].content = text;
    return activeSheetObject;
  }
  return null;
};

// Exports sheet data as a JSON file
export const exportSheets = (sheetsArray) => {
  const jsonData = JSON.stringify(sheetsArray);
  const blob = new Blob([jsonData], { type: "application/json" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "SheetData.json";
  link.click();
};

// Imports sheet data from a JSON file
export const importSheets = (file, setSheetsArray, setActiveSheetObject) => {
  const reader = new FileReader();
  reader.onload = () => {
    const data = JSON.parse(reader.result);
    setSheetsArray(data);
    setActiveSheetObject(data[0]); // Set the first sheet as active
  };
  reader.readAsText(file);
};

// Mathematical Functions
export const sum = (range, activeSheetObject) => {
  return range.reduce((acc, key) => acc + (parseFloat(activeSheetObject[key]?.content) || 0), 0);
};

export const average = (range, activeSheetObject) => {
  const total = sum(range, activeSheetObject);
  return total / range.length;
};

export const max = (range, activeSheetObject) => {
  return Math.max(...range.map(key => parseFloat(activeSheetObject[key]?.content) || -Infinity));
};

export const min = (range, activeSheetObject) => {
  return Math.min(...range.map(key => parseFloat(activeSheetObject[key]?.content) || Infinity));
};

export const count = (range, activeSheetObject) => {
  return range.filter(key => !isNaN(parseFloat(activeSheetObject[key]?.content))).length;
};

// Data Quality Functions
export const trim = (activeCell, activeSheetObject) => {
  if (activeCell && activeSheetObject) {
    activeSheetObject[activeCell].content = activeSheetObject[activeCell].content.trim();
    return activeSheetObject;
  }
  return null;
};

export const upper = (activeCell, activeSheetObject) => {
  if (activeCell && activeSheetObject) {
    activeSheetObject[activeCell].content = activeSheetObject[activeCell].content.toUpperCase();
    return activeSheetObject;
  }
  return null;
};

export const lower = (activeCell, activeSheetObject) => {
  if (activeCell && activeSheetObject) {
    activeSheetObject[activeCell].content = activeSheetObject[activeCell].content.toLowerCase();
    return activeSheetObject;
  }
  return null;
};

export const removeDuplicates = (activeSheetObject) => {
  const uniqueRows = {};
  for (const key in activeSheetObject) {
    const content = activeSheetObject[key].content;
    if (!uniqueRows[content]) {
      uniqueRows[content] = activeSheetObject[key];
    }
  }
  return uniqueRows;
};

export const findAndReplace = (searchText, replaceText, activeSheetObject) => {
  for (const key in activeSheetObject) {
    if (activeSheetObject[key].content.includes(searchText)) {
      activeSheetObject[key].content = activeSheetObject[key].content.replace(new RegExp(searchText, 'g'), replaceText);
    }
  }
  return activeSheetObject;
};