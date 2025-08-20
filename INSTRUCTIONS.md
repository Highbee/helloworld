## Bleaching Process Report and Infographic

This project includes a feature to parse WhatsApp chat logs of bleaching process reports and display the data in an interactive infographic.

### How to set up and use the new feature:

#### 1. Update the Database Schema

A new SQL file `schema_update.sql` has been created to add the necessary columns to your `bleaching_process` table. You need to run this script on your `ayodele` database.

You can do this using a MySQL client. For example, from your command line:
```bash
mysql -u root -p ayodele < schema_update.sql
```
*(You might need to enter your MySQL root password if you have one.)*

#### 2. Prepare the Data

A Python script `data_parser.py` has been created to read the `whatsapp_chat.txt` file and convert the chat logs into SQL `INSERT` statements.

Before running the script, you might want to review the `employee_map` dictionary inside `data_parser.py` and ensure the names and IDs match the records in your `employees` table.

To generate the data population script, run the following command from the root of the project:
```bash
python data_parser.py
```
This will create a new file named `data_population.sql`.

#### 3. Populate the Database with Chat Data

Now, run the newly generated `data_population.sql` script on your database to insert all the parsed report data.
```bash
mysql -u root -p ayodele < data_population.sql
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
