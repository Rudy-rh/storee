with open('apps/person/tasks.py', 'r') as f:
    lines = f.readlines()

# Cari baris kunci
url_line_idx = None
key_line_idx = None
for i, line in enumerate(lines):
    if "url = 'https://api.zuwinda.com/v2/messaging/whatsapp/message'" in line and url_line_idx is None:
        # pastikan ini di dalam fungsi send_verifycode_whatsapp, cek 15 baris sebelumnya
        context = ''.join(lines[max(0,i-15):i])
        if 'send_verifycode_whatsapp' in context:
            url_line_idx = i
    if url_line_idx is not None and 'x-access-key' in line and 'ZUWINDA_KEY' in line:
        key_line_idx = i
        break

if url_line_idx is not None and key_line_idx is not None:
    # cari akhir blok (baris berisi 'r = requests.post' dan 'logging.info(r.status_code)' setelah key_line_idx)
    end_idx = None
    for j in range(key_line_idx, len(lines)):
        if 'logging.info(r.status_code)' in lines[j]:
            end_idx = j
            break

    if end_idx is not None:
        new_lines = [
            "        url = 'https://api.fonnte.com/send'\n",
            "\n",
            "        payload = {\n",
            '            "target": to,\n',
            '            "message": "Kode Verifikasi Storee Barber %s Jangan berikan kepada siapapun!" % passcode\n',
            "        }\n",
            "        headers = {\n",
            "            'Authorization': settings.FONNTE_TOKEN\n",
            "        }\n",
            "        r = requests.post(url, data=payload, headers=headers)\n",
            "        logging.info(r.status_code)\n",
        ]
        lines[url_line_idx:end_idx+1] = new_lines
        with open('apps/person/tasks.py', 'w') as f:
            f.writelines(lines)
        print("BERHASIL - url_line=%d end_line=%d" % (url_line_idx, end_idx))
    else:
        print("GAGAL - end_idx tidak ketemu")
else:
    print("GAGAL - url_line_idx=%s key_line_idx=%s" % (url_line_idx, key_line_idx))
