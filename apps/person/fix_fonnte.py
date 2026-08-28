with open('apps/person/tasks.py', 'r') as f:
    lines = f.readlines()

# Cari baris "if to and passcode:" dan "else:" berikutnya di fungsi send_verifycode_whatsapp
start_idx = None
end_idx = None
for i, line in enumerate(lines):
    if 'def send_verifycode_whatsapp' in line:
        for j in range(i, len(lines)):
            if 'if to and passcode:' in lines[j]:
                start_idx = j
            if start_idx is not None and lines[j].strip() == 'else:':
                end_idx = j
                break
        break

if start_idx is not None and end_idx is not None:
    new_block = [
        '    if to and passcode:\n',
        "        url = 'https://api.fonnte.com/send'\n",
        '\n',
        '        payload = {\n',
        '            "target": to,\n',
        '            "message": "Kode Verifikasi Storee Barber %s Jangan berikan kepada siapapun!" % passcode\n',
        '        }\n',
        '        headers = {\n',
        "            'Authorization': settings.FONNTE_TOKEN\n",
        '        }\n',
        '        r = requests.post(url, data=payload, headers=headers)\n',
        '        logging.info(r.status_code)\n',
        '    else:\n',
    ]
    lines[start_idx:end_idx+1] = new_block
    with open('apps/person/tasks.py', 'w') as f:
        f.writelines(lines)
    print("BERHASIL: fungsi send_verifycode_whatsapp sudah diganti ke Fonnte")
else:
    print("GAGAL: tidak ketemu batas fungsi - start_idx=%s end_idx=%s" % (start_idx, end_idx))
