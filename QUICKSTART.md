# ⚡ Быстрый старт за 5 минут

## 🎯 Минимальная настройка

### 1. Установите Python 3.8+ 

```bash
python3 --version  # Проверьте версию
```

### 2. Клонируйте/скачайте проект

```bash
cd /Users/vishnyakovaleksandr/Work/twitch_girl
```

### 3. Установите зависимости

```bash
# Создайте виртуальное окружение
python3 -m venv venv

# Активируйте (macOS/Linux)
source venv/bin/activate

# Или на Windows:
# venv\Scripts\activate

# Установите пакеты
pip install -r requirements.txt
```

### 4. Получите токены (самое важное!)

#### Twitch токен:
1. Идите на https://twitchtokengenerator.com/
2. Нажмите **"Bot Chat Token"**
3. Авторизуйтесь
4. Скопируйте токен (начинается с `oauth:`)

#### OpenAI ключ:
1. Идите на https://platform.openai.com/api-keys
2. Создайте новый ключ
3. Скопируйте (начинается с `sk-`)
4. **Пополните баланс минимум $5**

### 5. Создайте .env файл

```bash
# Создайте из примера
cat > .env << 'EOF'
# Twitch Configuration
TWITCH_TOKEN=oauth:YOUR_TOKEN_HERE
TWITCH_CLIENT_ID=your_client_id_here
TWITCH_CHANNEL=your_channel_name
TWITCH_BOT_NAME=your_bot_name

# OpenAI Configuration
OPENAI_API_KEY=sk-YOUR_KEY_HERE

# Character Configuration
CHARACTER_NAME=Лиза
CHARACTER_PERSONALITY=Ты привлекательная и немного дерзкая стримерша. Отвечай кокетливо, с юмором и небольшой долей флирта. Будь дружелюбной и интересной.
EOF
```

Затем отредактируйте файл:
```bash
nano .env  # или используйте любой редактор
```

**Замените:**
- `YOUR_TOKEN_HERE` → ваш Twitch токен
- `YOUR_KEY_HERE` → ваш OpenAI ключ
- `your_channel_name` → имя вашего канала на Twitch
- `your_bot_name` → имя вашего бота

### 6. Проверьте настройку

```bash
python utils/test_setup.py
```

Должно быть **✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ!**

### 7. Запустите!

```bash
python main.py
```

Или используйте скрипт запуска:
```bash
# macOS/Linux
./start.sh

# Windows
start.bat
```

## 🎉 Готово!

Откроется окно с аватаром и бот подключится к Twitch чату.

**Напишите что-нибудь в чат** - и аватар ответит!

---

## ❓ Проблемы?

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "Invalid OAuth token"
Проверьте что токен:
- Начинается с `oauth:`
- Без пробелов
- Правильно скопирован

### "OpenAI API error"
- Проверьте что ключ правильный
- Убедитесь что есть баланс на аккаунте
- Проверьте на https://platform.openai.com/account/billing

### "Cannot connect to Twitch"
- Проверьте имя канала (без @)
- Убедитесь что канал существует
- Проверьте интернет соединение

### Окно не открывается
На Linux установите:
```bash
sudo apt-get install python3-opencv
```

---

## 📚 Дальше

- 📖 [Полная документация](README.md)
- 🛠️ [Подробная настройка](setup_guide.md)
- 💭 [Примеры личностей](PROMPTS.md)
- 🚀 [Деплой и монетизация](DEPLOYMENT.md)

---

## 🎨 Кастомизация

### Изменить голос

В `.env` добавьте:
```env
VOICE_MODEL=nova  # Женский, энергичный (рекомендуется)
```

Доступные: `alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`

### Изменить личность

Отредактируйте `CHARACTER_PERSONALITY` в `.env` или см. [PROMPTS.md](PROMPTS.md)

### Добавить свой аватар

Создайте два изображения 1280x720:
- `assets/avatar_idle.png` - с закрытым ртом
- `assets/avatar_talking.png` - с открытым ртом

Или используйте генератор:
```bash
python utils/create_custom_avatar.py
```

---

## 💡 Советы

1. **Начните с малого** - используйте `gpt-3.5-turbo` для экономии
2. **Установите лимиты** - в OpenAI Dashboard
3. **Тестируйте локально** - перед запуском на продакшен
4. **Собирайте фидбек** - спрашивайте зрителей
5. **Итерируйте** - улучшайте на основе отзывов

---

**Удачи! 🎀✨**

Есть вопросы? Проверьте [FAQ в README.md](README.md#-решение-проблем)

