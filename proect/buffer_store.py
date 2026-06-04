class BufferStore:
    """
    Класс для хранения данных в буфере фиксированного размера.
    При переполнении удаляются самые старые записи.
    """

    def __init__(self, size: int):
        """
        Инициализация буфера.

        Args:
            size: Максимальное количество элементов в буфере
        """
        self.size = size
        self.buffer = []

    def write(self, data):
        """
        Записывает данные в буфер.
        Если буфер переполнен, удаляет самый старый элемент.

        Args:
            data: Данные для записи
        """
        if len(self.buffer) >= self.size:
            self.buffer.pop(0)  # Удаляем самый старый элемент
        self.buffer.append(data)

    def read_all(self):
        """
        Возвращает все данные из буфера и очищает его.

        Returns:
            list: Копия данных буфера
        """
        data = self.buffer.copy()
        self.buffer.clear()
        return data

    def read_and_process(self, processor_func):
        """
        Читает данные и передает их в функцию-обработчик.

        Args:
            processor_func: Функция для обработки данных

        Returns:
            Результат выполнения функции-обработчика
        """
        if not self.buffer:
            return None

        # Копируем данные и очищаем буфер
        data = self.buffer.copy()
        self.buffer.clear()

        # Передаем данные в функцию обработки
        return processor_func(data)

    def __len__(self):
        """Возвращает текущее количество элементов в буфере"""
        return len(self.buffer)

    def __str__(self):
        """Строковое представление буфера"""
        return f"BufferStore(size={self.size}, items={len(self.buffer)})"
