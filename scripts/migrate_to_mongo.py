import os
from decimal import Decimal
import mysql.connector
from pymongo import MongoClient

# Configuración MariaDB
MARIADB_HOST = os.getenv("MARIADB_HOST", "mariadb")
MARIADB_PORT = int(os.getenv("MARIADB_PORT", "3306"))
MARIADB_DB   = os.getenv("MARIADB_DB", "airnostrum_sql")
MARIADB_USER = os.getenv("MARIADB_USER", "air")
MARIADB_PASS = os.getenv("MARIADB_PASS", "air")

# Configuración MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017")
MONGO_DB  = os.getenv("MONGO_DB", "airnostrum_nosql")

# Helper para convertir Decimal a float
def dec(v):
    return float(v) if isinstance(v, Decimal) else v

def main():
    print("[1/4] Conectando a MariaDB...")
    sql = mysql.connector.connect(
        host=MARIADB_HOST,
        port=MARIADB_PORT,
        user=MARIADB_USER,
        password=MARIADB_PASS,
        database=MARIADB_DB
    )
    cur = sql.cursor(dictionary=True)

    print("[2/4] Conectando a MongoDB...")
    mongo = MongoClient(MONGO_URI)
    db = mongo[MONGO_DB]

    # Limpiar colecciones para demo
    for c in ["airports","flights","passengers","bookings"]:
        db[c].drop()

    # --- Airports ---
    cur.execute("SELECT id, code, name, city, country FROM airports")
    airports = cur.fetchall()
    airport_by_id = {a["id"]: a for a in airports}
    if airports:
        # Mantener id original como _id
        db.airports.insert_many([{**a, "_id": a["id"]} for a in airports])

    # --- Flights (lookup aircraft) ---
    cur.execute(
        "SELECT f.id, f.flight_code, f.origin_airport_id, f.destination_airport_id,"
        " f.departure, f.arrival, f.base_price,"
        " ac.code AS aircraft_code, ac.model AS aircraft_model, ac.seats AS aircraft_seats"
        " FROM flights f JOIN aircraft ac ON ac.id = f.aircraft_id"
    )
    flights = cur.fetchall()
    flight_by_id = {f["id"]: f for f in flights}

    flight_docs = []
    for f in flights:
        o = airport_by_id.get(f["origin_airport_id"])
        d = airport_by_id.get(f["destination_airport_id"])
        flight_docs.append({
            "_id": f["id"],  # mantener id original
            "flight_code": f["flight_code"],
            "departure": f["departure"],
            "arrival": f["arrival"],
            "base_price": dec(f["base_price"]),
            "origin": {"id": o["id"], "code": o["code"], "city": o["city"], "country": o["country"]} if o else None,
            "destination": {"id": d["id"], "code": d["code"], "city": d["city"], "country": d["country"]} if d else None,
            "aircraft": {"code": f["aircraft_code"], "model": f["aircraft_model"], "seats": f["aircraft_seats"]}
        })
    if flight_docs:
        db.flights.insert_many(flight_docs)

    # --- Passengers ---
    cur.execute("SELECT id, full_name, email FROM passengers")
    passengers = cur.fetchall()
    passenger_by_id = {p["id"]: p for p in passengers}
    if passengers:
        db.passengers.insert_many([{**p, "_id": p["id"]} for p in passengers])

    # --- Bookings + tickets ---
    cur.execute("SELECT id, booking_code, passenger_id, flight_id, booked_at, status FROM bookings")
    bookings = cur.fetchall()

    booking_docs = []
    for b in bookings:
        cur.execute("SELECT id, seat, cabin, price FROM tickets WHERE booking_id=%s", (b["id"],))
        tickets = cur.fetchall()
        total = sum(dec(t["price"]) for t in tickets) if tickets else 0.0

        p = passenger_by_id.get(b["passenger_id"])
        f = flight_by_id.get(b["flight_id"])
        o = airport_by_id.get(f["origin_airport_id"]) if f else None
        d = airport_by_id.get(f["destination_airport_id"]) if f else None

        booking_docs.append({
            "_id": b["id"],  # mantener id original
            "booking_code": b["booking_code"],
            "booked_at": b["booked_at"],
            "status": b["status"],
            "passenger": {"id": p["id"], "full_name": p["full_name"], "email": p["email"]} if p else None,
            "flight": {
                "id": f["id"],
                "flight_code": f["flight_code"],
                "departure": f["departure"],
                "arrival": f["arrival"],
                "origin": {"id": o["id"], "code": o["code"], "city": o["city"]} if o else None,
                "destination": {"id": d["id"], "code": d["code"], "city": d["city"]} if d else None,
                "aircraft": {"code": f["aircraft_code"], "model": f["aircraft_model"], "seats": f["aircraft_seats"]} if f else None
            } if f else None,
            "tickets": [{"ticket_id": t["id"], "seat": t["seat"], "cabin": t["cabin"], "price": dec(t["price"])} for t in tickets],
            "total": total
        })

    if booking_docs:
        db.bookings.insert_many(booking_docs)

    # Índices útiles para demo
    db.bookings.create_index("booking_code", unique=True)
    db.bookings.create_index("passenger.email")
    db.bookings.create_index("flight.origin.code")
    db.bookings.create_index("flight.destination.code")

    print("[3/4] Migración completada.")
    print("  Airports  :", db.airports.count_documents({}))
    print("  Flights   :", db.flights.count_documents({}))
    print("  Passengers:", db.passengers.count_documents({}))
    print("  Bookings  :", db.bookings.count_documents({}))

    one = db.bookings.find_one()
    print("[4/4] Sample booking keys:", sorted(list(one.keys())) if one else None)

if __name__ == "__main__":
    main()
