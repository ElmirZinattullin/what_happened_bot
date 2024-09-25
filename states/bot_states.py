from telebot.handler_backends import State, StatesGroup


class MyStates(StatesGroup):
    main_menu = State()
    faq_menu = State()
    new_question_input = State()
    complaints_and_suggestions_menu = State()
    clinic_address_city_menu = State()
    clinic_address_city_block_menu = State()
    clinic_address_city_block_street_menu = State()
    clinic_address_clinic_name_menu = State()
    feedback_input = State()
    picture_add_menu = State()
    picture_input = State()
    phone_number_send_menu = State()