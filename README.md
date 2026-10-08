# SepPleretScreenshot-jadi-web

Skill Claude untuk mengubah **screenshot, mockup, atau video rekaman layar** sebuah UI menjadi kode **HTML/CSS** (plus JS sederhana bila perlu) yang siap dipakai sebagai tampilan web.

> A Claude skill that turns UI screenshots, mockups, or screen recordings into clean, responsive HTML/CSS.

## Fitur

- **Gambar → HTML**: menganalisis layout, warna, tipografi, dan komponen, lalu menulis `index.html` yang responsif dan aksesibel.
- **Video → HTML**: mengambil frame kunci dari video, lalu menerjemahkan perubahan antar-frame menjadi animasi CSS dan interaksi (tab, dropdown, modal, hover).
- **Cek visual**: merender hasilnya dan membandingkannya dengan gambar asli untuk memperbaiki selisih.
- Opsi keluaran: HTML/CSS biasa (bawaan), Tailwind, React, Vue, atau Svelte.

## Isi repo

```
SKILL.md                    # instruksi utama skill
references/conventions.md   # standar CSS, responsif, aksesibilitas, animasi
scripts/extract_frames.py   # ekstraksi frame kunci dari video (ffmpeg)
scripts/color_palette.py    # mengambil warna dominan (hex) dari gambar
scripts/render_preview.py   # merender HTML ke PNG (Playwright)
```

## Kebutuhan

Hanya untuk skrip pendukung (video dan pratinjau); skill tetap bisa dipakai untuk gambar tanpa ini.

- [ffmpeg](https://ffmpeg.org/) (termasuk `ffprobe`)
- Python 3 dan `pip install pillow playwright`, lalu `playwright install chromium`

## Cara memasang

**Claude Code**

```bash
git clone https://github.com/<username-kamu>/SepPleretScreenshot-jadi-web ~/.claude/skills/screenshot-to-html
```

Nama folder tujuan (`screenshot-to-html`) menjadi identitas skill. Mulai ulang sesi Claude Code setelah memasang.

**Claude Desktop / claude.ai**

1. Buat ZIP dari folder skill, dengan `SKILL.md` berada di dalam satu folder bernama `screenshot-to-html`.
2. Buka **Settings > Capabilities**, lalu **Upload skill** dan pilih ZIP tersebut. (Letak menu bisa berbeda tergantung versi aplikasi.)

## Cara memakai

Unggah screenshot atau video UI, lalu tulis misalnya:

- "Ubah screenshot ini jadi HTML."
- "Tiru UI di video ini lengkap dengan animasinya, pakai Tailwind."

## Batasan

- Font khusus, ikon, dan foto hanya diaproksimasi (placeholder atau SVG sederhana); ganti dengan aset asli Anda.
- Logo merek tidak digambar ulang.
- Durasi animasi dari video hanyalah estimasi.
- Gunakan hanya pada desain milik Anda atau yang Anda berhak tiru. Meniru situs orang lain dapat melanggar hak cipta atau merek dagang.

## Lisensi

[MIT](LICENSE) © 2026 Septian
