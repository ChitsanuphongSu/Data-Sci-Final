# เว็บเตรียมสอบ Data Science บท 7–12

เปิด `../index.html` ด้วยเบราว์เซอร์ ใช้หน้ารวมเดียวอ่านไฟล์หมวดย่อยทั้งหมด
ไม่ต้องมีเซิร์ฟเวอร์หรืออินเทอร์เน็ตสำหรับอ่านเนื้อหา ทำ Quiz และ Mock Exam
ต้องเก็บโฟลเดอร์ `exam-prep` อยู่ข้าง `index.html` เสมอ
ลิงก์เอกสารต้นฉบับต้องมีโฟลเดอร์ `lecture`, `quiz`, `pdf` และไฟล์เดิมอยู่ด้วย

## เนื้อหา
- บท 7–12 แยก HTML รายบท
- Workflow, Cheat Sheet, Code & Labs, ผลรันจริง, แหล่งข้อมูล
- Quiz 48 ข้อ พร้อมเฉลยและเหตุผล
- Mock Exam 120 นาที: ปรนัย 24 ข้อ (60 คะแนน), อัตนัย 6 ข้อ (40 คะแนน)
- อัตนัยใช้ rubric ตรวจด้วยตนเอง ไม่ใช่การให้คะแนนอัตโนมัติ

## การบันทึก
คำตอบและความคืบหน้าเก็บใน localStorage ของเบราว์เซอร์เมื่อได้รับอนุญาต
พฤติกรรม localStorage สำหรับ file:// แตกต่างกันตามเบราว์เซอร์
หากเปิดไฟล์แล้วบันทึกไม่ได้ ให้ดาวน์โหลดคำตอบ JSON ก่อนปิด
การย้ายโฟลเดอร์ เปลี่ยนเบราว์เซอร์ หรือเปลี่ยนจาก file:// เป็น HTTP อาจทำให้เห็นสถานะคนละชุด
เวลา Mock Exam เดินต่อเมื่อออกจากหน้า และตรวจวันเวลาหมดเมื่อกลับมา

## โค้ดและผลรัน
ติดตั้งแพ็กเกจตาม `../quiz/requirements.txt` ใน Python environment ของผู้เรียน
จากโฟลเดอร์ DataSci:

```powershell
python exam-prep/examples/core_models.py
python exam-prep/examples/lab_walkthrough.py
python exam-prep/examples/validation_patterns.py
```

แล็บเขียนผลลง `results/` โดยไม่แก้ notebook ต้นฉบับ
P03 refit บน development ก่อน final test แต่ P05 คง model/basis/scaler ที่ fit บน train เดิม
ผลและเวอร์ชันที่ทดสอบจริงอยู่ใน `results/versions.json`

## สำหรับแก้ไขเว็บ
เนื้อหาและตัวสร้างอยู่ `build.py`, ข้อสอบอยู่ `questions.py`
แก้ไขแล้วรัน `python exam-prep/build.py` จาก root เพื่อสร้าง HTML ใหม่
ไม่ต้อง build เมื่อต้องการเปิดอ่านตามปกติ
`source-notes/` เป็นข้อความที่สกัดจากเอกสารสำหรับทำงาน ไม่ใช่สรุปฉบับส่งมอบ
PDF บางไฟล์เป็นหน้ายาวมากและมี glyph ที่สกัดได้ไม่ครบ จึงอ้างอิงด้วยชื่อหัวข้อใน PDF ต้นฉบับ
เว็บที่เผยแพร่ไม่ต้องใช้ Python, Node.js หรือแพ็กเกจในการอ่าน

Quiz และ Mock Exam เป็นข้อฝึกแต่งใหม่ ไม่ใช่ข้อสอบจริงหรือเกณฑ์ผ่านของผู้สอน

## สร้างใหม่พร้อม One Dark Pro
ใช้ Node.js 22+ และ Python 3 จาก root ของ repository:

```powershell
npm ci --prefix exam-prep/tooling
python exam-prep/build.py
node exam-prep/tooling/highlight.mjs
node exam-prep/tooling/qa.mjs
python exam-prep/verify.py
python exam-prep/verify_content.py
```
ต้องรัน highlight หลัง build ทุกครั้ง สีถูกสร้างเป็น HTML ล่วงหน้า ไม่เรียก CDN
เมื่อแก้ CSS/JS ให้เพิ่มค่า `?v=` ใน build.py เพื่อป้องกันแคชเก่า
GitHub Pages ใช้ branch main และ root `/` มี `.nojekyll`
