from twilio.rest import Client
import requests, time
from datetime import datetime

# 🧾 Twilio Credentials (get from your dashboard)
account_sid = 'AC747164e603a45e326cbea1f6e77b644f'
auth_token = 'a61cc584fee48b4443a9a7436d10770e'
from_whatsapp_number='whatsapp:+14155238886'  # Twilio sandbox number
to_whatsapp_number='whatsapp:+919004334065'   # Your phone number with country code

client = Client(account_sid, auth_token)

WALLET = "GBC5OTNEGDC6LS4VRRWKQZ2YGVZWLWFOSK3DR4CSP7GTXQ6V4X4CBWMI"
API_URL = f"https://api.mainnet.minepi.com/accounts/{WALLET}/payments?limit=1&order=desc"

last_tx = None

while True:
    try:
        r = requests.get(API_URL)
        r.raise_for_status()
        record = r.json()["_embedded"]["records"][0]
        tx_hash = record["transaction_hash"]
        amount = record["amount"]
        from_wallet = record.get("from", "")
        to_wallet = record.get("to", "")
        timestamp = datetime.strptime(record["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        timestamp = timestamp.strftime("%Y-%m-%d %H:%M")

        if tx_hash != last_tx:
            if to_wallet == WALLET:
                msg = f"📥 *+{amount} Pi received*\n⏱ {timestamp}\n🧾 Tx: {tx_hash}"
            else:
                msg = f"📤 *-{amount} Pi sent*\n⏱ {timestamp}\n🧾 Tx: {tx_hash}\n➡️ To: {to_wallet}"

            client.messages.create(
                from_=from_whatsapp_number,
                body=msg,
                to=to_whatsapp_number
            )
            print("✅ WhatsApp alert sent")
            last_tx = tx_hash

    except Exception as e:
        print("❌ Error:", e)

    time.sleep(60)  # Check every 60 seconds
