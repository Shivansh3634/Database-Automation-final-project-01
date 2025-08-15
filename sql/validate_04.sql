USE project_db;

-- Structure checks
DESCRIBE ClimateData;

-- Column existence check
SELECT COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA='project_db' AND TABLE_NAME='ClimateData'
ORDER BY ORDINAL_POSITION;

-- Data presence check
SELECT COUNT(*) AS total_rows FROM ClimateData;

-- Business query checks
SELECT * FROM ClimateData WHERE temperature > 20 ORDER BY record_date LIMIT 5;

-- Humidity update sanity window
SELECT location, AVG(humidity) AS avg_humidity
FROM ClimateData
GROUP BY location
ORDER BY avg_humidity DESC
LIMIT 5;
