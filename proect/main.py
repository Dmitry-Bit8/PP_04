import asyncio
import random
import time
from buffer_store import BufferStore
from mongo_archiver import MongoArchiver

async def generate_test_data(buffer, interval: float = 1.0):
    """
    Генерирует тестовые данные и записывает их в буфер.

    Args:
        buffer: Экземпляр BufferStore
        interval: Интервал между записями в секундах
    """
    counter = 0
    while True:
        # Генерируем случайное тестовое сообщение
        test_data = {
            "timestamp": time.time(),
            "counter": counter,
            "value": random.randint(1, 100),
            "message": f"Тестовое сообщение #{counter}"
        }

        # Записываем в буфер
        buffer.write(test_data)
        print(f"📝 Записано: {test_data['counter']} | Буфер: {len(buffer)}/{buffer.size}")

        counter += 1
        await asyncio.sleep(interval)

async def main():
    """
    Главная функция приложения.
    Запускает генератор тестовых данных и архиватор.
    """
    print("="*50)
    print("🚀 Запуск системы архивации данных")
    print("="*50)

    # Создаем буфер на 100 элементов
    buffer = BufferStore(size=100)

    # Создаем архиватор с интервалом сброса 5 секунд
    archiver = MongoArchiver(
        buffer=buffer,
        mongo_uri="mongodb://localhost:27017",  # Измените на ваш URI
        db_name="test_archive",
        collection_name="buffered_data",
        flush_interval=5
    )

    # Запускаем обе задачи параллельно
    print("📊 Запуск генерации тестовых данных...")
    print("💾 Запуск архиватора...")

    # Создаем задачи
    tasks = [
        asyncio.create_task(generate_test_data(buffer, interval=0.5)),
        asyncio.create_task(archiver.run())
    ]

    # Ожидаем завершения (по Ctrl+C)
    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        print("⏹ Приложение остановлено")
    except KeyboardInterrupt:
        print("⏹ Получен сигнал остановки")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 До свидания!")
