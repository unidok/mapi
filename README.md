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





# Регистрация модуля в MAPI
Чтобы создать модуль для MAPI, необходимо при запуске мира создать словарь в игровую переменную `mapi=имямодуля` В имени модуля не должно быть пробелов и двоеточий, лучше всего писать просто латиницей в нижнем регистре, например: `worldedit`, `mapi`, `mymodule`. Далее эту переменную будем называть "основной переменной модуля".

```kt
Событие мира<Запуск мира> {
    var `mapi=имя` = Действие над переменной::Создать словарь из значений();
}
```





# Структура модуля
### `version`: **Текст**
> Версия модуля.

### `release`: **Число**
> Версия протокола модуля.

### `description`: **Текст**
> Описание модуля.

### `authors`: **Список<Текст>**
> Авторы модуля.

> [!TIP]
> Здесь можно указывать просто текст, и он автоматически разделится по пробелу.

### `commands`: **Список<Команда>**
> Команды модуля.

> [!TIP]
> Также можно сделать просто **Список<Текст>**, но тексты должны быть в виде JSON, и в нём можно не указывать `{` в начале и `}` в конце.

### `dependencies`: **Словарь<Текст, Текст>**
> Необходимые зависимости модуля. Без них модуль будет отключён: его команды не будут работать, и он будет подсвечен красным в команде `about`, и в его "проблемы" будет добавлена ошибка. В ключ указывается имя необходимого модуля, а в значение - его версию.
 
> [!TIP]
> Если указать `>=` перед версией, например, `>=1.0.2`, то будет требовать с протоколом версии `1.0.2` и выше.\
> Если указать `~`, например, `~1.0`, то будет требовать все версии с таким протоколом, как у `1.0`.

### `argumentsTypes`: **Словарь<Текст, Текст>**
> Добавляемые типы аргументов для команд. В ключ указывается имя типа, а в значение - функцию, которая обрабатывает этот тип аргумента.

### `stringArgumentsTypes`: **Список<Текст>**
> Добавляемые сложные типы аргументов для команд. То есть, в них используются пробелы. Для таких типов нужно ещё и определять границу.

### `contacts`: **Словарь<Текст, Текст>**
> Контакты. В ключ указывается название контакта (любой текст), а в значение - ссылку.

### `legacyCommands`: **Список<Текст>**
> Добавляемые legacy-команды.





# Команды
У каждого модуля могут быть свои команды. Чтобы ввести команду, нужно начать её со специального префикса команды. Он хранится в игровой переменной `pcmd`, и по умолчанию он `@`.\
Можно вводить как и просто имя команды или её псевдоним, так и полное её название, с указанием модуля: `@mymodule:mycommand`. Это будет полезно, когда в нескольких модулях есть команды с одинаковыми именами, и вы хотите обратиться к ней из определённого модуля.





# Структура команды
### `command`: **Текст**
> Имя команды.

### `executor`: **Текст**
> Имя обработчика команды.

### `aliases`: **Список<Текст>**
> Псевдонимы команды, например, у команды `spawn` на JustMC есть псевдонимы: `s`, `ы`, `і`.

### `hide`: **Любое значение**
> Скрытость команды. Если этот ключ указан, то команду может посмотреть только игрок, который имеет на неё права. Игрок без прав на неё, даже не будет знать, что такая команда существует. При попытке её ввода, игроку без прав будет выведено сообщение, что такой команды не сущестсвует.

### `description`: **Текст**
> Описание команды.





