# 📊 Anime2025-Rating-Sentiment-Analysis

โปรเจกต์วิเคราะห์ทัศนคติและเรตติ้งของอนิเมะในปี 2025 โดยการดึงข้อมูลจาก **Online Platforms (Comments & Threads)** มาประมวลผลโดยใช้

* **VADER Sentiment Analysis:** วิเคราะห์อารมณ์และความรู้สึกจากข้อความคอมเมนต์เพื่อแปลงเป็นคะแนนเรตติ้งเชิงคุณภาพ
* **Gender Classification:** ระบบจำแนกเพศของผู้ใช้งานเพื่อเปรียบเทียบความชื่นชอบระหว่างกลุ่มเป้าหมาย
* **Age Group Classification:** การจัดกลุ่มช่วงอายุของผู้ชมเพื่อวิเคราะห์ความเหมาะสมและเทรนด์ของเนื้อหาในแต่ละวัย

> **Objective:** นำ Insight ที่ได้จากเสียงของผู้ชมจริงๆ มาเปรียบเทียบกับสถิติภาพรวม เพื่อค้นหาปัจจัยที่ส่งผลต่อความสำเร็จของอนิเมะแต่ละประเภทในปี 2025
---

## 📈 สรุปผลการวิเคราะห์ข้อมูล (Visualized Analysis)

ในส่วนนี้เป็นการนำเสนอข้อมูลผ่านกราฟต่างๆ เพื่อให้เห็นภาพรวมของตลาดอนิเมะในปีนี้

### 1. เรตติ้งเฉลี่ยแบ่งตามประเภทอนิเมะ (Average Rating by Genre)
<p align="center">
  <img src="alnalysis/grap05.png" width="800px" alt="Genre Rating Graph">
</p>

> **คำอธิบาย:** กราฟแท่งแสดงค่าเฉลี่ยเรตติ้งของอนิเมะในแต่ละแนว (Genre) ช่วยให้เห็นว่าในปี 2025 แนวไหนที่ได้รับความนิยมสูงสุดและครองใจผู้ชมในภาพรวม โดยจะเห็นการเรียงลำดับจากแนวที่เรตติ้งสูงไปหาต่ำ

---

### 2. ความสัมพันธ์ระหว่างเรตติ้งกับช่วงอายุ (Rating vs. Age Group)
<p align="center">
  <img src="alnalysis/grap01.png" width="800px" alt="Age Group Analysis">
</p>

> **คำอธิบาย:** กราฟเปรียบเทียบระดับคะแนนตามช่วงอายุ (เช่น เด็ก, วัยรุ่น, ผู้ใหญ่) เพื่อวิเคราะห์ว่ากลุ่มอายุใดมีแนวโน้มให้คะแนนอนิเมะสูงกว่ากัน และช่วยระบุว่าเนื้อหาประเภทนั้นๆ ตอบโจทย์กลุ่ม Target Audience หลักหรือไม่

---

### 3. การเปรียบเทียบเรตติ้งระหว่างเพศ (Rating by Gender)
| Male vs Female Comparison |
| :---: |
| <img src="alnalysis/grpa04.png" width="700px" alt="Gender Comparison"> |

> **คำอธิบาย:** กราฟเปรียบเทียบค่าเฉลี่ยเรตติ้งระหว่างผู้ชมเพศชายและเพศหญิง เพื่อดูความแตกต่างของรสนิยมและการยอมรับในคุณภาพของอนิเมะที่รับชม

---

### 4. การกระจายตัวของเรตติ้งในแต่ละเพศ (Rating Distribution by Gender)
<p align="center">
  <img src="alnalysis/grpa05.png" width="800px" alt="Rating Distribution">
</p>

> **คำอธิบาย:** กราฟแสดงความหนาแน่นและการกระจายตัวของคะแนน (Distribution) ของผู้ชมแต่ละเพศ ช่วยให้เราเห็นภาพว่าคะแนนส่วนใหญ่อัดตัวกันอยู่ที่ช่วงใด (เช่น 7-8 คะแนน) และมีกลุ่มที่ให้คะแนนสุดโต่ง (Outliers) มากน้อยเพียงใด

---

## 🛠 Tools Used
* **Python** (Pandas, Matplotlib, Seaborn) สำหรับการทำ Data Visualization
* **Markdown** สำหรับการจัดทำรายงานบน GitHub

---


---

## 📂 แหล่งข้อมูล (Data Sources)

ข้อมูลทั้งหมดถูกรวบรวมและอ้างอิงจากแพลตฟอร์มชั้นนำ เพื่อความแม่นยำในการวิเคราะห์:

<p align="center">
  <a href="https://myanimelist.net/" target="_blank">
    <img src="alnalysis/myanimelist.png" height="50px" alt="MyAnimeList">
  </a> 
  &nbsp;&nbsp;&nbsp;&nbsp;
  <a href="https://anilist.co/" target="_blank">
    <img src="alnalysis/anilist.png" height="50px" alt="AniList">
  </a> 
  &nbsp;&nbsp;&nbsp;&nbsp;
  <a href="https://www.youtube.com/" target="_blank">
    <img src="alnalysis/youtubelogo.png" height="50px" alt="YouTube">
  </a>
</p>

> **Note:** คลิกที่โลโก้เพื่อไปยังเว็บไซต์ต้นทาง

---

* **MyAnimeList & AniList & YouTube:** ใช้สำหรับดึงข้อมูล Rating, Genre และ Comment ของอนิเมะแต่ละเรื่อง

---

<p align="center">
  <i>Created with ❤️ for Anime Community Analysis 2025</i>
</p>
