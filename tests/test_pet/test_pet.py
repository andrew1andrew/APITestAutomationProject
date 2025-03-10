import allure
import pytest
from faker import Faker


fake = Faker()


@pytest.mark.parametrize("pet_status", ["available", "pending", "sold"])
def test_get_pet_by_status(pet_api, pet_status):
    """Summary.

    - send a GET request to "/pet", specifying the pet status in query params
    check:
        - check the status code is 200 and the response is a list
        - check that a list of pets with the specified status is returned
    """
    params = {"status": pet_status}

    with allure.step('Make a request to GET "/pet", specifying the pet status in query params'):
        rs = pet_api.get_pet_by_status(params=params)
        result = rs.json()

    with allure.step('Check the status code is 200 and the response is a list'):
        assert rs.status_code == 200, f'Expected status code 200, but got {rs.status_code}'
        assert isinstance(result, list), f"Expected response to be a list, but got {type(rs.json())}"

    with allure.step(f'Check that a list of pets with the status {pet_status} is returned'):
        assert all(
            pet_status == results.get('status')
            for results in result), f"Expected all pets to have status '{pet_status}', but found different \
            status values. Response: {result}"


def test_get_pet_by_id(pet_api, get_random_pet):
    """Summary.

    - get random pet ID
    - send a GET request to "/pet/{pet_id}"
    check:
        - check the status code is 200 and the response is a dictionary
        - check that the name and id in the response matches the expected
    """
    pet_id, pet_name = get_random_pet

    with allure.step(f'Send a GET request to "/pet/{pet_id}"'):
        rs = pet_api.get_pet_by_id(pet_id=pet_id)
        result = rs.json()

    with allure.step('Check the status code is 200 and the response is a dictionary'):
        assert rs.status_code == 200, f'Expected status code 200, but got {rs.status_code}'
        assert isinstance(result, dict), f'Expected response to be a dict, but got {type(rs.json())}'

    with allure.step('Verify that the pet ID and name match the expected values'):
        assert pet_id == result.get('id'), f'Expected pet ID {pet_id}, but got {result.get("id")}'
        assert pet_name == result.get('name'), f'Expected pet name "{pet_name}", but got "{result.get("name")}"'


def test_create_pet(pet_api, generate_pet_data, delete_pet):
    """Summary.

    - generate data for the request body
    - send a POST request to "/pet"
    check:
        - check the status code is 200 and the response is a dictionary
        - check that the pet is created
    """

    with allure.step('Send a POST request to "/pet"'):
        rs = pet_api.create_pet(data=generate_pet_data)
        result = rs.json()

    with allure.step('Сheck the status code is 200 and the response is a dictionary'):
        assert rs.status_code == 200, f'Expected status code 200, but got {rs.status_code}'
        assert isinstance(result, dict), f'Expected response to be a dict, but got {type(rs.json())}'

    with allure.step('Check that the pet is created'):
        assert result == generate_pet_data, f"Expected pet data to be {generate_pet_data}, but got {result}"

    delete_pet = result.get('id')


def test_edit_pet(pet_api, create_pet, delete_pet):
    """Summary.

    - create pet and change name for request body
    - send a PUT request to "/pet"
    check:
        - check the status code is 200 and the response is a dictionary
        - check that the pet name is updated
    """
    pet_data = create_pet
    new_name = fake.first_name()
    pet_data['name'] = new_name

    with allure.step('Send a PUT request to "/pet"'):
        rs = pet_api.edit_pet(data=pet_data)
        result = rs.json()

    with allure.step('Сheck the status code is 200 and the response is a dictionary'):
        assert rs.status_code == 200, f'Expected status code 200, but got {rs.status_code}'
        assert isinstance(result, dict), f'Expected response to be a dict, but got {type(rs.json())}'

    with allure.step('Check that the pet name is updated'):
        assert result.get('name') == new_name, f"Expected pet name to be {new_name}, but got {result.get('name')}"

    delete_pet = result.get('id')


def test_delete_pet(pet_api, create_pet):
    """Summary.

    - create pet and get pet_id
    - send a DELETE request to "/pet/{pet_id}"
    check:
        - check the status code is 404 (pet is deleted)
    """
    pet_id = create_pet.get('id')

    with allure.step(f'Send a DELETE request to "/pet/{pet_id}"'):
        rs = pet_api.delete_pet(pet_id=pet_id)

    with allure.step('Сheck the status code is 404 (pet is deleted)'):
        assert rs.status_code == 404, f'Pet with id {pet_id} is not deleted'


def test_get_pet_by_status_using_mock(mocker, pet_api):
    """Summary.

    - mock the API response to return a 500 error
    - send a GET request to "/pet/findByStatus"
    check:
        - check the status code is 500
        - check the response contains error message
    """
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mock_response.json.return_value = {"error": "Internal Server Error"}
    mocker.patch.object(pet_api, 'get_pet_by_status', return_value=mock_response)

    with allure.step('Send a GET request to "/pet/findByStatus" with mocked server error'):
        rs = pet_api.get_pet_by_status(params={})

    with allure.step('Check the status code is 500'):
        assert rs.status_code == 500, f"Expected status code 500, but got {rs.status_code}"

    with allure.step('Check the response contains error message'):
        assert rs.json() == {"error": "Internal Server Error"}, f"Unexpected error response {rs.json()}"
