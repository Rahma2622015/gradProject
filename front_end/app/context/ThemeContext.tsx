// context/ThemeContext.tsx
"use client";
import React, { createContext, useContext, useState, ReactNode } from "react";

// تعريف الواجهة الخاصة بالـ Context
interface ThemeContextType {
  isDarkMode: boolean;   // حالة الوضع المظلم
  toggleDarkMode: () => void;  // دالة لتبديل الوضع بين المظلم والفاتح
}

// إنشاء Context جديد
const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

// مكون ThemeProvider لتغليف المكونات التي تحتاج إلى استخدام الـ Context
export const ThemeProvider = ({ children }: { children: ReactNode }) => {
  const [isDarkMode, setIsDarkMode] = useState(false);  // حالة الوضع المظلم

  // دالة لتبديل الوضع المظلم
  const toggleDarkMode = () => {
    setIsDarkMode((prev) => !prev);  // إذا كان الوضع الحالي مظلمًا، يتم تغييره إلى فاتح، والعكس
  };

  return (
    <ThemeContext.Provider value={{ isDarkMode, toggleDarkMode }}>
      <div className={isDarkMode ? "dark" : "light"}>{children}</div> {/* تغيير الـ class بناءً على الوضع */}
    </ThemeContext.Provider>
  );
};

// دالة useTheme لاستهلاك الـ Context في أي مكون
export const useTheme = () => {
  const context = useContext(ThemeContext);  // استخدام useContext للحصول على الـ context
  if (!context) {
    throw new Error("useTheme must be used within a ThemeProvider");  // التأكد من أن الـ Context متاح
  }
  return context;  // إرجاع الـ context
};