with open('apps/person/tasks.py', 'r') as f:
    content = f.read()

old_code = '''        url = 'https://api.zuwinda.com/v2/messaging/whatsapp/message'
        payload = {
            "content": "Terima kasih sudah berkunjung ke Storeebarbershop.Sorong hari ini."
            "Mohon dukungan Storeelove untuk memberikan rating penilaian kepada kami(penilaian terhadap Manjemen, Barberman, Kasir dan OB kami). Semoga kami terus menjadi lebih baik. Sila klik link ini %s"
            "\\n\\n Terima kasih" % link_to,

            "accountId": settings.ZUWINDA_INSTANCES_ID,
            "messageType": "text",
            "to": msisdn
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

new_code = '''        url = 'https://api.fonnte.com/send'
        payload = {
            "target": msisdn,
            "message": "Terima kasih sudah berkunjung ke Storeebarbershop.Sorong hari ini."
            "Mohon dukungan Storeelove untuk memberikan rating penilaian kepada kami(penilaian terhadap Manjemen, Barberman, Kasir dan OB kami). Semoga kami terus menjadi lebih baik. Sila klik link ini %s"
            "\\n\\n Terima kasih" % link_to
        }
        headers = {
            'Authorization': settings.FONNTE_TOKEN
        }
        r = requests.post(url, data=payload, headers=headers)
        logging.info(r.status_code)
    else:
        logging.warning(
            _("Tried to send whatsapp to non-existing VerifyCode Code"))'''

if old_code in content:
    content = content.replace(old_code, new_code)
    with open('apps/person/tasks.py', 'w') as f:
        f.write(content)
    print("BERHASIL: Kode Zuwinda di send_thanks_to_customer_whatsapp sudah diganti ke Fonnte")
else:
    print("GAGAL: kode lama tidak ditemukan persis - perlu edit manual")
