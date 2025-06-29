import logging
import asyncpg
from typing import Optional

from classes import Service, Task, User


class pgManager:
    """Класс с методами для работы с таблицами БД"""
    def __init__(
        self, 
        dbname: str, 
        user: str, 
        password: str, 
        host: Optional[str] = 'localhost', 
        port: Optional[str] = '5432'
    ):  
        self.host=host
        self.port=port
        self.user=user
        self.password=password
        self.dbname=dbname
        self.__connection = None

    async def connect(self):
        if self.__connection is None or self.__connection.is_closed():
            self.__connection = await asyncpg.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.dbname
            )

    async def close(self):
        if self.__connection or not self.__connection.is_closed():
            await self.__connection.close()

    async def get_services(self, category: str = None) -> list[Service]:
        """Получение всех услуг в виде списка объектов класса Service

        Returns:
            list[Service]: список услуг
        """
        services = []

        if category is None:
            rows = await self.__connection.fetch(
                "SELECT * FROM services"
            )
        else:
            rows = await self.__connection.fetch(
                "SELECT * FROM services WHERE age = $1", category
            )

        for row in rows:
            drow = dict(row)
            services.append(Service(
                drow['id'],
                drow['name'],
                drow['description'],
                drow['price'],
                drow['age'],
                drow['imgpath']
            ))
            
        return services

    async def create_task(
        self,
        cliend_id: str,
        number: str,
        name: str,
        services: str,
        guests: str,
        datetime: str
    ) -> str:
        query = """
            INSERT INTO tasks (client_id, number, name, services, guests, datetime)
            SELECT $1, $2, $3, $4, $5, $6
            WHERE NOT EXISTS (
                SELECT 1 FROM tasks
                WHERE client_id = $1
                AND number = $2
                AND name = $3
                AND services = $4
                AND guests = $5
                AND datetime = $6
            )
            RETURNING id
        """

        task_id = await self.__connection.fetchval(
            query, cliend_id, number, name, services, guests, datetime
        )
        return task_id
        
    async def delete_task(self, id: int) -> None:
        await self.__connection.execute(
            "DELETE FROM tasks WHERE id = $1", id
        )

    async def get_all_tasks(self) -> list[Task]:
        rows = await self.__connection.fetch(
            "SELECT * FROM tasks"
        )
        tasks = []
        for row in rows:
            drow = dict(row)
            tasks.append(Task(
                drow['id'],
                drow['client_id'],
                drow['number'],
                drow['name'],
                drow['services'],
                drow['guests'],
                drow['datetime']
            ))
        return tasks

    async def get_task(self, id: int) -> Task:
        task = await self.__connection.fetchrow(
            "SELECT * FROM tasks WHERE id = $1", id
        )
        dtask = dict(task)
        return Task(
            dtask['id'],
            dtask['client_id'],
            dtask['number'],
            dtask['name'],
            dtask['services'],
            dtask['guests'],
            dtask['datetime']
        )

    async def is_user_exist(self, id: int) -> bool:
        user = await self.__connection.fetchrow(
            "SELECT * FROM users WHERE id = $1", id
        )
        if user:
            return True
        return False

    async def add_user(self, id: int, phone: str, name: str) -> None:
        await self.__connection.execute(
            "INSERT INTO users (id, phone, name) VALUES ($1, $2, $3)", id, phone, name
        )

    async def get_user(self, id: int) -> User:
        user = await self.__connection.fetchrow(
            "SELECT * FROM users WHERE id = $1", id
        )
        if user:
            duser = dict(user)
            return User(
                duser['id'],
                duser['phone'],
                duser['name']
            )
        return None

    async def add_chat(self, adresant: str, adresat: str) -> None:
        await self.__connection.execute(
            "INSERT INTO chats (adresant, adresat) VALUES ($1, $2), ($2, $1)",
            adresant, adresat
        )

    async def get_chat(self, user_id: int) -> dict:
        chat = await self.__connection.fetchrow(
            "SELECT * FROM chats WHERE adresant = $1", user_id
        )
        return dict(chat)

    async def delete_chat(self, user_id: int) -> None:
        await self.__connection.execute(
            "DELETE FROM chats WHERE adresant = $1", user_id
        )
        await self.__connection.execute(
            "DELETE FROM chats WHERE adresat = $1", user_id
        )
