from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста
PROVIDER_TOKEN = env.str("PROVIDER_TOKEN")

channels = [-1001436025947]

DB_NAME = env.str("DB_NAME")
DB_PASS = env.str('DB_PASS')
DB_USER = env.str('DB_USER')
DB_HOST = env.str('DB_HOST')