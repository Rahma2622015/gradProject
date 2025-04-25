"use client";
import { useState, useEffect } from "react";
import styles from "./Config.module.css";
import variables from "../../variables.json";
function ConfigPage() {
  const [config, setConfig] = useState({});
  const [newKey, setNewKey] = useState("");
  const [newValue, setNewValue] = useState("");
  const [fileName, setFileName] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [isLoading, setIsLoading] = useState(false);
   const [jsonFiles, setJsonFiles] = useState([]);

 useEffect(() => {
  const fetchJsonFiles = async () => {
    try {
      const res = await fetch(variables.list_json_files);
      const files = await res.json();
      console.log("Files from API:", files);  // تحقق مما يتم استلامه من الـ API

      if (Array.isArray(files)) {
        setJsonFiles(files);
      } else {
        console.error("Unexpected response format:", files);
        setJsonFiles([]); // safe fallback
      }
    } catch (err) {
      console.error("Error fetching JSON files:", err);
      setJsonFiles([]); // fallback in case of error
    }
  };

  fetchJsonFiles();
}, []);


  const fetchSelectedFile = async (selectedFile: string) => {
  setIsLoading(true);
  try {
    const encodedPath = encodeURIComponent(selectedFile);
    const res = await fetch(`${variables.get_json}/${encodedPath}`);
    const data = await res.json();
    setConfig(data.content);
    setFileName(selectedFile);
  } catch (err) {
    console.error("Failed to load JSON:", err);
  } finally {
    setIsLoading(false);
  }
};


 const saveFileToServer = async () => {
  if (!fileName) return alert("No file loaded.");

  setIsLoading(true);
  try {
    const response = await fetch(`https://192.168.1.9:3001/save_json/${fileName}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ content: config }),
    });

    const data = await response.json();
    if (response.ok) {
      alert("File saved successfully!");
    } else {
      alert(data.message || "Failed to save file");
    }
  } catch (error) {
    console.error("Save error:", error);
  } finally {
    setIsLoading(false);
  }
};
    const deleteKeyByPath = (path) => {
      const keys = path.split(".");
      const updated = { ...config };
      let current = updated;

      for (let i = 0; i < keys.length - 1; i++) {
        if (!current[keys[i]]) return;
        current = current[keys[i]];
      }

      delete current[keys[keys.length - 1]];
      setConfig(updated);
    };

  const updateNestedValue = (path, value) => {
    const keys = path.split(".");
    const updated = { ...config };
    let current = updated;

    for (let i = 0; i < keys.length - 1; i++) {
      if (!current[keys[i]]) current[keys[i]] = {};
      current = current[keys[i]];
    }

    current[keys[keys.length - 1]] = value;
    setConfig(updated);
  };

  const handleKeyChange = (e, oldKey) => {
    const newKey = e.target.value;
    if (newKey && newKey !== oldKey) {
      const updated = { ...config };
      updated[newKey] = updated[oldKey];
      delete updated[oldKey];
      setConfig(updated);
    }
  };

  const filterConfig = (config, term) => {
    if (!term) return Object.entries(config);
    return Object.entries(config).filter(([key]) =>
      key.toLowerCase().includes(term.toLowerCase())
    );
  };

  const renderObject = (obj, parentKey = "", level = 0) => {
    return Object.entries(obj).map(([key, value]) => {
      const fullPath = parentKey ? `${parentKey}.${key}` : key;
      const paddingLeft = `${level * 20}px`;

      if (searchTerm && !key.toLowerCase().includes(searchTerm.toLowerCase())) {
        return null;
      }

      return (
        <div key={fullPath} className={styles.row} style={{ paddingLeft }}>
          <input
            type="text"
            value={key}
            onChange={(e) => handleKeyChange(e, key)}
            className={styles.input}
          />
          <label className={styles.label}>:</label>
          {typeof value === "object" && value !== null ? (
            <div className={styles.nestedObject}>
              {renderObject(value, fullPath, level + 1)}
            </div>
          ) : (
            <input
              type="text"
              value={value}
              onChange={(e) => updateNestedValue(fullPath, e.target.value)}
              className={styles.input}
            />
          )}
         <button
            className={styles.deleteButton}
            onClick={() => deleteKeyByPath(fullPath)}
            title="Delete"
             >
            🗑️
          </button>
        </div>
      );
    }).filter(Boolean);
  };

  const addEntry = () => {
    if (!newKey) return;

    let parsedValue;
    try {
      parsedValue = JSON.parse(newValue);
    } catch (e) {
      parsedValue = newValue;
    }

    setConfig((prev) => ({ ...prev, [newKey]: parsedValue }));
    setNewKey("");
    setNewValue("");
  };

  return (
    <div className={styles.container}>
      <h2 className={styles.title}>JSON Configuration Editor</h2>

      <div className={styles.topBar}>
        <input
          type="text"
          placeholder=" Search Task by Name"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className={styles.searchInput}
        />

        <select
          value={fileName}
          onChange={(e) => fetchSelectedFile(e.target.value)}
          className={styles.selectInput}
        >
          <option value="">📂 Select a JSON file</option>
          {jsonFiles.length > 0 ? (
            jsonFiles.map((file) => (
              <option key={file} value={file}>
                {file}
              </option>
            ))
          ) : (
            <option disabled>لا توجد ملفات JSON</option>
          )}
        </select>

      </div>

      <div className={styles.card}>
        <h3 className={styles.cardTitle}>Editing: {fileName || "No file selected"}</h3>
        {Object.keys(config).length > 0 ? (
          renderObject(Object.fromEntries(filterConfig(config, searchTerm)))
        ) : (
          <p className={styles.emptyText}>No config loaded yet. Please select a file.</p>
        )}
      </div>

      <div className={styles.addEntrySection}>
        <h4 className={styles.sectionTitle}>➕ Add New Entry</h4>
        <div className={styles.inputGroup}>
          <input
            type="text"
            placeholder=" Key (e.g. app.name)"
            value={newKey}
            onChange={(e) => setNewKey(e.target.value)}
            className={styles.input}
          />
          <input
            type="text"
            placeholder=' Value (e.g. "My App" or {"nested":true})'
            value={newValue}
            onChange={(e) => setNewValue(e.target.value)}
            className={styles.input}
          />
          <button onClick={addEntry} className={styles.addButton}>Add</button>
        </div>
      </div>

      <button onClick={saveFileToServer} className={styles.saveButton}>
        {isLoading ? " Saving..." : " Save"}
      </button>
    </div>
  );
}

export default ConfigPage;

