from telebot.handler_backends import State, StatesGroup


class WhatHappenedStates(StatesGroup):
    main_menu = State()
    faq_menu = State()
    new_question_input = State()
    complaints_and_suggestions_menu = State()
    clinic_address_choosing = State()

    feedback_input = State()
    picture_add_menu = State()
    picture_input = State()
    phone_number_send_menu = State()
    phone_number_send_request = State()
