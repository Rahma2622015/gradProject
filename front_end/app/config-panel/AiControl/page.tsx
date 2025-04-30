'use client';

import { useEffect, useState } from 'react';
import styles from './ai.module.css';
import { toast } from 'react-toastify';
import variables from "../../variables.json";

export default function AIConfigPage() {
  const [config, setConfig] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchConfig = async () => {
  try {
    const res = await fetch(`${variables.API_BASE}/get_ai_config`);
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    const data = await res.json();
    setConfig(data);
  } catch (err) {
    console.error('Error loading config:', err);
    toast.error('Failed to load configuration.');
  }
};
    fetchConfig();
  }, []);

  const handleChange = (key: string, value: any) => {
    setConfig((prev: any) => ({ ...prev, [key]: value }));
  };

  const handleSave = async () => {
    setIsLoading(true);
    try {
      const res = await fetch(`${variables.API_BASE}/update_ai_config`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config),
      });
      const result = await res.json();

      if (res.ok) {
        toast.success(result.message || 'Configuration saved!');
      } else {
        toast.error(result.error || 'Something went wrong.');
      }
    } catch (err) {
      console.error('Error saving config:', err);
      toast.error('Failed to save configuration.');
    } finally {
      setIsLoading(false);
    }
  };

  if (!config) return <div className={styles.container}>
  <div className={styles.loader}></div>
  </div>;
  return (
    <div className={styles.container}>
      <h1 className={styles.heading}>AI Config Panel</h1>

      <div className={styles.field}>
        <label className={styles.label}>Threshold</label>
        <input
          type="number"
          className={styles.input}
          value={config.threshold}
          onChange={(e) => handleChange('threshold', Number(e.target.value))}
        />
      </div>

      <div className={styles.field}>
        <label className={styles.label}>Use Semantic Mapper</label>
        <button
          className={`${styles.button} ${
            config.use_semantic_mapper ? styles.enabled : styles.disabled
          }`}
          onClick={() =>
            handleChange('use_semantic_mapper', !config.use_semantic_mapper)
          }
        >
          {config.use_semantic_mapper ? 'Enabled' : 'Disabled'}
        </button>
      </div>

      <div className={styles.field}>
        <label className={styles.label}>Use Semantic ARMapper</label>
        <button
          className={`${styles.button} ${
            config.use_semantic_armapper ? styles.enabled : styles.disabled
          }`}
          onClick={() =>
            handleChange('use_semantic_armapper', !config.use_semantic_armapper)
          }
        >
          {config.use_semantic_armapper ? 'Enabled' : 'Disabled'}
        </button>
      </div>

      <button
        onClick={handleSave}
        disabled={isLoading}
        className={styles.saveButton}
      >
        {isLoading ? 'Saving...' : 'Save Changes'}
      </button>
    </div>
  );
}
