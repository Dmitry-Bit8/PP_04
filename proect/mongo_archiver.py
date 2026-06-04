import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

class MongoArchiver:
    """
    Асинхронный архиватор данных из буфера в MongoDB.
    """

    def __init__(self, buffer, mongo_uri: str = "mongodb://localhost:27017",
                 db_name: str = "archive_db", collection_name: str = "data",
                 flush_interval: int = 5):
        """
        Инициализация архиватора.

        Args:
            buffer: Экземпляр BufferStore для чтения данных
            mongo_uri: URI подключения к MongoDB
            db_name: Имя базы данных
            collection_name: Имя коллекции
            flush_interval: Интервал сброса данных в секундах
        """
        self.buffer = buffer
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.flush_interval = flush_interval

        # Подключаемся к MongoDB
        self.client = None
        self.db = None
        self.collection = None

    async def connect(self):
        """Устанавливает соединение с MongoDB"""
        self.client = AsyncIOMotorClient(self.mongo_uri)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]
        print(f"✅ Подключено к MongoDB: {self.mongo_uri}/{self.db_name}")

    async def disconnect(self):
        """Закрывает соединение с MongoDB"""
        if self.client:
            self.client.close()
            print("🔌 Соединение с MongoDB закрыто")

    async def save_to_db(self, data):
        """
        Сохраняет данные в MongoDB.

        Args:
            data: Список данных для сохранения
        """
        if not data:
            return

        try:
            result = await self.collection.insert_many(data)
            print(f"✅ Сохранено {len(result.inserted_ids)} записей в MongoDB")
        except Exception as e:
            print(f"❌ Ошибка при сохранении в MongoDB: {e}")

    async def flush(self):
        """Сбрасывает данные из буфера в MongoDB"""
        # Используем read_and_process с функцией сохранения
        await self.buffer.read_and_process(self.save_to_db)

    async def periodic_flush(self):
        """Периодически сбрасывает данные из буфера в MongoDB"""
        while True:
            await asyncio.sleep(self.flush_interval)
            await self.flush()

    async def run(self):
        """Запускает архиватор с периодической отправкой данных"""
        await self.connect()
        try:
            print(f"🚀 Архиватор запущен, интервал сброса: {self.flush_interval} сек")
            # Запускаем периодический сброс данных
            await self.periodic_flush()
        except asyncio.CancelledError:
            print("⏹ Архиватор остановлен")
        except Exception as e:
            print(f"❌ Критическая ошибка: {e}")
        finally:
            await self.disconnect()
