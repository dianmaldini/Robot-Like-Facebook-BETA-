# Facebook Robot Liker (Beta)

Facebook Robot Liker adalah perangkat lunak desktop berbasis Python yang dirancang untuk mengotomatisasi interaksi pada platform Facebook, khususnya fungsi "Like". Aplikasi ini dikembangkan menggunakan Selenium WebDriver untuk otomatisasi peramban dan Tkinter untuk antarmuka pengguna grafis.

Tujuan utama aplikasi ini adalah untuk membantu pengelolaan aktivitas akun Facebook dengan fitur sesi persisten dan mekanisme penundaan waktu untuk menjaga keamanan akun.

## Fitur Utama

* **Antarmuka Pengguna Grafis (GUI)**
    Menyediakan tampilan yang terstruktur dan mudah dioperasikan tanpa memerlukan interaksi baris perintah.

* **Manajemen Sesi Persisten**
    Aplikasi menyimpan profil peramban lokal (profile_fb). Pengguna hanya perlu melakukan login satu kali, dan sesi akan tetap aktif untuk penggunaan selanjutnya.

* **Mekanisme Keamanan & Anti-Spam**
    Menerapkan jeda waktu otomatis (2 detik) antar aktivitas dan algoritma pengguliran (scrolling) untuk menimulasikan perilaku manusia.

* **Logika Pencegahan Redundansi**
    Sistem secara otomatis mendeteksi tombol yang sudah ditekan sebelumnya untuk mencegah pembatalan like (unlike) yang tidak disengaja.

* **Penanganan Dialog Otomatis**
    Mampu mendeteksi dan menutup jendela popup atau dialog sistem yang menghalangi proses otomatisasi.

## Prasyarat Sistem

Sebelum menjalankan aplikasi, pastikan sistem Anda memiliki:

1.  Python 3.x terinstal.
2.  Google Chrome versi terbaru.
3.  Koneksi internet yang stabil.

## Instalasi

Ikuti langkah-langkah berikut untuk mengatur lingkungan pengembangan:

1.  Kloning repositori ini ke komputer lokal Anda:
    git clone https://github.com/username-anda/facebook-robot-liker.git

2.  Disarankan untuk membuat Virtual Environment agar dependensi tidak tercampur:
    python -m venv venv

3.  Aktifkan Virtual Environment:
    * Windows: .\venv\Scripts\activate
    * Mac/Linux: source venv/bin/activate

4.  Instal pustaka Selenium:
    pip install selenium

## Cara Penggunaan

1.  Jalankan file utama aplikasi melalui terminal:
    python app.py

2.  Pada antarmuka aplikasi, masukkan URL target pada kolom yang tersedia. Target bisa berupa Beranda, Profil Pengguna, atau Grup.

3.  Pilih jumlah target interaksi pada menu dropdown.

4.  Klik tombol "Mulai Proses".

5.  Untuk penggunaan pertama kali, lakukan login Facebook secara manual pada jendela Chrome yang terbuka. Setelah masuk ke beranda, kembali ke aplikasi dan klik tombol konfirmasi login.

6.  Untuk menghentikan proses yang sedang berjalan, klik tombol "Stop".

## Penafian (Disclaimer)

Aplikasi ini dikembangkan untuk tujuan edukasi dan pembelajaran mengenai otomatisasi web menggunakan Python dan Selenium. Pengembang tidak bertanggung jawab atas penggunaan yang melanggar Ketentuan Layanan Facebook atau penyalahgunaan lainnya. Harap gunakan perangkat lunak ini dengan bijak dan bertanggung jawab.

Dikembangkan oleh Albani Computer.
All Rights Reserved.