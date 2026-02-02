# Migración SQL (MariaDB) a NoSQL (MongoDB y Neo4j)
## 1) Introducción
Este proyecto contiene un flujo completo de migración de datos desde una base de datos SQL (MariaDB) hacia MongoDB y Neo4j, incluyendo generación de CSVs y carga en Neo4j, todo usando contenedores Docker.

---

## 2) Integrantes
- Alberto Martínez Medina
- Joan Gelabert Colomar
- Alejandro Dehesa Delgado

---

## 3) Requisitos
- Docker y Docker Compose instalados
- Python 3.11+ con virtualenv (opcional, recomendado)
- Neo4j Browser (opcional, para consultas interactivas)
- Archivos CSV y .cypher preparados en neo4j_bonus/import/

---

## 4) Estructura del proyecto
```
airnostrum_migracion_practica2/
├─ GenerarBDD.py          # Script Python para exportar CSV desde MariaDB
├─ mongo_migration.py     # Script Python para migrar MariaDB → MongoDB
├─ docker-compose.yml     # Definición de contenedores (MariaDB, MongoDB, Neo4j)
├─ neo4j_bonus/
│  └─ import/
│     ├─ import.cypher    # Script Cypher para cargar datos en Neo4j
│     └─ *.csv            # CSVs generados desde MariaDB
└─ mariadb/
   └─ init/
       └─ *.sql
```

---

## 5) Proceso de ejecución
1. Activar entorno virtual
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

2. Crear contenedores
```bash
docker compose up -d
docker compose -f neo4j_bonus/docker-compose.neo4j.yml up -d
```

3. Comprobar BDD MariaDB
```bash
# Entrar al contenedor MariaDB
docker exec -it air_mariadb mariadb -u air -pair -D airnostrum_sql

# Dentro de MariaDB, listar bases de datos
SHOW DATABASES;

# Listar tablas de airnostrum_sql
USE airnostrum_sql;
SHOW TABLES;
```

4. Migrar a MongoDB
```bash
docker run --rm migrator
```
- Lee datos desde MariaDB
- Construye el modelo NoSQL (denormalizado) en MongoDB
- Borra colecciones destino y vuelve a cargar (idempotente para demo)

5. Migrar a Neo4J
```bash
docker exec -it air_neo4j bash
cypher-shell -u neo4j -p neo4jpass -f /var/lib/neo4j/import/import.cypher
```
- Lee datos desde CSV's
- Construye el modelo NoSQL (nodos) en Neo4J

---

## 6) Servicios
- MariaDB: localhost:3307 (usuario: air / pass: air, db: airnostrum_sql; root: root)
- MongoDB: localhost:27018
- Mongo Express (UI): http://localhost:8082
- Neo4J (UI): http://localhost:7475 (usuario: neo4j / pass: neo4jpass)

---

## 7) Fuentes
Chatgpt: https://chatgpt.com/ Classroom: https://classroom.google.com/

---

## 8) Conclusión
Este proyecto demuestra un flujo completo de migración de datos entre diferentes sistemas de bases de datos usando contenedores Docker, mostrando cómo combinar bases de datos relacionales (MariaDB), NoSQL orientadas a documentos (MongoDB) y grafos (Neo4j) de manera práctica y reproducible.