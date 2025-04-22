"use client";
import React, { useState } from "react";
import styles from "./Add.module.css";

const AddQuestionForm = ({ onQuestionAdded }) => {
  const [question, setQuestion] = useState({
    question: "",
    course_id: "",
    question_arabic:"",
  });

  const handleChange = (e) => {
    setQuestion({ ...question, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("https://192.168.1.9:3001/question", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(question),
      });

      const result = await response.json();

      if (response.ok) {
        alert("Question added successfully");
        onQuestionAdded(result);
        setQuestion({ question: "", course_id: ""});
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
      <h3 className={styles.h3}>Add New Question</h3>
      <input name="question" value={question.question} onChange={handleChange} placeholder="Question" required className={styles.input} />
      <input name="course_id" value={question.course_id} onChange={handleChange} placeholder="CourseId" required className={styles.input} />
       <input name="question_arabic" value={question.question_arabic} onChange={handleChange} placeholder="question_arabic" required className={styles.input} />
      <button type="submit" className={styles.button}>Add Course</button>
    </form>
  );
};

export default AddQuestionForm;
