import pytest
import requests


def get_pet(status):
    url = "https://petstore.swagger.io/v2/pet/findByStatus"
    data = {"status": status}
    response = requests.get(url, params=data)
    print(response.json())
    assert response.status_code == 200, "Wrong response code"
    for pet_data in response.json():
        # assert "name" in pet_data and pet_data["name"] == "doggie", "No main value for key status"
        assert "status" in pet_data and pet_data["status"] == status

#@pytest.mark.
class TestGetPetByStatus:
    def test_get_pet_available(self):
        get_pet("available")

    def test_get_pet_pending(self):
        get_pet("pending")

    def test_get_pet_sold(self):
        get_pet("sold")


