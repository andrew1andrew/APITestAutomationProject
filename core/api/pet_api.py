from requests import Session


class Pet:
    BASE_URL = 'https://petstore.swagger.io/v2/'

    def __init__(self):
        self.base_url = self.BASE_URL
        self.session = Session()

    def get_pet_by_status(self, params={}):
        url = self.base_url + 'pet/findByStatus'
        rs = self.session.get(url, params=params)
        return rs

    def get_pet_by_id(self, pet_id, params={}):
        url = self.base_url + f'pet/{pet_id}'
        rs = self.session.get(url, params=params)
        return rs

    def create_pet(self, data={}):
        url = self.base_url + 'pet'
        rs = self.session.post(url, json=data)
        return rs

    def edit_pet(self, data={}):
        url = self.base_url + 'pet'
        rs = self.session.put(url, json=data)
        return rs

    def delete_pet(self, pet_id):
        url = self.base_url + f'pet/{pet_id}'
        rs = self.session.delete(url)
        return rs
