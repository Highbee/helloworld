-- Add new columns to the bleaching_process table for detailed reporting
ALTER TABLE bleaching_process
ADD COLUMN process_start DATETIME,
ADD COLUMN heating_start DATETIME,
ADD COLUMN keeping_start DATETIME,
ADD COLUMN cooling_start DATETIME,
ADD COLUMN process_end DATETIME,
ADD COLUMN heating_duration_minutes INT,
ADD COLUMN process_duration_minutes INT,
ADD COLUMN number_of_cakes_dried INT,
ADD COLUMN technical_challenges TEXT,
ADD COLUMN maintenance_notes TEXT,
ADD COLUMN remarks TEXT;

-- Add whatsapp_number column to employees table for better identification
ALTER TABLE employees ADD COLUMN whatsapp_number VARCHAR(20) NULL;

-- Update existing employees with their WhatsApp numbers
-- Note: Please verify that the employee_id values are correct for your database.
UPDATE employees SET whatsapp_number = '+2347062716844' WHERE employee_id = 2; -- Olayemi Oyeniyi
UPDATE employees SET whatsapp_number = '+2347066150893' WHERE employee_id = 3; -- Afuye Joel
UPDATE employees SET whatsapp_number = '+2348105931726' WHERE employee_id = 4; -- Azeez Kabir
UPDATE employees SET whatsapp_number = '+2349060834296' WHERE employee_id = 1; -- Emmanuel Olaoye
