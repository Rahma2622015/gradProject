"use client";
import React, { useState } from "react";
import styles from "./Add.module.css";
import variables from "../../../variables.json";
const AddAnswerForm = ({ onAnswerAdded }) => {
  const [answer, setAnswer] = useState({
    answer: "",
    score: "",
    question_id:"",
    answer_arabic:"",
    question:"",
  });

  const handleChange = (e) => {
    setAnswer({ ...answer, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(variables.answers, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(answer),
      });

      const result = await response.json();

      if (response.ok) {
        alert("Answer added successfully");
        onAnswerAdded(result);
        setAnswer({ answer: "", score: ""});
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
      <h3 className={styles.h3}>Add New Answer</h3>
      <input name="answer" value={answer.answer} onChange={handleChange} placeholder="answer" required className={styles.input} />
      <input name="score" value={answer.score} onChange={handleChange} placeholder="score" required className={styles.input} />
      <input name="question_id" value={answer.question_id} onChange={handleChange} placeholder="question_id" required className={styles.input} />
      <input name="answer_arabic" value={answer.answer_arabic} onChange={handleChange} placeholder="answer_arabic" required className={styles.input} />
      <input name="question" value={answer.question} onChange={handleChange} placeholder="question" required className={styles.input} />
      <button type="submit" className={styles.button}>Add Answer</button>
    </form>
  );
};

export default AddAnswerForm;
