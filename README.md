
# Fireverse Music Bot

Fireverse Music Bot adalah sebuah bot yang dirancang untuk memutar musik secara otomatis di platform Fireverse. Bot ini dapat memutar lagu, menyukai lagu, dan memberikan komentar secara otomatis. Bot ini juga dapat melacak waktu mendengarkan dan menyelesaikan tugas harian yang terkait dengan musik.

---

## 📋 Persyaratan

Sebelum menjalankan bot ini, pastikan Anda telah menginstal dependensi yang diperlukan:

- **Python 3.7 atau lebih baru**
- **`aiohttp`**
- **`colorama`**

Anda dapat menginstal dependensi dengan menjalankan perintah berikut:

```bash
pip install aiohttp colorama
```
---

## 🚀 Cara Menggunakan

1. **Clone Repository**

   Pertama, clone repository ini ke komputer Anda:

   ```bash
   git clone https://github.com/Boren4anzz/fireverse-music-bot.git
   cd fireverse-music-bot
   ```

2. **Siapkan Tokens**

   Buat file `tokens.txt` di direktori yang sama dengan skrip ini. File ini harus berisi token API Fireverse Anda, satu token per baris. Contoh:

   ```
   token_anda_di_sini_1
   token_anda_di_sini_2
   ```

   > **Catatan**: Token dapat diperoleh dari akun Fireverse Anda.

3. **Jalankan Bot**

   Setelah menyiapkan `tokens.txt`, jalankan bot dengan perintah berikut:

   ```bash
   python main.py
   ```

   Bot akan mulai memutar musik secara otomatis dan melaporkan statusnya ke konsol.

---

## ✨ Fitur

- **Memutar Musik Otomatis**: Bot akan memutar lagu yang direkomendasikan secara otomatis.
- **Menyukai Lagu**: Bot akan secara otomatis menyukai lagu yang diputar.
- **Memberikan Komentar**: Bot akan memberikan komentar otomatis pada lagu yang diputar.
- **Melacak Waktu Mendengarkan**: Bot akan melacak total waktu mendengarkan musik.
- **Menyelesaikan Tugas Harian**: Bot akan melaporkan progres tugas harian yang terkait dengan musik.

---

## 🧩 Struktur Kode

- **`FireverseMusicBot`**: Kelas utama yang mengatur semua fungsi bot.
- **`read_tokens`**: Fungsi untuk membaca token dari file `tokens.txt`.
- **`main`**: Fungsi utama yang menjalankan bot untuk semua token yang diberikan.

---

## ⚠️ Catatan

- Bot ini dirancang untuk digunakan secara bertanggung jawab. Jangan menyalahgunakan bot ini untuk tujuan yang melanggar kebijakan Fireverse.
- Pastikan token yang Anda gunakan valid dan memiliki izin yang diperlukan.
- Bot ini memiliki batas harian (`DAILY_LIMIT`) untuk memutar lagu. Jika batas harian tercapai, bot akan menunggu 24 jam sebelum memulai sesi baru.

---

## 🤝 Kontribusi

Jika Anda ingin berkontribusi pada proyek ini, silakan buka **issue** atau **pull request** di GitHub. Kontribusi Anda sangat dihargai!

---

## 📌 Contoh Output

Berikut adalah contoh output yang akan ditampilkan di konsol saat bot berjalan:

```
==================================================
                     BOT STATUS
==================================================
>> Detected Account: 1
--------------------------------------------------
[ ACCOUNT 1 ] - USER STATS
--------------------------------------------------
   Level            : 5
   EXP              : 1200 / 1500
   Score           : 10,000
   Total Time      : 30 minutes
--------------------------------------------------
[ ACCOUNT 1 ] - DAILY TASKS PROGRESS
--------------------------------------------------
   [✔] Play Music (30/30)       (+100 pts)
   [ ] Like Songs (10/20)       (+50 pts)
--------------------------------------------------
[ ACCOUNT 1 ] - NOW PLAYING
--------------------------------------------------
   Title          : Song Name
   Artist        : Artist Name
   Music ID      : 12345
   Progress      : 10 / 50 songs today
   Duration      : 0:03:00
   Like Status   : SUCCESS
   Comment Status: SUCCESS
   Time Left     : 0:03:00
   Listening Time: 30 minutes
--------------------------------------------------
```
