import pytest
import requests
import allure
from urls import Urls
from data import Data


class TestCreateUser:
    @allure.title('Проверка успешной регистрации пользователя')
    def test_create_user(self):

        allure.step('Отправка POST-запроса на проверку успешной регистрации пользователя')
        response = requests.post(Urls.CREATE_USER, json=Data.user_data)
        response_data = response.json()

        assert response.status_code == 200 and 'accessToken' in response_data, 'В ответе должен присутствовать accessToken и статус код 200'

        access_token = response_data.get('accessToken')
        delete_response = requests.delete(Urls.USER_DELETE, headers={'Authorization': access_token,
        'Content-Type': 'application/json'})
        assert delete_response.status_code == 202


    @allure.title('Регистрация пользователя, который уже зарегистрирован')
    def test_register_exist_user(self, create_user):
        create_user_data, response_data, status_code = create_user

        allure.step('Отправка POST-запроса регистрации пользователя, который уже зарегистрирован')
        response = requests.post(Urls.CREATE_USER, json=create_user_data)
        response_data = response.json()

        assert response.status_code == 403, "Статус код должен быть 403, если пользователь уже существует"
        assert response_data['success'] == False, "Поле 'success' должно быть False"
        assert response_data['message'] == 'User already exists', "Сообщение должно быть 'User already exists'"


    @allure.title('Регистрация пользователя без обязательных параметров (пароль, email, name)')
    @pytest.mark.parametrize("test_user_data", [
        {"email": "", "password": "qwerty", "name": "Test"},
        {"email": "test@example.com", "password": "", "name": "Test"},
        {"email": "test@example.com", "password": "qwerty", "name": ""}
    ])
    def test_create_user_without_required_field(self, test_user_data):

        allure.step('Отправка POST-запроса регистрации пользователя без обязательных параметров (пароль, email, name)')
        response = requests.post(Urls.CREATE_USER, json=test_user_data)
        response_data = response.json()

        assert response.status_code == 403, "Статус код должен быть 403 при отсутствии обязательных полей"
        assert response_data['success'] == False, "Поле 'success' должно быть False"
        assert response_data['message'] == "Email, password and name are required fields", "Сообщение должно быть 'Email, password and name are required fields'"