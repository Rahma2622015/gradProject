"use client";

import Image from "next/image";
import '@chatscope/chat-ui-kit-styles/dist/default/styles.min.css';
import {MainContainer,ChatContainer, MessageList, Message, MessageInput,} from "@chatscope/chat-ui-kit-react";
import styles from "./chatstyle.module.css";
import Link from "next/link";
import React, { useEffect, useState } from 'react';
import { useTheme } from "../context/ThemeContext";
function ChatPage(){
   const { isDarkMode } = useTheme();
   useEffect(() => {
         const entries = performance.getEntriesByType("navigation");
        if (entries.length > 0 && (entries[0] as PerformanceNavigationTiming).type === "reload") {
          if (window.location.pathname !== "/") {
            window.location.href = "/";
          }
        }
     }, []);

    useEffect(()=> {
      document.title='Chatpage';
    });
    const stripHtmlTags = (html: string): string => {
      const doc = new DOMParser().parseFromString(html, "text/html");
      return doc.body.textContent || "";
    };
    const handlePaste = (event: React.ClipboardEvent<HTMLDivElement>): void => {
      event.preventDefault();
      const text = stripHtmlTags(event.clipboardData.getData("text/html"));
      const cleanedText = text.replace(/\n+/g, " ").trim();
      document.execCommand("insertText", false, cleanedText);
    };

    const [sessionMessage, setSessionMessage] = useState<string>("");
    const [isLoading, setISLoading] = useState<boolean>(false);
    const closeSession = async () => {
        const id = localStorage.getItem("client_id");
        if (!id) {
          console.error(" ID is missing");
          setSessionMessage(" ID is missing.");
          return;
        }
      try{
        setISLoading(true);
        const response = await fetch('https://192.168.1.4:3001/close-session', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
         body: JSON.stringify({client_id: id}),
        });
          console.log("Response status:", response.status);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data=await response.json();
        console.log("response data:",data);
        if (data.message === 'Session closed') {
          setSessionMessage("Session closed successfully.");
          localStorage.removeItem('client_id');
          console.log("Session closed successfully.");
        } else {
          setSessionMessage('Failed to close session: ' + data.message);
          console.log("Failed to close session");
        }
      }
      catch(error){
          console.error('Error closing session:', error);
        }
        finally{
          setISLoading(false);
        }
      };

  const [messages, setMessages] = useState([//array
    {
       message: "Hello, I'm Lazez! Ask me !",
        sender: "Lazez",
        direction: "incoming",
    }
  ]);

  const handleSend=async(message:string) =>
    {
    const cleanedMessage = stripHtmlTags(message);
    const newMessage={
      message:cleanedMessage.trim(),
      direction:"outgoing",
      sender: "user" ,
    };

    const newMessages = [...messages, newMessage];
    setMessages(newMessages);
    try {
      console.log('Sending message:', message);
      const token=localStorage.getItem("client_id");
      console.log(JSON.stringify({ userMessage:message,id:token}))
      const response = await fetch('https://192.168.1.4:3001/messages', {
        method: "POST",
         headers: {
             "Content-Type": "application/json",
          },
        body: JSON.stringify({ userMessage: cleanedMessage,id: token}),
      });
        console.log("Payload sent to server:", JSON.stringify({ userMessage: message, id: token }));
      console.log('Received response:', response);
      if (response.ok) {
         const data = await response.json();
          if (data.message === "The time is up!") {
              alert("The time is up!");
              window.location.reload();
              return;
          }
         if (data === undefined || !data.reply) {
            console.log("Error in data: No reply found");
            return;
          }
          console.log(data);
          const replyMessage = {
            message:data.reply,
            direction: "incoming",
            sender: "Lazez",
          };
          setMessages((prevMessages) => [...prevMessages, replyMessage]);
     }
     else {
          console.error("Failed to send message to server");
     }
     }
    catch (error) {
        console.error("Error sending message:", error);
    }

    };

  const[isShowlist,setList]=useState(false);
  const dropList = () => {
    setList(!isShowlist);
  };

  const deletchat=()=>{
    setMessages([messages[0]]);
  };

    return(
       <main className={styles.container}
          style={{
            backgroundColor: isDarkMode ? "#2e4a5d" : "#709cb4",
            color: isDarkMode ? "#fff" : "#000",
          }}
        >
        <div className={styles.hiddendiv}>
            {isLoading ? (
              <p>Loading...</p>
            ) : (
              <p>{sessionMessage}</p>
            )}
        </div>
        <div className={styles.menu}>
            <button className={styles.dropdown_btn} onClick={dropList}>
            <Image
              className={styles.image}
              src="/list.png"
              alt="list"
              width={30}
              height={30}
            />
            </button>
            {isShowlist&&(
              <ul className={styles.dropdown_list}>
                <li>
                  <Link href="/">
                    <Image
                      className={styles.image}
                      onClick={closeSession}
                      src="/arrow.png"
                      alt="back button"
                      width={30}
                      height={30}
                    />
                  </Link>
                </li>
                <li>
                  <button onClick={deletchat}>
                  <Image
                      className={styles.image}
                      src="/bin.png"
                      alt="Delete button"
                      width={30}
                      height={30}
                    />
                  </button>
                </li>
              </ul>
            )}
            </div>
         <div  className={styles.ChatContainer}>
              <MainContainer>
                <ChatContainer>
                  <MessageList scrollBehavior="auto" >
                  {
                      messages.map((message, i) => {
                        const direction = message.direction === "incoming" || message.direction === "outgoing" ? message.direction : "incoming";
                        //const cleanedMessage = message.message.trim();
                        return <Message key={i} model={{message : message.message,direction:direction,sender:message.sender,position: "single"}}
                        style={{ whiteSpace: "pre-line" }}/>
                      })
                  }
                  </MessageList>
                  <MessageInput placeholder='Enter Your Question' onSend={handleSend} onPaste={handlePaste} />
                </ChatContainer>
              </MainContainer>
            </div>
      </main>
    )
  }
  export default ChatPage;