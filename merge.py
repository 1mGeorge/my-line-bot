import os
import requests
from PyPDF2 import PdfMerger

def download_line_content(message_id, access_token):
    url = f"https://api-data.line.me/v2/bot/message/{message_id}/content"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to download content: {response.status_code} {response.text}")

def send_line_push(user_id, text, access_token):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    payload = {
        "to": user_id,
        "messages": [{"type": "text", "text": text}]
    }
    requests.post(url, headers=headers, json=payload)

def main():
    access_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
    pdf1_id = os.environ.get("PDF1_ID")
    pdf2_id = os.environ.get("PDF2_ID")
    user_id = os.environ.get("USER_ID")

    print(f"Downloading PDF 1: {pdf1_id}")
    content1 = download_line_content(pdf1_id, access_token)
    with open("pdf1.pdf", "wb") as f:
        f.write(content1)

    print(f"Downloading PDF 2: {pdf2_id}")
    content2 = download_line_content(pdf2_id, access_token)
    with open("pdf2.pdf", "wb") as f:
        f.write(content2)

    print("Merging PDFs...")
    if not os.path.exists("news"):
        os.makedirs("news")
        
    merger = PdfMerger()
    merger.append("pdf1.pdf")
    merger.append("pdf2.pdf")
    merger.write("news.pdf")
    merger.close()

    print("Sending success notification...")
    send_line_push(user_id, "The merge is complete and your news.pdf has been updated!", access_token)

if __name__ == "__main__":
    main()
