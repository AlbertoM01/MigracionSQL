// ----------------
// Crear índices / restricciones
CREATE CONSTRAINT airport_code IF NOT EXISTS FOR (a:Airport) REQUIRE a.code IS UNIQUE;
CREATE CONSTRAINT aircraft_code IF NOT EXISTS FOR (ac:Aircraft) REQUIRE ac.code IS UNIQUE;
CREATE CONSTRAINT flight_code IF NOT EXISTS FOR (f:Flight) REQUIRE f.flight_code IS UNIQUE;
CREATE CONSTRAINT passenger_email IF NOT EXISTS FOR (p:Passenger) REQUIRE p.email IS UNIQUE;
CREATE CONSTRAINT booking_code IF NOT EXISTS FOR (b:Booking) REQUIRE b.booking_code IS UNIQUE;

// ----------------
// Airports
LOAD CSV WITH HEADERS FROM 'file:///airports.csv' AS row
MERGE (a:Airport {code: row.code})
SET a.name = row.name, a.city = row.city, a.country = row.country;

// ----------------
// Aircraft
LOAD CSV WITH HEADERS FROM 'file:///aircraft.csv' AS row
MERGE (ac:Aircraft {code: row.code})
SET ac.model = row.model, ac.seats = toInteger(row.seats);

// ----------------
// Passengers
LOAD CSV WITH HEADERS FROM 'file:///passengers.csv' AS row
MERGE (p:Passenger {email: row.email})
SET p.full_name = row.full_name;

// ----------------
// Flights y relaciones a Airports y Aircraft
LOAD CSV WITH HEADERS FROM 'file:///flights.csv' AS row
MATCH (o:Airport), (d:Airport), (ac:Aircraft)
WHERE o.id = toInteger(row.origin_airport_id)
  AND d.id = toInteger(row.destination_airport_id)
  AND ac.id = toInteger(row.aircraft_id)
MERGE (f:Flight {flight_code: row.flight_code})
SET f.departure = datetime(row.departure),
    f.arrival = datetime(row.arrival),
    f.base_price = toFloat(row.base_price)
MERGE (f)-[:ORIGIN]->(o)
MERGE (f)-[:DESTINATION]->(d)
MERGE (f)-[:OPERATED_BY]->(ac);

// ----------------
// Bookings y relaciones
LOAD CSV WITH HEADERS FROM 'file:///bookings.csv' AS row
MATCH (p:Passenger), (f:Flight)
WHERE p.id = toInteger(row.passenger_id)
  AND f.id = toInteger(row.flight_id)
MERGE (b:Booking {booking_code: row.booking_code})
SET b.booked_at = datetime(row.booked_at), b.status = row.status
MERGE (b)-[:BOOKED_BY]->(p)
MERGE (b)-[:FOR_FLIGHT]->(f);

// ----------------
// Tickets y relaciones
LOAD CSV WITH HEADERS FROM 'file:///tickets.csv' AS row
MATCH (b:Booking)
WHERE b.id = toInteger(row.booking_id)
MERGE (t:Ticket {id: toInteger(row.id)})
SET t.seat = row.seat, t.cabin = row.cabin, t.price = toFloat(row.price)
MERGE (t)-[:BELONGS_TO]->(b);