import requests
import os
import uuid

# Configuration des informations d'authentification et d'upload
username = 'admin@gmail.com'
password = 'pmc'
url_token = 'http://localhost:8000/api-auth/token/'
url_initialize_upload = 'http://localhost:8000/api/initialize-upload/'  # URL pour initialiser l'upload
url_upload_chunk = 'http://localhost:8000/api/upload-chunk/'  # URL pour uploader les chunks

# Étape 1: Obtenir le token d'authentification
response_token = requests.post(url_token, data={'username': username, 'password': password})

if response_token.status_code == 200:
    token = response_token.json().get('token')
    print(f"Token obtenu : {token}")

    # Étape 2: Initialiser l'upload
    filename = 'typescript-fr.pdf'
    total_chunks = 10
    path_to_file = r"C:\Users\PEMOCHAMDEV\Desktop\typescript-fr.pdf"
    file_size = os.path.getsize(path_to_file)
    chunk_size = file_size // total_chunks

    with open(path_to_file, 'rb') as file:
        data_initialize = {
            'totalChunks': total_chunks,
            'filename': filename,
            'id': str(uuid.uuid4())  # ID unique pour l'upload
        }

        headers = {
            'Authorization': f'Token {token}'
        }

        response_initialize = requests.post(url_initialize_upload, data=data_initialize, headers=headers)

        if response_initialize.status_code == 201:
            response_data = response_initialize.json()
            upload_id = response_data['upload_id']
            print(f"Upload initialized with ID: {upload_id}")

            # Étape 3: Envoyer les chunks
            for chunk_number in range(total_chunks):
                # Lire le fichier chunk par chunk
                file.seek(chunk_number * chunk_size)
                chunk_data = file.read(chunk_size)

                files = {
                    'chunk': ('chunk', chunk_data)
                }

                data_chunk = {
                    'chunkNumber': chunk_number,
                    'filename': filename,
                    'totalChunks': total_chunks
                }

                # Assurez-vous que l'URL inclut l'upload_id
                upload_chunk_url = f"{url_upload_chunk}{upload_id}/"

                response_upload = requests.post(upload_chunk_url, headers=headers, files=files, data=data_chunk)

                print(f"Réponse de l'upload du chunk {chunk_number}: {response_upload.status_code}")
                if response_upload.status_code != 200:
                    print(f"Erreur lors de l'upload du chunk {chunk_number}: {response_upload.text}")

        else:
            print("Erreur lors de l'initialisation de l'upload :", response_initialize.status_code, response_initialize.text)
else:
    print("Erreur lors de l'obtention du token :", response_token.status_code, response_token.text)
