import pandas as pd

# Константа тарифов
ST_NORMATIV = 301.26
ST_SCETCHIK = 1.52

# Загружаем данные из таблички
abonents_data = pd.read_csv("абоненты.csv", delimiter=";", encoding="utf-8")


# Рассчитываем начисления
def calculate_charge(row):
    if row["Тип начисления"] == 1:  # По нормативу
        return ST_NORMATIV
    elif row["Тип начисления"] == 2:  # По счетчику
        return (row["Текущее"] - row["Предыдущее"]) * ST_SCETCHIK
    return 0  # На случай, если тип начисления не определен


abonents_data["Начислено"] = abonents_data.apply(calculate_charge, axis=1)

# Сохраняем файл с начислениями по абонентам
abonents_data.to_csv("Начисления_абоненты.csv", sep=";", index=False, encoding="utf-8")

# Группируем начисления по домам
houses_df = (
    abonents_data.groupby(["Улица", "№ дома"], as_index=False)["Начислено"]
        .sum()
        .reset_index()
        .rename(columns={"index": "№ строки"})
)

# Сохраняем файл с начислениями по домам
houses_df.to_csv("Начисления_дома.csv", sep=";", index=False, encoding="utf-8")

print("Готово! Файлы 'Начисления_абоненты.csv' и 'Начисления_дома.csv' созданы.")
