"use client";
import React, { useState } from "react";
import styles from "./Add.module.css";
import variables from "../../../variables.json";
const AddCourseForm = ({ onCourseAdded }) => {
  const [course, setCourse] = useState({
    name: "",
    description: "",
    short_name: "",
    code: "",
    name_arabic:"",
    description_arabic:"",
    course_hours:"",
    course_degree:"",
    short_name_arabic:"",
    department_id:""

  });

  const handleChange = (e) => {
    setCourse({ ...course, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(variables.courses, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(course),
      });

      const result = await response.json();

      if (response.ok) {
        alert("Course added successfully");
        onCourseAdded(result);
        setCourse({ name: "", description: "", short_name: "", code: "",name_arabic:"",description_arabic:"",course_hours:"",course_degree:"",short_name_arabic:"",department_id:"" });
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
      <h3 className={styles.h3}>Add New Course</h3>
      <input name="name" value={course.name} onChange={handleChange} placeholder="Course Name" required className={styles.input} />
      <input name="description" value={course.description} onChange={handleChange} placeholder="Description" required className={styles.input} />
      <input name="short_name" value={course.short_name} onChange={handleChange} placeholder="Short Name" className={styles.input} />
      <input name="code" value={course.code} onChange={handleChange} placeholder="Code" required className={styles.input} />
       <input name="name_arabic" value={course.name_arabic} onChange={handleChange} placeholder="Course Name Arabic" required className={styles.input} />
      <input name="description_arabic" value={course.description_arabic} onChange={handleChange} placeholder="Description Arabic" required className={styles.input} />
      <input name="course_hours" value={course.course_hours} onChange={handleChange} placeholder="course_hours" className={styles.input} />
       <input name="course_degree" value={course.course_degree} onChange={handleChange} placeholder="course_degree" className={styles.input} />
       <input name="short_name_arabic" value={course.short_name_arabic} onChange={handleChange} placeholder="Short Name Arabic" className={styles.input} />
       <input name="department_id" value={course.department_id} onChange={handleChange} placeholder="department_id" className={styles.input} />
      <button type="submit" className={styles.button}>Add Course</button>
    </form>
  );
};

export default AddCourseForm;
