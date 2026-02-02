DROP DATABASE IF EXISTS airnostrum_sql;
CREATE DATABASE airnostrum_sql CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE airnostrum_sql;

CREATE TABLE airports (
  id INT PRIMARY KEY AUTO_INCREMENT,
  code VARCHAR(5) NOT NULL UNIQUE,
  name VARCHAR(120) NOT NULL,
  city VARCHAR(80) NOT NULL,
  country VARCHAR(80) NOT NULL
);

CREATE TABLE aircraft (
  id INT PRIMARY KEY AUTO_INCREMENT,
  code VARCHAR(10) NOT NULL UNIQUE,
  model VARCHAR(80) NOT NULL,
  seats INT NOT NULL
);

CREATE TABLE flights (
  id INT PRIMARY KEY AUTO_INCREMENT,
  flight_code VARCHAR(10) NOT NULL UNIQUE,
  origin_airport_id INT NOT NULL,
  destination_airport_id INT NOT NULL,
  departure DATETIME NOT NULL,
  arrival DATETIME NOT NULL,
  aircraft_id INT NOT NULL,
  base_price DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (origin_airport_id) REFERENCES airports(id),
  FOREIGN KEY (destination_airport_id) REFERENCES airports(id),
  FOREIGN KEY (aircraft_id) REFERENCES aircraft(id)
);

CREATE TABLE passengers (
  id INT PRIMARY KEY AUTO_INCREMENT,
  full_name VARCHAR(120) NOT NULL,
  email VARCHAR(120) NOT NULL UNIQUE
);

CREATE TABLE bookings (
  id INT PRIMARY KEY AUTO_INCREMENT,
  booking_code VARCHAR(12) NOT NULL UNIQUE,
  passenger_id INT NOT NULL,
  flight_id INT NOT NULL,
  booked_at DATETIME NOT NULL,
  status VARCHAR(20) NOT NULL,
  FOREIGN KEY (passenger_id) REFERENCES passengers(id),
  FOREIGN KEY (flight_id) REFERENCES flights(id)
);

CREATE TABLE tickets (
  id INT PRIMARY KEY AUTO_INCREMENT,
  booking_id INT NOT NULL,
  seat VARCHAR(5) NOT NULL,
  cabin VARCHAR(20) NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (booking_id) REFERENCES bookings(id)
);