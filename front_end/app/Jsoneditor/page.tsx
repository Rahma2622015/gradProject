"use client";
import { useState, useEffect } from "react";
import styles from "./jsoneditor.module.css";
import Bar from "../component/bar";
import { toast } from "react-toastify";

function JSONEditor() {
  const [jsonData, setJsonData] = useState({});
  const [searchKey, setSearchKey] = useState("");
  const [jsonValue, setJsonValue] = useState("");
  const [isKeyFound, setIsKeyFound] = useState(false);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file && file.type === "application/json") {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const parsedJson = JSON.parse(e.target.result);
          console.log("Loaded JSON:", parsedJson); // ✅ تأكيد تحميل JSON
          setJsonData(parsedJson);
          localStorage.setItem("jsonData", JSON.stringify(parsedJson));
          toast.success("JSON file loaded successfully!");
        } catch (error) {
          toast.error("Invalid JSON file format.");
        }
      };
      reader.readAsText(file);
    } else {
      toast.error("Please select a valid JSON file.");
    }
  };

  useEffect(() => {
    const storedJson = localStorage.getItem("jsonData");
    if (storedJson) {
      setJsonData(JSON.parse(storedJson));
    }
  }, []);

  const deepSearchKey = (obj, key) => {
    if (obj.hasOwnProperty(key)) {
      return obj[key];
    }
    for (const k in obj) {
      if (typeof obj[k] === "object" && obj[k] !== null) {
        const result = deepSearchKey(obj[k], key);
        if (result !== undefined) {
          return result;
        }
      }
    }
    return undefined;
  };

  const searchJsonKey = () => {
    if (!searchKey.trim()) {
      toast.error("Please enter a key to search!");
      return;
    }

    const value = deepSearchKey(jsonData, searchKey);
    if (value !== undefined) {
      setJsonValue(JSON.stringify(value, null, 2)); // ✅ عرض القيمة بشكل JSON منظم
      setIsKeyFound(true);
    } else {
      toast.error(`Key "${searchKey}" not found in JSON!`);
      setIsKeyFound(false);
    }
  };

  const deepUpdateKey = (obj, key, newValue) => {
    if (obj.hasOwnProperty(key)) {
      obj[key] = newValue;
      return true;
    }
    for (const k in obj) {
      if (typeof obj[k] === "object" && obj[k] !== null) {
        if (deepUpdateKey(obj[k], key, newValue)) {
          return true;
        }
      }
    }
    return false;
  };

  const saveJsonKey = () => {
    try {
      const parsedValue = JSON.parse(jsonValue);
      const updatedJson = { ...jsonData };
      if (deepUpdateKey(updatedJson, searchKey, parsedValue)) {
        setJsonData(updatedJson);
        localStorage.setItem("jsonData", JSON.stringify(updatedJson));
        toast.success("JSON Updated Successfully!");
      } else {
        toast.error("Key not found in JSON!");
      }
    } catch (error) {
      toast.error("Invalid JSON format!");
    }
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    if (file && file.type === "application/json") {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const parsedJson = JSON.parse(e.target.result);
          setJsonData(parsedJson);
          localStorage.setItem("jsonData", JSON.stringify(parsedJson));
          toast.success("JSON file loaded successfully!");
        } catch (error) {
          toast.error("Invalid JSON file format.");
        }
      };
      reader.readAsText(file);
    } else {
      toast.error("Please select a valid JSON file.");
    }
  };

  const getJsonValueStyle = () => {
    if (typeof jsonValue === "number") return styles.number;
    if (typeof jsonValue === "boolean") return styles.boolean;
    return styles.string;
  };

  return (
    <div>
      <div className={styles.menu}>
         <Bar className={styles.Bar}/>
      </div>
    <div className={styles.container} onDragOver={(e) => e.preventDefault()} onDrop={handleDrop}>
    <div className={styles.card}>
      <h2 className={styles.title}>JSON Editor</h2>

      <input type="file" accept=".json" onChange={handleFileUpload} className={styles.fileInput} />

      <input
        type="text"
        placeholder="Enter key to search..."
        value={searchKey}
        onChange={(e) => setSearchKey(e.target.value)}
        className={styles.input}
      />
      <button onClick={searchJsonKey} className={styles.button}>
        Search
      </button>

      {isKeyFound && (
        <div className={styles.card}>
          <h3>Value for "{searchKey}":</h3>
          <textarea
            rows="4"
            value={jsonValue}
            onChange={(e) => setJsonValue(e.target.value)}
            className={`${styles.textarea} ${getJsonValueStyle()}`}
          ></textarea>
          <button onClick={saveJsonKey} className={styles.button}>
            Save Changes
          </button>
        </div>
      )}
     </div>
    </div>
   </div>
  );
}

export default JSONEditor;
