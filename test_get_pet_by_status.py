import pytest
import requests
import random
from config.links import Links

class TestGetPetByStatus:
    @staticmethod
    def get_pet(status):
        data = {"status": status}
        response = requests.get(Links.FIND_BY_STATUS, params=data)
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
        url = "https://petstore.swagger.io/v2/pet/findByStatus?status=available"
        response = requests.get(url)
        assert response.status_code == 200, "Wrong response code"
        all_ids = [pet["id"] for pet in response.json()]
        random_id = random.choice(all_ids)
        return random_id

    def test_get_pet_by_id(self):
        response = requests.get(f"{Links.HOST}/{self.get_pet_by_id()}")
        assert response.status_code == 200, "Wrong response code"
        assert "name" and "id" and "status" in response.json(), "ID for the pet is incorrect"
        assert response.json()["status"] == "available", "Status is not 'available'"
        assert isinstance(response.json()["id"], int), "ID should be an integer"




