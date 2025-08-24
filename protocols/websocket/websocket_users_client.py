import asyncio
import websockets


async def client():
    uri = "ws://localhost:8765"  # Адрес сервера
    async with websockets.connect(uri) as websocket:
        message = "Привет, сервер!"  # Сообщение, которое отправит клиент
        print(f"Отправка: {message}")
        await websocket.send(message)  # Отправляем сообщение

        # Получаем пять ответных сообщений
        for _ in range(5):
            response = await websocket.recv()
            print(f"Ответ от сервера: {response}")


if __name__ == "__main__":
    asyncio.run(client())
