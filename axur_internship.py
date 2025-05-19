# Código feito por Arthur Angelo - 19/05

# Importações necessárias
import os
import sys
import logging
import json
import requests
import base64

from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Config básica de logging 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Conseguir fonte da imagem
def fetch_src(page_url):
    response = requests.get(page_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    img = soup.find("img")

    if not img or not img.get("src"):
        logging.error("Nenhuma imagem encontrada")
        sys.exit(1)

    return img["src"]

# Baixar imagem da fonte
def save_img_from_src(img_src, save_path):
    if img_src.startswith("data:image"):
        header, encoded = img_src.split(",", 1)
        data = base64.b64decode(encoded)
        with open(save_path, "wb") as f:
            f.write(data)
        logging.info(f"Imagem Base64 salva em {save_path}")
    else:
        response = requests.get(img_src, stream=True)
        response.raise_for_status()
        with open(save_path, "wb") as f:
            for chunk in resp.iter_content(8192):
                f.write(chunk)
        logging.info(f"Imagem baixada de {img_src} para {save_path}")
    return save_path

# Mandar imagem para inferência - modelo microsoft-florence-2-large
def infer_image(image_path, api_url, token):
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()

        payload = {
            "model": "microsoft-florence-2-large",
            "messages": [
                {"role": "user", "content": "<DETAILED_CAPTION>"}
        ],
        "image": {
            "data": b64,
            "format": "jpeg"
            }
        }
        headers = { 
            "Authorization": f"Bearer {token}"
        }

        logging.info("Imagem sendo enviada para inferência")
        openai_response = requests.post(api_url, headers=headers, json=payload)

    logging.info(f"Status de resposta da inferência: {openai_response.status_code}")
    if openai_response.status_code != 200:
        logging.error(f"Resposta da API de inferência: {openai_response.text}")

    openai_response.raise_for_status()
    
    result = openai_response.json()
    logging.info("JSON de inferência recebido")
    return result

# Envia json retornado para endpoint de resposta
def submit_response(json_payload, submit_url, token):

    headers = { 
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    logging.info(f"Mensagem sendo enviada para endpoint de resposta: {submit_url}")

    answer_response = requests.post(submit_url, headers=headers, json=json_payload)

    logging.info(f"Status da resposta da submissão: {answer_response.status_code}")
    if answer_response.status_code != 200:
         logging.error(f"Resposta da API de submissão: {answer_response.text}")
    answer_response.raise_for_status()
    logging.info("Envio realizado com sucesso. Status: %s", answer_response.status_code)

def main():
    page_url = "https://intern.aiaxuropenings.com/scrape/44358eaf-b267-45d1-b493-41d129e3027b"
    image_path = "imagem_baixada.jpg"
    infer_url = "https://intern.aiaxuropenings.com/v1/chat/completions"
    submit_url = "https://intern.aiaxuropenings.com/api/submit-response"

    # Carregar .env com token
    load_dotenv()
    token = os.getenv("API_TOKEN")

    if not token:
        logging.error("Token não encontrado")
        sys.exit(1)

    # Fluxo principal - ((1)Adquirir fonte da imagem, (2)Baixar imagem, (3)Enviar imagem para inferência, (4)Enviar resposta)
    img_src = fetch_src(page_url)

    img_file = save_img_from_src(img_src, image_path)
    
    json_result = infer_image(img_file, infer_url, token)

    submit_response(json_result, submit_url, token)

    logging.info("Pipeline finalizado")

if __name__ == "__main__":
    main()
