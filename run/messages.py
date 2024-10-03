from .glob_variables import BotState
from .buttons import Buttons
from utils import db, TweetCapture
from telethon.errors.rpcerrorlist import MessageNotModifiedError


class BotMessageHandler:
    start_message = """
Добро пожаловать в **Music Downloader!** 🎧

Отправьте мне название песни или исполнителя, и я найду и отправлю вам загружаемый трек. 🎶

Чтобы увидеть, что я могу, введите: /help
Или просто нажмите кнопку Инструкции ниже.. 👇
"""

    instruction_message = """
🎧 Бот загрузки музыки 🎧

1. Поделитесь ссылкой на песню из Spotify/YouTube 🔗
2. Подождите подтверждения загрузки 📣
3. Получите файл песни 💾
4. Или отправьте голосовое сообщение с образцом песни 
   для лучшего совпадения и деталей 🎤🔍📩
5. Попросите тексты, информацию об исполнителе и т.д. 📜👨‍🎤

💡 Совет: Ищите по названию, тексту или другим деталям!

📺 Загрузчик YouTube 📺

1. Отправьте ссылку на видео YouTube 🔗
2. Выберите качество видео (если будет предложено) 🎥
3. Подождите загрузки ⏳
4. Получите файл видео 📤

📸 Загрузчик Instagram 📸

1. Отправьте ссылку на пост/Reel/IGTV в Instagram 🔗
2. Подождите загрузки ⏳
3. Получите файл 📤

🐦 TweetCapture 🐦

1. Укажите ссылку на твит 🔗
2. Подождите скриншот 📸
3. Получите скриншот 🖼️
4. Для медиа-контента используйте кнопку "Скачать медиа" 
   после получения скриншота 📥


Для любых вопросов или предложений свяжитесь с @azizkhabdullaev
        """

    search_result_message = """🎵 The following are the top search results that correspond to your query:
"""

    core_selection_message = """🎵 Выберите предпочитаемый способ загрузки 🎵

"""
    JOIN_CHANNEL_MESSAGE = """Похоже, вы еще не являетесь участником нашего канала. Пожалуйста, присоединитесь, чтобы продолжить."""

    search_playlist_message = """В плейлисте содержатся следующие песни:
:"""

    @staticmethod
    async def send_message(event, text, buttons=None):
        chat_id = event.chat_id
        user_id = event.sender_id
        await BotState.initialize_user_state(user_id)
        await BotState.BOT_CLIENT.send_message(chat_id, text, buttons=buttons)

    @staticmethod
    async def edit_message(event, message_text, buttons=None):
        user_id = event.sender_id

        await BotState.initialize_user_state(user_id)
        try:
            await event.edit(message_text, buttons=buttons)
        except MessageNotModifiedError:
            pass

    @staticmethod
    async def edit_quality_setting_message(e):
        music_quality = await db.get_user_music_quality(e.sender_id)
        if music_quality:
            message = (f"Your Quality Setting:\nFormat: {music_quality['format']}\nQuality: {music_quality['quality']}"
                       f"\n\nAvailable Qualities :")
        else:
            message = "No quality settings found."
        await BotMessageHandler.edit_message(e, message, buttons=Buttons.get_quality_setting_buttons(music_quality))

    @staticmethod
    async def edit_core_setting_message(e):
        downloading_core = await db.get_user_downloading_core(e.sender_id)
        if downloading_core:
            message = BotMessageHandler.core_selection_message + f"\nCore: {downloading_core}"
        else:
            message = BotMessageHandler.core_selection_message + "\nNo core setting found."
        await BotMessageHandler.edit_message(e, message, buttons=Buttons.get_core_setting_buttons(downloading_core))

    @staticmethod
    async def edit_subscription_status_message(e):
        is_subscribed = await db.is_user_subscribed(e.sender_id)
        message = f"Subscription settings:\n\nYour Subscription Status: {is_subscribed}"
        await BotMessageHandler.edit_message(e, message,
                                             buttons=Buttons.get_subscription_setting_buttons(is_subscribed))

    @staticmethod
    async def edit_tweet_capture_setting_message(e):
        night_mode = await TweetCapture.get_settings(e.sender_id)
        mode = night_mode['night_mode']
        mode_to_show = "Light"
        match mode:
            case "1":
                mode_to_show = "Dark"
            case "2":
                mode_to_show = "Black"
        message = f"Tweet capture settings:\n\nYour Night Mode: {mode_to_show}"
        await BotMessageHandler.edit_message(e, message, buttons=Buttons.get_tweet_capture_setting_buttons(mode))
