from typing import Union

import asyncpg
from asyncpg import Pool, Connection

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            database=config.DB_NAME,
            host=config.DB_HOST
        )

    async def execute(self, command, *args,
                      fetch: bool = False, fetchval: bool = False,
                      fetchrow: bool = False, execute: bool = False):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def add_user(self, user_id, full_name, username, refferal=None, money=0):
        sql = """INSERT INTO users values ($1, $2, $3, $4, $5)"""
        return await self.execute(sql, user_id, full_name, username, refferal, money, execute=True)

    async def get_user_by_user_id(self, user_id):
        sql = """select * from users where user_id=$1"""
        return await self.execute(sql, user_id, fetchrow=True)

    async def check_money_by_user_id(self, user_id):
        sql = """select money from users where user_id=$1"""
        return await self.execute(sql, user_id, fetchval=True)

    async def add_money_by_user_id(self, user_id):
        sql = """update users set money=money+10 where user_id=$1"""
        return await self.execute(sql, user_id, execute=True)



