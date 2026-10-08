from config import POSTGRES_CONFIG

print("CONFIGURAÇÃO CARREGADA:")
print("host:", repr(POSTGRES_CONFIG.get("host")))
print("port:", repr(POSTGRES_CONFIG.get("port")))
print("user:", repr(POSTGRES_CONFIG.get("user")))
print("dbname:", repr(POSTGRES_CONFIG.get("dbname")))
print("password configurada:", bool(POSTGRES_CONFIG.get("password")))
