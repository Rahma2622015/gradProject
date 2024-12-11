"use client";
import "./globals.css";
import "./chat_page/chatstyle.module.css";
import "./page.module.css";
import { ThemeProvider } from "./context/ThemeContext";

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
        <ThemeProvider>
          {children}
        </ThemeProvider>
        </body>
      </html>
  );
}