# MAPI
Module API - ядро для модулей, использующихся на сервере JustMC. Оно похоже на ядро Bukkit для серверов в майнкрафте, только Bukkit загружает плагины, а MAPI загружает модули.

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

`description`: **Текст**
> Описание модуля.

> [!TIP]
> Здесь можно применять любой тип стилизации текста.

`authors`: **Список<Текст>**
> Авторы модуля.

> [!TIP]
> Здесь можно указывать просто текст, и он автоматически разделится по пробелу.

`commands`: **Список<Команда>**
> Команды модуля.

> [!TIP]
> Также можно сделать просто **Список<Текст>**, но тексты должны быть в виде JSON, и в нём можно не указывать `{` в начале и `}` в конце.

`dependencies`: **Словарь<Текст, Текст>**
> Необходимые зависимости модуля. Без них модуль будет отключён: его команды не будут работать, и он будет подсвечен красным в команде `about`, и в его "проблемы" будет добавлена ошибка. В ключ указывается имя необходимого модуля, а в значение - его версию.
 
> [!TIP]
> Если указать `>=` перед версией, например, `>=1.0.2`, то будет требовать с протоколом версии `1.0.2` и выше.\
> Если указать `~`, например, `~1.0`, то будет требовать все версии с таким протоколом, как у `1.0`.

`argumentsTypes`: **Словарь<Текст, Текст>**
> Добавляемые типы аргументов для команд. В ключ указывается имя типа, а в значение - функцию, которая обрабатывает этот тип аргумента.

`stringArgumentsTypes`: **Список<Текст>**
> Добавляемые сложные типы аргументов для команд. То есть, в них используются пробелы. Для таких типов нужно ещё и определять границу.
