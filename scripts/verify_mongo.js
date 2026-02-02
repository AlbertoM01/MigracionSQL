// Ejecuta esto en mongosh conectado a airnostrum_nosql
db.bookings.countDocuments()

// 1) Un booking completo (pasajero + vuelo + tickets)
db.bookings.findOne({}, {booking_code:1, booked_at:1, status:1, passenger:1, flight:1, tickets:1, total:1})

// 2) Reservas por email
db.bookings.find({"passenger.email":"alejandro@example.com"}, {booking_code:1, total:1, "flight.flight_code":1})

// 3) Top destinos desde PMI
db.bookings.aggregate([
  {$match: {"flight.origin.code":"PMI"}},
  {$group:{_id:"$flight.destination.code", totalBookings:{$sum:1}}},
  {$sort:{totalBookings:-1}}
])
