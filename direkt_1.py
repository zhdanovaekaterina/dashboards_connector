import logging
import time
import gspread
import config_1 as config
from functions import *


def main_direkt():
    start_time = time.time()

    # Задаем путь для ключей
    path = r'C:\Users\nasedkina\Desktop\Docs\Programming\dashboards_connector\keys\google_key_1.json'

    # Получение листа Google таблиц для работы
    gc = gspread.service_account(filename=path)
    sheet = gc.open_by_key(config.sheet)
    worksheet = sheet.worksheet(config.worksheet_direkt)

    # Импорт доступов
    token = config.token_direkt
    client_login = config.client_login

    # Получение начальной и конечной даты диапазона загрузки данных
    dates = get_needed_data(worksheet)
    if dates is None:
        return None

    # Задание необходимых полей для выгрузки
    field_names = [
                "Date",
                "CampaignName",
                'CampaignId',
                "Impressions",
                "Clicks",
                "Cost"
            ]

    # Импорт данных из Директа
    result = import_direkt_data(token, dates, field_names, client_login)

    # Парсим массив данных в список списков для загрузки в Google таблицы
    if dates[2]:
        values = parse_direkt_tsv_tolist(result, field_names)
    else:
        values = parse_direkt_tsv_tolist(result)

    # Загружаем данные в Google таблицы
    worksheet.append_rows(values)

    end_time = time.time()
    total_time = round((end_time - start_time), 3)
    logging.info(f'Total time: {total_time} s.')


if __name__ == '__main__':
    pass
