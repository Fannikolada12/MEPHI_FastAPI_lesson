"""Эндпоинты API для FastAPI приложения."""

from fastapi import APIRouter, Body

from .forms import UserNameParts, BirthDate
from .query import getIp, getTime, getZodiacSign, getHoroscope

router = APIRouter()


@router.get("/")
async def index() -> dict[str, str]:
    """Корневой эндпоинт для проверки работы сервера."""
    return {"status": "Ok"}


@router.get("/users/{username}", name="Hello user")
async def read_user(username: str) -> dict[str, str]:
    """Возвращает приветствие для пользователя.

    Args:
        username: Имя пользователя из пути

    Returns:
        Словарь с сообщением приветствия
    """
    return {"message": f"Hello {username}"}


@router.post("/users/full-name", name="Full name")
async def full_name(user_from: UserNameParts = Body(..., embed=True)) -> dict[str, str]:
    """Возвращает полное имя из частей.

    Args:
        user_from: Модель с частями имени

    Returns:
        Словарь с полным именем
    """
    return {
        "fullName": f"{user_from.lastName.strip()} {user_from.firstName.strip()} {user_from.middleName.strip()}"
    }


@router.get("/users/current/ip", name="Получить текущий ip")
async def current_ip() -> str:
    """Возвращает текущий IP-адрес клиента.

    Returns:
        Строка с IP-адресом
    """
    ip = getIp()
    return ip


@router.get('/users/current/full-time', name='Получить IP и точное время')
async def current_full_time():
    # 1. Сначала получаем IP с помощью готовой функции
    user_ip = getIp()

    # 2. Передаем этот IP в нашу новую функцию
    time_data = getTime(user_ip)

    # 3. Возвращаем результат пользователю
    return {
        "ip": user_ip,
        "time_info": time_data
    }
# ЗАДАНИЕ 1: Реализуйте эндпоинт GET /users/current/full-time
# Этот эндпоинт должен:
# 1. Получить текущий IP-адрес пользователя (используйте функцию getIp())
# 2. По IP-адресу получить текущее время из внешнего API
#    Документация API: https://www.timeapi.io/swagger/index.html
# 3. Вернуть информацию о времени в формате JSON

# @router.get("/users/current/full-time", name="Получить текущее время")
# async def current_full_time() -> dict:
#     """Получает текущее время по IP-адресу.
#
#     Returns:
#         Словарь с информацией о времени
#     """
#     # TODO: Студент должен реализовать этот метод
#     pass


# ЗАДАНИЕ 2: Реализуйте эндпоинт POST /horoscope
# Этот эндпоинт должен:
# 1. Принять дату рождения в теле запроса (модель BirthDate из forms.py)
# 2. Определить знак зодиака по дате рождения
# 3. Получить гороскоп на сегодня для этого знака зодиака
#    API: https://www.ohmanda.com/api/horoscope/
# 4. Вернуть знак зодиака и гороскоп в формате JSON

# @router.post("/horoscope", name="Получить гороскоп")
# async def horoscope(birth_data: BirthDate) -> dict[str, str]:
#     """Возвращает знак зодиака и гороскоп по дате рождения.
#
#     Args:
#         birth_data: Модель с датой рождения
#
#     Returns:
#         Словарь с знаком зодиака и гороскопом
#     """
#     # TODO: Студент должен реализовать этот метод
#     pass
@router.post('/horoscope', name='Получить гороскоп по дате рождения')
async def get_user_horoscope(user_date: BirthDate = Body(...)):
    # Извлекаем месяц и день из полученной даты
    # user_date.birthDate - это объект даты, у которого есть свойства .month и .day
    month = user_date.birthDate.month
    day = user_date.birthDate.day

    # 1. Узнаем знак зодиака
    sign = getZodiacSign(month, day)

    # 2. Получаем гороскоп по этому знаку
    horoscope_data = getHoroscope(sign)

    # 3. Возвращаем красивый ответ пользователю
    return {
        "zodiac_sign": sign,
        "horoscope": horoscope_data
    }