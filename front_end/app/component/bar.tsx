"use client"
import Link from "next/link";
import { useState } from "react";
import Image from "next/image";
import styles from './bar.module.css'
import { useRouter } from "next/navigation";
function Bar() {

    const router = useRouter();

    const navigateTo = (path) => {
      router.push(path);
    };

  const [isOpen, setIsOpen] = useState(false);

  return (
    <div>
      <button onClick={() => setIsOpen(!isOpen)} className={styles.menuButton}>
        <Image
                src="/list.png"
                alt="list"
                width={46}
                height={46}
              />
      </button>
      {isOpen && (
        <div className="sidebar">
          <div className={styles.sidebarItem} onClick={() => navigateTo("/GeneralSettings")}>
            <Image src="/settings.png" alt="settings" width={46} height={46} />
            <h4>GeneralSetting</h4>
          </div>
          <div className={styles.sidebarItem} onClick={() => navigateTo("/Jsoneditor")}>
            <Image src="/writing.png" alt="Json Editor" width={46} height={46} />
            <h4>Jsoneditor</h4>
          </div>
        </div>
      )}
    </div>
  );
};

export default Bar;
