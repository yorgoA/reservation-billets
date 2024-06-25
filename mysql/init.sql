CREATE DATABASE IF NOT EXISTS reservationdb;
USE reservationdb;

CREATE TABLE IF NOT EXISTS events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    date DATETIME NOT NULL,
    location VARCHAR(255) NOT NULL,
    available_tickets INT NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    event_id INT,
    num_tickets INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (event_id) REFERENCES events(id)
);

INSERT INTO events (name, date, location, available_tickets) VALUES 
('Concert Coldplay', '2024-07-24 19:00:00', 'Stadium A', 100),
('Concert Taylor Swift', '2024-07-15 20:00:00', 'Arena B', 150),
('Classico barca vs real', '2024-08-05 18:30:00', 'Field C', 200);

INSERT INTO users (name, email) VALUES 
('Yorgo Aoun', 'yorgo@gmail.com'),
('Bruno Mougheraba', 'bruno@gmail.com'),
('Tony godzilla', 'godzilla@yahoo.com');

INSERT INTO reservations (user_id, event_id, num_tickets) VALUES 
(1, 1, 2),
(2, 1, 3),
(3, 2, 1);
