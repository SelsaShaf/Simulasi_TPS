# Dinamika Penumpukan Sampah di TPS dan Pengangkutan oleh Truk

Tugas Pemodelan dan Simulasi Sistem Dinamik (Teknik Informatika, UNIBBA).
Simulasi volume sampah di Tempat Penampungan Sementara (TPS) dengan jadwal pengangkutan truk, memakai Python (`odeint` dari SciPy).

## Model

```
dm/dt = q_in - c * (u / 100)
```

| Simbol | Arti | Nilai | Satuan |
|---|---|---|---|
| m | volume sampah di TPS | variabel | m³ |
| q_in | laju sampah masuk (2000 orang x 0,0025) | 5 | m³/hari |
| c | laju angkut truk saat u = 100% | 15 | m³/hari |
| u | pengangkutan truk | 0 atau 100 | % |
| m_max | kapasitas TPS | 25 | m³ |
| m(0) | volume awal | 5 | m³ |

Semua nilai parameter adalah data asumsi untuk keperluan simulasi.

## Skenario

- **A**: truk datang tiap 3 hari (hari ke-2, 5, 8, ...)
- **B**: truk datang tiap 5 hari (hari ke-4, 9, 14, ...)

## Isi repository

- `Simulasi_TPS_Colab.ipynb` : notebook Google Colab
- `simulasi_tps.py` : versi file Python
- `grafik/` : hasil grafik simulasi

## Cara menjalankan

1. Buka `Simulasi_TPS_Colab.ipynb` di Google Colab, lalu pilih Runtime > Run all.
2. Atau di komputer: `pip install numpy scipy matplotlib` kemudian `python simulasi_tps.py`.

## Hasil singkat

- Skenario A: volume naik turun antara 5 dan 15 m³, tidak pernah melebihi kapasitas.
- Skenario B: TPS melebihi kapasitas mulai sekitar hari ke-7, volume mencapai 55 m³ pada hari ke-19.

Link video tutorial: (isi link YouTube)
