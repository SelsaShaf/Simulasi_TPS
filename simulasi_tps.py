# Simulasi Dinamika Penumpukan Sampah di TPS dan Pengangkutan oleh Truk
# Pemodelan Sistem Dinamik - menggunakan odeint (SciPy)

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


# ---------------------------------------------------------------
# Model TPS: dm/dt = q_in - c * (u / 100)
# ---------------------------------------------------------------
def tps(m, t, q_in, c, truk):
    # laju perubahan volume sampah di TPS (m3/hari)
    dmdt = q_in - c * (truk / 100.0)
    return dmdt


# ---------------------------------------------------------------
# Parameter (data asumsi)
# ---------------------------------------------------------------
penduduk = 2000              # jumlah penduduk yang dilayani (orang)
timbulan = 0.0025            # timbulan sampah (m3/orang/hari) = 2,5 liter
q_in = penduduk * timbulan   # laju sampah masuk (m3/hari)
c = 15.0                     # laju angkut truk saat u = 100% (m3/hari)
m_max = 25.0                 # kapasitas TPS (m3)
m0 = 5.0                     # volume sampah awal (m3)

# waktu simulasi 20 hari, setiap 0.1 hari
ts = np.linspace(0, 20, 201)


# ---------------------------------------------------------------
# Jadwal kedatangan truk (u = 100% selama 1 hari penuh)
# ---------------------------------------------------------------
def jadwal_truk(periode, hari_pertama):
    u = np.zeros(201)
    for hari in range(20):
        if hari >= hari_pertama and (hari - hari_pertama) % periode == 0:
            u[hari * 10:(hari + 1) * 10] = 100.0
    return u


u_A = jadwal_truk(3, 2)   # skenario A: truk tiap 3 hari (hari ke-2, 5, 8, ...)
u_B = jadwal_truk(5, 4)   # skenario B: truk tiap 5 hari (hari ke-4, 9, 14, ...)


# ---------------------------------------------------------------
# Simulasi dengan ODEINT
# ---------------------------------------------------------------
def simulasi(u):
    m = m0
    z = np.zeros(201)
    z[0] = m0
    for i in range(200):
        truk = u[i]
        y = odeint(tps, m, [0, 0.1], args=(q_in, c, truk))
        m = y[-1][0]          # ambil titik terakhir
        z[i + 1] = m          # simpan volume untuk plot
    return z


z_A = simulasi(u_A)
z_B = simulasi(u_B)

# ---------------------------------------------------------------
# Cek kapasitas TPS
# ---------------------------------------------------------------
for nama, z in [("A", z_A), ("B", z_B)]:
    if np.any(z > m_max + 1e-6):
        t_penuh = ts[np.argmax(z > m_max + 1e-6)]
        print(f"Skenario {nama}: TPS melebihi kapasitas pada t = {t_penuh:.1f} hari")
    else:
        print(f"Skenario {nama}: TPS tidak pernah melebihi kapasitas")
    print(f"  volume maksimum = {z.max():.1f} m3, volume akhir = {z[-1]:.1f} m3")


# ---------------------------------------------------------------
# Validasi: metode Euler manual (dt = 1 hari)
# ---------------------------------------------------------------
print("\nValidasi Euler (dt = 1 hari)")
for nama, u in [("A", u_A), ("B", u_B)]:
    m = m0
    hasil = []
    for n in range(10):
        truk = u[n * 10]
        m = m + 1.0 * (q_in - c * truk / 100.0)
        hasil.append(float(m))
    print(f"Skenario {nama}:", hasil)


# ---------------------------------------------------------------
# Grafik
# ---------------------------------------------------------------
def plot_skenario(z, u, judul):
    plt.figure(figsize=(8, 5))
    plt.subplot(2, 1, 1)
    plt.title(judul)
    plt.plot(ts, z, 'b-', label='Volume sampah m(t)')
    plt.axhline(m_max, color='k', linestyle=':', label='Kapasitas TPS')
    plt.ylabel('Volume Sampah m(t), (m3)')
    plt.legend(frameon=False)
    plt.subplot(2, 1, 2)
    plt.plot(ts, u, 'r--')
    plt.ylabel('Pengangkutan Truk u(t), (%)')
    plt.xlabel('t, (hari)')
    plt.tight_layout()
    plt.show()


plot_skenario(z_A, u_A, 'Skenario A: Truk Datang Tiap 3 Hari')
plot_skenario(z_B, u_B, 'Skenario B: Truk Datang Tiap 5 Hari')

# perbandingan dua skenario
plt.figure(figsize=(8, 4))
plt.plot(ts, z_A, 'b-', label='A (tiap 3 hari)')
plt.plot(ts, z_B, 'g--', label='B (tiap 5 hari)')
plt.axhline(m_max, color='k', linestyle=':', label='Kapasitas TPS')
plt.xlabel('t, (hari)')
plt.ylabel('Volume Sampah m(t), (m3)')
plt.title('Perbandingan Skenario A dan B')
plt.legend(frameon=False)
plt.show()
