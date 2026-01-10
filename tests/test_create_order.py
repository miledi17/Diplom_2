import pytest
import requests
import allure
from urls import Urls
from data import Data


class TestCreateOrder:
    @allure.title('Создание заказа с авторизацией')
    def test_create_order_with_auth(self, create_user):
        create_user_data, response_data, status_code = create_user
        access_token = response_data.get('accessToken')
        response = requests.post(Urls.CREATE_ORDER, headers={"Authorization": access_token}, data=Data.INGREDIENTS)
        response_data = response.json()

        assert response.status_code == 200, "Статус код должен быть 200"
        assert response_data['success'] == True, "Поле 'success' должно быть True"
        assert 'name' in response_data, 'В ответе должен присутствовать name'


    @allure.title('Создание заказа без авторизации')
    def test_create_order_without_auth(self):
        response = requests.post(Urls.CREATE_ORDER, data=Data.INGREDIENTS)

        assert response.status_code == 200, "Статус код должен быть 200"
        assert response.json()['success'] is True, "Поле 'success' должно быть True"


    @allure.title('Создание заказа без ингредиентов')
    def test_create_order_without_ingredients(self, create_user):
        create_user_data, response_data, status_code = create_user
        access_token = response_data.get('accessToken')
        response = requests.post(Urls.CREATE_ORDER, headers={"Authorization": access_token})
        response_data = response.json()

        assert response.status_code == 400, "Статус код должен быть 400"
        assert response_data['success'] == False, "Поле 'success' должно быть False"
        assert response_data['message'] == 'Ingredient ids must be provided', "Сообщение должно быть 'Ingredient ids must be provided'"


    @allure.title('Создание заказа с неверным хешем ингредиентов')
    def test_create_order_invalid_hash_ingredients(self, create_user):
        create_user_data, response_data, status_code = create_user
        access_token = response_data.get('accessToken')
        response = requests.post(Urls.CREATE_ORDER, headers={"Authorization": access_token}, data=Data.INVALID_HASH_INGREDIENTS)

        assert response.status_code == 400, "Статус код должен быть 400"