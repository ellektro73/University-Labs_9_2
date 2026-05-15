"""
дані про країни (населення, площа, щільність)
"""

import json
import os

JSON_FILE = "countries_data.json"
RESULTS_FILE = "output_result.json"

# ========== ПОЧАТКОВІ ДАНІ (10 КРАЇН) ==========
INITIAL_COUNTRIES = [
    {"name": "Україна", "population": 41.0, "area": 603.5},
    {"name": "Польща", "population": 38.0, "area": 312.7},
    {"name": "Німеччина", "population": 83.2, "area": 357.6},
    {"name": "Франція", "population": 67.8, "area": 643.8},
    {"name": "Італія", "population": 60.4, "area": 301.3},
    {"name": "Іспанія", "population": 47.4, "area": 505.9},
    {"name": "Велика Британія", "population": 67.2, "area": 243.6},
    {"name": "Японія", "population": 125.8, "area": 377.9},
    {"name": "США", "population": 331.9, "area": 9833.5},
    {"name": "Канада", "population": 38.2, "area": 9984.7}
]


# ========== ФУНКЦІЇ ДЛЯ РОБОТИ З JSON ==========

def load_data(filename):
    """
    Завантажує дані з JSON файлу
    Якщо файл не існує - створює з початковими даними
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        print(f"✓ Дані завантажено з файлу '{filename}'")
        return data
    except FileNotFoundError:
        print(f"Файл '{filename}' не знайдено. Створюємо новий з початковими даними...")
        save_data(filename, INITIAL_COUNTRIES)
        return INITIAL_COUNTRIES.copy()
    except json.JSONDecodeError as e:
        print(f"Помилка читання JSON файлу: {e}")
        return []
    except Exception as e:
        print(f"Непередбачена помилка: {e}")
        return []


def save_data(filename, data):

    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        print(f"✓ Дані збережено у файл '{filename}'")
        return True
    except IOError as e:
        print(f"Помилка запису у файл: {e}")
        return False
    except Exception as e:
        print(f"Непередбачена помилка: {e}")
        return False


def calculate_density(population, area):

    if area > 0:
        return round(population / area, 2)  # млн осіб / тис. км² = осіб/км²
    return 0


def add_country(data):

    print("\n--- ДОДАВАННЯ НОВОЇ КРАЇНИ ---")
    try:
        name = input("Введіть назву країни: ").strip()
        if not name:
            raise ValueError("Назва країни не може бути порожньою")

        # Перевірка на дублікат
        for country in data:
            if country["name"].lower() == name.lower():
                print(f"Країна '{name}' вже існує!")
                return data

        population = float(input("Введіть чисельність населення (в млн): "))
        area = float(input("Введіть площу (в тис. км²): "))

        if population < 0 or area <= 0:
            raise ValueError("Населення має бути невід'ємним, а площа - додатною")

        new_country = {
            "name": name,
            "population": population,
            "area": area
        }

        data.append(new_country)
        save_data(JSON_FILE, data)
        print(f"✓ Країну '{name}' успішно додано!")

    except ValueError as e:
        print(f"Помилка введення: {e}")
    except Exception as e:
        print(f"Непередбачена помилка: {e}")

    return data


def delete_country(data):

    print("\n--- ВИДАЛЕННЯ КРАЇНИ ---")
    if not data:
        print("Список країн порожній!")
        return data

    name = input("Введіть назву країни для видалення: ").strip()

    for i, country in enumerate(data):
        if country["name"].lower() == name.lower():
            removed = data.pop(i)
            save_data(JSON_FILE, data)
            print(f"✓ Країну '{removed['name']}' успішно видалено!")
            return data

    print(f"Країну '{name}' не знайдено!")
    return data


def display_data(data):

    print("\n" + "=" * 85)
    print("ВМІСТ JSON ФАЙЛУ".center(85))
    print("=" * 85)

    if not data:
        print("Дані відсутні!")
        return

    print(
        f"{'№':<4} {'Назва країни':<25} {'Населення (млн)':<18} {'Площа (тис. км²)':<18} {'Щільність (осіб/км²)':<15}")
    print("-" * 85)

    for i, country in enumerate(data, 1):
        density = calculate_density(country["population"], country["area"])
        print(f"{i:<4} {country['name']:<25} {country['population']:<18.2f} {country['area']:<18.2f} {density:<15.2f}")

    print("=" * 85)
    print(f"ВСЬОГО КРАЇН: {len(data)}")
    print("=" * 85)


def search_country(data):

    print("\n--- ПОШУК ДАНИХ ---")
    if not data:
        print("Дані відсутні!")
        return

    print("Виберіть поле для пошуку:")
    print("1 - Назва країни")
    print("2 - Населення (діапазон)")
    print("3 - Площа (діапазон)")

    choice = input("Ваш вибір (1/2/3): ").strip()

    results = []

    if choice == '1':
        search_name = input("Введіть назву країни (або частину назви): ").strip().lower()
        results = [c for c in data if search_name in c["name"].lower()]

        if results:
            print(f"\nЗнайдено {len(results)} країн:")
            for country in results:
                density = calculate_density(country["population"], country["area"])
                print(f"  • {country['name']}: населення {country['population']} млн, "
                      f"площа {country['area']} тис. км², щільність {density} осіб/км²")
        else:
            print(f"Країни '{search_name}' не знайдено")

    elif choice == '2':
        try:
            min_pop = float(input("Мінімальне населення (млн): "))
            max_pop = float(input("Максимальне населення (млн): "))
            results = [c for c in data if min_pop <= c["population"] <= max_pop]

            if results:
                print(f"\nЗнайдено {len(results)} країн з населенням від {min_pop} до {max_pop} млн:")
                for country in results:
                    print(f"  • {country['name']}: {country['population']} млн")
            else:
                print("Країни не знайдено")
        except ValueError:
            print("Помилка: введіть коректні числа")

    elif choice == '3':
        try:
            min_area = float(input("Мінімальна площа (тис. км²): "))
            max_area = float(input("Максимальна площа (тис. км²): "))
            results = [c for c in data if min_area <= c["area"] <= max_area]

            if results:
                print(f"\nЗнайдено {len(results)} країн з площею від {min_area} до {max_area} тис. км²:")
                for country in results:
                    print(f"  • {country['name']}: {country['area']} тис. км²")
            else:
                print("Країни не знайдено")
        except ValueError:
            print("Помилка: введіть коректні числа")

    else:
        print("Невірний вибір!")

    return results


def find_max_density_country(data):

    if not data:
        print("Дані відсутні!")
        return None, None

    max_density = -1
    max_country = None

    for country in data:
        density = calculate_density(country["population"], country["area"])
        if density > max_density:
            max_density = density
            max_country = country

    return max_country, max_density


def solve_task(data):

    print("\n" + "=" * 60)
    print("РОЗВ'ЯЗАННЯ ЗАВДАННЯ")
    print("Визначення держави з максимальною щільністю населення")
    print("=" * 60)

    max_country, max_density = find_max_density_country(data)

    if max_country:
        print(f"\nРезультат:")
        print(f"  Держава: {max_country['name']}")
        print(f"  Населення: {max_country['population']} млн")
        print(f"  Площа: {max_country['area']} тис. км²")
        print(f"  Щільність населення: {max_density} осіб/км²")

        # Формуємо результат для збереження
        result = {
            "task": "Визначення держави з максимальною щільністю населення",
            "result": {
                "country_name": max_country["name"],
                "population_million": max_country["population"],
                "area_thousand_km2": max_country["area"],
                "density_people_per_km2": max_density
            },
            "total_countries_analyzed": len(data),
            "all_countries_data": data
        }

        # Зберігаємо результат в інший JSON файл
        try:
            with open(RESULTS_FILE, 'w', encoding='utf-8') as file:
                json.dump(result, file, ensure_ascii=False, indent=2)
            print(f"\n✓ Результат збережено у файл '{RESULTS_FILE}'")
        except Exception as e:
            print(f"Помилка збереження результатів: {e}")

        return max_country
    else:
        print("Немає даних для аналізу!")
        return None


def display_results_file():

    try:
        with open(RESULTS_FILE, 'r', encoding='utf-8') as file:
            results = json.load(file)

        print("\n" + "=" * 60)
        print("ВМІСТ ФАЙЛУ З РЕЗУЛЬТАТАМИ")
        print("=" * 60)
        print(json.dumps(results, ensure_ascii=False, indent=2))

    except FileNotFoundError:
        print(f"Файл '{RESULTS_FILE}' не знайдено. Спочатку виконайте завдання.")
    except Exception as e:
        print(f"Помилка читання файлу: {e}")


# ========== ГОЛОВНА ФУНКЦІЯ ==========
def main():

    # Завантажуємо дані
    data = load_data(JSON_FILE)

    while True:
        print("\n" + "=" * 50)
        print("РОБОТА З JSON ФАЙЛОМ")
        print("=" * 50)
        print("1. Вивести вміст JSON файлу")
        print("2. Додати нову країну")
        print("3. Видалити країну")
        print("4. Пошук даних")
        print("5. Визначити країну з max щільністю (завдання)")
        print("6. Показати результати завдання")
        print("0. Вихід")
        print("-" * 50)

        choice = input("Ваш вибір: ").strip()

        if choice == '1':
            display_data(data)

        elif choice == '2':
            data = add_country(data)

        elif choice == '3':
            data = delete_country(data)

        elif choice == '4':
            search_country(data)

        elif choice == '5':
            solve_task(data)

        elif choice == '6':
            display_results_file()

        elif choice == '0':
            print("\nДо побачення!")
            break

        else:
            print("Невірний вибір. Спробуйте ще раз.")


# ========== ЗАПУСК ПРОГРАМИ ==========
if __name__ == "__main__":
    main()