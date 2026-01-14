import pytest
import requests
from faker import Faker
from urls import Urls
from data import Data

fake = Faker()

@pytest.fixture
def create_user():
    response = requests.post(Urls.CREATE_USER, json=Data.user_data)
    response_data = response.json()

    yield Data.user_data, response_data, response.status_code

    access_token = response_data.get('accessToken')
    requests.delete(Urls.USER_DELETE, headers={'Authorization': access_token})