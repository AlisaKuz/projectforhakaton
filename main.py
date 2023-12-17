
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random

# Инициализация VK API и авторизация
vk_session = vk_api.VkApi(token='vk1.a.LV8q8HpEfJiVtbLlz1O6hwtiCExsTe8q2tMKkX0zdTMH-dhov8ylCKzKxH6I-Ox4IGEuRuh38vAiOM0lj8Whme2vh7yALEVyWKnpxCvWatswWUrUH7lbLaNaxA2yzw2V_DbB00nGjzgoEB6kk0jDpTO5hE51PtmZlswcD7a3DW0peEPzAEHO2MwqnpIkZ6uKsnlkhExZ-LU9N9PzNZvOvA')
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


# Словарь для хранения контекста прошлых обращений пользователей
user_context = {}
# Функция для обработки запросов и отправки ответов
def process_message(event):
    user_id = event.user_id
    message_text = event.text.lower()

    # Если пользователь уже обращался, получаем его контекст
    if user_id in user_context:
        context = user_context[user_id]
    else:
        context = None

    # Обработка запросов в зависимости от контекста
    if context == 'reporting_problem':
        if "адрес" in message_text:
            user_context[user_id] = 'address_problem'
            return "Пожалуйста, уточните адрес проблемы."
        else:
            user_context[user_id] = None
            return "Прошу прощения, не могу понять ваш запрос."

    elif context == 'address_problem':
        # Здесь можно добавить логику для обработки уточнения адреса
        user_context[user_id] = None
        return "Спасибо за информацию. Мы рассмотрим вашу заявку. Документацию по срокам решения можно посмотреть на saitgoroda.ru"

    else:
        if "дыра в асфальте" in message_text.lower() or "дыра" in message_text.lower() or "асфальт" in message_text.lower() :
            user_context[user_id] = 'reporting_problem'
            return "Обращение по проблеме рядом с домом. Пожалуйста, опишите проблему подробнее."
        if "жкх" in message_text.lower():
            user_context[user_id] = 'reporting_problem'
            return "Обращение по проблеме с жкх. Пожалуйста, опишите проблему подробнее."


        else:
            user_context[user_id] = None
            return "Извините, не могу понять ваш запрос. Пожалуйста, уточните."


# Основной цикл бота
for event in longpoll.listen():
    try:
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            # Обрабатываем запрос и получаем ответ
            response = process_message(event)

            # Отправляем ответ пользователю
            vk.messages.send(
                user_id=event.user_id,
                message=response,
                random_id=random.randint(1, 1000)
            )
    except vk_api.exceptions.ApiError as api_error:
        if isinstance(api_error, vk_api.exceptions.ApiError) and api_error.code == 6:
            time.sleep(1)
            continue
    except Exception as e:
        print(f"Произошла ошибка: {e}")
