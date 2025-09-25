import os
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
TOKEN = ("7993810257:AAEEU1jmQWLaICjS1rrgHYCwyODAMfNmJx0") # Получаем токен из переменной окружения
def get_recipe(ingredients):
    """Ищет рецепт в интернете. Возвращает текст или сообщение об ошибке."""
    query = f"{ingredients} рецепт"  # Формируем поисковый запрос
    url = f"https://www.google.com/search?q={query}"  # URL для поиска

    try:  # Обработка возможных ошибок при запросе
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        response.raise_for_status()  # Проверяем статус код ответа

        soup = BeautifulSoup(response.text, 'html.parser') # Разбираем HTML

        for link in soup.find_all('a'): #Сбор ссылок
          href = link.get('href')
          if href and "povarenok.ru" in href: #Если ссылка ведет на сайт с рецептами
            return "Рецепт тут:" + href.replace('/url?q=', '') #Возвращаем ссылку, очищенную от мусора
        return f"Не удалось найти прямой рецепт. Попробуйте другие ингредиенты."

    except requests.exceptions.RequestException as e:
        return f"Произошла ошибка при поиске: {e}"

def recipe_handler(update: Update, context: CallbackContext):
    """Обработчик сообщений от пользователя."""
    ingredients = update.message.text  # Получаем текст сообщения
    recipe_text = get_recipe(ingredients)  # Ищем рецепт
    update.message.reply_text(recipe_text)  # Отправляем результат пользователю

def start(update: Update, context: CallbackContext):
    """Обработчик команды /start."""
    update.message.reply_text("Привет! Введите игредиенты.")

def main():
    """Функция запуска бота."""
    application = ApplicationBuilder().token(TOKEN).build() # ну наконец то 

    application.add_handler(CommandHandler("start", start)) # Обработчик команды /start
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, recipe_handler)) # Обработчик текстовых сообщений

    application.run_polling() # Запуск пж

if __name__ == '__main__':
    main()
