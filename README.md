# Simulasi Dinamik Suhu Ruangan dengan Pemanas

Project Tugas Akhir 06 mata praktikum Pemodelan dan Simulasi.
Nama: Selsa Shafana Alifiyani | NIM: 301240041 | Kelas 4B, Teknik Informatika, Universitas Bale Bandung

## Tujuan

Mengetahui perubahan suhu ruangan T(t) yang dipanaskan oleh pemanas sampai mencapai steady state, dan melihat respons suhu terhadap sinyal step, ramp, dan sinusoida pada daya pemanas.

## Model

Dari kesetimbangan energi:

    C * dT/dt = Q_heater - UA * (T - T_luar)

Diselesaikan dengan metode Euler. Pada steady state:

    T_ss = T_luar + Q_heater / UA = 28 + 200 / 20 = 38 C

| Parameter | Simbol | Nilai |
|---|---|---|
| Kapasitas panas ruangan | C | 50.000 J/K |
| Koefisien kehilangan panas | UA | 20 W/K |
| Daya pemanas | Q_heater | 200 W |
| Suhu awal dan suhu luar | T(0), T_luar | 28 C |
| Selang waktu | dt | 10 s |

## Isi Simulasi

1. Steady state (dibandingkan dengan rumus analitik)
2. Respons step (pemanas menyala pada t = 1.800 s)
3. Respons ramp (daya naik 0 sampai 200 W)
4. Respons sinusoida (daya berosilasi 0 sampai 200 W)
5. Pengaruh suhu luar dari data Kaggle

## Struktur Folder

    simulasi_suhu_ruangan.py
    data/IoT-temp.csv
    grafik/
    requirements.txt
    README.md

## Cara Menjalankan

    pip install -r requirements.txt
    python simulasi_suhu_ruangan.py

Isi `requirements.txt`:

    numpy
    matplotlib
    pandas

## Sumber Data

Temperature Readings: IoT Devices (Kaggle):
https://www.kaggle.com/datasets/atulanandjha/temperature-readings-iot-devices

Data ini dipakai untuk suhu luar dan sebagai pembanding suhu dalam. Parameter C, UA, dan Q_heater bersifat sintetis karena dataset tidak memuat daya pemanas.

