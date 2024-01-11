import allure
import json
import requests
import random
from config.links import LinksPet

class TestGetRequest:
    @staticmethod
    def get_pet(status):
        data = {"status": status}
        response = requests.get(LinksPet.FIND_BY_STATUS, params=data)
        assert response.status_code == 200, "Wrong response code"
        for pet_data in response.json():
            assert "status" in pet_data and pet_data["status"] == status, "No main value for key status"

    def test_get_pet_available(self):
        self.get_pet("available")

    def test_get_pet_pending(self):
        self.get_pet("pending")

    def test_get_pet_sold(self):
        self.get_pet("sold")

    @staticmethod
    def get_pet_by_id():
        response = requests.get(f"{LinksPet.FIND_BY_STATUS}?status=available")
        assert response.status_code == 200, "Wrong response code"
        all_ids = [pet["id"] for pet in response.json()]
        random_id = random.choice(all_ids)
        return random_id

    def test_get_pet_by_id(self):
        response = requests.get(f"{LinksPet.HOST}/{self.get_pet_by_id()}")
        assert response.status_code == 200, "Wrong response code"
        assert "name" and "id" and "status" in response.json(), "ID for the pet is incorrect"
        assert response.json()["status"] == "available", "Status is not 'available'"
        assert isinstance(response.json()["id"], int), "ID should be an integer"


class TestPostRequest:
    @staticmethod
    def test_add_pet():
        body_str = '''{
            "id": 178,
            "category": {
                "id": 178,
                "name": "cat"
            },
            "name": "Mary",
            "photoUrls": [
                "string"
            ],
            "tags": [
                {
                    "id": 0,
                    "name": "british"
                }
            ],
            "status": "available"
        }'''
        body = json.loads(body_str)
        response = requests.post(LinksPet.HOST, json=body)
        with allure.step("Checking in the request post"):
            assert response.status_code == 200, "Wrong response code"
            assert "id" in response.json() and response.json()["id"] == 178, "There is no ID key with value 178 in the response body"
        with allure.step("Post request was completed successfully. Checking in the request 'get_pet_by_id'"):
            response_get_id = requests.get(f"{LinksPet.HOST}/178")
            assert response_get_id.status_code == 200, "Wrong response code"
            assert "id" in response.json() and response.json()["id"] == 178, "There is no ID key with value 178 in the response body"




