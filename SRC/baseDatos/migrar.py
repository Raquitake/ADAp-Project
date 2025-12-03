import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Añadir la columna foto_perfil si no existe
try:
    cursor.execute("ALTER TABLE usuario ADD COLUMN foto_perfil TEXT;")
    print("Columna foto_perfil añadida correctamente")
except sqlite3.OperationalError:
    print("La columna foto_perfil ya existe o hay otro problema")

conn.commit()
conn.close()
