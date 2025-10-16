# 🤝 Contributing to Twitch AI Girl

Спасибо за интерес к проекту! Мы приветствуем любой вклад.

## 📋 Как внести вклад

### 🐛 Сообщить о баге

1. Проверьте что баг еще не был сообщен в [Issues](https://github.com/yourname/twitch_girl/issues)
2. Создайте новый Issue с тегом `bug`
3. Опишите:
   - Что вы делали
   - Что ожидали
   - Что произошло на самом деле
   - Версия Python, ОС
   - Логи ошибок

**Шаблон:**
```markdown
**Описание бага:**
Краткое описание проблемы

**Шаги для воспроизведения:**
1. Запустить...
2. Отправить сообщение...
3. Увидеть ошибку...

**Ожидаемое поведение:**
Что должно было произойти

**Скриншоты:**
Если применимо

**Окружение:**
- OS: [macOS 14.0]
- Python: [3.11.5]
- Version: [1.0.0]

**Логи:**
```
Вставьте логи ошибок здесь
```
```

### 💡 Предложить функцию

1. Проверьте что функция еще не предложена в [Issues](https://github.com/yourname/twitch_girl/issues)
2. Создайте новый Issue с тегом `enhancement`
3. Опишите:
   - Зачем нужна эта функция
   - Как она должна работать
   - Примеры использования

### 🔧 Pull Request Process

1. **Fork** репозиторий
2. **Создайте ветку** для вашей функции (`git checkout -b feature/AmazingFeature`)
3. **Внесите изменения** следуя стайл-гайду
4. **Добавьте тесты** если применимо
5. **Commit** изменения (`git commit -m 'Add some AmazingFeature'`)
6. **Push** в ветку (`git push origin feature/AmazingFeature`)
7. **Откройте Pull Request**

### ✅ Checklist для PR

- [ ] Код следует стайл-гайду проекта
- [ ] Добавлены комментарии в сложных местах
- [ ] Обновлена документация (если нужно)
- [ ] Добавлены тесты
- [ ] Все тесты проходят
- [ ] Обновлен CHANGELOG.md

## 📐 Стайл-гайд

### Python Code Style

Мы следуем [PEP 8](https://peps.python.org/pep-0008/) с небольшими дополнениями:

#### Импорты
```python
# Стандартная библиотека
import os
import sys
from pathlib import Path

# Сторонние библиотеки
import numpy as np
from openai import AsyncOpenAI

# Локальные импорты
import config
from ai_brain import AIBrain
```

#### Именование
```python
# Классы: PascalCase
class TwitchChatBot:
    pass

# Функции и переменные: snake_case
def process_message(user_name, message):
    response_time = 0.5
    
# Константы: UPPER_SNAKE_CASE
MAX_RESPONSE_LENGTH = 200
API_TIMEOUT = 30

# Приватные: _leading_underscore
def _internal_helper():
    pass
```

#### Docstrings
```python
def function_name(param1: str, param2: int) -> bool:
    """
    Short description of function
    
    Longer description if needed with more details about
    what the function does and how it works.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When something goes wrong
    """
    pass
```

#### Type Hints
```python
from typing import List, Dict, Optional

def get_response(message: str, history: List[Dict[str, str]]) -> Optional[str]:
    """Always use type hints for better code clarity"""
    pass
```

### Комментарии

```python
# Хорошие комментарии объясняют "почему", а не "что"

# ❌ Плохо
x = x + 1  # Increment x

# ✅ Хорошо
x = x + 1  # Компенсация нулевого индекса массива

# ✅ Отлично
# Обрабатываем сообщения с задержкой чтобы избежать rate limiting от Twitch API
await asyncio.sleep(MESSAGE_COOLDOWN)
```

### Структура файлов

```python
"""
Module docstring describing the file
"""

# Imports
import os
from typing import Optional

# Constants
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# Classes
class MyClass:
    """Class docstring"""
    
    def __init__(self):
        """Initialize"""
        pass
        
    def public_method(self):
        """Public method"""
        pass
        
    def _private_method(self):
        """Private method"""
        pass

# Functions
def main():
    """Main function"""
    pass

# Main execution
if __name__ == "__main__":
    main()
```

## 🧪 Тестирование

### Запуск тестов

```bash
# Все тесты
pytest

# Конкретный файл
pytest tests/test_ai_brain.py

# С покрытием
pytest --cov=.
```

### Написание тестов

```python
import pytest
from ai_brain import AIBrain

class TestAIBrain:
    """Test AIBrain functionality"""
    
    def test_initialization(self):
        """Test that AIBrain initializes correctly"""
        brain = AIBrain()
        assert brain is not None
        assert len(brain.conversation_history) > 0
        
    def test_response_generation(self):
        """Test response generation"""
        brain = AIBrain()
        response = await brain.get_response("test_user", "Hello")
        assert isinstance(response, str)
        assert len(response) > 0
```

## 📝 Документация

### Обновление документации

При добавлении новых функций, обновите:

1. **README.md** - если изменяется основная функциональность
2. **CHANGELOG.md** - всегда добавляйте изменения
3. **Docstrings** - в коде
4. **setup_guide.md** - если меняется процесс установки
5. **DEPLOYMENT.md** - если меняется деплой

### Стиль документации

- Используйте Markdown
- Добавляйте примеры кода
- Скриншоты для UI изменений
- Эмодзи для наглядности (но умеренно)

## 🏗️ Архитектурные решения

### Принципы проекта

1. **Простота** - код должен быть понятным
2. **Модульность** - каждый модуль делает одно дело
3. **Расширяемость** - легко добавлять новые функции
4. **Производительность** - оптимизация где важно
5. **Безопасность** - защита данных пользователей

### Структура модулей

```
twitch_girl/
├── core/                   # Основная логика
│   ├── ai_brain.py        # AI обработка
│   ├── voice_engine.py    # TTS
│   └── avatar.py          # Анимация
├── integrations/          # Интеграции
│   ├── twitch/           # Twitch API
│   └── openai/           # OpenAI API
├── utils/                 # Утилиты
└── config/                # Конфигурация
```

## 🎯 Приоритеты разработки

### High Priority
- Исправление критических багов
- Улучшения безопасности
- Оптимизация производительности

### Medium Priority
- Новые функции
- Улучшения UX
- Документация

### Low Priority
- Рефакторинг
- Косметические изменения
- Экспериментальные функции

## 💬 Коммуникация

### Стиль коммуникации

- Будьте вежливыми и конструктивными
- Объясняйте свои решения
- Принимайте фидбек позитивно
- Помогайте новичкам

### Где общаться

- **GitHub Issues** - баги и предложения
- **Pull Requests** - обсуждение кода
- **Discord** - общие вопросы (если есть)

## 📜 Code of Conduct

### Наши стандарты

- ✅ Уважительное общение
- ✅ Конструктивная критика
- ✅ Фокус на улучшении проекта
- ✅ Помощь другим участникам

- ❌ Оскорбления и агрессия
- ❌ Троллинг и spam
- ❌ Дискриминация любого вида
- ❌ Harassment

## 🎓 Для новичков

### Хорошие первые задачи

Ищите Issues с тегом `good first issue`:
- Исправление опечаток в документации
- Добавление примеров
- Улучшение сообщений об ошибках
- Добавление тестов

### Нужна помощь?

- Прочитайте документацию
- Посмотрите существующий код
- Задайте вопрос в Issue
- Не бойтесь ошибиться!

## 🙏 Благодарности

Каждый вклад ценен:
- 🐛 Сообщения о багах
- 💡 Предложения функций
- 📝 Улучшения документации
- 🔧 Pull requests
- ⭐ Stars на GitHub
- 📢 Распространение информации

---

**Спасибо что делаете проект лучше!** 🎀✨

