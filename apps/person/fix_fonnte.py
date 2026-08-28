with open('apps/person/tasks.py', 'r') as f:
    content = f.read()

old_code = '''    if to and passcode:
        url = 'https://api.zuwinda.com/v2/messaging/whatsapp/message'

        payload = {
            "content": "Kode Verifikasi Storee Barber %s Jangan berikan kepada siapapun!" % passcode,
            "accountId": "509849e3-040a-4793-a9d5-ddace5c5bf98",
            "messageType": "text",
            "to": to
        }
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x-access-key': settings.ZUWINDA_KEY
        }
        r = requests.post(url, json=payload, headers=headers)
        logging.info(r.status_code)
    else:'''

new_code = '''    if to and passcode:
        url = 'https://api.fonnte.com/send'

        payload = {
            "target": to,
            "message": "Kode Verifikasi Storee Barber %s Jangan berikan kepada siapapun!" % passcode
        }
        headers = {
            'Authorization': settings.FONNTE_TOKEN
        }
        r = requests.post(url, data=payload, headers=headers)
        logging.info(r.status_code)
    else:'''

if old_code in content:
    content = content.replace(old_code, new_code)
    with open('apps/person/tasks.py', 'w') as f:
        f.write(content)
    print("BERHASIL: Kode Zuwinda di send_verifycode_whatsapp sudah diganti ke Fonnte")
else:
    print("GAGAL: kode lama tidak ditemukan persis - perlu edit manual")
