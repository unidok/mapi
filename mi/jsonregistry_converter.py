import json
import base64
import zlib
import os
import requests

os.system("color")
os.chdir(os.path.dirname(os.path.realpath(__file__)))

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"
CYAN  = "\033[36m"

def end(msg: str):
    input(f"{msg}\n\nНажмите ENTER для выхода.")
    exit()


name = input(f"Введите имя файла без расширения: {CYAN}")
print(f"{RESET}Проверка файла...")

if not (os.path.exists(f"{name}.json")):
    end(f"{RED}Файл {CYAN}{name}.json{RED} не существует.{RESET}")

data = open(f"{name}.json", "rb").read()

try:
    data = json.loads(data)
except json.JSONDecodeError as e:
    end(f"{RED}Не удалось разобрать JSON:{RESET} {e}")

if type(data) is not dict:
    end(f"{RED}Содержимое файла должно быть словарём.{RESET}")

if len(data) < 1:
    end(f"{RED}Не обнаружено ни одного модуля.{RESET}")

for module, versions in data.items():
    print(f"Проверка модуля {CYAN}{module}{RESET}...")

    if type(versions) is not dict:
        end(f"    {RED}Значение должно быть словарём.{RESET}") 

    if len(versions) < 1:
        end(f"    {RED}Не обнаружено ни одной версии.{RESET}")

    previousRelease = None

    for version, versionData in versions.items():
        print(f"    Проверка версии {CYAN}{version}{RESET}...")
        if type(versionData) is not dict:
            end(f"        {RED}Значение должно быть словарём.{RESET}")

        if "release" not in versionData:
            end(f"        {RED}Ключ {CYAN}release{RED} не найден.{RESET}")
        
        release = versionData["release"]

        number = type(release)

        if number is int:
            pass
        elif number is float:
            print(f"        {YELLOW}В версии протокола использовано вещественное число, рекомендуется использовать целое.{RESET}")
        else:
            end(f"        {RED}Значение под ключом {CYAN}release{RED} должно быть числом.{RESET}")
        
        if release < 0:
            print(f"        {YELLOW}В версии протокола использовано отрицательное число, рекомендуется использовать положительное или 0.{RESET}")

        if previousRelease != None:
            if previousRelease < release:
                end(f"        {RED}Версии должны быть расположены в порядке убывания (от самой новой до самой старой).{RESET}")

        if "load" not in versionData:
            end(f"        {RED}Ключ {CYAN}load{RED} не найден.{RESET}")

        load = versionData["load"]

        if type(load) is not str:
            end(f"        {RED}Значение под ключом {CYAN}load{RED} должно быть строкой.{RESET}")

        if load.startswith(("http:/", "https:/")):
            try:
                if "handlers" not in requests.get(load).json():
                    end(f"        {RED}Ссылка не вёдет на загрузку модуля или не работает.{RESET}")
            except:
                end(f"        {RED}Ссылка не вёдет на загрузку модуля или не работает.{RESET}")
        else:
            print(f"        {YELLOW}Использована обычная загрузка, рекомендуется использовать загрузку по ссылке.{RESET}")

        previousRelease = release


file = open(name, "wb")
file.write(base64.b64encode(zlib.compress(json.dumps(data, separators=(",", ":")).encode())))
file.close()

end(f"{GREEN}Успешно сохранено в {CYAN}{name}{GREEN}!{RESET}")