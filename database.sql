-- ============================================
-- Ticketing System Database
-- Tables: Users, Routes, Buses, Fares, Trips, Tickets, OfflineDevices
-- ============================================

-- 1. Users Table
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    phone_number TEXT UNIQUE NOT NULL,
    email TEXT,
    password_hash TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Routes Table
CREATE TABLE IF NOT EXISTS Routes (
    route_id INTEGER PRIMARY KEY AUTOINCREMENT,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    distance_km REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 3. Buses Table
CREATE TABLE IF NOT EXISTS Buses (
    bus_id INTEGER PRIMARY KEY AUTOINCREMENT,
    plate_number TEXT UNIQUE NOT NULL,
    bus_type TEXT,
    capacity INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 4. Fares Table
CREATE TABLE IF NOT EXISTS Fares (
    fare_id INTEGER PRIMARY KEY AUTOINCREMENT,
    route_id INTEGER NOT NULL,
    vehicle_type TEXT,
    amount REAL NOT NULL,
    effective_date DATE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (route_id) REFERENCES Routes(route_id)
);

-- 5. Trips Table
CREATE TABLE IF NOT EXISTS Trips (
    trip_id INTEGER PRIMARY KEY AUTOINCREMENT,
    bus_id INTEGER NOT NULL,
    route_id INTEGER NOT NULL,
    departure_time DATETIME NOT NULL,
    seats_available INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bus_id) REFERENCES Buses(bus_id),
    FOREIGN KEY (route_id) REFERENCES Routes(route_id)
);

-- 6. Tickets Table
CREATE TABLE IF NOT EXISTS Tickets (
    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    trip_id INTEGER NOT NULL,
    seat_number INTEGER,
    qr_code TEXT NOT NULL,
    status TEXT DEFAULT 'unused' CHECK(status IN ('unused','used','cancelled')),
    purchase_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    used_time DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (trip_id) REFERENCES Trips(trip_id)
);

-- 7. Offline Device Sync Table
CREATE TABLE IF NOT EXISTS OfflineDevices (
    device_id INTEGER PRIMARY KEY AUTOINCREMENT,
    last_sync DATETIME,
    location TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Optional: Indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_tickets_user_id ON Tickets(user_id);
CREATE INDEX IF NOT EXISTS idx_tickets_trip_id ON Tickets(trip_id);
CREATE INDEX IF NOT EXISTS idx_trips_route_id ON Trips(route_id);
CREATE INDEX IF NOT EXISTS idx_fares_route_id ON Fares(route_id);
