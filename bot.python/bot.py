from aiogram import types, executor, Bot, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database import add_user, add_user_name, add_user_surname, add_user_phone, get_user_name, get_user_surname, \
    get_user_phone, drop_user_reg, add_user_disease, get_user_disease, drop_user_disease

bot = Bot("5869417515:AAG-li-49XccNgxRZ8nvXU0t20I4B20qXTg")
dp = Dispatcher(bot, storage=MemoryStorage())


class user_reg(StatesGroup):
    name = State()
    surname = State()
    phone = State()


class user_disease(StatesGroup):
    disease = State()


class user_consult(StatesGroup):
    symptoms = State()
    headache_symptom = State()
    abdominal_pain_symptom = State()
    throat_discomfort_symptom = State()


async def cancel_category_selection(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    await state.finish()
    await bot.send_message(chat_id, "Selection canceled.", reply_markup=ReplyKeyboardRemove())


symptom_categories = {
    "Headache": {
    },
    "Abdominal Pain": {
    },
    "Throat Discomfort": {
    },
}

categories = list(symptom_categories.keys())


@dp.message_handler(state=user_reg.name)
async def add_name_(message: types.Message, state=FSMContext):
    chat_id = message.chat.id
    await state.finish()
    add_user_name(message)
    await bot.send_message(chat_id, f"Send your surname: ")
    await user_reg.surname.set()


@dp.message_handler(state=user_reg.surname)
async def add_surname_(message: types.Message, state=FSMContext):
    chat_id = message.chat.id
    await state.finish()
    add_user_surname(message)
    await bot.send_message(chat_id, f"Send your phone number: ")
    await user_reg.phone.set()


@dp.message_handler(state=user_reg.phone)
async def add_phone_(message: types.Message, state=FSMContext):
    chat_id = message.chat.id
    await state.finish()
    add_user_phone(message)
    await bot.send_message(chat_id, f"Medical Card added successful! "
                                    f"Congratulation, you are in our base ☺ \n"
                                    f"Your data is important to us and will always be kept confidential 💌 \n\n"
                                    f"If you are looking for suitable medicines, you can always consult with us and visit our Med & Care Pharmacy website, "
                                    f"where you will definitely find something useful for yourself 🌸.")


@dp.message_handler(commands=['drop'])
async def drop_message(message: types.Message, state=FSMContext):
    chat_id = message.chat.id
    drop_user_reg(chat_id)
    await bot.send_message(chat_id, "Your medical card has been deleted!")


@dp.message_handler(commands=['show'])
async def show_message(message: types.Message, state=FSMContext):
    chat_id = message.chat.id
    user_status = add_user(message)
    if user_status == False:
        user_name = get_user_name(chat_id)
        user_surname = get_user_surname(chat_id)
        user_phone = get_user_phone(chat_id)
        user_disease = get_user_disease(chat_id)
        await bot.send_message(chat_id, "Hello!\n"
                                        f"Your name is: {user_name}\n"
                                        f"Your surname is: {user_surname}\n"
                                        f"Your phone number is: {user_phone}\n"
                                        f"Your diagnosed disease is: {user_disease}\n"
                                        f"You are in our base ☺️ "
                                        f"To delete your medical card please use the command /drop \n\n"
                                        f"If you are looking for suitable medicines, you can always consult with us and visit our Med & Care Pharmacy website, "
                                        f"where you will definitely find something useful for yourself 🌸.")
    else:
        await bot.send_message(chat_id, f"You don't have any medical card by your id {message.chat.first_name} :(\n"
                                        f"Please send me your name: ")
        await user_reg.name.set()


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message, state=FSMContext):
    chat_id = message.chat.id
    user_status = add_user(message)
    if user_status == False:
        user_name = get_user_name(chat_id)
        user_surname = get_user_surname(chat_id)
        user_phone = get_user_phone(chat_id)
        user_disease = get_user_disease(chat_id)
        await bot.send_message(chat_id, "Hello!\n"
                                        f"Your name is: {user_name}\n"
                                        f"Your surname is: {user_surname}\n"
                                        f"Your phone number is: {user_phone}\n"
                                        f"Your diagnosed disease is: {user_disease}\n"
                                        f"Congratulation, you are in our base ☺️ \n"
                                        f"Your data is important to us and will always be kept confidential 💌"
                                        f"To delete your medical card, please use the command /drop \n\n"
                                        f"If you are looking for suitable medicines, you can always consult with us and visit our Med & Care Pharmacy website, "
                                        f"where you will definitely find something useful for yourself 🌸.")
    else:
        await bot.send_message(chat_id, f"Hello {message.chat.first_name}! Glad to see you ❤\n"
                                        f"This is the bot that can you help make\n"
                                        f"a medical card to our pharmacy 'Med&Care, so we can see that you our client 📋'\n\n"
                                        f"Please send me your name: ")
        await user_reg.name.set()


