USE project_db;

INSERT INTO ClimateData (location, record_date, temperature, precipitation, humidity)
VALUES
('Chester',     '2025-07-01', 26.2,  3.1, 62.0),
('Vancouver',   '2025-07-02', 21.4,  5.3, 74.0),
('Ottawa',      '2025-07-03', 28.6,  0.4, 56.0),
('Calgary',     '2025-07-04', 24.9,  1.2, 45.0),
('Montreal',    '2025-07-05', 29.8,  2.5, 65.0),
('Scarborough',     '2025-07-06', 22.1,  6.8, 80.0),
('Winnipeg',    '2025-07-07', 29.3,  0.0, 40.0),
('Kitchener',      '2025-07-08', 25.7,  0.8, 48.0),
('Leader',   '2025-07-09', 26.9,  1.9, 50.0),
('Edmonton',    '2025-07-10', 23.5,  1.0, 52.0),
('Victoria',    '2025-07-11', 20.8,  4.6, 67.0),
('Waterloo', '2025-07-12', 32.0,  3.0, 68.0);
