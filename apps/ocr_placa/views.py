from .models import OCR
from apps.core import gateway
from apps.user.models import User
from apps.log.utils import registrar_log
from .serializers import OCRSerializer
from apps.user.views import TokenRequiredMixin
from django.core.files.storage import FileSystemStorage
from .helpers import encontrar_padrao
import base64
import time
import requests
import json


class OCRCreate(TokenRequiredMixin, gateway.Create):
    def create(self, request, *args, **kwargs):
        

        data = request.POST
        data_ = json.dumps(data)
        archive = request.FILES['archive']
        
        fs = FileSystemStorage()
        filename = fs.save(archive.name, archive)
        ocr = OCR.objects.create(
            user= request.user,
            input=data_,
            status="1"
        )
        ocr.save()
        
        api_key = "AIzaSyDAt2Km3VeG5Rc9u2FEqL6sLqrbA3N7F1I"
        image_path = f"./media/{filename}"
            
        # Lendo a imagem e codificando em base64
        with open(image_path, "rb") as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode()

        # Criando o JSON da solicitação
        json_request = {
                "requests": [{
                    "image": {
                        "content": image_base64,
                        # "source": {
                        #     "imageUri": file_url
                        # }
                    },
                    "features": [
                        {
                            "type": "TEXT_DETECTION",
                        }
                    ],
                }
            ]
        }

        url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
        response = requests.post(url, json=json_request)


        if response.status_code == 200:
            data = response.json()

            # Verifica se a resposta contém resultados
            if "responses" in data and len(data["responses"]) > 0:
                # Verifica se há textos encontrados na imagem
                if "textAnnotations" in data["responses"][0]:
                    text_annotations = data["responses"][0]["textAnnotations"]
                    texts_found = []

                    # O primeiro elemento da lista "textAnnotations" é o texto completo encontrado na imagem
                    full_text = text_annotations[0]["description"]
                    texts_found.append(full_text)

                    # Se houver mais elementos na lista, eles podem conter textos adicionais ou detalhes sobre a análise
                    # Você pode decidir se deseja extrair apenas o texto completo ou se precisa de mais informações específicas
                    # Neste exemplo, estou extraindo apenas os textos adicionais encontrados na imagem (caso existam)
                    if len(text_annotations) > 1:
                        for text_data in text_annotations[1:]:
                            texts_found.append(text_data["description"])

                    # Agora, a lista "texts_found" contém os textos encontrados na imagem
                    placa_encontrada = encontrar_padrao(texts_found)
                    print(f"A placa encontrada nesta foto é: {placa_encontrada}")

                else:
                    print("Nenhum texto encontrado na imagem.")
            else:
                print("Resposta inválida ou nenhum resultado retornado.")
        else:
            print("Erro na requisição:", response.status_code)
            
        ocr = OCR.objects.filter(id=ocr.id).values().last()
        ocr.update(output={"placas":placa_encontrada})
            

        # registrar_log(request, OCRSerializer(instance=ocr).data)

        return gateway.response_log_user(request, content=OCRSerializer(instance=ocr).data)


class OCRRetrieve(TokenRequiredMixin, gateway.Retrieve):
    queryset = OCR.objects.filter(is_active=True)
    serializer_class = OCRSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        ocr = OCR.objects.filter(id=instance.id).values().last()
        # registrar_log(request, str(match))
        return gateway.response_log_user(request, ocr)
