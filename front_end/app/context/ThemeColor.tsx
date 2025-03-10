"use client";
import React, { createContext, useContext, useState, ReactNode, useEffect } from "react";

// تعريف الواجهة الخاصة بالـ Context
interface ThemeContextType {
  themeColor: string; // اللون الحالي
  changeTheme: (color: string) => void; // دالة لتغيير اللون
}

// إنشاء Context جديد
const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

// مكون ThemeProvider لتغليف المكونات التي تحتاج إلى استخدام الـ Context
export const ThemeProvider = ({ children }: { children: ReactNode }) => {
  const [themeColor, setThemeColor] = useState<string>("default");

  useEffect(() => {
    const savedColor = localStorage.getItem("themeColor") || "default";
    setThemeColor(savedColor);
  }, []); // تحميل اللون عند بدء التطبيق

  const changeTheme = (color: string) => {
    setThemeColor(color);
    localStorage.setItem("themeColor", color);
  };

  return (
    <ThemeContext.Provider value={{ themeColor, changeTheme }}>
      <div className={`theme-${themeColor}`}>{children}</div>
    </ThemeContext.Provider>
  );
};

// دالة useTheme لاستهلاك الـ Context في أي مكون
export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error("useTheme must be used within a ThemeProvider");
  }
  return context;
};
