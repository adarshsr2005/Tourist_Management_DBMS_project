-- Create the database
CREATE DATABASE tourism_management;

-- Use the created database
USE tourism_management;

-- Admin table
CREATE TABLE Admin (
    admin_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

--  Travel Agents Table 
CREATE TABLE Travel_agents (
    agent_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    contact VARCHAR(20),
    email VARCHAR(255) UNIQUE,
    agencyname VARCHAR(255),
    admin_id INT,
    FOREIGN KEY (admin_id) REFERENCES Admin(admin_id)
);

--  Packages
CREATE TABLE Packages (
    package_id INT PRIMARY KEY AUTO_INCREMENT,
    package_name VARCHAR(255) NOT NULL,
    tourist_place VARCHAR(255),
    price DECIMAL(10, 2),
    duration VARCHAR(50),
    admin_id INT,
    FOREIGN KEY (admin_id) REFERENCES Admin(admin_id)
);

-- Customer
CREATE TABLE Customer (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    nationality VARCHAR(100),
    referred_customer_id INT,
    admin_id INT,
    FOREIGN KEY (referred_customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (admin_id) REFERENCES Admin(admin_id)
);

-- Customer Phone Numbers
CREATE TABLE Cust_phone_no (
    customer_id INT,
    phone_no VARCHAR(20),
    PRIMARY KEY (customer_id, phone_no),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

-- Tourist Place
CREATE TABLE Tourist_Place (
    place_id INT PRIMARY KEY AUTO_INCREMENT,
    place_name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    description TEXT,
    entry_fee DECIMAL(10, 2)
);

-- Junction table for Customer <-> TouristPlace
CREATE TABLE Customer_TouristPlace (
    customer_id INT,
    place_id INT,
    visit_date DATE,  
    PRIMARY KEY (customer_id, place_id),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (place_id) REFERENCES tourist_Place(place_id)
);

-- Homestays
CREATE TABLE Homestays (
    homestay_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    price_per_night DECIMAL(10, 2),
    rating DECIMAL(3, 2)
);

-- Junction table
CREATE TABLE TouristPlace_Homestay (
    place_id INT,
    homestay_id INT,
    PRIMARY KEY (place_id, homestay_id),
    FOREIGN KEY (place_id) REFERENCES tourist_place(place_id),
    FOREIGN KEY (homestay_id) REFERENCES homestays(homestay_id)
);

-- Review
CREATE TABLE Review (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    homestay_id INT,
    rating INT,
    review_text TEXT,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (homestay_id) REFERENCES Homestays(homestay_id)
);

--  Booking
CREATE TABLE Booking (
    booking_id INT PRIMARY KEY AUTO_INCREMENT,
    checkin_date DATE,
    checkout_date DATE,
    price DECIMAL(10, 2),
    customer_id INT,
    homestay_id INT,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (homestay_id) REFERENCES Homestays(homestay_id)
);

--  Payment
CREATE TABLE Payment (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    payment_type VARCHAR(50),
    payment_status VARCHAR(50),
    price DECIMAL(10, 2),
    transaction_id VARCHAR(255) UNIQUE,
    booking_id INT,
    FOREIGN KEY (booking_id) REFERENCES Booking(booking_id)
);

--  Stays At relationship
CREATE TABLE Stays_at (
    booking_id INT,
    customer_id INT,
    homestay_id INT,
    PRIMARY KEY (booking_id, customer_id, homestay_id),
    FOREIGN KEY (booking_id) REFERENCES Booking(booking_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (homestay_id) REFERENCES Homestays(homestay_id)
);



-- Inserting sample data

-- Admins
INSERT INTO Admin (username, password) VALUES
('admin1', 'pass123'),
('admin2', 'pass456');

-- Travel Agents
INSERT INTO Travel_agents (name, contact, email, agencyname, admin_id) VALUES
('John Doe', '1234567890', 'john.doe@travel.com', 'Doe Travels', 1),
('Jane Smith', '0987654321', 'jane.smith@travel.com', 'Smith Tours', 2),
('Raj Kumar', '9876543210', 'raj.k@travel.com', 'Explore India', 2),
('Sara Lee', '7890123456', 'sara.lee@travel.com', 'Global Trips', 2),
('Michael Brown', '6789012345', 'mike.brown@travel.com', 'Adventure World', 1);

-- Packages
INSERT INTO Packages (package_name, tourist_place, price, duration, admin_id) VALUES
('Desert Safari', 'Rajasthan', 450.00, '4 Days', 2),
('Backwater Bliss', 'Kerala', 600.00, '6 Days', 1),
('Golden Triangle Tour', 'Delhi-Agra-Jaipur', 900.00, '8 Days', 1),
('Andaman Escape', 'Andaman Islands', 1200.00, '7 Days', 2),
('Himalayan Adventure', 'Manali', 500.00, '7 Days', 1),
('Coastal Getaway', 'Goa', 700.00, '5 Days', 2);

-- Customers
INSERT INTO Customer (name, email, nationality, admin_id) VALUES
('Carlos Mendes', 'carlos.m@email.com', 'Brazilian', 2),
('Sophia Chen', 'sophia.c@email.com', 'Chinese', 1),
('David Miller', 'david.m@email.com', 'Canadian', 1),
('Fatima Noor', 'fatima.n@email.com', 'Emirati', 2),
('Alice Johnson', 'alice.j@email.com', 'American', 1),
('Bob Williams', 'bob.w@email.com', 'British', 2);
UPDATE Customer SET referred_customer_id = 1 WHERE customer_id = 2;

-- Customer Phone Numbers
INSERT INTO Cust_phone_no (customer_id, phone_no) VALUES
(3, '555-0103'),
(4, '555-0104'),
(5, '555-0105'),
(6, '555-0106'),
(1, '555-0101'),
(2, '555-0102');

-- Tourist Places
INSERT INTO Tourist_Place (place_name, location, description, entry_fee) VALUES
('Amber Fort', 'Jaipur', 'Historic fort overlooking Maota Lake.', 3.00),
('Taj Mahal', 'Agra', 'Iconic symbol of love in white marble.', 10.00),
('Alleppey Backwaters', 'Kerala', 'Serene network of lagoons and canals.', 5.00),
('Radhanagar Beach', 'Andaman', 'One of Asia’s best beaches.', 0.00),
('Hadimba Temple', 'Manali', 'An ancient cave temple dedicated to Hidimbi Devi.', 2.00),
('Calangute Beach', 'Goa', 'The largest beach in North Goa.', 0.00);

-- Homestays
INSERT INTO Homestays (name, location, price_per_night, rating, place_id) VALUES
('Desert Camp Stay', 'Rajasthan', 90.00, 4.3, 3),
('Backwater Houseboat', 'Alleppey', 200.00, 4.7, 4),
('Heritage Haveli', 'Jaipur', 130.00, 4.6, 5),
('Beachfront Resort', 'Andaman', 220.00, 4.9, 6),
('Mountain View Villa', 'Manali', 120.00, 4.5, 1),
('Sea Breeze Cottage', 'Goa', 150.00, 4.8, 2);

-- Reviews
INSERT INTO Review (customer_id, homestay_id, rating, review_text) VALUES
(3, 3, 5, 'The camel safari was unforgettable!'),
(4, 4, 4, 'Peaceful stay on the water, highly recommend.'),
(5, 5, 5, 'Loved the royal treatment at the Haveli.'),
(6, 6, 5, 'Paradise! The best beach I’ve ever seen.'),
(1, 1, 5, 'Absolutely stunning views and great hospitality!'),
(2, 2, 4, 'Loved the proximity to the beach. Very relaxing stay.');

-- Bookings
INSERT INTO Booking (checkin_date, checkout_date, price, customer_id, homestay_id) VALUES
('2025-10-20', '2025-10-27', 840.00, 1, 5),  -- Alice -> Mountain View Villa
('2025-11-15', '2025-11-20', 750.00, 2, 6),  -- Bob -> Sea Breeze Cottage
('2025-12-05', '2025-12-09', 360.00, 3, 1),  -- David -> Desert Camp Stay
('2026-01-10', '2026-01-15', 1000.00, 4, 2), -- Fatima -> Backwater Houseboat
('2026-02-01', '2026-02-07', 780.00, 5, 3),  -- Carlos -> Heritage Haveli
('2026-03-12', '2026-03-18', 1320.00, 6, 4); 

-- Payments
INSERT INTO Payment (payment_type, payment_status, price, transaction_id, booking_id) VALUES
('Credit Card', 'Completed', 840.00, 'txn_12345abc', 1),
('PayPal', 'Completed', 750.00, 'txn_67890def', 2),
('UPI', 'Completed', 360.00, 'txn_11223ghi', 3),
('Debit Card', 'Pending', 1000.00, 'txn_44556jkl', 4),
('Credit Card', 'Completed', 780.00, 'txn_77889mno', 5),
('Net Banking', 'Completed', 1320.00, 'txn_99001pqr', 6);

-- Stays At (now consistent)
INSERT INTO Stays_at (booking_id, customer_id, homestay_id) VALUES
(1, 1, 5),
(2, 2, 6),
(3, 3, 1),
(4, 4, 2),
(5, 5, 3),
(6, 6, 4);



INSERT INTO customer_touristplace (customer_id, place_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6);

INSERT INTO touristplace_homestay (place_id, homestay_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6);
select * from Payment;

UPDATE Customer
SET nationality = 'Indian'
WHERE customer_id = 2;


DROP FUNCTION IF EXISTS total_revenue_by_place;
DELIMITER $$
CREATE FUNCTION total_revenue_by_place(pid INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
  DECLARE total DECIMAL(10,2);
  SELECT IFNULL(SUM(p.price),0.00) INTO total
  FROM Payment p
  JOIN Booking b ON p.booking_id=b.booking_id
  JOIN Homestays h ON b.homestay_id=h.homestay_id
  WHERE h.place_id = pid;
  RETURN total;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS register_payment;
DELIMITER $$
CREATE PROCEDURE register_payment(
  IN p_booking_id INT,
  IN p_payment_type VARCHAR(50),
  IN p_amount DECIMAL(10,2),
  IN p_txn VARCHAR(255)
)
BEGIN
  DECLARE required DECIMAL(10,2);
  SELECT price INTO required FROM Booking WHERE booking_id = p_booking_id;

  IF required IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Invalid booking ID.';
  END IF;

  IF p_amount <> required THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Payment amount mismatch!';
  END IF;

  INSERT INTO Payment(payment_type,payment_status,price,transaction_id,booking_id)
  VALUES(p_payment_type, NULL, p_amount, p_txn, p_booking_id);
END$$
DELIMITER ;



