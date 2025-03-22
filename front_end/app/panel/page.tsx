"use client"
import Image from "next/image";
import styles from "./panel.module.css";
import Link from "next/link";
import {useState,useEffect} from 'react'
import {toast}from 'react-toastify'
import { useRouter } from "next/navigation";
function login() {
    const router = useRouter();
     useEffect(() => {
         const entries = performance.getEntriesByType("navigation");
        if (entries.length > 0 && (entries[0] as PerformanceNavigationTiming).type === "reload") {
          if (window.location.pathname !== "/") {
            window.location.href = "/";
          }
        }
     }, []);
    useEffect(() => {
    document.title = 'Login Page';
    }, []);
    const[email,setEmail]=useState("");
    const[password,setPassword]=useState("");
    const allowedUsers = [
        { email: "Rahma_Mohamed@gmail.com", password: "rahma123" },
        { email: "Heba_gamal@gmail.com", password: "heba123" },
      ];
    const formSubmitHandler = (e:React.FormEvent)=>{
        e.preventDefault();
        if(email==="")
           toast.error("Email is required");
        if(password==="")
            toast.error("Password is required");
        const validUser = allowedUsers.find(
          (user) => user.email === email && user.password === password
        );

        if (validUser) {
          toast.success("Login successful!");
          router.push("/GeneralSettings");
        } else {
          toast.error("Invalid email or password!");
        }
        console.log({email,password});
        }
    return(
    <section className={styles.container}>
        <div className={styles.card}>
            <h1  className={styles.title}>Log In</h1>
            <form onSubmit={formSubmitHandler} >
            <input
            className={styles.input}
            type="email"
            placeholder="Enter Your Email"
            value={email}
            onChange={(e)=> setEmail(e.target.value)}
            />
            <input
            className={styles.input}
            type="password"
            placeholder="Enter Your password"
            value={password}
            onChange={(e)=> setPassword(e.target.value)}
            />
            <button
            type="submit"
            className={styles.button}
            >
              Login
            </button>
            </form>
        </div>
    </section>
    );
}
export default login;