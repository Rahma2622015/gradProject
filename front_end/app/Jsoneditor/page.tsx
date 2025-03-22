"use client"
import Bar from "../component/bar";
import styles from './jsoneditor.module.css'
import { useState , useEffect} from "react"
import {toast}from 'react-toastify'

function JSONEditor  () {
     useEffect(() => {
         const entries = performance.getEntriesByType("navigation");
        if (entries.length > 0 && (entries[0] as PerformanceNavigationTiming).type === "reload") {
          if (window.location.pathname !== "/") {
            window.location.href = "/";
          }
        }
     }, []);
    useEffect(() => {
    document.title = 'JSONEditor Page';
    }, []);
  const [jsonContent, setJsonContent] = useState("{}");

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file && file.type === "application/json") {
      const reader = new FileReader();
      reader.onload = (e) => {
        setJsonContent(e.target.result);
      };
      reader.readAsText(file);
    } else {
      toast.success("Please select a valid JSON file.");
    }
  };

  function saveJson  () {
   toast.success("JSON Saved!");
    console.log("JSON Data:", jsonContent);
  };

  return (
      <div>
      <div className={styles.menu}>
         <Bar className={styles.Bar}/>
      </div>
    <div className={styles.container}>
      <div className={styles.card}>
        <h2>JSON Editor</h2>
        <input type="file" accept=".json" onChange={handleFileUpload} className={styles.input} />
        <textarea
          rows="10"
          value={jsonContent}
          onChange={(e) => setJsonContent(e.target.value)}
          className={styles.textarea}
        ></textarea>
        <button onClick={saveJson} className={styles.button}>Save JSON</button>
      </div>
    </div>
    </div>
  );
};

export default JSONEditor;
