import json
import pytest
import requests
from config.links import LinksUser
import allure

class TestUserAuth:
    @staticmethod
    @allure.title("POST - create_user")
    @allure.story("Positive")
    def test_create_user():
        body_str = '''{
              "id": 0,
              "username": "andrew_andrew",
              "firstName": "Andrew",
              "lastName": "Andrew",
              "email": "andrew_andrew@gmail.com",
              "password": "andrew123",
              "phone": "string",
              "userStatus": 0 }'''
        body = json.loads(body_str)
        response = requests.post(f"{LinksUser.HOST}", json=body)
        assert response.status_code == 200, "Wrong response code"
        assert "message" in response.json(), "There is no message with success key message in the response"
        #eqw

    @staticmethod
    def test_user_auth():
        body = {"username": "andrew_andrew",
                "password": "andrew123"}
        response = requests.get(LinksUser.USER_LOGIN, data=body)
        assert response.status_code == 200, "Wrong response code"
        assert "logged in user session" in response.json()["message"], "There is no message with success authentication in the response json"
        assert "Authorization" in response.headers["Access-Control-Allow-Headers"], "There is no message 'Authorization' in the response headers"

    @staticmethod
    def test_get_user_by_name():
        username = "string"
        response = requests.get(f"{LinksUser.HOST}/{username}")
        assert response.status_code == 200, "Wrong response code"
        assert "firstName" and "lastName" and "email" in response.json(), "There is no first name, lastName and email is the response"