"use client";
import { useState, useEffect } from "react";
import styles from "./question.module.css";
import AddQuestionForm from "./Add.tsx";
import variables from "../../../variables.json";
 function DatabaseManager() {
  const [dbData, setDbData] = useState([]);
  const [editingRow, setEditingRow] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [fileName, setFileName] = useState("");
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const [databaseUploaded, setDatabaseUploaded] = useState(false);
  const [question, setQuestion] = useState([]);
  const fetchQuestion = async () => {
      try {
        const response = await fetch(variables.question);
        if (response.ok) {
          const data = await response.json();
          setDbData(data);
        } else {
          console.error("Failed to fetch question:", response.status);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };
    useEffect(() => {
      if (databaseUploaded) {
        fetchQuestion();
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
        const response = await fetch(variables.upload_sqlite, {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          const data = await response.json();
          await fetchQuestion();
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
      const response = await fetch(variables.question, {
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

  const handleRowEdit = (index) => {
    setEditingRow(index);
  };

  const handleRowChange = (e, columnName, index) => {
    const updatedData = [...dbData];
    updatedData[index][columnName] = e.target.value;
    setDbData(updatedData);
  };

  const handleRowSave = async (index) => {
    const updatedRow = dbData[index];
    setEditingRow(null);

    try {
      const response = await fetch(`${variables.question}/${updatedRow.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updatedRow),
      });

      if (!response.ok) {
        const errorData = await response.json();
        alert(`Failed to save row. Error: ${errorData.error || response.status}`);
      } else {
        const updatedData = [...dbData];
        updatedData[index] = updatedRow;
        setDbData(updatedData);
        alert("Row saved successfully!");
      }
    } catch (error) {
      alert(`Error saving row: ${error.message}`);
    }
  };

  const handleRowDelete = async (index) => {
  const deletedRow = dbData[index];
  const confirmDelete = window.confirm(`Are you sure you want to delete ${deletedRow.name}?`);

  if (confirmDelete) {
    try {
      const response = await fetch(`${variables.question}/${deletedRow.id}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        alert(`Failed to delete row. Error: ${response.status}`);
      } else {
        const updatedData = dbData.filter((_, i) => i !== index);
        setDbData(updatedData);
        alert("Row deleted successfully!");
      }
    } catch (error) {
      alert(`Error deleting row: ${error.message}`);
    }
  }
};

  const handleAddRow = () => {
    const newRowObj = { id: Date.now(), name: "", type: "", status: "" };
    setDbData([...dbData, newRowObj]);
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
          val != null && val.toString().toLowerCase().includes(searchTerm.toLowerCase())
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
              <th>Edit</th>
              <th>Delete</th>
            </tr>
          </thead>
          <tbody>
            {filteredData.map((row, index) => (
              <tr key={row.id || index}>
                {headers.map((col) => (
                  <td key={col}>
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
                <td>
                  {editingRow === index ? (
                    <button onClick={() => handleRowSave(index)}>Save</button>
                  ) : (
                    <button onClick={() => handleRowEdit(index)}>Edit</button>
                  )}
                </td>
                <td>
                  <button onClick={() => handleRowDelete(index)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
        <AddQuestionForm onQuestionAdded={(newQuestion) => {
          setQuestion((prev) => [...prev, newQuestion]);
        }} />
    </div>
  );
};

export default DatabaseManager;
