# Dinamika Penumpukan Sampah di TPS dan Pengangkutan oleh Truk
# Pemodelan dan Simulasi Sistem Dinamik: ODEINT (SciPy) dan GEKKO
# Model: rho * A * dh/dt = ci * ui - co * uo
# Catatan: untuk Program 3 dan 4 install dulu dengan  pip install gekko


# ==============================================================
# Program 1: Simulasi TPS Tanpa Pengangkutan Truk (ODEINT)
# ==============================================================
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# model TPS: tinggi tumpukan sampah h(t)
def tps(h, t, ui, uo):
    rho = 250.0    # massa jenis sampah (kg/m3)
    A = 10.0       # luas alas TPS (m2)
    ci = 10.0      # koefisien sampah masuk (kg/hari per %)
    co = 40.0      # koefisien pengangkutan truk (kg/hari per %)
    # laju perubahan tinggi tumpukan (m/hari)
    dhdt = (ci * ui - co * uo) / (rho * A)
    return dhdt

# waktu simulasi 8 hari, setiap 0.1 hari
ts = np.linspace(0, 8, 81)

# aktivitas warga (ui) dan truk (uo)
ui = 100.0 * np.ones(81)   # warga membuang sampah setiap hari
uo = np.zeros(81)          # truk tidak pernah datang

# kondisi awal dan batas TPS
h_awal = 0.5
hmax = 2.0

# untuk menyimpan hasil
z = np.zeros(81)
z[0] = h_awal

# simulasi dengan ODEINT
h = h_awal
for i in range(80):
    y = odeint(tps, h, [0, 0.1], args=(ui[i + 1], uo[i + 1]))
    h = y[-1][0]       # ambil titik terakhir
    z[i + 1] = h       # simpan tinggi untuk plot

# cek batas TPS
t_lewat = ts[np.argmax(z > hmax)]
print("Tumpukan melewati batas pada t =", round(t_lewat, 1), "hari")
print("Tinggi akhir =", round(z[-1], 2), "m")

# plot hasil
plt.figure(figsize=(8, 5))
plt.subplot(2, 1, 1)
plt.title('Simulasi TPS Tanpa Pengangkutan Truk')
plt.plot(ts, z, 'b-', label='Tinggi sampah h(t)')
plt.axhline(hmax, color='k', linestyle=':', label='Batas TPS')
plt.ylabel('Tinggi Sampah h(t), (m)')
plt.legend(frameon=False)
plt.subplot(2, 1, 2)
plt.plot(ts, ui, 'r--', label='ui (warga)')
plt.plot(ts, uo, 'g--', label='uo (truk)')
plt.ylim(-5, 115)
plt.ylabel('Aktivitas u(t), (%)')
plt.xlabel('t, (hari)')
plt.legend(frameon=False, loc='center left')
plt.tight_layout()
plt.show()


# ==============================================================
# Program 2: Simulasi TPS dengan Jadwal Truk Skenario A dan B (ODEINT)
# ==============================================================
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# model TPS: tinggi tumpukan sampah h(t)
def tps(h, t, ui, uo):
    rho = 250.0    # massa jenis sampah (kg/m3)
    A = 10.0       # luas alas TPS (m2)
    ci = 10.0      # koefisien sampah masuk (kg/hari per %)
    co = 40.0      # koefisien pengangkutan truk (kg/hari per %)
    # laju perubahan tinggi tumpukan (m/hari)
    dhdt = (ci * ui - co * uo) / (rho * A)
    return dhdt

# waktu simulasi 16 hari, setiap 0.1 hari
ts = np.linspace(0, 16, 161)

# warga membuang sampah setiap hari
ui = 100.0 * np.ones(161)

# jadwal truk: uo = 100% selama 1 hari pada hari kedatangan
def jadwal_truk(hari_datang):
    uo = np.zeros(161)
    for hari in hari_datang:
        awal = int(round(hari * 10)) + 1
        uo[awal:awal + 10] = 100.0
    return uo

uo_A = jadwal_truk([3, 7, 11, 15])   # skenario A: truk tiap 4 hari
uo_B = jadwal_truk([5, 11])          # skenario B: truk tiap 6 hari

# kondisi awal dan batas TPS
h_awal = 0.5
hmax = 2.0

# simulasi dengan ODEINT
def simulasi(ui, uo):
    h = h_awal
    z = np.zeros(161)
    z[0] = h
    for i in range(160):
        y = odeint(tps, h, [0, 0.1], args=(ui[i + 1], uo[i + 1]))
        h = y[-1][0]        # ambil titik terakhir
        z[i + 1] = h        # simpan tinggi untuk plot
    return z

zA = simulasi(ui, uo_A)
zB = simulasi(ui, uo_B)

