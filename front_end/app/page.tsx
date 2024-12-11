"use client"
import './globals.css';
import Image from "next/image";
import styles from "./page.module.css";
import Link from "next/link";
import React, { useEffect, useState} from 'react';
import { useTheme} from "./context/ThemeContext";
export default function Home() {
  //علشان اغير ال title بتاع الصفحة
  useEffect(()=> {
    document.title='Chatbot | Home';
  },[]);

  const { isDarkMode, toggleDarkMode } = useTheme();
  const[sessionMessage,setSessionMessage]=useState("");
  //علشان اعرف التحميل بتاع لصفحة
  const[isLoading,setISLoading]=useState(false);

  const startSession = async () => {
    try{
      setISLoading(true);
      const response = await fetch('https://192.168.1.4:5000/start-session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data=await response.json();
    if(data.message === 'Session started'){
          if (data.client_id) {
            localStorage.setItem('client_id', data.client_id);
            setSessionMessage(`Session started successfully. Session ID: ${data.client_id}`);
            console.log(`Session started successfully. Session ID:${data.client_id}`);
          } else {
            setSessionMessage('Session started successfully, but no session ID was received.');
            console.log('Session started successfully, but no session ID was received.');
          }

      }
      else {
        setSessionMessage('Failed to start the session: ' + data.message);
      }

    }
    catch(error){
        console.error('Error starting session:', error);
      }
      finally{
        setISLoading(false);
      }
    };
  return (
   <div className={` ${isDarkMode ? styles.dark : styles.light}`}>
     <main className={styles.container}>
      <div>
         <a
          onClick={toggleDarkMode}
           className={styles.modebutton}
          >
            <img
              src={isDarkMode ? "/night-mode.png" : "/brightness.png"}
              alt="mode image"
              width={30}
              height={30}
          />
         </a>
        </div>
        <div className={styles.hiddendiv}>{sessionMessage}</div>
        <Image
           className={styles.image}
           src="/output.png"
           alt="Robot image"
           width={500}
           height={400}
           /* بتضمن تحميل الصوره بشكل اسرع*/
           priority
           unoptimized // تعطيل التحسين التلقائي
        />
        <div className={styles.description}>
        <h2>Hello</h2>
        <h3>I am Lazez</h3>
        <h4>How can I help you?</h4>
        </div>
        <button onClick={startSession} disabled={isLoading} className={styles.nextbutton} >
          <Link href="/chat_page">
            I want to Know!
            &nbsp;&nbsp;&nbsp;
            <Image
              className={styles.logo}
              src="/next.png"
              alt="next page"
              width={25}
              height={25}
            />
          </Link>
        </button>
      </main>
    </div>
  );
}