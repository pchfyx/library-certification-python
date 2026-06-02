# Database Structure

Aplikasi Library Certification App menggunakan database SQLite dengan 4 tabel utama, yaitu `members`, `collections`, `loans`, dan `loan_items`.

## 1. members

Tabel `members` digunakan untuk menyimpan data anggota perpustakaan.

| Field | Tipe Data | Keterangan |
|---|---|---|
| id | INTEGER | Primary key, auto increment |
| name | TEXT | Nama anggota |
| email | TEXT | Email anggota |
| phone | TEXT | Nomor telepon anggota |

## 2. collections

Tabel `collections` digunakan untuk menyimpan data koleksi atau buku perpustakaan.

| Field | Tipe Data | Keterangan |
|---|---|---|
| id | INTEGER | Primary key, auto increment |
| title | TEXT | Judul koleksi |
| author | TEXT | Penulis |
| category | TEXT | Kategori koleksi |
| status | TEXT | Status koleksi, yaitu Available atau Borrowed |

## 3. loans

Tabel `loans` digunakan untuk menyimpan data transaksi peminjaman.

| Field | Tipe Data | Keterangan |
|---|---|---|
| id | INTEGER | Primary key, auto increment |
| member_id | INTEGER | Foreign key ke tabel members |
| borrow_date | TEXT | Tanggal peminjaman |
| due_date | TEXT | Tanggal harus kembali, otomatis 7 hari setelah tanggal pinjam |

## 4. loan_items

Tabel `loan_items` digunakan untuk menyimpan detail koleksi yang dipinjam dalam satu transaksi peminjaman.

| Field | Tipe Data | Keterangan |
|---|---|---|
| id | INTEGER | Primary key, auto increment |
| loan_id | INTEGER | Foreign key ke tabel loans |
| collection_id | INTEGER | Foreign key ke tabel collections |

## Relasi Antar Tabel

- Satu anggota dapat memiliki banyak transaksi peminjaman.
- Satu transaksi peminjaman dimiliki oleh satu anggota.
- Satu transaksi peminjaman dapat memiliki satu atau lebih koleksi yang dipinjam.
- Satu koleksi dapat tercatat dalam detail peminjaman.

## Diagram Relasi Sederhana

```text
members
  └── id
      └── loans.member_id

loans
  └── id
      └── loan_items.loan_id

collections
  └── id
      └── loan_items.collection_id