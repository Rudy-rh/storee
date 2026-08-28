old_func = '@shared_task\ndef send_verifycode_whatsapp(data):\n    logging.info(_("Send verifyCode whatsapp run"))\n\n    to = data.get(\'msisdn\', None)\n    passcode = data.get(\'passcode\', None)\n\n    # modify msisdn\n    if to.startswith(\'0\'):\n        to = to.replace(\'0\', \'62\', 1)\n\n    if to and passcode:\n        url = \'https://api.zuwinda.com/v2/messaging/whatsapp/message\'\n\n        payload = {\n            "content": "Kode Verifikasi Storee Barber %s Jangan berikan kepada siapapun!" % passcode,\n            "accountId": "509849e3-040a-4793-a9d5-ddace5c5bf98",\n        "messageType": "text",\n            "to": to\n        }\n        headers = {\n            \'Accept\': \'application/json\',\n            \'Content-Type\': \'application/json\',\n            \'x-access-key\': settings.ZUWINDA_KEY\n        }\n        r = requests.post(url, json=payload, headers=headers)\n        logging.info(r.status_code)\n    else:\n        logging.warning(\n            _("Tried to send whatsapp to non-existing VerifyCode Code"))\n\n'

new_func = '@shared_task\ndef send_verifycode_whatsapp(data):\n    logging.info(_("Send verifyCode whatsapp run"))\n\n    to = data.get(\'msisdn\', None)\n    passcode = data.get(\'passcode\', None)\n\n    # modify msisdn\n    if to.startswith(\'0\'):\n        to = to.replace(\'0\', \'62\', 1)\n\n    if to and passcode:\n        url = \'https://api.fonnte.com/send\'\n\n        payload = {\n            "target": to,\n            "message": "Kode Verifikasi Storee Barber %s Jangan berikan kepada siapapun!" % passcode\n        }\n        headers = {\n            \'Authorization\': settings.FONNTE_TOKEN\n        }\n        r = requests.post(url, data=payload, headers=headers)\n        logging.info(r.status_code)\n    else:\n        logging.warning(\n            _("Tried to send whatsapp to non-existing VerifyCode Code"))\n\n'

with open('apps/person/tasks.py', 'r') as f:
    content = f.read()

if old_func in content:
    content = content.replace(old_func, new_func)
    with open('apps/person/tasks.py', 'w') as f:
        f.write(content)
    print("BERHASIL")
else:
    print("MASIH GAGAL - butuh cara lain")
