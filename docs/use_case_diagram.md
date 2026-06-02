# Use Case Diagram

## Aktor

Aplikasi ini memiliki dua aktor utama:

1. Anggota Perpustakaan
2. Petugas Perpustakaan

## Use Case

| Aktor | Use Case | Keterangan |
|---|---|---|
| Anggota Perpustakaan | Melihat katalog | Anggota dapat melihat daftar koleksi perpustakaan |
| Petugas Perpustakaan | Mengelola anggota | Petugas dapat menambahkan data anggota |
| Petugas Perpustakaan | Mengelola koleksi | Petugas dapat menambahkan data koleksi atau buku |
| Petugas Perpustakaan | Mencatat peminjaman | Petugas dapat mencatat transaksi peminjaman koleksi |
| Petugas Perpustakaan | Melihat riwayat peminjaman | Petugas dapat melihat daftar transaksi peminjaman |
| Petugas Perpustakaan | Mengekspor laporan PDF | Petugas dapat membuat laporan peminjaman dalam bentuk PDF |

## Diagram Use Case Sederhana

```text
+-----------------------+
| Anggota Perpustakaan  |
+-----------------------+
            |
            | Melihat Katalog
            v
+-------------------------------+
| Library Certification App     |
+-------------------------------+
            ^
            |
            | Mengelola Anggota
            | Mengelola Koleksi
            | Mencatat Peminjaman
            | Melihat Riwayat Peminjaman
            | Mengekspor Laporan PDF
            |
+-----------------------+
| Petugas Perpustakaan  |
+-----------------------+