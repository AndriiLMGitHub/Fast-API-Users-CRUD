import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import uvicorn

from src.users.routes import router
from src.db.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Керує життєвим циклом додатку"""
    # Startup
    await init_db()
    yield
    # Shutdown - додайте тут логіку закриття з'єднань з БД якщо потрібно
    pass


def create_app() -> FastAPI:
    """Фабрика для створення FastAPI додатку"""
    app = FastAPI(
        title="Fast API Example",
        description="API для роботи з користувачами",
        version="1.0.0",
        lifespan=lifespan,
        # Оптимізації для продуктивності
        docs_url="/docs" if __debug__ else None,  # Відключити docs в продакшн
        redoc_url="/redoc" if __debug__ else None,
    )

    # Middleware для стиснення відповідей
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    # CORS middleware (налаштуйте під ваші потреби)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],  # Замініть на ваші домени
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )

    # Підключення роутерів
    app.include_router(router, prefix="/api/v1/users", tags=["Users"])

    return app


# Створення екземпляру додатку
app = create_app()


# Health check endpoint
@app.get("/health", tags=["System"])
async def health_check():
    """Перевірка стану додатку"""
    return {"status": "healthy"}


def main():
    """Точка входу для запуску сервера"""
    config = uvicorn.Config(
        "main:app",
        host="0.0.0.0",  # Дозволяє підключення ззовні
        port=8000,
        reload=__debug__,  # Reload тільки в debug режимі
        log_level="info",
        access_log=True,
        # Оптимізації для продуктивності
        loop="uvloop" if not __debug__ else "asyncio",  # uvloop швидший в продакшн
        http="httptools",  # Швидший HTTP парсер
        # Налаштування для продуктивності
        backlog=2048,
        limit_concurrency=1000,
        limit_max_requests=10000,
    )

    server = uvicorn.Server(config)

    try:
        asyncio.run(server.serve())
    except KeyboardInterrupt:
        print("\nСервер зупинено користувачем")


if __name__ == '__main__':
    main()
