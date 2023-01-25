TEXTS: dict = {
    "start": {
        "new": "Правила - ...",
        "default": "..."
    },
    "wait": "Подождите пожалуйста...",
    "lines": {
        "list": {
            "default": "Ваши строки:\n{lines}",
            "format": "{line}"
        },
        "add": {
            "default": "Введите строки в таком формате:\nстрока 1\nстрока 2\nстрока 3",
            "added": {
                "default": "Добавлено: <i>{added_count}</i>\nНе добавлено: <i>{not_added_count}</i>\nВ общем: <i>{total_count}</i>",
                "admins": "#id{user_id} добавил <i>{added_count}</i> строк!"
            }
        },
        "check": {
            "default": "Введите адреса в таком формате:\nстрока 1\nстрока 2\nстрока 3",
            "finished": "Баланс:\n{lines}",
            "format": "<i>{line}</i> - <b>{balance} ETH</b>"
        }
    },
    "keyboards": {
        "accept": "Согласиться ✅",
        "lines": {
            "list": "Мои строки",
            "add": "Добавить строку",
            "check": "Проверить баланс"
        },
        "menu": "Главное меню"
    }
}
