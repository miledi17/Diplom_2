import pytest
import requests
import allure
from urls import Urls


class TestLoginUser:
    @allure.title('Логин под существующим пользователем')
    def test_login_existing_user(self, create_user):
        create_user_data, response_data, status_code = create_user
        response = requests.post(Urls.USER_LOGIN, json=create_user_data)
        response_data = response.json()

        assert response.status_code == 200, "Статус код должен быть 200, если пользователь спешно авторизован"
        assert response_data['success'] == True, "Поле 'success' должно быть True"
        assert 'accessToken' in response_data, 'В ответе должен присутствовать accessToken'
        assert 'refreshToken' in response_data, 'В ответе должен присутствовать refreshToken'
        assert response_data['user']['email'] == create_user_data['email'], 'Поле email '
        assert response_data['user']['name'] == create_user_data['name'], ''


    @allure.title('Логин с неверным логином')
    def test_login_with_incorrect_login(self, create_user):
        create_user_data, response_data, status_code = create_user
        login_data_faild = {
            "email": "faild@example.com",
            "password": create_user_data["password"]
        }
        response = requests.post(Urls.USER_LOGIN, json=login_data_faild)
        response_data = response.json()

        assert response.status_code == 401, "Статус код должен быть 401"
        assert response_data['success'] == False, "Поле 'success' должно быть False"
        assert response_data['message'] == 'email or password are incorrect', "Сообщение должно быть 'email or password are incorrect'"


    @allure.title('Логин с неверным паролем')
    def test_login_with_incorrect_password(self, create_user):
        create_user_data, response_data, status_code = create_user
        login_data_faild = {
            "email": create_user_data["email"],
            "password": "faild"
        }
        response = requests.post(Urls.USER_LOGIN, json=login_data_faild)
        response_data = response.json()

        assert response.status_code == 401, "Статус код должен быть 401"
        assert response_data['success'] == False, "Поле 'success' должно быть False"
        assert response_data['message'] == 'email or password are incorrect', "Сообщение должно быть 'email or password are incorrect'"