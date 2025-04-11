"use client";

import Image from "next/image";
import "react-chat-elements/dist/main.css";
import { MessageList, Input } from "react-chat-elements";
import styles from "./chatstyle.module.css";
import Link from "next/link";
import React, { useEffect, useState ,useRef } from "react";
import dynamic from "next/dynamic";
import { useRouter } from "next/navigation";
import { toast } from "react-toastify";
import variables from "../variables.json";
// تحميل مكتبة الإيموجي بطريقة ديناميكية لتجنب مشاكل SSR
const Picker = dynamic(() => import("emoji-picker-react"), { ssr: false });

function ChatPage() {
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
  const [exampleQuestions, setExampleQuestions] = useState<string[]>([]);
  const [isDropdownVisible, setDropdownVisible] = useState(false);
  const [isInputVisible, setInputVisible] = useState(true);
  const [selectedQuestion, setSelectedQuestion] = useState<string | null>(null);
  const emojiPickerRef = useRef<HTMLDivElement | null>(null);
  const messageListRef = useRef(null);

    // عند تحميل الصفحة، نضيف مستمع للأحداث لغلق القائمة عند الضغط خارجها
    useEffect(() => {
      const handleClickOutside = (event: Event) => {
       if (
          emojiPickerRef.current &&
          event.target instanceof Node &&
          !emojiPickerRef.current.contains(event.target)
        )
         {
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
    const removeEmojis = (text: string): string => {
      return text.replace(/[\p{Extended_Pictographic}]+/gu, "");
    };


    const stripHtmlTags = (html: string): string => {
      const doc = new DOMParser().parseFromString(html, "text/html");
      return doc.body.textContent || "";
    };
    const [sessionMessage, setSessionMessage] = useState<string>("");
    const [isLoading, setISLoading] = useState<boolean>(false);
    const closeSession = async () => {
        const id = sessionStorage.getItem("client_id");
        if (!id) {
          console.error(" ID is missing");
          setSessionMessage(" ID is missing.");
          return;
        }
      try{
        setISLoading(true);
        const response = await fetch(variables.close_session, {
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
   const toggleInputMethod = () => {
    setInputVisible(!isInputVisible);
    setDropdownVisible(false); // إغلاق أي قائمة أخرى عند التبديل
  };

    const handleQuestionClick = (question: string) => {
      setSelectedQuestion(question);
      setDropdownVisible(false);
      handleSend(question);
    };

    useEffect(() => {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);
    const router = useRouter();
    const [isClient, setIsClient] = useState(false);
    useEffect(() => {
      setIsClient(true); // تأكيد تحميل المكون على العميل
    }, []);

   useEffect(() => {
    if (!isClient) return;
    const clientId = sessionStorage.getItem("client_id");
    if (!clientId) {
      router.push("/");
    }
    }, [isClient, router]);
    const handleSend = async (message: string =selectedQuestion || inputValue) => {
     const finalMessage =stripHtmlTags(message) || inputValue;
     if (typeof finalMessage !== "string" || !removeEmojis(finalMessage).trim()) {
          toast.warn("Message is empty, please enter some text!");
          return;
     }

      const messageWithoutEmojis = removeEmojis(finalMessage); // حذف الإيموجي عند الإرسال فقط
      const newMessage = {
        message: finalMessage,
        direction: "outgoing",
        sender: "user",
     };

    const newMessages = [...messages, newMessage];
    setMessages(newMessages);
    setInputValue("");
    try {
      console.log('Sending message:', message);
      const token=sessionStorage.getItem("client_id");
      //console.log(JSON.stringify({ userMessage:message,id:token}))
      const response = await fetch(variables.ip_messages, {
        method: "POST",
         headers: {
             "Content-Type": "application/json",
          },
        body: JSON.stringify({ userMessage: messageWithoutEmojis,id: token}),
      });
      console.log('Received response:', response);
      if (response.ok) {
         const data = await response.json();
          if (data.message === "The time is up!") {
             toast.warn("The time is up!");
            setTimeout(() => {
                window.location.reload();
            }, 3000);
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
          if (data.list && data.list.length > 0) {
            setExampleQuestions(data.list);
            setInputVisible(false);
          } else {
            setInputVisible(true);
          }

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
    <main className={styles.container} onClick={() => setShowEmojiPicker(false)}  >
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
              <Link href="/" onClick={closeSession}>
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
          referance={messageListRef}
          className="message-list"
          lockable={true}
          toBottomHeight={"100%"}
          dataSource={messages.map((message, i) => ({
            id: i,
            position: message.direction === "incoming" ? "left" : "right",
            type: "text",
            text: message.message,
            title: message.sender === "user" ? "You" : message.sender,
            focus: false,
            date: new Date(),
            titleColor: "#000",
            forwarded: false,
            replyButton: false,
            removeButton: fetch,
            status: "sent",
            notch: true,
            retracted: false,
            onClick: () => console.log("Message clicked"),
           }))}
       />

    {/* عنصر غير مرئي لمتابعة التمرير */}
    <div ref={messagesEndRef} />
    <div className={styles.inputContainer}>
       <button className={styles.dropdown_change} onClick={toggleInputMethod}>
          <Image src="/exchange.png" alt="Switch Input" width={35} height={35} />
        </button>
      {showEmojiPicker && (
          <div ref={emojiPickerRef} className={styles.emojiPicker} onClick={(e) => e.stopPropagation()}>
            <Picker onEmojiClick={addEmoji} />
          </div>
      )}
        {isInputVisible ? (
         <Input
          placeholder="Enter Your Question"
          value={inputValue}
           onChange={(e: React.ChangeEvent<HTMLInputElement>) => setInputValue(e.target.value)}
           onKeyPress={(e: React.KeyboardEvent<HTMLInputElement>) => {
            if (e.key === "Enter") {
              handleSend();
              e.preventDefault(); // لمنع حدوث كسر سطر جديد
            }
          }}
          multiline={true}
           maxHeight={100}
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

            <button onClick={() => handleSend(inputValue)} className={styles.sendButton}>
              <Image src="/send.png" alt="Send" width={25} height={25} />
            </button>

          </div>
        }
      />
       ) : (
            <div className={styles.dropdownContainer}>
              {exampleQuestions.length > 0 && (
                  <ul className={styles.dropdownList}>
                    {exampleQuestions.map((question, index) => (
                      <li key={index} onClick={() => handleQuestionClick(question)}>
                        {question}
                      </li>
                    ))}
                  </ul>
                )}
            </div>
          )}
    </div>
    </div>
    </main>
  );
}



export default ChatPage;