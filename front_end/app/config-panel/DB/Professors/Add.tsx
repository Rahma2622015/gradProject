"use client";
import React, { useState } from "react";
import styles from "./Add.module.css";

const AddProfessorForm = ({ onProfessorAdded }) => {
  const [professor, setProfessor] = useState({
    name: "",
    description: "",
    name_arabic: "",
    description_arabic: "",
  });

  const handleChange = (e) => {
    setProfessor({ ...professor, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("https://192.168.1.9:3001/professor", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(professor),
      });

      const result = await response.json();

      if (response.ok) {
        alert("professor added successfully");
        onProfessorAdded(result);
        setProfessor({ name: "", description: "",name_arabic:"",description_arabic:""});
      } else {
        alert(`Error: ${result.error}`);
      }
    } catch (err) {
      alert("Failed to connect to server");
      console.error(err);
    }
  };

  return (
    <form onSubmit={handleSubmit} className={styles.form}>
      <h3 className={styles.h3}>Add New Professor</h3>
      <input name="name" value={professor.name} onChange={handleChange} placeholder="professor Name" required className={styles.input} />
      <input name="description" value={professor.description} onChange={handleChange} placeholder="Description" required className={styles.input} />
       <input name="name_arabic" value={professor.name_arabic} onChange={handleChange} placeholder="professor Name Arabic" required className={styles.input} />
      <input name="description_arabic" value={professor.description_arabic} onChange={handleChange} placeholder="Description Arabic" required className={styles.input} />
      <button type="submit" className={styles.button}>Add Course</button>
    </form>
  );
};

export default AddProfessorForm;
