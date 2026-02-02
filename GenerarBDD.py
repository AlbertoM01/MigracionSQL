# import mysql.connector
# import csv
# from datetime import datetime

# # Conexión a MariaDB
# conn = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="1234",
#     database="airnostrum_sql"
# )

# cursor = conn.cursor(dictionary=True)

# # Tablas a exportar
# tables = ["airports", "aircraft", "flights", "passengers", "bookings", "tickets"]

# for table in tables:
#     cursor.execute(f"SELECT * FROM {table}")
#     rows = cursor.fetchall()
#     if rows:
#         with open(f"neo4j_bonus/import/{table}.csv", "w", newline="", encoding="utf-8") as f:
#             writer = csv.DictWriter(f, fieldnames=rows[0].keys())
#             writer.writeheader()
#             for row in rows:
#                 # Convertir datetimes a string ISO para Neo4j
#                 for k, v in row.items():
#                     if isinstance(v, datetime):
#                         row[k] = v.isoformat()
#                 writer.writerow(row)

# print("CSV generados correctamente")
# cursor.close()
# conn.close()




import mysql.connector
import csv
from datetime import datetime
import os

# Conexión a MariaDB
DB_NAME = "airnostrum_sql"

conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3307,
    user="air",
    password="air",
    database=DB_NAME,
    use_pure=True,
    auth_plugin="mysql_native_password"
)

print("✅ Conectado")

cursor = conn.cursor(dictionary=True)

# Obtener todas las tablas de la base de datos
cursor.execute("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = %s
      AND table_type = 'BASE TABLE'
""", (DB_NAME,))

tables = [row["table_name"] for row in cursor.fetchall()]

print(f"Tablas detectadas: {tables}")

# Asegurar carpeta destino
output_dir = "neo4j_bonus/import"
os.makedirs(output_dir, exist_ok=True)

# Exportar cada tabla a CSV
for table in tables:
    cursor.execute(f"SELECT * FROM `{table}`")
    rows = cursor.fetchall()

    if not rows:
        print(f"Tabla vacía: {table}")
        continue

    output_file = f"{output_dir}/{table}.csv"

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()

        for row in rows:
            # Convertir datetimes a ISO 8601 (compatible con Neo4j)
            for k, v in row.items():
                if isinstance(v, datetime):
                    row[k] = v.isoformat()
            writer.writerow(row)

    print(f"CSV generado: {output_file}")

print("✅ CSV generados correctamente")

cursor.close()
conn.close()