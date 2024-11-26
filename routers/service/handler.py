from aiogram import Router
from aiogram.types import Message
from utils import logger

router = Router(name=__name__)


#
# @router.message(F.photo)
# async def handle_photo(msg: Message):
#     await msg.reply("I can`t see could you describe?")


@router.message()
async def message_handler(msg: Message):
    await msg.answer(text=f"Пагади...")
    logger.info(f"{msg.chat.id}")
    try:
        await msg.forward(chat_id=msg.chat.id)
        # await msg.copy_to(chat_id=msg.chat.id)
        # await msg.send_copy(chat_id=msg.chat.id)
    except TypeError:
        await msg.reply(text="Чо то новенькое")
