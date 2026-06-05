import asyncio
import random
import time
from buffer_store import BufferStore
from mongo_archiver import MongoArchiver

async def generate_test_data(buffer, interval: float = 1.0):
   
    counter = 0
    while True:
     
        test_data = {
            "timestamp": time.time(),
            "counter": counter,
            "value": random.randint(1, 100),
            "message": f"Тестовое сообщение #{counter}"
        }

      
        buffer.write(test_data)
        print(f"📝 Записано: {test_data['counter']} | Буфер: {len(buffer)}/{buffer.size}")

        counter += 1
        await asyncio.sleep(interval)

async def main():
    
    print("="*50)
    print("🚀 Запуск системы архивации данных")
    print("="*50)

  
    buffer = BufferStore(size=100)

    archiver = MongoArchiver(
        buffer=buffer,
        mongo_uri="mongodb://localhost:27017",  
        db_name="test_archive",
        collection_name="buffered_data",
        flush_interval=5
    )

    print("📊 Запуск генерации тестовых данных...")
    print("💾 Запуск архиватора...")

    tasks = [
        asyncio.create_task(generate_test_data(buffer, interval=0.5)),
        asyncio.create_task(archiver.run())
    ]

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
