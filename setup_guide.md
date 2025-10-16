# 📖 Подробная инструкция по настройке

## Шаг 1: Получение Twitch токенов

### 1.1 Создание Twitch приложения

1. Перейдите на https://dev.twitch.tv/console/apps
2. Нажмите "Register Your Application"
3. Заполните форму:
   - **Name**: Ваше название (например, "AI Girl Bot")
   - **OAuth Redirect URLs**: `http://localhost`
   - **Category**: Chat Bot
4. Нажмите "Create"
5. Скопируйте **Client ID**

### 1.2 Получение OAuth токена

1. Перейдите на https://twitchtokengenerator.com/
2. Выберите **"Bot Chat Token"**
3. Авторизуйтесь через Twitch
4. Скопируйте токен (начинается с `oauth:`)

**Важно**: Храните токен в секрете!

### 1.3 Настройка .env

```env
TWITCH_TOKEN=oauth:ваш_токен_здесь
TWITCH_CLIENT_ID=ваш_client_id_здесь
TWITCH_CHANNEL=имя_вашего_канала
TWITCH_BOT_NAME=имя_вашего_бота
```

## Шаг 2: Получение OpenAI API ключа

### 2.1 Создание аккаунта OpenAI

1. Перейдите на https://platform.openai.com/
2. Зарегистрируйтесь или войдите
3. Пополните баланс (минимум $5)

### 2.2 Создание API ключа

1. Перейдите на https://platform.openai.com/api-keys
2. Нажмите "Create new secret key"
3. Дайте имя ключу (например, "Twitch Bot")
4. Скопируйте ключ (показывается только один раз!)

### 2.3 Добавление в .env

```env
OPENAI_API_KEY=sk-ваш_ключ_здесь
```

## Шаг 3: Установка Python и зависимостей

### 3.1 Установка Python (если не установлен)

**macOS:**
```bash
brew install python3
```

**Windows:**
- Скачайте с https://www.python.org/downloads/
- Установите, отметив "Add Python to PATH"

**Linux:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv
```

### 3.2 Создание виртуального окружения

```bash
cd /Users/vishnyakovaleksandr/Work/twitch_girl
python3 -m venv venv
```

### 3.3 Активация окружения

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 3.4 Установка зависимостей

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Шаг 4: Создание или установка аватара

### Вариант A: Использовать placeholder (автоматически)

Просто запустите программу - она создаст базовый аватар автоматически.

### Вариант B: Создать свой аватар с помощью AI

#### Используя Midjourney:

1. Перейдите на https://midjourney.com/
2. Введите промпт:
```
beautiful anime girl portrait, attractive, slight smile, purple hair, 
looking at camera, soft lighting, high quality, digital art --ar 16:9
```

3. Сгенерируйте две версии:
   - С закрытым ртом
   - С открытым ртом (добавьте в промпт: "mouth open, talking")

#### Используя Stable Diffusion (бесплатно):

1. Установите Stable Diffusion Web UI
2. Используйте модель для аниме (например, "Anything V5")
3. Промпт:
```
(masterpiece, best quality), 1girl, beautiful, attractive, purple hair, 
long hair, smiling, looking at viewer, upper body, soft lighting
```

4. Negative prompt:
```
lowres, bad anatomy, bad hands, text, error, missing fingers, 
extra digit, fewer digits, cropped, worst quality, low quality
```

### Вариант C: Заказать у художника

Платформы:
- Fiverr: от $20
- ArtStation: от $50
- Twitter/X: поиск по #commissionsopen

**Требования для художника:**
- Два изображения (рот закрыт / рот открыт)
- Разрешение: 1280x720 или выше
- Формат: PNG с прозрачным фоном
- Одинаковая поза и фон

## Шаг 5: Первый запуск

### 5.1 Проверка конфигурации

Создайте `.env`:
```bash
cp .env.example .env
nano .env  # или используйте любой текстовый редактор
```

Заполните все обязательные поля.

### 5.2 Тестовый запуск

```bash
python main.py
```

**Что должно произойти:**
1. ✓ Загрузка конфигурации
2. ✓ Создание/загрузка изображений аватара
3. ✓ Открытие окна с аватаром
4. ✓ Подключение к Twitch чату
5. ✓ Сообщение "ВСЕ СИСТЕМЫ ЗАПУЩЕНЫ!"

### 5.3 Тестирование

1. Откройте ваш Twitch канал в браузере
2. Напишите в чат: "Привет!"
3. Подождите 2-3 секунды
4. Бот должен ответить голосом, аватар будет двигать губами

## Шаг 6: Настройка OBS для стрима

### 6.1 Установка OBS Studio

Скачайте с https://obsproject.com/

### 6.2 Настройка сцены

1. Откройте OBS Studio
2. В разделе "Sources" нажмите "+"
3. Выберите "Window Capture"
4. Выберите окно с аватаром
5. Измените размер и позицию по желанию

### 6.3 Добавление дополнительных элементов

**Фон:**
- Source → Image
- Выберите красивый фон

**Чат:**
- Source → Browser
- URL: используйте Twitch chat overlay

**Информация:**
- Source → Text
- Добавьте название стрима, соцсети и т.д.

### 6.4 Настройка стрима

1. Settings → Stream
2. Service: Twitch
3. Получите ключ стрима: https://dashboard.twitch.tv/settings/stream
4. Вставьте ключ в OBS
5. Нажмите "Start Streaming"

## Шаг 7: Оптимизация

### 7.1 Уменьшение задержки

В `config.py`:
```python
MESSAGE_COOLDOWN = 3  # Уменьшить с 5 до 3 секунд
```

### 7.2 Настройка модели GPT

В `ai_brain.py`:
```python
model="gpt-3.5-turbo"  # Дешевле и быстрее
```

### 7.3 Изменение голоса

В `config.py`:
```python
VOICE_MODEL = 'nova'  # Женский, энергичный (рекомендуется)
```

Доступные голоса:
- `alloy` - Нейтральный
- `echo` - Мужской
- `fable` - Британский акцент
- `onyx` - Мужской, глубокий
- `nova` - Женский, энергичный ⭐
- `shimmer` - Женский, мягкий

## 🎉 Готово!

Теперь у вас полностью рабочая AI стримерша!

## Следующие шаги:

1. **Настройте личность** - отредактируйте CHARACTER_PERSONALITY
2. **Создайте расписание стримов** - регулярность привлекает зрителей
3. **Продвигайте канал** - поделитесь в соцсетях
4. **Мониторьте расходы** - проверяйте OpenAI Dashboard
5. **Собирайте фидбек** - спрашивайте зрителей что улучшить

## Советы для успешного стрима:

- 📅 Стримьте регулярно (например, каждый день в одно время)
- 🎮 Добавьте игры или активности на фоне
- 💬 Поощряйте общение в чате
- 🎁 Настройте донаты и алерты
- 📱 Продвигайтесь в соцсетях
- 🎨 Регулярно обновляйте дизайн
- ⚡ Быстро реагируйте на тренды

Удачи с вашей AI стримершей! 🎀✨

