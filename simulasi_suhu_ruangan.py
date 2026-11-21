import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Parameter
C = 50000        # J/K
UA = 20          # W/K
Q_on = 200       # W
T_luar = 28      # C
T0 = 28          # C
dt = 10          # s
t_end = 10800    # s (3 jam)

t = np.arange(0, t_end + dt, dt)
tau = C / UA                    # konstanta waktu (s)
T_ss = T_luar + Q_on / UA       # steady state (C)


def simulasi(Q, T_out, T_awal):
    # Metode Euler
    T = np.zeros(len(T_out))
    T[0] = T_awal
    for i in range(1, len(T)):
        dTdt = (1 / C) * (Q[i - 1] - UA * (T[i - 1] - T_out[i - 1]))
        T[i] = T[i - 1] + dTdt * dt
    return T


def plot_dua_panel(waktu, T, Q, judul, T_ref=None, label_ref='',
                   label_atas='Suhu Ruangan T(t)', label_bawah='Q_heater (W)'):
    fig, ax = plt.subplots(2, 1, sharex=True, figsize=(8, 6))
    ax[0].plot(waktu, T, 'b', label=label_atas)
    if T_ref is not None:
        ax[0].plot(waktu, T_ref, 'g--', label=label_ref)
    ax[0].set_ylabel('Suhu T(t) (C)')
    ax[0].set_title(judul)
    ax[0].legend()
    ax[0].grid(True)
    ax[1].plot(waktu, Q, 'r--')
    ax[1].set_ylabel(label_bawah)
    ax[1].set_xlabel('t (s)')
    ax[1].grid(True)
    plt.tight_layout()
    plt.show()


# 1. Steady state (Q konstan)
T_out = np.full_like(t, T_luar, dtype=float)
Q_ss = np.full_like(t, Q_on, dtype=float)
T_euler = simulasi(Q_ss, T_out, T0)
T_analitik = T_luar + (Q_on / UA) * (1 - np.exp(-t / tau))

plt.plot(t, T_euler, 'b', label='Euler')
plt.plot(t, T_analitik, 'g:', label='Analitik')
plt.axhline(T_ss, color='orange', linestyle='--', label=f'Steady State ({T_ss:.0f} C)')
plt.xlabel('Waktu (s)')
plt.ylabel('Suhu T(t) (C)')
plt.title('Simulasi Steady State Suhu Ruangan')
plt.legend()
plt.grid(True)
plt.show()
print(f'T akhir Euler    : {T_euler[-1]:.2f} C')
print(f'T akhir analitik : {T_analitik[-1]:.2f} C')

# 2. Sinyal step: pemanas menyala pada t = 1800 s
Q_step = np.where(t >= 1800, Q_on, 0.0)
T_step = simulasi(Q_step, T_out, T0)
plot_dua_panel(t, T_step, Q_step, 'Respons Step Pemanas')

# 3. Sinyal ramp: daya naik 0 -> 200 W dari t = 1800 s sampai 5400 s
Q_ramp = np.clip((t - 1800) * Q_on / 3600, 0, Q_on)
T_ramp = simulasi(Q_ramp, T_out, T0)
plot_dua_panel(t, T_ramp, Q_ramp, 'Respons Ramp Pemanas')

# 4. Sinyal sinusoida: daya berosilasi 0 - 200 W, periode 3600 s
Q_sin = 100 + 100 * np.sin(2 * np.pi * t / 3600)
T_sin = simulasi(Q_sin, T_out, T0)
plot_dua_panel(t, T_sin, Q_sin, 'Respons Sinusoida Pemanas')

# 5. Gangguan suhu luar dari dataset Kaggle (pemanas mati)
# Ganti nama file sesuai hasil unduhan
df = pd.read_csv('IOT-temp.csv')
mulai = '2018-10-20 07:00'   # awal jendela 25 jam (data lengkap)
df['noted_date'] = pd.to_datetime(df['noted_date'], dayfirst=True)
df['out/in'] = df['out/in'].str.lower()

def rata_per_jam(label):
    d = df[df['out/in'] == label].set_index('noted_date')['temp']
    return d.resample('1h').mean().interpolate().loc[mulai:].iloc[:25]

suhu_luar = rata_per_jam('out')
suhu_dalam = rata_per_jam('in')

t_data = np.arange(len(suhu_luar)) * 3600
t2 = np.arange(0, t_data[-1] + dt, dt)
T_out_data = np.interp(t2, t_data, suhu_luar.values)
T_dalam_data = np.interp(t2, t_data, suhu_dalam.values)
Q_off = np.zeros_like(t2)

T_model = simulasi(Q_off, T_out_data, T_out_data[0])
plot_dua_panel(t2, T_model, T_out_data, 'Pengaruh Suhu Luar (Data Kaggle)',
               T_ref=T_dalam_data, label_ref='Suhu dalam (data)',
               label_atas='Model T(t), pemanas mati', label_bawah='Suhu luar (C)')
