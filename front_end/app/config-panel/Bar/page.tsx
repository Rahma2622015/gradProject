"use client";
import Link from 'next/link';
import styles from './bar.module.css'; // استيراد ملف CSS

 function Home() {
  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Admin Panel</h1>
      <div className={styles.links}>
        <ul className={styles.list}>
          <li className={styles.listItem}>
            <Link href="/config-panel/Config" className={styles.link}>Edit JSON Config</Link>
          </li>
          <li className={styles.listItem}>
            <Link href="/database" className={styles.link}>Manage Database</Link>
          </li>
        </ul>
      </div>
    </div>
  );
}
export default  Home;