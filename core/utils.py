import os

def combine_chunks(folder_path, filename, total_chunks):
    chunk_folder = os.path.join(folder_path, 'chunks')
    target_path = os.path.join(folder_path, filename)
    
    try:
        with open(target_path, "wb") as target_file:
            for i in range(total_chunks):
                chunk_path = os.path.join(chunk_folder, f"chunk_{i}")
                if not os.path.exists(chunk_path):
                    print(f"Erreur : Chunk {i} pour {filename} non trouvé.")
                    return None
                with open(chunk_path, "rb") as source_file:
                    target_file.write(source_file.read())
        
        print(f"Tous les chunks combinés pour {filename}")
        return target_path
    except Exception as e:
        print(f"Erreur lors de la combinaison des chunks : {e}")
        return None    
