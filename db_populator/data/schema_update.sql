-- This script updates the database schema.
-- It modifies existing columns to allow NULL values and adds a new column to the employees table.
-- It is safe to re-run this script.

-- Modify columns in the bleaching_process table to allow NULL values
ALTER TABLE bleaching_process
MODIFY COLUMN process_start DATETIME NULL,
MODIFY COLUMN heating_start DATETIME NULL,
MODIFY COLUMN keeping_start DATETIME NULL,
MODIFY COLUMN cooling_start DATETIME NULL,
MODIFY COLUMN process_end DATETIME NULL,
MODIFY COLUMN heating_duration_minutes INT NULL,
MODIFY COLUMN process_duration_minutes INT NULL,
MODIFY COLUMN number_of_cakes_dried INT NULL,
MODIFY COLUMN technical_challenges TEXT NULL,
MODIFY COLUMN maintenance_notes TEXT NULL,
MODIFY COLUMN remarks TEXT NULL;

-- Add whatsapp_number column to employees table for better identification
-- The following command might fail if the column already exists, which is safe to ignore.
ALTER TABLE employees ADD COLUMN whatsapp_number VARCHAR(20) NULL;

-- Update existing employees with their WhatsApp numbers
-- Note: Please verify that the employee_id values are correct for your database.
UPDATE employees SET whatsapp_number = '+2347062716844' WHERE employee_id = 2; -- Olayemi Oyeniyi
UPDATE employees SET whatsapp_number = '+2347066150893' WHERE employee_id = 3; -- Afuye Joel
UPDATE employees SET whatsapp_number = '+2348105931726' WHERE employee_id = 4; -- Azeez Kabir
UPDATE employees SET whatsapp_number = '+2349060834296' WHERE employee_id = 1; -- Emmanuel Olaoye
