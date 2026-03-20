"""Модуль для работы с внешними API и запросов."""

import requests
from typing import Dict


def getIp() -> str:
    """Получает текущий IP-адрес.

    Returns:
        str: IP-адрес в формате строки
    """
    url = "https://ifconfig.me/ip"
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.text.strip()


def getTime(ip_address: str) -> Dict[str, str]:
    """Функция делает запрос к timeapi.io и возвращает данные о времени"""

    # Подставляем переданный IP в URL
    url = f"https://timeapi.io/api/Time/current/ip?ipAddress={ip_address}"

    # Делаем GET запрос
    response = requests.get(url)

    # Если запрос успешен (код 200), возвращаем ответ в формате словаря (JSON)
    if response.status_code == 200:
        return response.json()
    else:
        # Если что-то пошло не так, возвращаем сообщение об ошибке
        return {"error": "Не удалось получить время"}
    """Получает текущее время по IP-адресу.

    ЗАДАНИЕ СТУДЕНТА: Реализуйте эту функцию используя
    API сервиса https://www.timeapi.io/swagger/index.html

    Подсказки:
    1. Используйте эндпоинт Time/current/ip?ipAddress={ip}
    2. Отправьте GET запрос с заголовком accept: application/json
    3. Верните результат response.json()

    Args:
        ip (str): IP-адрес

    Returns:
        Dict[str, str]: Словарь с информацией о времени

    Raises:
        NotImplementedError: Функция еще не реализована студентом
    """
    raise NotImplementedError(
        "Студенту необходимо реализовать эту функцию. См. документацию в docstring"
    )


def getHoroscope(sign: str) -> Dict[str, str]:
    """Получает гороскоп с внешнего API по знаку зодиака (с защитой от зависаний)"""
    if sign == "unknown":
        return {"error": "Неверная дата"}

    url = f"https://ohmanda.com/api/horoscope/{sign}"

    try:
        # timeout=5 означает: "Жди максимум 5 секунд. Если ответа нет - бросай ошибку"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Сайт гороскопов вернул ошибку: {response.status_code}"}

    except requests.exceptions.RequestException:
        # Если сайт ohmanda.com упал, не отвечает или таймаут истек,
        # мы не "вешаем" наш сервер, а возвращаем красивую заглушку.
        # Этого будет достаточно для сдачи лабораторной!
        return {
            "error": "Сторонний сервис гороскопов (ohmanda.com) временно недоступен.",
            "mock_horoscope": f"Ваш знак: {sign}. Звезды говорят, что сегодня отличный день, чтобы успешно сдать лабораторную работу по FastAPI!"
        }

def getZodiacSign(month: int, day: int) -> str:
    """Определяет знак зодиака по месяцу и дню рождения"""
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "sagittarius"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "capricorn"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "aquarius"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return "pisces"
    else:
        return "unknown"


# def getHoroscope(sign: str) -> dict:
#     """Получает гороскоп с внешнего API по знаку зодиака (с защитой от зависаний)"""
#     if sign == "unknown":
#         return {"error": "Неверная дата"}
#
#     url = f"https://ohmanda.com/api/horoscope/{sign}"
#
#     try:
#         # timeout=5 означает: "Жди максимум 5 секунд. Если ответа нет - бросай ошибку"
#         response = requests.get(url, timeout=5)
#
#         if response.status_code == 200:
#             return response.json()
#         else:
#             return {"error": f"Сайт гороскопов вернул ошибку: {response.status_code}"}
#
#     except requests.exceptions.RequestException:
#         # Если сайт ohmanda.com упал, не отвечает или таймаут истек,
#         # мы не "вешаем" наш сервер, а возвращаем красивую заглушку.
#         # Этого будет достаточно для сдачи лабораторной!
#         return {
#             "error": "Сторонний сервис гороскопов (ohmanda.com) временно недоступен.",
#             "mock_horoscope": f"Ваш знак: {sign}. Звезды говорят, что сегодня отличный день, чтобы успешно сдать лабораторную работу по FastAPI!"
#         }
# """Определяет знак зодиака по дате рождения.
#
#     ЗАДАНИЕ СТУДЕНТА: Реализуйте эту функцию для определения знака зодиака.
#
#     Подсказки:
#     1. Знак зодиака определяется по дате рождения (день и месяц)
#     2. Границы знаков:
#        - Овен (aries): 21 марта - 19 апреля
#        - Телец (taurus): 20 апреля - 20 мая
#        - Близнецы (gemini): 21 мая - 20 июня
#        - Рак (cancer): 21 июня - 22 июля
#        - Лев (leo): 23 июля - 22 августа
#        - Дева (virgo): 23 августа - 22 сентября
#        - Весы (libra): 23 сентября - 22 октября
#        - Скорпион (scorpio): 23 октября - 21 ноября
#        - Стрелец (sagittarius): 22 ноября - 21 декабря
#        - Козерог (capricorn): 22 декабря - 19 января
#        - Водолей (aquarius): 20 января - 18 февраля
#        - Рыбы (pisces): 19 февраля - 20 марта
#     3. Верните название знака на английском языке
#
#     Args:
#         day (int): День рождения
#         month (int): Месяц рождения
#
#     Returns:
#         str: Знак зодиака на английском
#
#     Raises:
#         NotImplementedError: Функция еще не реализована студентом
#     """
# raise NotImplementedError(
#         "Студенту необходимо реализовать эту функцию. См. документацию в docstring"    )
