# Бот-администратор в салон
Данный бот разработан на языке Python при помощи библиотеки aiogram.
Бот был создан под определенное ТЗ, поэтому в нем есть определенные не универсальные решения.
В целом, бот имеет все функции, необходимые для организации записей и работы мастеров.

Воспользоваться образцом можно по ссылке: https://t.me/maddyrucos_tattoes_bot

# Установка
<ol>
    <li>Склонируйте репозиторий с помощью команды:<br>
      <code>git clone https://github.com/maddyrucos/tattoes_manager_bot_telegram.git</code></li><br>
    <li>Перейдите в каталог проекта:<br><code>cd tattoes_manager_bot_telegram</code></li> <br>
    <li>Создайте виртуальное окружение:<br><code>python3 -m venv venv</code></li> <br>
    <li>Активируйте виртуальное окружение:</li>
    <ul>
      <li>Для Linux/Mac:<br>
        <code>source venv/bin/activate</code></li>
      <li>Для Windows:<br>
        <code>venv\Scripts\activate</code></li>
    </ul> <br>
    <li>Установите зависимости, указанные в файле <code>requirements.txt</code>:<br><code>pip install -r requirements.txt</code></li> <br>
    <li>Создайте файл <code>.env</code> в корневом каталоге проекта и добавьте следующие переменные среды:
      <ul> 
        <li><code>BOT_TOKEN</code> - токен вашего телеграм-бота. Для получения токена создайте нового бота с помощью <a href="https://core.telegram.org/bots#botfather">BotFather</a>.</li><br>
      </ul>
    <li>Запустите бота:<br><code>python3 main.py</code></li> 
  </ol>
