class BufferStore:


    def __init__(self, size: int):
        
        self.size = size
        self.buffer = []

    def write(self, data):
        
        if len(self.buffer) >= self.size:
            self.buffer.pop(0)  # Удаляем самый старый элемент
        self.buffer.append(data)

    def read_all(self):
      
        data = self.buffer.copy()
        self.buffer.clear()
        return data

    def read_and_process(self, processor_func):
        
        if not self.buffer:
            return None
        
        data = self.buffer.copy()
        self.buffer.clear()

        return processor_func(data)

    def __len__(self):
       
        return len(self.buffer)

    def __str__(self):
       
        return f"BufferStore(size={self.size}, items={len(self.buffer)})"