@dp.message_handler(commands=['consult'])
async def start_consultation(message: types.Message, state: FSMContext):
    chat_id = message.chat.id

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)  # Adjust the row_width as needed
    buttons = [KeyboardButton(category) for category in categories]

    markup.add(*buttons)

    await bot.send_message(chat_id,
                           "Welcome to the consultation! Please select the area where you feel discomfort 🌱. \n\n"
                           "If you could not find the answers, then it is better for you "
                           "to consult a doctor and buy medicines from us.\n\n"
                           "Know that we have an open platform website 'Med & Care' "
                           "for those who also want to sell their goods, "
                           "doing good and improving health together 🥰",
                           reply_markup=markup)
    await user_consult.symptoms.set()


@dp.message_handler(state=user_consult.symptoms)
async def handle_symptoms(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    selected_symptom = message.text

    if selected_symptom.lower() == 'headache':
        options = "\n".join(symptom_categories[selected_symptom].keys())
        await bot.send_message(chat_id, f"Where exactly does it hurt? Choose: \n"
                                        f"1. front of the head \n"
                                        f"2. back of the head \n"
                                        f"3. one hemisphere or full head \n"
                                        f"4. exit conversation"
                               )
        await state.update_data(selected_symptom=selected_symptom)
        await getattr(user_consult, f"{selected_symptom.replace(' ', '_').lower()}_symptom").set()

    elif selected_symptom.lower() == 'abdominal pain':
        options = "\n".join(symptom_categories[selected_symptom].keys())
        await bot.send_message(chat_id, f"Where exactly does it hurt? Choose: \n"
                                        f"1. upper \n"
                                        f"2. lower \n"
                                        f"3. around the navel \n"
                                        f"4. exit conversation"
                               )
        await state.update_data(selected_symptom=selected_symptom)
        await getattr(user_consult, f"{selected_symptom.replace(' ', '_').lower()}_symptom").set()

    elif selected_symptom.lower() == 'throat discomfort':
        options = "\n".join(symptom_categories[selected_symptom].keys())
        await bot.send_message(chat_id, f"Where exactly does it hurt? Choose: \n"
                                        f"1. sore throat \n"
                                        f"2. swelling \n"
                                        f"3. dryness \n"
                                        f"4. exit conversation"
                               )
        await state.update_data(selected_symptom=selected_symptom)
        await getattr(user_consult, f"{selected_symptom.replace(' ', '_').lower()}_symptom").set()

    else:
        await bot.send_message(chat_id,
                               "Invalid selection. Please choose from the provided categories or type '4' to cancel.")
        await user_consult.symptoms.set()


@dp.message_handler(state=user_consult.headache_symptom)
async def handle_headache_symptom(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    selected_option = message.text

    if selected_option.lower() == "1":
        response_message = (
            "The pain can be caused by stress. We recommend taking care of yourself and "
            "drinking painkillers like Pentalgin to relieve pain. Additionally, consider starting a course "
            "of magnesium with vitamin B6 supplements. Pentalgin is a combined analgesic drug with a unique "
            "formula of five active components to relieve pain, inflammation, and spasms. Magnesium helps with "
            "muscle spasms and has a positive effect on the nervous system.\n\n"
            "All these items are available on our website Med & Care Pharmacy ❤️‍🩹.\n\n"
            "ATTENTION: Consultation with a qualified doctor is essential as there may be contraindications.\т"
            "Type '4' to cancel conversation"
        )
        await bot.send_message(chat_id, response_message)
    elif selected_option.lower() == "2":
        response_message = (
            "In the back of the head can give pain from: fatigue, lack of sleep, strong emotions. "
            "It can also be the cause of pressure problems. This symptom may indicate a number of diseases of the cervical spine, "
            "blood vessels and nerves that require timely diagnosis and treatment ✨. "
            "You can quickly stop the pain in the occipital part of the head with a cold compress 🧊 – you need to attach a gauze napkin "
            "soaked in cold water or a hot water bottle with ice to the problem area. \n"
            "To get rid of the pain faster, we recommend drinking 'Analgin' painkiller, "
            "but if you have problems with low blood pressure, then 'Citramon' and prescribe a rest for yourself. \n\n "
            "Take care of yourself. All these items are available on our website Med & Care Pharmacy ❤️‍🩹. \n\n"
            "ATTENTION: Consultation with a qualified doctor is essential as there may be contraindications.\n"
            "Type '4' to cancel conversation"
        )
        await bot.send_message(chat_id, response_message)
    elif selected_option.lower() == "3":
        response_message = (
            "If you have pain in one hemisphere or the whole head, "
            "then this may be the cause of developing migraines. We strongly recommend that you take a rest "
            "and consult a doctor in case of severe pain. To relieve pain, you can take medications "
            "such as Ibuprofen or Aspirin (acetylsalicylic acid) , which will help reduce discomfort, "
            "as well as dip your feet in warm water 🛁, if possible. \n\n"
            "Take care of yourself. All these items are available on our website Med & Care Pharmacy ❤️‍🩹. \n\n"
            "ATTENTION: Consultation with a qualified doctor is essential as there may be contraindications.\n"
            "Type '4' to cancel conversation "
        )
        await bot.send_message(chat_id, response_message)
    elif selected_option.lower() == "4":
        await bot.send_message(chat_id,
                               "Conversation ended. Feel free to reach out if you have more questions! We always waiting you ✨")
        await state.finish()
    else:
        await bot.send_message(chat_id, "Invalid selection. Please choose a valid option or enter '4' to exit.")


@dp.message_handler(state=user_consult.abdominal_pain_symptom)
async def handle_abdominal_pain_symptom(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    selected_option = message.text

    if selected_option.lower() == "1":
        response_message = (
            "Pain in the upper abdomen is often observed in such common "
            "diseases of the gastrointestinal tract as gastritis, stomach cramps "
            "and disorders of the gallbladder. Maybe you have stomach problems "
            "and you ate something wrong. We recommend taking a course of treatment 'Creon' "
            "or drinking 'Polysorb'. If you have diarrhea, 'Lapiramide' capsules can help you.\n\n"
            "All these items are available on our website Med & Care Pharmacy ❤️‍🩹.\n\n"
            "ATTENTION: Consultation with a qualified doctor is essential as there may be contraindications.\n"
            "Type '4' to cancel conversation"
        )
        await bot.send_message(chat_id, response_message)
    elif selected_option.lower() == "2":
        response_message = (
            "Pain in the lower abdomen — painful sensations of varying intensity in the abdomen below the navel. "
            "Pain can be a symptom of inflammation of the genitourinary organs, poisoning, "
            "appendicitis, hernia pinching, injuries, intestinal problems and some other conditions "
            "and diseases. Make sure that your lower right side does not hurt, otherwise it may be one "
            "of the symptoms of appendicitis. "
            "These are serious problems that should not be ignored. Try taking 'Linex' pills.\n\n"
            "All these items are available on our website Med & Care Pharmacy ❤️‍🩹.\n\n"
            "ATTENTION: Consultation with a qualified doctor is essential as there may be contraindications.\n"
            "Type '4' to cancel conversation"
        )
        await bot.send_message(chat_id, response_message)
    elif selected_option.lower() == "3":
        response_message = (
            "Most often, pain in the navel area is not dangerous and goes away on "
            "its own in a couple of hours. At this time, it is worth giving the digestive "
            "organs a rest. But the main thing is to monitor your well—being. "
            "If the pain does not stop or increases, you should seek medical help "
            "as soon as possible. The stomach, liver, gallbladder, duodenum, small intestine, "
            "appendix can give pain to this area. In most cases, the doctor can guess the cause of the pain"
            "by the nature of the pain and the accompanying symptoms. To confirm the diagnosis, laboratory blood "
            "tests are prescribed, as well as ultrasound (ultrasound), radiography, endoscopic examination or computed tomography.\n\n"
            "All the items are available on our website Med & Care Pharmacy ❤️‍🩹.\n\n"
            "ATTENTION: Consultation with a qualified doctor is essential as there may be contraindications.\n"
            "Type '4' to cancel conversation"
        )
        await bot.send_message(chat_id, response_message)
    elif selected_option.lower() == "4":
        await bot.send_message(chat_id,
                               "Conversation ended. Feel free to reach out if you have more questions! We always waiting you ✨")
        await state.finish()
    else:
        await bot.send_message(chat_id, "Invalid selection. Please choose a valid option or enter '4' to exit.")


@dp.message_handler(state=user_consult.throat_discomfort_symptom)
async def handle_throat_discomfort_symptom(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    selected_option = message.text

    if selected_option.lower() == "1":
        response_message = (
            "A sore throat often indicates inflammation or irritation of the throat, typically due to "
            "infections like the common cold, flu, or strep throat. You can help saltwater gargle: "
            "mix warm water with salt and gargle several times a day to reduce swelling and discomfort. "
            "You need to stay hydrated, drink plenty of fluids, such as water, herbal tea, or warm liquids "
            "with honey and lemon. If the sore throat persists for more than a few days, gets increasingly severe, "
            "or is accompanied by a high fever, it's advisable to seek medical attention. We recommend that you take "
            "pills such as 'Strepsils' or 'Doctor Mom'. They will help to relieve inflammation.\n\n"
            "All these items are available on our website Med & Care Pharmacy ❤️‍🩹.\n\n"
            "ATTENTION: Consultation with a qualified doctor is essential as there may be contraindications.\n"
            "Type '4' to cancel conversation"
        )
        await bot.send_message(chat_id, response_message)
    elif selected_option.lower() == "2":
        response_message = (
            "A swollen throat can be caused by various factors, including infections, allergies, or irritants. "
            "If the swelling persists, worsens, or is accompanied by difficulty breathing, severe pain, or fever, "
            "seek medical attention immediately. Swelling in the throat can sometimes indicate a more serious "
            "condition that requires prompt medical care. We recommend you spray 'Tanflex' and drink warm drinks.\n\n"
            "All these items are available on our website Med & Care Pharmacy ❤️‍🩹.\n\n"
            "ATTENTION: Consultation with a qualified doctor is essential as there may be contraindications.\n"
            "Type '4' to cancel conversation"
        )
        await bot.send_message(chat_id, response_message)
    elif selected_option.lower() == "3":
        response_message = (
            "A dry throat can occur due to various factors like dehydration, dry air, or excessive talking. "
            "If dryness persists for an extended period, consult a healthcare professional. "
            "Persistent dryness could be a symptom of an underlying condition that requires attention. "
            "We recommend that you take a course of treatment with 'ACC' and eat bread and butter, "
            "and also do not forget to drink liquids. If dryness is accompanied by severe pain, difficulty "
            "swallowing or other alarming symptoms, consult a doctor immediately.\n\n"
            "All these items are available on our website Med & Care Pharmacy ❤️‍🩹.\n\n"
            "ATTENTION: Consultation with a qualified doctor is essential as there may be contraindications.\n"
            "Type '4' to cancel conversation"
        )
        await bot.send_message(chat_id, response_message)
    elif selected_option.lower() == "4":
        await bot.send_message(chat_id,
                               "Conversation ended. Feel free to reach out if you have more questions! We always waiting you ✨")
        await state.finish()
    else:
        await bot.send_message(chat_id, "Invalid selection. Please choose a valid option or enter '4' to exit.")


@dp.message_handler(commands=['add_disease'])
async def add_disease(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "Please enter your diagnosed disease:")
    await user_disease.disease.set()


@dp.message_handler(state=user_disease.disease)
async def handle_disease(message: types.Message, state=FSMContext):
    chat_id = message.chat.id
    diagnosed_disease = message.text

    added = add_user_disease(chat_id, diagnosed_disease)
    if added:
        await bot.send_message(chat_id, f"The disease '{diagnosed_disease}' has been added to your profile. \n"
                                        f"To clear your diseases list please use command /drop_disease")
    else:
        await bot.send_message(chat_id, "User profile not found or unable to add the disease :(.")

    await state.finish()


@dp.message_handler(commands=['drop_disease'])
async def drop_disease_message(message: types.Message, state=FSMContext):
    chat_id = message.chat.id
    drop_user_disease(chat_id)
    await bot.send_message(chat_id, "Your diagnosed diseases has been deleted!")


@dp.message_handler(commands=['stop'])
async def stop_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    await state.finish()
    await bot.send_message(chat_id, "Operation canceled. What would you like to do next?")


if __name__ == '__main__':
    executor.start_polling(dp)
