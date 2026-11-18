# Dinamika Penumpukan Sampah di TPS dan Pengangkutan oleh Truk

Tugas Pemodelan dan Simulasi Sistem Dinamik (Teknik Informatika, UNIBBA).
Simulasi tinggi tumpukan sampah di Tempat Penampungan Sementara (TPS) yang dipengaruhi sampah dari warga dan jadwal pengangkutan truk. Persamaan diferensialnya diselesaikan dengan dua cara, yaitu **ODEINT (SciPy)** dan **GEKKO**.

## Model

```
rho * A * dh/dt = ci * ui - co * uo
```

| Simbol | Arti | Nilai | Satuan |
|---|---|---|---|
| h | tinggi tumpukan sampah | variabel | m |
| rho | massa jenis sampah | 250 | kg/m³ |
| A | luas alas TPS | 10 | m² |
| ci | koefisien sampah masuk | 10 | kg/hari per % |
| co | koefisien pengangkutan truk | 40 | kg/hari per % |
| ui | aktivitas warga membuang sampah | 100 | % |
| uo | pengangkutan truk | 0 atau 100 | % |
| h(0) | tinggi awal | 0,5 | m |
| hmax | batas tinggi TPS | 2,0 | m |

Semua nilai parameter adalah data asumsi untuk simulasi.

## Skenario

- **Tanpa pengangkutan**: truk tidak pernah datang (8 hari)
- **A**: truk datang tiap 4 hari (hari ke-3, 7, 11, 15)
- **B**: truk datang tiap 6 hari (hari ke-5, 11)

## Isi repository

- `Simulasi_TPS_Colab.ipynb` : notebook Google Colab (Program 1 sampai 4)
- `simulasi_tps.py` : versi file Python (isi sama dengan notebook)
- `grafik/` : hasil grafik simulasi

| Program | Isi |
|---|---|
| 1 | Simulasi tanpa pengangkutan (ODEINT) |
| 2 | Skenario A dan B (ODEINT) |
| 3 | Skenario A dan B (GEKKO) |
| 4 | Perbandingan ODEINT, GEKKO, dan perhitungan manual |

## Cara menjalankan

1. **Google Colab**: buka `Simulasi_TPS_Colab.ipynb`, lalu pilih Runtime > Run all. GEKKO sudah diinstall oleh sel `!pip install gekko`.
2. **Di komputer**: `pip install numpy scipy matplotlib gekko`, kemudian `python simulasi_tps.py`.

## Hasil singkat

- Tanpa pengangkutan, tinggi sampah naik 0,4 m/hari dan melewati batas 2,0 m pada hari ke-3,75.
- Skenario A: tinggi naik turun antara 0,5 dan 1,7 m, tidak pernah melewati batas.
- Skenario B: tinggi terus naik sampai 3,7 m di hari ke-16 dan melewati batas.
- ODEINT, GEKKO, dan perhitungan manual memberi hasil yang sama (selisih sekitar 1e-14 m).

Link video tutorial: :  https://youtu.be/OTdY1LuSiyc?si=o3Ab8JQKS0mMSN-v 
