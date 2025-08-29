class ExpertBot:
    def __init__(self):
        # база знаний = набор правил
        self.rules = [
            {"if": {"температура": "высокая"}, "then": "У вас лихорадка"},
            {"if": {"температура": "высокая", "кашель": "да"}, "then": "Возможно простуда"},
            {"if": {"голова": "болит"}, "then": "Выпейте таблетку от головы"},
        ]

    def diagnose(self, facts: dict):
        """делаем выводы по правилам"""
        conclusions = []
        for rule in self.rules:
            cond = rule["if"]
            # проверяем, совпадают ли все условия
            if all(facts.get(k) == v for k, v in cond.items()):
                conclusions.append(rule["then"])
        return conclusions or ["Не знаю что сказать..."]

# пример использования
bot = ExpertBot()

# у пациента температура высокая и кашель
facts = {"температура": "высокая", "кашель": "да"}

print(bot.diagnose(facts))
