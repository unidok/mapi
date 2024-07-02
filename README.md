> Документация написана для 0.9

# MAPI
Module API - ядро для модулей, использующихся на сервере JustMC. Оно похоже на ядро Bukkit для серверов в майнкрафте, только Bukkit загружает плагины, а MAPI загружает модули.





# Содержание
1. [Регистрация модуля в MAPI](#Регистрация-модуля-в-MAPI)
2. [Структура модуля](#Структура-модуля)
3. [Команды](#Команды)
4. [Структура команды](#Структура-команды)
5. [Обработка команды](#Обработка-команды)
6. [Структура аргументов команды](#Структура-аргументов-команды)
7. [Настройки команды](#Настройки-команды)
8. [Кастомные типы аргументов](#Кастомные-типы-аргументов)
9. [Структура типа аргумента](#Структура-типа-аргумента)
10. [Реестр MI](#Реестр-MI)
11. [Игровые переменные](#Игровые-переменные)
12. [Сохранённые переменные](#Сохранённые-переменные)





# Регистрация модуля в MAPI
Чтобы создать модуль для MAPI, необходимо при запуске мира создать словарь в игровую переменную `mapi=имямодуля`. В имени модуля не должно быть пробелов и двоеточий, лучше всего писать просто латиницей в нижнем регистре, например: `worldedit`, `mapi`, `mymodule`. Далее эту переменную будем называть "основной переменной модуля".

```kt
Событие мира<Запуск мира> {
    var `mapi=имя` = Действие над переменной::Создать словарь из значений();
}
```





# Структура модуля
### `version`: **Текст**
> Версия модуля.
-
> [!WARNING]
> Обязательный параметр.

### `release`: **Число**
> Версия протокола модуля.

> [!NOTE]
> Принято указывать целое число, начиная с 0.

> [!WARNING]
> Обязательный параметр.

### `description`: **Текст**
> Описание модуля.

### `authors`: **Список<Текст>**
> Авторы модуля.

> [!TIP]
> Здесь можно указывать просто текст, и он автоматически разделится по пробелу.

### `commands`: **Список<[Команда](#Структура-команды)>**
> Команды модуля.

> [!TIP]
> Также можно сделать просто **Список<Текст>**, но тексты должны быть в виде JSON, и в нём можно не указывать `{` в начале и `}` в конце.

### `dependencies`: **Словарь<Текст, Текст>**
> Необходимые зависимости модуля. Без них модуль будет отключён: его команды не будут работать, и он будет подсвечен красным в команде `about`, и в его "проблемы" будет добавлена ошибка. В ключ указывается имя необходимого модуля, а в значение - его версию.
 
> [!TIP]
> Если указать `>=` перед версией, например, `>=1.0.2`, то будет требовать с протоколом версии `1.0.2` и выше.\
> Если указать `~`, например, `~1.0`, то будет требовать все версии с таким протоколом, как у `1.0`.

### `argumentTypes`: **Словарь<Текст, [Тип аргумента](#Структура-типа-аргумента)>**
> Добавляемые типы аргументов для команд.

> [!TIP]
> Также можно сделать просто **Список<Текст>**, но тексты должны быть в виде JSON, и в нём можно не указывать `{` в начале и `}` в конце.


### `links`: **Словарь<Текст, Текст>**
> Ссылки. В ключ указывается название (любой текст), а в значение - ссылку. Ссылки можно посмотреть при помощи команды `about <модуль>`.

### `legacyCommands`: **Список<Текст>**
> Добавляемые legacy-команды. Legacy-команды - это команды, сделанные не с помощью MAPI, и добавлен список таких команд, чтобы MAPI не конфликтовало с ними. Legacy-команду также можно добавить при помощи команды `lcmd add <команда>`.





# Команды
У каждого модуля могут быть свои команды. Чтобы ввести команду, нужно начать её со специального префикса команды. Он хранится в игровой переменной `pcmd`, и по умолчанию префикс - `@`.\
Можно вводить как и просто имя команды или её псевдоним, так и полное её название, с указанием модуля: `@mymodule:mycommand`. Это будет полезно, когда в нескольких модулях есть команды с одинаковыми именами, и вы хотите обратиться к ней из определённого модуля.





# Структура команды
### `command`: **Текст**
> Название команды.

> [!WARNING]
> Обязательный параметр.

### `executor`: **Текст**
> Название функции-обработчика команды.

> [!WARNING]
> Обязательный параметр.

### `aliases`: **Список<Текст>**
> Псевдонимы команды, например, у команды `symbols` на JustMC есть псевдонимы: `sym`, `emo`, `emoji`.

### `description`: **Текст**
> Описание команды.





# Обработка команды
Обработчик команды - это функция, которая вызывается при вводе команды. В ней вы можете писать любой код. Из неё можно запускать функцию `Mapi.commandConstructor`, которая принимает локальную переменную (**Список<Текст>**) `args`, в которую пишется конструктор аргументов команды. В этот список кладутся тексты с описанием аргументов. Каждый текст - новый аргумент.
```ts
// Пример команды msg <ник> <сообщение>
var args = Действие с переменной::Создать список(
    "name: player, type: Player",
    "name: message, type: String"
);
Вызвать функцию("Mapi.commandConstructor");
Выбрать цель::Игрок по имени(player);
Действие над игроком::Отправить сообщение(message);
```





# Структура аргументов команды

### `type`: **Текст**
> Тип аргумента. У каждого типа аргумента свой обработчик, который считывает из текста аргумент. 

> [!TIP]
> Существуют базовые типы: `Integer`, `Float`, `Word`, `String`, `Player`, [`Option`](#Настройки-команды).\
> По умолчанию `Word`.

### `name`: **Текст**
> Имя локальной переменной, в которую будет присвоен аргумент. 

> [!TIP]
> Если не указать, то будет имя типа `arg0`, где 0 - индекс аргумента.

### `optional`: **Любое значение**
> Если этот ключ указан, то аргумент будет необязательным.

> [!TIP]
> В случае, когда аргумент не указали при вводе команды, переменная аргумента не будет существовать, и вы можете это использовать для проверки, указан ли этот аргумент.

### `literal`: **Список<Текст>**
> Литералы. Они позволяют вводить не сам аргумент, а какое-либо слово из этого списка, функция-обработчик не будет вызываться, если пользователь указал литерал вместо аргумента. Например, дана команда `number <type: int, literal: [min_value, max_value]>`, и здесь пользователь может ввести как сам аргумент (в данном случае это int, целое число), так и один из литералов (в данном случае `min_value` и `max_value`).

> [!NOTE]
> Если тип - `Word`, то пользователь может ввести только литерал. Например, дана команда `list <literal: [add, remove, clear]>` (Тип не указали, поэтому он по умолчанию ставится на `Word`). И пользователь может ввести только `add`, `remove` или `clear`.

> [!WARNING]
> Следующие параметры работют только для `Integer` и `Float`.

### `less`: **Число**
> Проверяет, что число меньше этого.

### `greater`: **Число**
> Проверяет, что число больше этого.

### `min`: **Число**
> Проверяет, что число не меньше этого. 

### `max`: **Число**
> Проверяет, что число не больше этого.

> [!TIP]
> Можно применять несколько условий на один аргумент.

---------------------------------------------

> [!NOTE]
> Все эти аргументы необязательны к указанию, если вам не надо указывать ни один, то вы можете положить пустой текст или пустой словарь в виде JSON: `{}`.





# Настройки команды
Если указать `type: Option` (`option`), то это уже будет аргумент-настройка команды. Он не указывается при вводе команды.

### `permission`: **Текст**
> Право, необходимое для последуещего исполнения команды.

> [!TIP]
> Есть обычные права: `dev`, (`developer`), `build`, (`builder`), `build_or_dev`, `build_and_dev`, (`builder_and_developer`), `whitelist`, (`whitelisted`), `owner`.

> [!NOTE]
> Если указано ни одно из выше перечисленного, то это будет считаться как кастомное право. Кастомные права хранятся в сохранённой переменной у каждого игрока: `permissions_%uuid%`, это **Список<Текст>**.

### `unlimitedArguments`: **Любое значение**
> Если этот ключ указан, то не будет ограничения по количеству аргументов.





# Кастомные типы аргументов
MAPI предоставляет базовые типы аргументов: `Word` (`word`) - слово, `String` (`str`, `string`) - текст (без границ), `Integer` (`int`, `integer`, `Int`) - целое число, `Float` (`float`) - вещественное число, `Player` (`player`) - имя онлайн-игрока. Но вы можете создать свой тип аргумента.

Зарегистрируйте тип: создайте список с JSON-текстами, в котором у вас описаны типы аргументов ([Структура типа аргумента](#Структура-типа-аргумента)), и укажите этот список в основную переменную модуля под ключ `argumentTypes`.

Затем создайте функцию-обработчика этого типа аргумента.
Если вашему типу необходимо определить границу, то стройте по такому плану: (Иначе оставьте только обработку итогового аргумента)
```kt
Если переменная::Существует(#defineBorder) {
    // Обозначение границы аргумента.
} Иначе {
    // Обработка итогового аргумента из текста.
}
```
## Локальные переменные при обработке аргумента
### `#defineBorder`: **Число**
> Существует, если сейчас идёт определение границы аргумента.

### `#border`: **Список<Текст>**
> Если сейчас идёт определение границы, то в эту переменную необходимо присвоить список элементов аргумента.
> Если у вас количество элементов аргумента больше 1, то отсюда вы можете получать эти элементы.

### `wordList`: **Список<Текст>**
> Список оставшихся слов (элементов).

### `wordListSize`: **Число**
> Количество оставшихся слов (элементов).

### `#arg`: **Текст**
> Элементы, объединённые по пробелу, либо просто один элемент.

### `#argValue`: **Любое значение**
> В эту переменную вы должны присвоить значение аргумента.

### `#dataArg`: **Словарь<Текст, Любое значение>**
> Параметры аргумента.

## Вызов исключения/ошибки при обработке аргумента
Чтобы вызвать ошибку, вы должны присвоить ниже перечисленные переменные, и вызвать функцию `Mapi.argumentException`.

### `#argumentException`: **Текст**
> Присвойте к этой переменной текст исключения (ошибки).

> [!TIP]
> Выделяется красным цветом.

### `#arg`: **Текст**
> При необходимости вы можете указать элементы, вызвавшие эту ошибку.

> [!TIP]
> Выделяется красным цветом и подчёркивается.

### `commandInput`: **Текст**
> При необходимости вы можете добавить к этой переменной элементы, предшествующие `#arg`.

> [!TIP]
> Выделяется серым цветом.




# Структура типа аргумента

### `name`: **Текст**
> Имя типа.

> [!WARNING]
> Обязательный параметр.

### `displayName`: **Текст**
> Отображаемое имя типа.

### `aliases`: **Список<Текст>**
> Псевдонимы типа. Например, у типа `Integer` это `Int`, `integer` и `int`.

### `count`: **Число**
> Количество необходимых элементов (слов) для этого типа аргумента. Например, для числа нужен 1 элемент, для вектора - 3 элемента: x, y, z, для местоположения - 5 элементов: x, y, z, yaw, pitch.

> [!NOTE]
> Если у вас произвольное количество элементов, то не указывайте этот ключ. Но тогда вам нужно будет самим определять границу аргумента, об этом рассказывалось в предыдущей главе.

### `handler`: **Текст**
> Название функции, которая обрабатывает этот тип аргумента.

> [!WARNING]
> Обязательный параметр.





# Реестр MI
Module Information - реестр, в котором хранится информация о модулях. Он загружается при помощи веб-запроса. Хранится в JSON, сжатом с помощью Zlib. Реестр используется для более подробной информации при исключениях в необходимых зависимостях.
Структура:
```json
{
    "имямодуля": {
        "версия": {
            "release": 1, // версия протокола
            "load": "https://example.com/" // ссылка для загрузки модуля
        }
        // другие версии (от самой новой до самой старой)
    }
    // другие модули
}
```
Есть [основной реестр](https://raw.githubusercontent.com/unidok/mi/main/registry.txt), который загружается по умолчанию, но можно и создавать собственные:
1. Создайте JSON-файл со специальной структурой, указанной выше.
2. Преобразуйте его с помощью zlib. (Лучше изменить расширение на .txt).
3. Загрузите на любой файлообменник, где можно получать содержимое файла напрямую по ссылке. В тот же GitHub, например.
4. Используйте в мире команду `mi add <ссылка>`
5. Перезагрузите мир

> [!TIP]
> Вы можете попросить меня добавить ваш модуль в основной реестр. (Discord: unidok)




# Игровые переменные

### `mapi`: **Число**
> Если существует, MAPI есть в мире.

### `modules`: **Список<Модуль>**
> Список загруженных модулей.

### `commands`: **Словарь<Текст, Команда>**
> Команды.

### `mapi=имямодуля`: **Словарь<Текст, Любое значение>**
> Основная переменная модуля. (Вместо "имямодуля" должно быть имя модуля, логично)

### `argumentTypes`: **Словарь<Текст, Тип аргумента>**
> Типы аргументов.

### `pcmd`: **Текст**
> Префикс команды. (По умолчанию `@`)



# Сохранённые переменные

### `uuid_%player%`: **Текст**
> UUID игрока с данным именем.

> [!NOTE]
> Когда игрок поменяет ник и зайдёт в мир, то переменная с прошлым ником очистится, и создастся новая.

### `name_%uuid%`: **Текст**
> Имя игрока с данным UUID.

> [!NOTE]
> Когда игрок поменяет ник и зайдёт в мир, то в переменную присвоится новый ник игрока.

### `permissions_%uuid%`: **Список<Текст>**
> Кастомные права игрока с данным UUID.

### `miReminderDays`: **Число**
> Задержка напоминания о перезагрузке реестров. (В днях)

### `mapiDebug`: **Число**
> Если существует, то системные сообщения включены.
