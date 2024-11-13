import csv
import logging


from deep_dict_update import deep_dict_update

ADDRESS_IN_MEMORY = {}


def get_address_from_row(clinic_row: list) -> dict:
    """Создает словарь адреса из строки клиники
        clinic_row[0]: Порядковый номер клиники
        clinic_row[1]: Название клиники
        clinic_row[2:]: Уровень адресов с верхнего на нижний
    """
    name = clinic_row[1]
    clinic_address = clinic_row[2:].copy()
    clinic_address.reverse()
    clinic_address_dict = {}
    buffer_address = {}
    for address_level in clinic_address:
        clear_address_level = address_level.strip()
        if address_level:
            if not clinic_address_dict:
                clinic_address_dict[clear_address_level] = name
            else:
                clinic_address_dict[clear_address_level] = clinic_address_dict.copy()
                clinic_address_dict.pop(buffer_address)
            buffer_address = clear_address_level
    return clinic_address_dict

def parse_address(file_name) -> dict:
    """Получить адреса из файла"""
    addresses = {}
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            clinics_csv = csv.reader(file, delimiter=";")
            tittle = next(clinics_csv)
            for clinic in clinics_csv:
                clinic_address = get_address_from_row(clinic)
                if clinic_address:
                    addresses = deep_dict_update(addresses, clinic_address)
    except Exception:
        logging.error("Нет файла clinics.csv")
    return addresses


def get_clinic_address():
    global ADDRESS_IN_MEMORY
    if not ADDRESS_IN_MEMORY:
        logging.debug("ADDRESS init")
        ADDRESS_IN_MEMORY = parse_address("clinics.csv")
        return ADDRESS_IN_MEMORY
    logging.debug("Address in memory")
    return ADDRESS_IN_MEMORY
