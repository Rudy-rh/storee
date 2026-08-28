with open('apps/person/tasks.py', 'r') as f:
    lines = f.readlines()

# Verifikasi dulu baris 129 dan 144 sesuai yang kita lihat, biar aman
line_129 = lines[128]
line_144 = lines[143]

if 'zuwinda' in line_129 and 'requests.post' in line_144:
    new_block = [
        "        url = 'https://api.fonnte.com/send'\n",
        "        payload = {\n",
        '            "target": msisdn,\n',
        '            "message": "Terima kasih sudah berkunjung ke Storeebarbershop.Sorong hari ini."\n',
        '            "Mohon dukungan Storeelove untuk memberikan rating penilaian kepada kami(penilaian terhadap Manjemen, Barberman, Kasir dan OB kami). Semoga kami terus menjadi lebih baik. Sila klik link ini %s"\n',
        '            "\\n\\n Terima kasih" % link_to\n',
        "        }\n",
        "        headers = {\n",
        "            'Authorization': settings.FONNTE_TOKEN\n",
        "        }\n",
        "        r = requests.post(url, data=payload, headers=headers)\n",
    ]
    lines[128:144] = new_block
    with open('apps/person/tasks.py', 'w') as f:
        f.writelines(lines)
    print("BERHASIL: baris 129-144 diganti ke Fonnte")
else:
    print("GAGAL: baris 129/144 tidak sesuai yang diharapkan - cek manual")
    print("Baris 129 saat ini:", repr(line_129))
    print("Baris 144 saat ini:", repr(line_144))