# Обработка команды
Обработчик команды - это функция, которая вызывается при вводе команды. В ней вы можете писать любой код. Из неё можно запускать функцию `Mapi.commandConstructor`, которая принимает локальную переменную (**Список<Текст>**) `args`, в которую пишется конструктор аргументов команды. В этот список кладутся тексты с описанием аргументов. Каждый текст - новый аргумент.
```ts
// Пример обработки команды msg <ник> <сообщение>
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
> Существуют базовые типы: `Int`, `Number`, `String`, `Player`, [`Option`](#Настройки-команды).\
> Если не указывать, то у вас будет просто одно слово.

### `name`: **Текст**
> Имя локальной переменной, в которую будет присвоен аргумент. 

> [!TIP]
> Если не указать, то будет имя типа `arg0`, где 0 - индекс аргумента.

### `optional`: **Любое значение**
> Если этот ключ указан, то этот аргумент необязателен к указанию.

> [!TIP]
> В случае, когда аргумент не указали при вводе команды, переменная аргумента не будет существовать, и вы можете это использовать для проверки, указан ли этот аргумент.

### `equals`: **Список<Текст>**
> Проверка на полное сходство указанного аргумента с одним из этого списка.

### `in_range`: **Список<Число>**
> Проверка на то, что аргумент находится в определённом диапазоне.

### `greater`: **Число**
> Проверка на то, что аргумент больше определённого значения.

### `greater_or_equals`: **Число**
> Проверка на то, что аргумент больше или равен определённому значению.

> [!NOTE]
> Все эти аргументы необязательны к указанию, если вам не надо указывать ни один, то вы можете положить любое число вместо текста, например, 0.





# Настройки команды
Если указать `type: Option`, то это уже будет аргумент-настройка команды. Он не указывается при вводе команды.

### `exception`: **Текст**
> Сообщение при исключении, связанное с неправильностью указания аргументов. Обычно, здесь вводят информацию об использовании команды, например: "Использование: &7$scmd &b<аргумент>".

> [!WARNING]
> Здесь можно применять только цветной тип преобразования текста.

> [!NOTE]
> `$scmd` - специальный плейсхолдер, который заменяется на введённую команду.

### `sound`: **Текст**
> Звук при исключении. Принимает звук в виде текста, то есть, звук в виде JSON.

### `permission`: **Текст**
> Право, необходимое для исполнения команды.

> [!TIP]
> Есть обычные права: `dev`, (`developer`), `build`, (`builder`), `build_or_dev`, `build_and_dev`, (`builder_and_developer`), `whitelist`, (`whitelisted`), `owner`.

> [!NOTE]
> Если указано ни одно из выше перечисленного, то это будет считаться как кастомное право. Кастомные права хранятся в сохранённой переменной у каждого игрока: `%player%.permissions`, это **Список<Текст>**.

### `maxArguments`: **Число**
> При необходимости можно указать максимальное количество аргументов.

### `minArguments`: **Число**
> При необходимости можно указать минимальное количество аргументов.





# Кастомные типы аргументов
MAPI предоставляет базовые типы аргументов: `String` - текст (без границ), `Int` - целое число, `Number` - число, `Player` - имя игрока онлайн. Но вы можете создать свои типы аргументов.

Создайте функцию аргумента и укажите в основную переменную модуля под ключ `argumentsTypes` имя аргумента (принято его называть с заглавной буквы) и название функции.

Если в вашем типе аргумента могут быть пробелы, также добавьте его под `stringArgumentsTypes` 

Перейдём к функции. Её строят так:
```kt
Если переменная::Существует(#defineBorder) {
    // Обозначение границ аргумента.
} Иначе {
    // Обработка итогового аргумента из текста.
}
```
## Локальные переменные при обозначении границ 
### `#defineBorder`: **Список<Текст>**
> Оставшиеся указанные аргументы (разделены по пробелу).

### `#border`: **Список<Текст>**
> Вы должны присвоить к этой переменной выделенный аргумент.

## Локальные переменные при обработке итогового аргумента
### `#arg`: **Текст**
> Аргумент, границы которого вы обозначили в предыдущем условии.

> [!NOTE]
> В эту же переменную вы должны присвоить обработанный аргумент. Вы можете изменить тип значения, необязательно, чтобы это был текст.

## Общее

### `#vArg`: **Текст**
> Стилизует аругмент для вывода ошибки: `#ABC4D6` + аргумент + `#FF6E6E`

> [!NOTE]
> Экранирует `&` и `\n`

> [!TIP]
> Удобно использовать в сообщении об исключении `%var_local(#vArg)`, например, `&#FF6E6EИгрок %var_local(#vArg) не найден`

### `#exceptionArgument`: **Текст**
> Если аргумент не удалось обработать, присвойте к этой переменной текст исключения (ошибки), который будет выведен игроку.