# cek batas TPS
for nama, z in [("A", zA), ("B", zB)]:
    if np.any(z > hmax + 1e-6):
        t_lewat = ts[np.argmax(z > hmax + 1e-6)]
        print(f"Skenario {nama}: melewati batas pada t = {t_lewat:.1f} hari")
    else:
        print(f"Skenario {nama}: tidak pernah melewati batas")
    print(f"  tinggi maksimum = {z.max():.2f} m, tinggi akhir = {z[-1]:.2f} m")

# tinggi pada hari bulat
print("hari     A      B")
for hari in range(17):
    print(f"{hari:4d} {zA[hari * 10]:6.2f} {zB[hari * 10]:6.2f}")

# grafik tiap skenario
def plot_skenario(z, uo, judul):
    plt.figure(figsize=(8, 5))
    plt.subplot(2, 1, 1)
    plt.title(judul)
    plt.plot(ts, z, 'b-', label='Tinggi sampah h(t)')
    plt.axhline(hmax, color='k', linestyle=':', label='Batas TPS')
    plt.ylim(0, max(z.max(), hmax) * 1.35)
    plt.ylabel('Tinggi Sampah h(t), (m)')
    plt.legend(frameon=False, ncol=2, loc='upper center')
    plt.subplot(2, 1, 2)
    plt.plot(ts, ui, 'r--', label='ui (warga)')
    plt.plot(ts, uo, 'g--', label='uo (truk)')
    plt.ylim(-5, 115)
    plt.ylabel('Aktivitas u(t), (%)')
    plt.xlabel('t, (hari)')
    plt.legend(frameon=False, loc='center left')
    plt.tight_layout()
    plt.show()

plot_skenario(zA, uo_A, 'Skenario A: Truk Datang Tiap 4 Hari')
plot_skenario(zB, uo_B, 'Skenario B: Truk Datang Tiap 6 Hari')

# perbandingan dua skenario
plt.figure(figsize=(8, 4))
plt.plot(ts, zA, 'b-', label='A (tiap 4 hari)')
plt.plot(ts, zB, 'g--', label='B (tiap 6 hari)')
plt.axhline(hmax, color='k', linestyle=':', label='Batas TPS')
plt.xlabel('t, (hari)')
plt.ylabel('Tinggi Sampah h(t), (m)')
plt.title('Perbandingan Skenario A dan B')
plt.legend(frameon=False)
plt.show()


# ==============================================================
# Program 3: Simulasi TPS dengan Jadwal Truk Skenario A dan B (GEKKO)
# ==============================================================
import numpy as np
from gekko import GEKKO
import matplotlib.pyplot as plt

rho = 250.0    # massa jenis sampah (kg/m3)
A = 10.0       # luas alas TPS (m2)
ci = 10.0      # koefisien sampah masuk (kg/hari per %)
co = 40.0      # koefisien pengangkutan truk (kg/hari per %)
h_awal = 0.5   # tinggi tumpukan awal (m)
hmax = 2.0     # batas tinggi TPS (m)

# waktu simulasi 16 hari, setiap 0.1 hari
ts = np.linspace(0, 16, 161)

# warga membuang sampah setiap hari
ui = 100.0 * np.ones(161)

# jadwal truk: uo = 100% selama 1 hari pada hari kedatangan
def jadwal_truk(hari_datang):
    uo = np.zeros(161)
    for hari in hari_datang:
        awal = int(round(hari * 10)) + 1
        uo[awal:awal + 10] = 100.0
    return uo

uo_A = jadwal_truk([3, 7, 11, 15])   # skenario A: truk tiap 4 hari
uo_B = jadwal_truk([5, 11])          # skenario B: truk tiap 6 hari

# simulasi dengan GEKKO
def simulasi_gekko(ui, uo):
    m = GEKKO(remote=False)                  # buat model GEKKO
    m.time = ts                              # titik waktu
    u_in = m.Param(value=ui)                 # sinyal warga
    u_out = m.Param(value=uo)                # sinyal truk
    h = m.Var(value=h_awal)                  # tinggi tumpukan
    m.Equation(rho * A * h.dt() == ci * u_in - co * u_out)   # persamaan model
    m.options.IMODE = 4                      # mode simulasi dinamik
    m.solve(disp=False)
    return np.array(list(h.value))

hA = simulasi_gekko(ui, uo_A)
hB = simulasi_gekko(ui, uo_B)

# cek batas TPS
for nama, z in [("A", hA), ("B", hB)]:
    if np.any(z > hmax + 1e-6):
        t_lewat = ts[np.argmax(z > hmax + 1e-6)]
        print(f"Skenario {nama}: melewati batas pada t = {t_lewat:.1f} hari")
    else:
        print(f"Skenario {nama}: tidak pernah melewati batas")
    print(f"  tinggi maksimum = {z.max():.2f} m, tinggi akhir = {z[-1]:.2f} m")

