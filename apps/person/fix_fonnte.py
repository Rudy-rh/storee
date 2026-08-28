with open('apps/person/tasks.py', 'r') as f:
    content = f.read()

old_func = '''@shared_task
def send_verifycode_whatsapp(data):
    logging.info(_("Send verifyCode whatsapp run"))

    to = data.get('msisdn', None)
    passcode = data.get('passcode', None)

    # modify msisdn
    if to.startswith('0'):
        to = to.replace('0', '62', 1)

    if to and passcode:
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
    else:
        logging.warning(
            _("Tried to send whatsapp to non-existing VerifyCode Code"))'''

new_func = '''@shared_task
def send_verifycode_whatsapp(data):
    logging.info(_("Send verifyCode whatsapp run"))

    to = data.get('msisdn', None)
    passcode = data.get('passcode', None)

    # modify msisdn
    if to.startswith('0'):
        to = to.replace('0', '62', 1)

    if to and passcode:
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
    else:
        logging.warning(
            _("Tried to send whatsapp to non-existing VerifyCode Code"))'''

if old_func in content:
    content = content.replace(old_func, new_func)
    with open('apps/person/tasks.py', 'w') as f:
        f.write(content)
    print("BERHASIL")
else:
    print("GAGAL - tidak cocok persis")
    # Debug: cari fungsi di file untuk lihat isi sebenarnya
    import re
    match = re.search(r'@shared_task\ndef send_verifycode_whatsapp.*?(?=\n@shared_task|\Z)', content, re.DOTALL)
    if match:
        print("--- ISI FUNGSI SEBENARNYA ---")
        print(repr(match.group()))
