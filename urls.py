class Urls:
    BASE_URL = 'https://stellarburgers.education-services.ru/'
    CREATE_USER = BASE_URL + '/api/auth/register'   #Создание пользователя
    USER_UPDATE = BASE_URL + '/api/auth/user'    #Получение и обновление информации о пользователе
    USER_DELETE = BASE_URL + '/api/auth/user'   #Удаление пользователя
    CREATE_ORDER = BASE_URL + '/api/orders'   #Создание заказа
    USER_LOGIN = BASE_URL + '/api/auth/login'  #Авторизация пользователя