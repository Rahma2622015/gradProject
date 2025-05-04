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
        if (Array.isArray(files)) {
          setJsonFiles(files);
        } else {
          setJsonFiles([]);
        }
      } catch (err) {
        console.error("Error fetching JSON files:", err);
        setJsonFiles([]);
      }
    };
    fetchJsonFiles();
  }, []);

  const fetchSelectedFile = async (selectedFile) => {
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
      const response = await fetch(`${variables.save_json}/${fileName}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
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

 function deleteAtPath(obj, path) {
  if (!obj || !Array.isArray(path) || path.length === 0) return;

  const lastKey = path[path.length - 1];
  const parentPath = path.slice(0, -1);
  const parent = parentPath.reduce((acc, key) => acc?.[key], obj);

  if (!parent) return;

  if (Array.isArray(parent)) {
    const index = parseInt(lastKey, 10);
    if (!isNaN(index)) {
      parent.splice(index, 1);
    }
  } else if (typeof parent === "object" && lastKey in parent) {
    delete parent[lastKey];
  }

  const target = parentPath.reduce((acc, key) => acc?.[key], obj);
  if (
    (Array.isArray(target) && target.length === 0) ||
    (typeof target === "object" && target !== null && Object.keys(target).length === 0)
  ) {
    deleteAtPath(obj, parentPath);
  }
}


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

  const handleKeyChange = (e, fullPath) => {
    const newKey = e.target.value;
    if (!newKey) return;

    const keys = fullPath.split(".");
    const updated = { ...config };
    let current = updated;
    for (let i = 0; i < keys.length - 1; i++) {
      if (!current[keys[i]]) return;
      current = current[keys[i]];
    }

    const oldKey = keys[keys.length - 1];
    if (newKey !== oldKey) {
      current[newKey] = current[oldKey];
      delete current[oldKey];
      setConfig(updated);
    }
  };

  const filterConfig = (config, term) => {
    if (!term) return Object.entries(config);
    return Object.entries(config).filter(([key]) =>
      key.toLowerCase().includes(term.toLowerCase())
    );
  };

  const addNestedEntry = (parentKey) => {
    const newKey = prompt("Enter new key:");
    const newValue = prompt("Enter value (you can use JSON format):");

    if (newKey !== null && newValue !== null) {
      let parsedValue;
      try {
        parsedValue = JSON.parse(newValue);
      } catch {
        parsedValue = newValue;
      }

      const updated = { ...config };
      let current = updated;
      const keys = parentKey.split(".");
      for (let i = 0; i < keys.length; i++) {
        current = current[keys[i]];
      }

      current[newKey] = parsedValue;
      setConfig(updated);
    }
  };

  const renderObject = (obj, path = "") => {
    return Object.entries(obj).map(([key, value]) => {
      const fullPath = path ? `${path}.${key}` : key;

      return (
        <div key={fullPath} className={styles.entry}>
          <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <strong>{key}:</strong>
           <button
              className={`${styles.button} ${styles.deleteButton}`}
              onClick={() => {
                const pathArray = fullPath.split(".");
                const updated = JSON.parse(JSON.stringify(config));
                deleteAtPath(updated, pathArray);
                setConfig(updated);
              }}
              title="Delete this entry"
            >
              Delete
            </button>
          </div>
          {typeof value === "object" && value !== null ? (
            <div className={styles.nested}>
              {renderObject(value, fullPath)}
              <button
                className={styles.button}
                onClick={() => addNestedEntry(fullPath)}
                title="Add Entry"
              >
                Add Entry
              </button>
            </div>
          ) : (
            <input
              type="text"
              value={value === null || value === undefined ? "" : value}
              onChange={(e) => updateNestedValue(fullPath, e.target.value)}
              className={styles.input}
            />
          )}
        </div>)
    });
  };
  const addEntry = () => {
    if (!newKey) return;
    let parsedValue;
    try {
      parsedValue = JSON.parse(newValue);
    } catch {
      parsedValue = newValue;
    }
    const keys = newKey.split(".");
    const updated = { ...config };
    let current = updated;

    for (let i = 0; i < keys.length - 1; i++) {
      if (!current[keys[i]]) current[keys[i]] = {};
      current = current[keys[i]];
    }

    const lastKey = keys[keys.length - 1];

    if (Array.isArray(current[lastKey])) {
      current[lastKey].push(parsedValue);
    } else if (current[lastKey] && typeof current[lastKey] === "object") {
      current[lastKey] = { ...current[lastKey], ...parsedValue };
    } else if (current[lastKey] !== undefined) {
      current[lastKey] = [current[lastKey], parsedValue];
    } else {
      current[lastKey] = parsedValue;
    }

    setConfig(updated);
    setNewKey("");
    setNewValue("");
  };

  return (
    <div className={styles.container}>
      <h2 className={styles.title}> JSON Configuration Editor</h2>

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
          <option value=""> Select a JSON file</option>
          {jsonFiles.length > 0 ? (
            jsonFiles.map((file) => (
              <option key={file} value={file}>
                {file}
              </option>
            ))
          ) : (
            <option disabled> No JSON files available</option>
          )}
        </select>
      </div>

      <div className={styles.card}>
        <h3 className={styles.cardTitle}>
          Editing: <span className={styles.fileName}>{fileName || "No file selected"}</span>
        </h3>
        {Object.keys(config).length > 0 ? (
          renderObject(Object.fromEntries(filterConfig(config, searchTerm)))
        ) : (
          <p className={styles.emptyText}>
             No config loaded yet. Please select a file.
          </p>
        )}
      </div>

      <div className={styles.addEntrySection}>
        <h4 className={styles.sectionTitle}> Add New Entry</h4>
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
          <button onClick={addEntry} className={styles.addButton}>
             Add
          </button>
        </div>
      </div>

      <div className={styles.footer}>
        <button onClick={saveFileToServer} className={styles.saveButton}>
          {isLoading ? " Saving..." : " Save"}
        </button>
      </div>
    </div>
  );
}

export default ConfigPage;
