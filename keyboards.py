from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from basic_data import TEXTS


texts: dict = TEXTS["keyboards"]


class Keyboards:
    def __init__(self) -> None:
        self.start_new: InlineKeyboardMarkup = InlineKeyboardMarkup(
            inline_keyboard = [
                [
                    InlineKeyboardButton(
                        text = texts["accept"],
                        callback_data = "accept"
                    )
                ]
            ]
        )

        self.start: InlineKeyboardMarkup = InlineKeyboardMarkup(
            inline_keyboard = [
                [
                    InlineKeyboardButton(
                        text = texts["lines"]["list"],
                        callback_data = "lines_list"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text = texts["lines"]["add"],
                        callback_data = "lines_add"
                    ),
                    InlineKeyboardButton(
                        text = texts["lines"]["check"],
                        callback_data = "lines_check"
                    )
                ]
            ]
        )

        self.menu: InlineKeyboardMarkup = InlineKeyboardMarkup(
            inline_keyboard = [
                [
                    InlineKeyboardButton(
                        text = texts["menu"],
                        callback_data = "menu"
                    )
                ]
            ]
        )

    # def cancel(self, lang: str) -> InlineKeyboardMarkup:
    #     markup = InlineKeyboardMarkup()

    #     markup.add(
    #         InlineKeyboardButton(
    #             text = self._texts[lang]["cancel"],
    #             callback_data = "cancel"
    #         )
    #     )

    #     return markup
