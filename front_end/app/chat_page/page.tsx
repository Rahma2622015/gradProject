"use client";

import Image from "next/image";
import "react-chat-elements/dist/main.css";
import { MessageBox, MessageList, Input, Button ,Message } from "react-chat-elements";
import styles from "./chatstyle.module.css";
import Link from "next/link";
import React, { useEffect, useState ,useRef } from "react";
import { useTheme } from "../context/ThemeContext";
import dynamic from "next/dynamic";

// تحميل مكتبة الإيموجي بطريقة ديناميكية لتجنب مشاكل SSR
const Picker = dynamic(() => import("emoji-picker-react"), { ssr: false });

function ChatPage() {
  const { isDarkMode } = useTheme();
  useEffect(() => {
         const entries = performance.getEntriesByType("navigation");
        if (entries.length > 0 && (entries[0] as PerformanceNavigationTiming).type === "reload") {
          if (window.location.pathname !== "/") {
            window.location.href = "/";
          }
        }
     }, []);
  useEffect(() => {
    document.title = "Chatpage";
  }, []);
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const [inputValue, setInputValue] = useState("");
  const emojiPickerRef = useRef(null);
    // عند تحميل الصفحة، نضيف مستمع للأحداث لغلق القائمة عند الضغط خارجها
    useEffect(() => {
      const handleClickOutside = (event) => {
        if (
          emojiPickerRef.current &&
          !emojiPickerRef.current.contains(event.target) &&
          !event.target.closest(".emojiButton")
        ) {
          setShowEmojiPicker(false);
        }
      };

      document.addEventListener("mousedown", handleClickOutside);
      return () => {
        document.removeEventListener("mousedown", handleClickOutside);
      };
    }, []);
   const addEmoji = (emojiObject: { emoji: string }) => {
      setInputValue((prevInput) => prevInput + emojiObject.emoji);
    };
    const removeEmojis = (text) => {
        return text.replace(/[\p{Emoji}\u200d]+/gu, ""); // إزالة الإيموجي فقط
    };

    const stripHtmlTags = (html: string): string => {
      const doc = new DOMParser().parseFromString(html, "text/html");
      return doc.body.textContent || "";
    };
    const handlePaste = (event: React.ClipboardEvent<HTMLDivElement>): void => {
      event.preventDefault();
      const text = stripHtmlTags(event.clipboardData.getData("text/html"));
      const cleanedText = text.replace(/<\/?[^>]+(>|$)/g, "").trim();
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
        const response = await fetch('https://192.168.1.6:3001/close-session', {
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
  const messagesEndRef = useRef<HTMLDivElement | null>(null);
    useEffect(() => {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]); // التمرير عند كل تحديث للمحادثة
  const handleSend = async (message: string = inputValue) => {
  if (!inputValue.trim()) return; // منع إرسال رسالة فارغة

    const messageWithoutEmojis = removeEmojis(inputValue); // حذف الإيموجي عند الإرسال فقط
  const newMessage = {
    message: inputValue,
    direction: "outgoing",
    sender: "user",
  };


    const newMessages = [...messages, newMessage];
    setMessages(newMessages);
    setInputValue(""); // تفريغ الإدخال بعد الإرسال
    try {
      console.log('Sending message:', message);
      const token=localStorage.getItem("client_id");
      //console.log(JSON.stringify({ userMessage:message,id:token}))
      const response = await fetch('https://192.168.1.6:3001/messages', {
        method: "POST",
         headers: {
             "Content-Type": "application/json",
          },
        body: JSON.stringify({ userMessage: messageWithoutEmojis,id: token}),
      });
      //  console.log("Payload sent to server:", JSON.stringify({ userMessage: message, id: token }));
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
  return (
    <main className={styles.container} onClick={() => setShowEmojiPicker(false)} >
       <div className={styles.hiddendiv}>
            {isLoading ? (
              <p>Loading...</p>
            ) : (
              <p>{sessionMessage}</p>
            )}
        </div>
      <div className={styles.menu}>
        <button className={styles.dropdown_btn} onClick={dropList}>
          <Image className={styles.image} src="/list.png" alt="list" width={30} height={30} />
        </button>
        {isShowlist && (
          <ul className={styles.dropdown_list}>
            <li>
              <Link href="/">
                <Image className={styles.image} src="/arrow.png" alt="back button" width={30} height={30} />
              </Link>
            </li>
            <li>
              <button onClick={deletchat}>
                <Image className={styles.image} src="/bin.png" alt="Delete button" width={30} height={30} />
              </button>
            </li>
          </ul>
        )}
      </div>

      <div className={styles.ChatContainer}>
       <MessageList
          className="message-list"
          lockable={true}
          toBottomHeight={"100%"}
          dataSource={messages.map((message, i) => ({
            id: i,
            position: message.direction === "incoming" ? "left" : "right",
            type: "text",
            text: message.message,
            title: message.sender,
            className: "message",
          }))}
       />
    {/* عنصر غير مرئي لمتابعة التمرير */}
    <div ref={messagesEndRef} />
    <div className={styles.inputContainer}>
      {showEmojiPicker && (
          <div ref={emojiPickerRef} className={styles.emojiPicker} onClick={(e) => e.stopPropagation()}>
            <Picker onEmojiClick={addEmoji} />
          </div>
      )}

         <Input
          placeholder="Enter Your Question"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === "Enter") {
              handleSend();
              e.preventDefault(); // لمنع حدوث كسر سطر جديد
            }
          }}
          multiline={false}
          rightButtons={
            <div className={styles.buttonsContainer}>
              <button
                className={styles.emojiButton}
                onClick={(e) => {
                  e.stopPropagation(); // لمنع غلق الإيموجي عند الضغط عليه
                  setShowEmojiPicker(!showEmojiPicker);
                }}
            >
              <Image src="/smile-plus.png" alt="EmojiButton" width={30} height={30} />
            </button>

            <button onClick={handleSend} className={styles.sendButton}>
              <Image src="/send.png" alt="Send" width={25} height={25} />
            </button>

          </div>
        }
      />
    </div>
    </div>
    </main>
  );
}



export default ChatPage;
