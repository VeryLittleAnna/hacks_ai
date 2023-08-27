from rest_framework.views import APIView
import pandas as pd
from .models import NLPmodel
from rest_framework.response import Response
from django.http import JsonResponse
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import json
from .src.base_solution import find_address
from .src.parsing import parsing

class DefaultView(APIView):
    def get(self, request):
        output = [
            {
                "address": output.address,
            } for output in NLPmodel.objects.all()
        ]
        return Response(output)

class NLPmodelView(APIView):

    def get(self, request):
        output = [
            {
                "address": output.address,
            } for output in NLPmodel.objects.all()
        ]
        return Response(output)

    # Основной метод, где происходит основная работа с адресом
    def post(self, request):

        address = request.data.get('address')
        file = request.data.get('file')
        file_ref = request.data.get('file_ref')

        print("УРА ЭТО ЭТОЛОН: ", file_ref)

        print(address)
        # Проверяем, есть ли адрес в запросе
        if address:
            print('Адрес получен', address)

            response_data = {
                "success": False,
                "query": {"address": address},
                "result": []
            }

            success, target_address, target_building_id = find_address(address)

            response_data["success"] = success
            response_data["result"].append({
                "target_building_id": target_building_id,
                "target_address": target_address,
            })

            with open('results/response_signle.json', 'w') as json_file:
                json.dump(response_data, json_file)
                json_file.write('\n')

            print(target_address)
            return JsonResponse({'success': True, 'target_address': target_address})

        elif file:
            print('Файл получен', file)
            dataset = pd.DataFrame(pd.read_csv(file))
            responses = []

            for _, row in dataset.iterrows():
                if len(responses) == 10:
                    break

                response_data = {
                    "success": False,
                    "query": {"address": row['address']},
                    "result": []
                }

                ## АЛГОРИТМ
                success, target_address, target_building_id = find_address(row['address'])


                response_data["success"] = success
                response_data["result"].append({
                    "target_building_id": target_building_id,
                    "target_address": target_address,
                })
                responses.append(response_data)

            with open('results/responses.json', 'w') as json_file:
                for response in responses:
                    json.dump(response, json_file)
                    json_file.write('\n')

            if any(response["success"] for response in responses):
                print('Возвращаются ответы на фронтенд из файла')
                return JsonResponse({'success': True, 'message_file': 'Responses written to file'})
            else:
                return JsonResponse({'success': False, 'message_file': 'No coordinates found in the file'})
        elif file_ref:
            print('Эталонный файл получен', file_ref)
            dataset = pd.DataFrame(pd.read_csv(file_ref))
            parsing(dataset["target_address"], dataset["target_building_id"])
            print("PERFECT")
            return JsonResponse(
                {'success': True, 'message_file': 'Responses written to file'})

        return JsonResponse({'success': False, 'message_file': 'Invalid request method'})