# plot hasil
plt.figure(figsize=(8, 4))
plt.plot(ts, hA, 'b-', label='A (tiap 4 hari)')
plt.plot(ts, hB, 'g--', label='B (tiap 6 hari)')
plt.axhline(hmax, color='k', linestyle=':', label='Batas TPS')
plt.xlabel('t, (hari)')
plt.ylabel('Tinggi Sampah h(t), (m)')
plt.title('Hasil Simulasi GEKKO')
plt.legend(frameon=False)
plt.show()


# ==============================================================
# Program 4: Perbandingan ODEINT, GEKKO, dan Perhitungan Manual
# ==============================================================
import numpy as np
from scipy.integrate import odeint
from gekko import GEKKO
import matplotlib.pyplot as plt

rho = 250.0    # massa jenis sampah (kg/m3)
A = 10.0       # luas alas TPS (m2)
ci = 10.0      # koefisien sampah masuk (kg/hari per %)
co = 40.0      # koefisien pengangkutan truk (kg/hari per %)
h_awal = 0.5   # tinggi tumpukan awal (m)
hmax = 2.0     # batas tinggi TPS (m)

ts = np.linspace(0, 16, 161)
ui = 100.0 * np.ones(161)

# jadwal truk: uo = 100% selama 1 hari pada hari kedatangan
def jadwal_truk(hari_datang):
    uo = np.zeros(161)
    for hari in hari_datang:
        awal = int(round(hari * 10)) + 1
        uo[awal:awal + 10] = 100.0
    return uo

uo_A = jadwal_truk([3, 7, 11, 15])   # skenario A
uo_B = jadwal_truk([5, 11])          # skenario B

# model untuk ODEINT
def tps(h, t, ui, uo):
    return (ci * ui - co * uo) / (rho * A)

def simulasi_odeint(ui, uo):
    h = h_awal
    z = np.zeros(161)
    z[0] = h
    for i in range(160):
        y = odeint(tps, h, [0, 0.1], args=(ui[i + 1], uo[i + 1]))
        h = y[-1][0]
        z[i + 1] = h
    return z

# model untuk GEKKO
def simulasi_gekko(ui, uo):
    m = GEKKO(remote=False)
    m.time = ts
    u_in = m.Param(value=ui)
    u_out = m.Param(value=uo)
    h = m.Var(value=h_awal)
    m.Equation(rho * A * h.dt() == ci * u_in - co * u_out)
    m.options.IMODE = 4
    m.solve(disp=False)
    return np.array(list(h.value))

# perhitungan manual per hari (metode Euler, dt = 1 hari)
def manual(hari_datang):
    h = h_awal
    hasil = [h]
    for n in range(16):
        u_truk = 100.0 if n in hari_datang else 0.0
        h = h + 1.0 * (ci * 100.0 - co * u_truk) / (rho * A)
        hasil.append(h)
    return np.array(hasil)

hA_ode = simulasi_odeint(ui, uo_A)
hB_ode = simulasi_odeint(ui, uo_B)
hA_gek = simulasi_gekko(ui, uo_A)
hB_gek = simulasi_gekko(ui, uo_B)
hA_man = manual([3, 7, 11, 15])
hB_man = manual([5, 11])

# selisih terbesar antar metode
print("Selisih maksimum ODEINT vs GEKKO   A:", np.abs(hA_ode - hA_gek).max())
print("Selisih maksimum ODEINT vs GEKKO   B:", np.abs(hB_ode - hB_gek).max())
print("Selisih maksimum ODEINT vs manual  A:", np.abs(hA_ode[::10] - hA_man).max())
print("Selisih maksimum ODEINT vs manual  B:", np.abs(hB_ode[::10] - hB_man).max())

# plot perbandingan
plt.figure(figsize=(8, 6))
plt.subplot(2, 1, 1)
plt.title('Skenario A: ODEINT vs GEKKO')
plt.plot(ts, hA_ode, 'b-', linewidth=3, label='ODEINT')
plt.plot(ts, hA_gek, 'r--', label='GEKKO')
plt.plot(np.arange(17), hA_man, 'ko', markersize=4, label='Manual (tiap hari)')
plt.axhline(hmax, color='k', linestyle=':')
plt.ylim(0.3, 2.4)
plt.ylabel('h(t), (m)')
plt.legend(frameon=False, ncol=3, loc='upper center')
plt.subplot(2, 1, 2)
plt.title('Skenario B: ODEINT vs GEKKO')
plt.plot(ts, hB_ode, 'b-', linewidth=3, label='ODEINT')
plt.plot(ts, hB_gek, 'r--', label='GEKKO')
plt.plot(np.arange(17), hB_man, 'ko', markersize=4, label='Manual (tiap hari)')
plt.axhline(hmax, color='k', linestyle=':')
plt.ylabel('h(t), (m)')
plt.ylim(0.3, 4.6)
plt.xlabel('t, (hari)')
plt.legend(frameon=False, ncol=3, loc='upper center')
plt.tight_layout()
plt.show()
