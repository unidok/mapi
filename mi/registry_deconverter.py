import json
import base64
import zlib
import os
import requests

os.system("color")
os.chdir(os.path.dirname(os.path.realpath(__file__)))

RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"
CYAN  = "\033[36m"

def end(msg: str):
    input(f"{msg}\n\nНажмите ENTER для выхода.")
    exit()


src = input(f"Введите ссылку/имя файла: {CYAN}")
print(end=RESET)

if src.startswith(("http:/", "https:/")):
    try:
        data = requests.get(src).content
    except:
        end(f"{RED}Ссылка не работает.{RESET}")

    name = input(f"Введите имя файла, в который надо сохранить: {CYAN}") + ".json"
    print(end=RESET)
else:
    if not os.path.exists(src):
        end(f"{RED}Файл {CYAN}{src}{RED} не существует.{RESET}")

    data = open(src, "rb").read()
    name = src + ".json"

try:
    data = zlib.decompress(base64.b64decode(data.replace(b"\n", b"")))
except Exception as e:
    end(f"{RED}Не удалось разжать данные:{RESET} {e}")

try:
    data = json.loads(data)
except json.JSONDecodeError as e:
    end(f"{RED}Не удалось разобрать JSON:{RESET} {e}")

file = open(name, "w")
file.write(json.dumps(data, indent=4))
file.close()

end(f"{GREEN}Успешно сохранено в {CYAN}{name}{GREEN}!{RESET}")