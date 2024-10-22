import os
from rest_framework.views import APIView
from rest_framework.response import Response
from core.utils import combine_chunks
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import FileMeta
from core.serializers import FileMetaSerializer
from django.conf import settings

class InitializeUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        filename = request.data.get('filename')
        file_id = request.data.get('id')
        total_chunks = int(request.data.get('totalChunks', 0))
        user = request.user

        if not filename or not file_id or total_chunks <= 0:
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            folder_path = os.path.join(settings.MEDIA_ROOT, 'Upload' ,str(user.email))
            os.makedirs(folder_path, exist_ok=True)

            # Création ou récupération de l'état d'upload
            upload_state, created = FileMeta.objects.get_or_create(
                id=file_id,
                defaults={
                    'filename': filename,
                    'folder_path': folder_path,
                    'total_chunks': total_chunks,
                    'chunk_number': 0,  # Définir explicitement chunk_number à 0
                    'chunks_processed': 0,
                    'user':user,
                    'is_complete': False
                }
            )

            if not created:
                upload_state.total_chunks = total_chunks
                upload_state.save()

            return Response({
                'status': 'success',
                'file_id': file_id,
                'upload_id': str(upload_state.id),
                'next_chunk': 0,
                'total_chunks': total_chunks
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class UploadChunkView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, upload_id):
        try:
            # Récupérer les données de la requête
            chunk_number = int(request.data.get('chunkNumber'))
            chunk_data = request.FILES.get('chunk')
            filename = request.data.get('filename')
            total_chunks = int(request.data.get('totalChunks'))

            if not chunk_data:
                return Response({"error": "Missing chunk data."}, status=status.HTTP_400_BAD_REQUEST)

            # Vérifiez si l'état de l'upload existe déjà
            upload_state = FileMeta.objects.get(id=upload_id)

            if not upload_state:
                return Response({"error": f"Upload non trouvé pour l'ID: {upload_id}"}, status=status.HTTP_404_NOT_FOUND)

            # Créer un dossier utilisateur dans "Upload/" s'il n'existe pas
            user_folder = os.path.join(settings.MEDIA_ROOT, 'Upload', str(upload_state.user.email))
            os.makedirs(user_folder, exist_ok=True)

            # Créer un sous-dossier "chunks" dans le dossier utilisateur pour stocker les morceaux de fichier
            chunk_folder = os.path.join(user_folder, 'chunks')
            os.makedirs(chunk_folder, exist_ok=True)

            # Sauvegarder le chunk
            chunk_path = os.path.join(chunk_folder, f"chunk_{chunk_number}")
            with open(chunk_path, "wb") as f:
                f.write(chunk_data.read())  # Sauvegarder le contenu du chunk

            # Mettez à jour l'état de l'upload
            upload_state.chunk_number = max(upload_state.chunk_number, chunk_number)
            upload_state.chunks_processed += 1
            upload_state.save()

            # Vérifier si tous les chunks ont été reçus
            if upload_state.chunks_processed == total_chunks:
                # Combiner les chunks
                combined_filename = f"{upload_state.id}.{filename.split('.')[-1]}"  # Renomme le fichier avec l'ID et l'extension d'origine
                combined_path = os.path.join(user_folder, combined_filename)

                all_chunks_present = all(os.path.exists(os.path.join(chunk_folder, f"chunk_{i}")) for i in range(total_chunks))
                if all_chunks_present:
                    # Combiner les chunks en un seul fichier
                    with open(combined_path, "wb") as combined_file:
                        for i in range(total_chunks):
                            chunk_path = os.path.join(chunk_folder, f"chunk_{i}")
                            with open(chunk_path, "rb") as chunk_file:
                                combined_file.write(chunk_file.read())

                    # Supprimer les chunks après la combinaison
                    for i in range(total_chunks):
                        os.remove(os.path.join(chunk_folder, f"chunk_{i}"))

                    # Supprimer le dossier chunks
                    os.rmdir(chunk_folder)

                    # Mettre à jour l'état d'upload comme complet
                    upload_state.is_complete = True
                    upload_state.folder_path = combined_path  # Mettre à jour le chemin final
                    upload_state.save()

                    return Response({
                        'status': 'completed',
                        'upload_id': upload_id,
                        'filename': combined_filename,
                        'path': combined_path,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({"error": f"Tous les chunks ne sont pas présents pour {filename}"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'status': 'ready',
                'upload_id': upload_id,
                'chunk_number': chunk_number,
                'next_chunk': chunk_number + 1 if chunk_number < total_chunks - 1 else None
            }, status=status.HTTP_200_OK)

        except FileMeta.DoesNotExist:
            return Response({"error": "Upload non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)