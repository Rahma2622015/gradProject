"use client";

import Image from "next/image";
// توفر المكتبة تصاميم جاهزة لعناصر الدردشة مثل الرسائل، قائمة المحادثات، شريط الإدخال، ومؤشرات الكتابة
import '@chatscope/chat-ui-kit-styles/dist/default/styles.min.css';
//مكونات للchat
import {MainContainer,ChatContainer, MessageList, Message, MessageInput,} from "@chatscope/chat-ui-kit-react";
import styles from "./chatstyle.module.css";
import Link from "next/link";
//hooks
import React, { useEffect, useState } from 'react';
import { useTheme } from "../context/ThemeContext";
function ChatPage(){
   const { isDarkMode } = useTheme();
   useEffect(() => {
        // بشوف هل عملت reload و لا لا
         const entries = performance.getEntriesByType("navigation");
        if (entries.length > 0 && (entries[0] as PerformanceNavigationTiming).type === "reload") {
          // بشوف هل انا في ال home اصلا و لا لا
          if (window.location.pathname !== "/") {
            window.location.href = "/";
          }
        }
     }, []);

    //علشان اغير ال title بتاع الصفحة
    useEffect(()=> {
      document.title='Chatpage';
    });
    //بشيل تنسيقات ال html
    const stripHtmlTags = (html: string): string => {
      const doc = new DOMParser().parseFromString(html, "text/html");
      return doc.body.textContent || "";
    };
    const handlePaste = (event: React.ClipboardEvent<HTMLDivElement>): void => {
      event.preventDefault();
      const text = stripHtmlTags(event.clipboardData.getData("text/html")); // اشيل التنسيقات
      const cleanedText = text.replace(/\n+/g, " ").trim(); // اشيل ال new line
      document.execCommand("insertText", false, cleanedText); // لما اعمل past اعمل من غير التنسيقات
    };

    const [sessionMessage, setSessionMessage] = useState<string>("");
    const [isLoading, setISLoading] = useState<boolean>(false);
    const closeSession = async () => {
        const id = localStorage.getItem("client_id"); // الحصول على ID من التخزين
        if (!id) {
          console.error(" ID is missing");
          setSessionMessage(" ID is missing.");
          return;
        }
      try{
        setISLoading(true);
        const response = await fetch('https://192.168.1.4:5000/close-session', {
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

  //و متغير state يحتوي على الرسائل التي سيتم عرضها في الدردشة
  const [messages, setMessages] = useState([//array
    {
       message: "Hello, I'm Lazez! Ask me !",
        sender: "Lazez",
        direction: "incoming",
    }
  ]);

  //بتضيف الرسايل الجديده
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
      //علشان اعرض الرسالة الي بتتبعت
      console.log('Sending message:', message);
      // إرسال الرسالة إلى server عبر POST
      //في ال fetch المفروض احط لينك ال server
      const token=localStorage.getItem("client_id");
      console.log(JSON.stringify({ userMessage:message,id:token}))
      const response = await fetch('https://192.168.1.4:5000/messages', {
        method: "POST",
         headers: {
             "Content-Type": "application/json",
          },
        //بتحول الكود ل jason
        body: JSON.stringify({ userMessage: cleanedMessage,id: token}),
      });
        console.log("Payload sent to server:", JSON.stringify({ userMessage: message, id: token }));
      //عرض الرد
      console.log('Received response:', response);
      if (response.ok) {
         const data = await response.json();
         if (data === undefined || !data.reply) {
            console.log("Error in data: No reply found");
            return;
          }
          console.log(data);
          const replyMessage = {
            message:data.reply, // الرد من server
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

  //بمسح كل الشات معادا الرسالة التعريفية للشات
  const deletchat=()=>{
    setMessages([messages[0]]);
  };
  //width=1520px

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
                    // بتكرار كل رسالة موجودة في ال array messages
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