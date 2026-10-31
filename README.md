# NusantaraCare AI Assistant

Project ini dibuat untuk tugas akhir AI Engineer. Tujuannya adalah membuat asisten AI yang bisa menjawab pertanyaan berdasarkan dokumen panduan operasional internal NusantaraCare.

## 1. Problem & Success Criteria

### Problem

Dokumen operasional terkadang membutuhkan waktu untuk dicari dan dibaca. Karena itu, dibuatlah asisten AI yang bisa membantu mencari informasi dari dokumen tersebut.

Aplikasi ini diharapkan bisa menjawab pertanyaan sesuai isi dokumen dan tidak membuat jawaban sendiri jika informasinya tidak tersedia.

### Success Criteria

Beberapa hal yang ingin dicapai dari project ini:

- Bisa menjawab pertanyaan berdasarkan dokumen.
- Bisa membedakan kebijakan aktif dan kebijakan lama.
- Bisa memberikan informasi sumber jawaban.
- Bisa menolak menjawab jika informasi tidak ditemukan.
- Tidak mengikuti perintah yang meminta AI mengarang jawaban.

Pertanyaan yang ditargetkan adalah pertanyaan seputar panduan dan aturan operasional NusantaraCare.

## 2. Knowledge Base Understanding

Dokumen yang digunakan adalah:

`nusantaracare_panduan_operasional_internal_v2.md`

Dokumen tersebut memiliki dua versi kebijakan:

- **Versi 2.0:** Kebijakan yang masih aktif.
- **Versi 1.4:** Kebijakan lama atau arsip.

Kedua versi dibedakan agar aplikasi tidak menggunakan informasi dari kebijakan lama untuk menjawab pertanyaan tentang aturan yang berlaku saat ini.

Metadata yang digunakan dalam setiap chunk:

Metadata => Keterangan
`doc_id` => ID dokumen
`chunk_id` => ID setiap bagian dokumen
`doc_title` => Judul dokumen
`section_title` => Judul bagian dokumen
`doc_version` => Versi dokumen
`is_active` => Status aktif atau tidak aktif

Saat pengguna bertanya tentang kebijakan lama, sistem mencari informasi dari dokumen arsip. Untuk pertanyaan biasa, sistem menggunakan dokumen yang masih aktif.

## 3. RAG Design & Data Preparation

### Chunking

Dokumen dibagi menjadi beberapa bagian kecil agar lebih mudah dicari.

Pengaturan yang digunakan:

- Chunk size: 1000 karakter.
- Overlap: 150 karakter.

Overlap digunakan agar informasi di antara dua bagian dokumen tidak mudah terputus.

### Embedding

FastEmbed digunakan dengan model:

`intfloat/multilingual-e5-large`

Model ini digunakan untuk mengubah teks menjadi embedding agar sistem bisa mencari informasi berdasarkan kemiripan makna pertanyaan dan isi dokumen.

### Vector Database

ChromaDB digunakan untuk menyimpan dokumen dan embedding.

ChromaDB dipilih karena cukup mudah digunakan untuk project RAG seperti ini.

### Retrieval

Saat pengguna mengirim pertanyaan, sistem mencari maksimal 4 bagian dokumen yang paling sesuai.

Pengaturan yang digunakan:

- Top-k: 4
- Distance threshold: 0.65
- Filtering berdasarkan `is_active`

Dengan filtering tersebut, sistem bisa membedakan dokumen aktif dan dokumen arsip.

### Prompt

Ada beberapa aturan yang diberikan ke AI, yaitu:

- Jawaban harus berdasarkan isi dokumen.
- Tidak boleh mengarang informasi.
- Jika informasi tidak ditemukan, AI harus menyampaikan bahwa informasi tidak tersedia.
- Jawaban harus menyebutkan sumber bagian dokumen.
- Informasi dari kebijakan arsip harus dijelaskan sebagai kebijakan lama.

Aturan ini dibuat agar jawaban lebih sesuai dengan dokumen yang digunakan.

### Penanganan Dokumen Lama

Dokumen versi 1.4 disimpan sebagai arsip dan tidak digunakan untuk pertanyaan biasa.

Jika pengguna secara khusus bertanya tentang versi 1.4, sistem akan mencari informasi dari dokumen arsip tersebut.

## 4. Kesimpulan & Dokumentasi

### Arsitektur

Alur kerja aplikasi:

1. Pengguna mengirim pertanyaan melalui API.
2. FastAPI menerima pertanyaan.
3. Sistem mencari informasi di ChromaDB.
4. Informasi yang ditemukan dikirim ke OpenAI.
5. OpenAI membuat jawaban berdasarkan konteks dokumen.
6. Hasil jawaban dikirim kembali melalui API.

### Kontrak API

Aplikasi memiliki dua endpoint.

**GET /**

Digunakan untuk memeriksa apakah aplikasi berjalan.

**POST /ask**

Digunakan untuk mengirim pertanyaan kepada asisten AI.

Contoh request:

```json
{
  "text": "Berapa lama waktu minimum pengajuan permintaan peralatan?"
}
```

Contoh response:

```json
{
  "answer": "Jawaban berdasarkan dokumen...",
  "confidence_label": "high",
  "reason_code": "answered"
}
```

Keterangan:

- `answer`: Jawaban dari AI.
- `confidence_label`: Tingkat keyakinan (`high`, `medium`, atau `low`).
- `reason_code`: Status hasil pencarian, seperti `answered` atau `no_relevant_context`.

### Cara Menjalankan Lokal

Install library yang dibutuhkan:

```bash
pip install -r requirements.txt
```

Buat file `.env` dan isi API key OpenAI:

```env
OPENAI_API_KEY=isi_api_key_di_sini
```

Jalankan aplikasi:

```bash
uvicorn app.main:app --port 8001
```

Buka alamat berikut untuk mencoba API:

`http://127.0.0.1:8001/docs`

### Deployment

Project ini menggunakan FastAPI dan direncanakan untuk di-deploy menggunakan FastAPI Cloud.

API key OpenAI akan disimpan di pengaturan environment variable pada platform deployment agar tidak dimasukkan ke GitHub.

Status deployment: Belum dilakukan.

### Keterbatasan

Beberapa keterbatasan aplikasi saat ini:

- Dokumen yang digunakan masih satu file.
- Jawaban bergantung pada informasi yang ditemukan dalam dokumen.
- Jika informasi tidak ditemukan, aplikasi tidak bisa memberikan jawaban.
- Confidence label masih menggunakan aturan berdasarkan hasil pencarian, bukan hasil pengukuran akurasi jawaban.

### Kesimpulan & Rekomendasi

Dari project ini, saya belajar cara membuat aplikasi AI menggunakan RAG untuk mencari informasi dari dokumen.

Aplikasi sudah bisa menerima pertanyaan, mencari informasi yang sesuai, membedakan dokumen aktif dan arsip, serta memberikan jawaban menggunakan OpenAI.

Ke depannya, aplikasi masih bisa dikembangkan dengan menambahkan dokumen lain dan melakukan pengujian lebih banyak agar hasil pencarian dan jawabannya semakin baik.
