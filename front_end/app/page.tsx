"use client";
import './globals.css';
import Image from "next/image";
import styles from "./page.module.css";
import Link from "next/link";
import React, { useEffect, useState, useRef } from 'react';
import { useTheme as useThemeMode } from "./context/ThemeContext";
import { useTheme as useThemeColor } from "./context/ThemeColor";
import { motion } from "framer-motion";
import variables from "./variables.json";

export default function Home() {
  useEffect(() => {
    document.title = 'Chatbot | Home';
  }, []);
  const [isClicked, setIsClicked] = useState(false);

  const handleClick = () => {
    setIsClicked(!isClicked);
  };

  const [isShowlist, setList] = useState(false);
  const dropdownRef = useRef<HTMLDivElement | null>(null);

  const dropList = () => {
    setList(!isShowlist);
  };

  const handleClickOutside = (event: MouseEvent) => {
    if (!dropdownRef.current || dropdownRef.current.contains(event.target as Node)) {
      return;
    }
    setList(false);
  };

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const { isDarkMode, toggleDarkMode } = useThemeMode();
  const { themeColor, changeTheme } = useThemeColor();
  const [sessionMessage, setSessionMessage] = useState("");
  const [isLoading, setISLoading] = useState(false);

  useEffect(() => {
    document.body.className = `theme-${themeColor} ${isDarkMode ? 'dark-mode' : 'light-mode'}`;
  }, [themeColor, isDarkMode]);

  const startSession = async () => {
    try {
      setISLoading(true);
      const response = await fetch(variables.start_session, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      if (data.message === 'Session started') {
        if (data.client_id) {
          sessionStorage.setItem('client_id', data.client_id);
          setSessionMessage(`Session started successfully. Session ID: ${data.client_id}`);
          console.log(`Session started successfully. Session ID:${data.client_id}`);
        } else {
          setSessionMessage('Session started successfully, but no session ID was received.');
          console.log('Session started successfully, but no session ID was received.');
        }
      } else {
        setSessionMessage('Failed to start the session: ' + data.message);
      }
    } catch (error) {
      console.error('Error starting session:', error);
    } finally {
      setISLoading(false);
    }
  };

  return (
    <div className={` ${isDarkMode ? styles.dark : styles.light}`}>
      <main className={styles.container}>
          <div className={styles.hiddendiv}>
          {isLoading ? (
            <p>Loading...</p>
          ) : (
            <p>{sessionMessage}</p>
          )}
      </div>
          <div>
            <a onClick={toggleDarkMode} className={styles.modebutton}>
              <Image
                src={isDarkMode ? "/night-mode.png" : "/brightness.png"}
                alt="mode image"
                width={46}
                height={46}
              />
            </a>
          </div>
          <div ref={dropdownRef} className={styles.menu}>
            <button className={styles.dropdown_btn} onClick={dropList}>
              <Image
                src="/color-wheel.png"
                alt="list"
                width={46}
                height={46}
              />
            </button>
            {isShowlist && (
              <ul className={styles.dropdown_list}>
                <li onClick={() => changeTheme("mov")}>
                  <Image src={isDarkMode ? "/Ellipse_4-removebg-preview.png" : "/Ellipse_4.png"} alt="color1" width={30} height={30} />
                </li>
                <li onClick={() => changeTheme("blue")}>
                  <Image src={isDarkMode ? "/Ellipse_5-removebg-preview.png" : "/Ellipse_5.png"} alt="color2" width={30} height={30} />
                </li>
                <li onClick={() => changeTheme("bage")}>
                  <Image src={isDarkMode ? "/Ellipse_6-removebg-preview.png" : "/Ellipse_6.png"} alt="color3" width={30} height={30} />
                </li>
                 <li onClick={() => changeTheme("babygreen")}>
                  <Image src={isDarkMode ? "/Ellipse_8-removebg-preview.png" : "/Ellipse_7-removebg-preview.png"} alt="color4" width={30} height={30} />
                </li>
                 <li onClick={() => changeTheme("white")}>
                  <Image src={isDarkMode ? "/Ellipse_9-removebg-preview.png" : "/Ellipse_8__2_-removebg-preview.png"} alt="color5" width={30} height={30} />
                </li>
                 <li onClick={() => changeTheme("green")}>
                  <Image src={isDarkMode ? "/Ellipse 8.png" : "/Ellipse 13.png"} alt="color5" width={30} height={30} />
                </li>
                 <li onClick={() => changeTheme("red")}>
                  <Image src={isDarkMode ? "/Ellipse 9.png" : "/Ellipse 14.png"} alt="color5" width={30} height={30} />
                </li>
                 <li onClick={() => changeTheme("purple")}>
                  <Image src={isDarkMode ? "/Ellipse 11.png" : "/Ellipse 12.png"} alt="color5" width={30} height={30} />
                </li>
              </ul>
            )}
          </div>

      <motion.div
        animate={{
            y: [0, -25, 0],
            rotate: isClicked ? [0, 10, -10, 10, -10, 0] : 0,
          }}
         transition={{
            y: { repeat: Infinity, repeatType: "reverse", duration: 1 },
            rotate: { duration: 0.5 },
          }}
        onClick={handleClick}
      >
        <Image
          src="/robot1.png"
          alt="Robot "
          className={styles.image}
          width={400}
          height={300}
          priority
          unoptimized
        />
      </motion.div>
      <div className={styles.description}>
        {isClicked ? (
          <motion.h3
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            <div className={styles.container}>
              <div>Hello! 👋 My name is <span className={styles.bold}>Lazeez</span>,</div>
              <div>
                and I'm here to help <em>new students</em> at the <span className={styles.bold}>Faculty of Science</span>
              </div>
              <div>
                who need info about the <span className={styles.highlight}>Computer Science program</span>
              </div>
              <div>
                and dual degree programs in <span className={styles.bold}>Computer Science</span>,
              </div>
              <div>or who simply have some questions and curiosities! 🤔</div>

              <div className="mt-4">This assistant was proudly created by:</div>
              <ul style={{ listStyle: "disc", paddingLeft: "1.5rem" }}>
                <li><span className={styles.bold}>Hagar Mohamed Kamel</span></li>
                <li><span className={styles.bold}>Heba Gamal Ahmed</span></li>
                <li><span className={styles.bold}>Hagar Basuony Attia</span></li>
                <li><span className={styles.bold}>Rahma Mohamed Sayed</span></li>
              </ul>

              <div className={styles.subtle}>— Computer Science students at Ain Shams University 💻🎓</div>
            </div>
          </motion.h3>
        ) : (
          <motion.div
            initial={{ opacity: 1 }}
            animate={{ opacity: isClicked ? 0 : 1 }}
            transition={{ duration: 0.5 }}
          >
            <h2>Hello</h2>
            <h3>I am Lazeez</h3>
            <h4>How can I help you?</h4>
          </motion.div>
        )}
      </div>
       <Link href="/chat_page">
         <button onClick={startSession} disabled={isLoading} className={styles.nextbutton}>
            I want to Know!
         </button>
       </Link>
       <motion.div
      className={styles.cornerImage}
      whileHover={{ scale: 2.5 }}
      transition={{ type: "spring", stiffness: 300 }}
    >
      <Image
        src="/chat_bot.png"
        alt="Image"
        width={100}
        height={100}
      />
    </motion.div>

      </main>
    </div>
  );
}
