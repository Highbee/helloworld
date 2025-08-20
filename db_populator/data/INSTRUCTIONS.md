## Bleaching Process Report and Infographic

This project includes a feature to parse WhatsApp chat logs of bleaching process reports and display the data in an interactive infographic.

### How to set up and use the new feature:

#### 1. Update the Database Schema

The SQL file to update your database schema is located at `db_populator/data/schema_update.sql`. You need to run this script on your `ayodele` database.

You can do this using a MySQL client. For example, from the project root:
```bash
mysql -u root -p ayodele < db_populator/data/schema_update.sql
```
*(You might need to enter your MySQL root password if you have one.)*

#### 2. Prepare the Data

A Django management command has been created to parse the `whatsapp_chat.txt` file and generate an SQL script with the report data.

The chat file is located at `db_populator/data/whatsapp_chat.txt`.

To generate the data population script, run the following command from the project root:
```bash
python db_populator/manage.py import_bleaching_reports db_populator/data/whatsapp_chat.txt db_populator/data/data_population.sql
```
This will parse the chat log and create/overwrite the `data_population.sql` file in the `db_populator/data/` directory.

*Note: Before running, you may want to review the `employee_map` dictionary inside the management command (`db_populator/populator/management/commands/import_bleaching_reports.py`) to ensure the names, phone numbers, and IDs match your `employees` table.*

#### 3. Populate the Database with Chat Data

Now, run the newly generated `data_population.sql` script on your database to insert all the parsed report data.
```bash
mysql -u root -p ayodele < db_populator/data/data_population.sql
```

#### 4. Run the Application

Once the database is updated and populated, you can run the Django application as usual:
```bash
python db_populator/manage.py runserver
```

#### 5. View the Infographic

Open your web browser and navigate to the following URL to see the new infographic dashboard:
[http://127.0.0.1:8000/bleaching-infographic/](http://127.0.0.1:8000/bleaching-infographic/)

You can use the date filters on the page to narrow down the data displayed in the charts.
