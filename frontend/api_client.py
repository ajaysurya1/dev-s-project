import requests

BASE_URL = "https://dev-s-project.onrender.com"
def upload_file(file_bytes, file_name):
    response = requests.post(
        BASE_URL + "/upload",
        files={"file": (file_name, file_bytes)}
    )
    return response

def get_documents():
    response = requests.get(BASE_URL + "/documents")
    return response

def delete_document(document_id):
    response = requests.delete(BASE_URL + "/documents/" + str(document_id))
    return response

def preview_document(document_id):
    response = requests.get(BASE_URL + "/documents/" + str(document_id) + "/preview")
    return response

def ask_question(question, document_ids=None):
    payload = {"question": question}
    if document_ids:
        payload["document_ids"] = document_ids
    response = requests.post(BASE_URL + "/query", json=payload)
    return response

def check_health():
    try:
        response = requests.get(BASE_URL + "/health", timeout=15)
        return response.status_code == 200
    except Exception:
        return False
