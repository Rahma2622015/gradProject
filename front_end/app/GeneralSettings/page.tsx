"use client"
import Bar from "../component/bar";
import styles from './Setting.module.css'
import { useState ,useEffect} from "react";

function Setting() {
    useEffect(() => {
         const entries = performance.getEntriesByType("navigation");
        if (entries.length > 0 && (entries[0] as PerformanceNavigationTiming).type === "reload") {
          if (window.location.pathname !== "/") {
            window.location.href = "/";
          }
        }
     }, []);
    useEffect(() => {
    document.title = 'GeneralSetting Page';
    }, []);
  const [settings, setSettings] = useState({
    serverName: "",
    portNumber: "",
    ipAddress: "",
  });

  const handleChange = (e) => {
    setSettings({ ...settings, [e.target.name]: e.target.value });
  };

  const saveSettings = () => {
    alert("Settings Saved!");
    console.log(settings);
  };

  return (
      <div>
      <div className={styles.menu}>
         <Bar className={styles.Bar}/>
      </div>
    <div className={styles.container}>
      <div className={styles.card}>
        <h2 className={styles.title}>General Settings</h2>
        <label>Server Name</label>
        <input
        type="text"
        name="serverName"
        value={settings.serverName}
        onChange={handleChange}
         className={styles.input}
         />

        <label>Port Number</label>
        <input
        type="number"
        name="portNumber"
        value={settings.portNumber}
        onChange={handleChange}
        className={styles.input}/>

        <label>IP Address</label>
        <input
        type="text"
        name="ipAddress"
        value={settings.ipAddress}
        onChange={handleChange}
        className={styles.input}/>

        <button
        className={styles.button}
        onClick={saveSettings}
        >
        Save Changes
        </button>
      </div>
    </div>
    </div>
  );
};

export default Setting;