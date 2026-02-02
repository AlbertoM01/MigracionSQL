USE airnostrum_sql;

INSERT INTO airports(code,name,city,country) VALUES
('PMI','Palma de Mallorca Airport','Palma','Spain'),
('BCN','Barcelona-El Prat Airport','Barcelona','Spain'),
('MAD','Adolfo Suárez Madrid–Barajas Airport','Madrid','Spain'),
('VLC','Valencia Airport','Valencia','Spain'),
('BIO','Bilbao Airport','Bilbao','Spain');

INSERT INTO aircraft(code,model,seats) VALUES
('CRJ1000','Bombardier CRJ-1000',100),
('ATR72','ATR 72-600',72);

-- Flights for next 48h
INSERT INTO flights(flight_code,origin_airport_id,destination_airport_id,departure,arrival,aircraft_id,base_price) VALUES
('YW101', 1, 2, NOW() + INTERVAL 2 HOUR,  NOW() + INTERVAL 3 HOUR, 1, 59.90),
('YW102', 2, 1, NOW() + INTERVAL 6 HOUR,  NOW() + INTERVAL 7 HOUR, 1, 64.90),
('YW201', 1, 3, NOW() + INTERVAL 4 HOUR,  NOW() + INTERVAL 5 HOUR, 2, 79.90),
('YW301', 1, 5, NOW() + INTERVAL 10 HOUR, NOW() + INTERVAL 12 HOUR,2, 89.90),
('YW401', 4, 1, NOW() + INTERVAL 8 HOUR,  NOW() + INTERVAL 9 HOUR, 1, 54.90);

INSERT INTO passengers(full_name,email) VALUES
('Alejandro Dehesa','alejandro@example.com'),
('Marta López','marta@example.com'),
('Sergio Ruiz','sergio@example.com'),
('Lucía Pérez','lucia@example.com');

INSERT INTO bookings(booking_code,passenger_id,flight_id,booked_at,status) VALUES
('AN-000001',1,1,NOW() - INTERVAL 1 DAY,'CONFIRMED'),
('AN-000002',2,3,NOW() - INTERVAL 6 HOUR,'CONFIRMED'),
('AN-000003',3,4,NOW() - INTERVAL 2 HOUR,'PENDING'),
('AN-000004',4,2,NOW() - INTERVAL 3 DAY,'CANCELLED');

INSERT INTO tickets(booking_id,seat,cabin,price) VALUES
(1,'12A','ECONOMY',69.90),
(1,'12B','ECONOMY',69.90),
(2,'03C','ECONOMY',89.90),
(3,'08D','ECONOMY',99.90),
(4,'18F','ECONOMY',74.90);

