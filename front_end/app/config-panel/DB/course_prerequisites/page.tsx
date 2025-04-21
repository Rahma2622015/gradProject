"use client";
import { useState, useEffect } from "react";
import styles from "./pre.module.css";

 function DatabaseManager() {
  const [dbData, setDbData] = useState([]);
  const [editingRow, setEditingRow] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [fileName, setFileName] = useState("");
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const [databaseUploaded, setDatabaseUploaded] = useState(false);
 const [pre, setPre] = useState([]);
   const fetchPre = async () => {
      try {
        const response = await fetch("https://192.168.1.9:3001/pre");
        if (response.ok) {
          const data = await response.json();
          setDbData(data);
        } else {
          console.error("Failed to fetch pre:", response.status);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };
    useEffect(() => {
      if (databaseUploaded) {
        fetchPre();
      }
    }, [databaseUploaded]);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const fileType = file.type;
    const fileExtension = file.name.split(".").pop().toLowerCase();
    const reader = new FileReader();

    if (fileType === "application/json" || fileExtension === "json") {
      reader.onload = async (e) => {
        try {
          const json = JSON.parse(e.target.result);
          setDbData(json);
          setFileName(file.name);
          setUploadSuccess(true);
          await uploadDataToAPI(json);
        } catch (error) {
          alert("Invalid JSON file");
        }
      };
      reader.readAsText(file);
    } else if (fileType === "text/csv" || fileExtension === "csv") {
      reader.onload = async (e) => {
        const csvData = e.target.result;
        const rows = csvData.split("\n").filter(Boolean);
        const headers = rows[0].split(",");

        const jsonData = rows.slice(1).map((row) => {
          const values = row.split(",");
          const obj = {};
          headers.forEach((header, idx) => {
            obj[header.trim()] = values[idx]?.trim();
          });
          return obj;
        });

        setDbData(jsonData);
        setFileName(file.name);
        setUploadSuccess(true);
        await uploadDataToAPI(jsonData);
      };
      reader.readAsText(file);
    } else if (fileType === "application/octet-stream" || fileExtension === "sqlite" || fileExtension === "db") {
      alert("SQLite file detected. Sending it to the server to extract data.");
      const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await fetch("https://192.168.1.9:3001/upload-sqlite", {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          const data = await response.json();
          await fetchPre();
          setDbData(data);
          setFileName(file.name);
          setUploadSuccess(true);
          setDatabaseUploaded(true);
        } else {
          console.error("Failed to upload SQLite DB:", response.status);
        }
      } catch (error) {
        console.error("Error uploading SQLite DB:", error);
      }
    } else if (fileType === "text/xml" || fileExtension === "xml") {
      reader.onload = async (e) => {
        const parser = new DOMParser();
        const xmlDoc = parser.parseFromString(e.target.result, "text/xml");

        const items = Array.from(xmlDoc.getElementsByTagName("record"));
        const jsonData = items.map((item) => {
          const obj = {};
          Array.from(item.children).forEach((child) => {
            obj[child.tagName] = child.textContent;
          });
          return obj;
        });

        setDbData(jsonData);
        setFileName(file.name);
        setUploadSuccess(true);
        await uploadDataToAPI(jsonData);
      };
      reader.readAsText(file);
    } else {
      alert("Unsupported file type");
    }
  };

  const uploadDataToAPI = async (data) => {
    try {
      const response = await fetch("https://192.168.1.9:3001/pre", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        console.error("Failed to upload data:", response.status);
      }
    } catch (error) {
      console.error("Error uploading data:", error);
    }
  };


  const handleRowChange = (e, columnName, index) => {
    const updatedData = [...dbData];
    updatedData[index][columnName] = e.target.value;
    setDbData(updatedData);
  };

  const filterData = (data) => {
    if (Array.isArray(data)) {
      return data.filter((row) =>
        Object.values(row).some((val) =>
          val != null && val.toString().toLowerCase().includes(searchTerm.toLowerCase())
        )
      );
    } else if (data?.courses && Array.isArray(data.courses)) {
      return data.courses.filter((row) =>
        Object.values(row).some((val) =>
          val.toString().toLowerCase().includes(searchTerm.toLowerCase())
        )
      );
    }
    return [];
  };

  const filteredData = filterData(dbData);
  const headers = dbData.length > 0 ? Object.keys(dbData[0]) : [];

   return (
    <div className={styles.container}>
      <h2 className={styles.title}>Database Manager</h2>

      <div className={styles.uploadSection}>
        <label htmlFor="sqliteUpload" className={styles.uploadLabel}>
          Upload SQLite Database
        </label>
        <input
          id="sqliteUpload"
          type="file"
          accept=".sqlite,.db"
          onChange={handleFileUpload}
          className={styles.uploadInput}
        />
        {fileName && <p className={styles.fileName}>Current File: {fileName}</p>}
        {uploadSuccess && <p className={styles.successMessage}>Upload successful!</p>}
      </div>

      <input
        type="text"
        placeholder="Search"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className={styles.inputField}
        style={{ marginTop: "10px" }}
      />

      <div className={styles.tableWrapper}>
        <table className={styles.table}>
          <thead>
            <tr>
              {headers.map((header) => (
                <th key={header}>{header}</th>
              ))}
            </tr>
          </thead>
          <tbody>
             {filteredData.map((row, index) => (
              <tr key={index}>
                {headers.map((col) => (
                  <td key={`${index}-${col}`}>
                    {editingRow === index ? (
                      <input
                        value={row[col] || ""}
                        onChange={(e) => handleRowChange(e, col, index)}
                      />
                    ) : (
                      row[col]
                    )}
                  </td>
                ))}

              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DatabaseManager;
