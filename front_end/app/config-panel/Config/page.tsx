"use client";
import { useState, useEffect } from "react";
import styles from "./Config.module.css";

function ConfigPage() {
  const [config, setConfig] = useState({});
  const [newKey, setNewKey] = useState("");
  const [newValue, setNewValue] = useState("");
  const [fileName, setFileName] = useState("config.json");
  const [searchTerm, setSearchTerm] = useState(""); // حالة البحث

  useEffect(() => {
    const savedConfig = localStorage.getItem("configData");
    if (savedConfig) {
      setConfig(JSON.parse(savedConfig));
    }
  }, []);

  useEffect(() => {
    localStorage.setItem("configData", JSON.stringify(config));
  }, [config]);

  // تحديث قيمة داخل كائن متداخل
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

  // دالة لتحديث اسم المفتاح (الـ task)
  const handleKeyChange = (e, oldKey) => {
    const newKey = e.target.value;
    if (newKey && newKey !== oldKey) {
      const updated = { ...config };
      updated[newKey] = updated[oldKey];
      delete updated[oldKey];
      setConfig(updated);
    }
  };

  // تصفية البيانات بناءً على البحث
  const filterConfig = (config, term) => {
    if (!term) return Object.entries(config); // إذا كان البحث فارغًا، عرض جميع البيانات
    return Object.entries(config).filter(([key]) => {
      return key.toLowerCase().includes(term.toLowerCase());
    });
  };

  // عرض الـ JSON بشكل متداخل مع الفلاتر
  const renderObject = (obj, parentKey = "", level = 0) => {
    return Object.entries(obj).map(([key, value]) => {
      const fullPath = parentKey ? `${parentKey}.${key}` : key;
      const paddingLeft = `${level * 20}px`;

      // تطبيق الفلترة على الـ key قبل العرض
      if (searchTerm && !key.toLowerCase().includes(searchTerm.toLowerCase())) {
        return null; // تجاهل العناصر التي لا تطابق البحث
      }

      return (
        <div key={fullPath} className={styles.row} style={{ paddingLeft }}>
          {/* الـ key يظهر هنا كـ input */}
          <input
            type="text"
            value={key}
            onChange={(e) => handleKeyChange(e, key)}
            className={styles.input}
          />
          <label className={styles.label}>:</label>
          {/* الـ value يمكن تعديله باستخدام input */}
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
        </div>
      );
    }).filter(Boolean); // إزالة العناصر التي تم تجاهلها (null)
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

  const deleteEntry = (key) => {
    const updatedConfig = { ...config };
    delete updatedConfig[key];
    setConfig(updatedConfig);
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const json = JSON.parse(e.target.result);
        setConfig(json);
        setFileName(file.name);
      } catch (error) {
        alert("Invalid JSON file");
      }
    };
    reader.readAsText(file);
  };

  const downloadJSON = () => {
    const blob = new Blob([JSON.stringify(config, null, 2)], {
      type: "application/json",
    });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = fileName;
    link.click();
  };

  // تصفية البيانات بناءً على البحث
  const filteredConfig = filterConfig(config, searchTerm);

  return (
    <div className={styles.container}>
      <h2 className={styles.title}>JSON Configuration Editor</h2>

      {/* حقل البحث */}
      <input
        type="text"
        placeholder="Search Task by Name"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className={styles.input}
      />

      <input type="file" accept="application/json" onChange={handleFileUpload} />

      <div className={styles.card}>
        <h3>Editing: {fileName}</h3>
        {filteredConfig.length > 0 ? (
          renderObject(Object.fromEntries(filteredConfig)) // تمرير الـ filteredConfig هنا
        ) : (
          <p>No tasks match the search. Start adding entries!</p>
        )}
      </div>

      <div className={styles.addEntry}>
        <input
          type="text"
          placeholder="Key (e.g. app.name)"
          value={newKey}
          onChange={(e) => setNewKey(e.target.value)}
          className={styles.input}
        />
        <input
          type="text"
          placeholder='Value (e.g. "My App" or {"nested":true})'
          value={newValue}
          onChange={(e) => setNewValue(e.target.value)}
          className={styles.input}
        />
        <button onClick={addEntry} className={styles.addButton}>Add</button>
      </div>

      <button onClick={downloadJSON} className={styles.downloadButton}>Download JSON</button>
    </div>
  );
}

export default ConfigPage;
