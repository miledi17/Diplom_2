import pytest
import requests
import allure
from urls import Urls
from data import Data


class TestGetOrder:
    @allure.title('Получение заказов авторизованным пользователем')
    def test_get_orders_with_auth(self, create_user):
        create_user_data, response_data, status_code = create_user
        access_token = response_data.get('accessToken')

        allure.step('Отправка POST-запроса на получение заказов авторизованным пользователем')
        requests.post(Urls.CREATE_ORDER, headers={"Authorization": access_token}, data=Data.INGREDIENTS)
        response = requests.get(Urls.CREATE_ORDER, headers={"Authorization": access_token})
        response_data = response.json()

        assert response.status_code == 200, "Статус код должен быть 200"
        assert response_data['success'] == True, "Поле 'success' должно быть True"
        assert 'orders' in response_data, 'В ответе должен присутствовать orders'


    @allure.title('Получение заказов не авторизованным пользователем')
    def test_get_orders_without_auth(self):

        allure.step('Отправка POST-запроса на получение заказов не авторизованным пользователем')
        response = requests.get(Urls.CREATE_ORDER)
        response_data = response.json()

        assert response.status_code == 401, "Статус код должен быть 401"
        assert response_data['message'] == "You should be authorised", "Сообщение должно быть 'You should be authorised'"