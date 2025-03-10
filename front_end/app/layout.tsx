"use client";
import "./globals.css";
import "./chat_page/chatstyle.module.css";
import "./page.module.css";
import { ThemeProvider as ModeProvider } from "./context/ThemeContext"; // للـ Dark/Light Mode
import { ThemeProvider as ColorProvider } from "./context/ThemeColor"; // لتغيير الألوان

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/favicon.ico" type="image/x-icon" />
        <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      </head>
      <body>
        <ModeProvider>  {/* للتحكم في الـ Mode */}
          <ColorProvider>  {/* للتحكم في الألوان */}
            {children}
          </ColorProvider>
        </ModeProvider>
      </body>
    </html>
  );
}
