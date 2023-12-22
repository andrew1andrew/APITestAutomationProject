import requests


def get_pet(status):
    url = "https://petstore.swagger.io/v2/pet/findByStatus"
    data = {"status": status}
    response = requests.get(url, params=data)
    assert response.status_code == 200, "Wrong response code"
    # assert "category" in response.json(), "No main value for key status"


class TestGetPetByStatus:
    def test_get_pet_available(self):
        get_pet("available")
