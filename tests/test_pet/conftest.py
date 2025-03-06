import pytest
import random
from faker import Faker
from core.api.pet_api import Pet


fake = Faker()


@pytest.fixture(scope='module')
def pet_api():
    return Pet()


@pytest.fixture(scope='function')
def get_random_pet(pet_api):
    data = ['available', 'pending', 'sold']
    random_status = random.choice(data)
    rs = pet_api.get_pet_by_status(params={'status': random_status})
    random_pet = random.choice(rs.json())
    pet_id = random_pet.get('id')
    pet_name = random_pet.get('name')
    return pet_id, pet_name


@pytest.fixture(scope='function')
def generate_pet_data():
    random_name = fake.first_name()
    random_status = random.choice(["available", "pending", "sold"])
    pet_data = {
        "id": random.randint(1, 100000),
        "category": {
            "id": random.randint(1, 10),
            "name": fake.word()
        },
        "name": random_name,
        "photoUrls": [f"https://example.com/{random_name}.jpg"],
        "tags": [
            {
                "id": random.randint(1, 100),
                "name": fake.word()
            }
        ],
        "status": random_status
    }

    return pet_data


@pytest.fixture(scope='function')
def delete_pet(pet_api):
    pet_id = None
    yield pet_id
    if pet_id:
        pet_api.delete_pet(pet_id=pet_id)


@pytest.fixture(scope='function')
def create_pet(pet_api, generate_pet_data):
    result = pet_api.create_pet(data=generate_pet_data).json()
    yield result
