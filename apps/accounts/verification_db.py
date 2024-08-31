import os
import random
import sqlite3
from django.conf import settings
from django.utils import timezone


BASE_DIR = settings.BASE_DIR


class DB:
    """
    Database handler for interacting with the 'VERIFICATION_DB' SQLite database.

    Attributes:
        connection (sqlite3.Connection): Connection to the SQLite database.
        cursor (sqlite3.Cursor): Cursor object for executing SQL queries.
        table (str): Name of the table within the database.

    Methods:
        __init__: Initializes the database and creates the table if it doesn't exist.
        get: Retrieves a record based on the provided identifier.
        insert: Inserts a new record into the database table.
        delete: Deletes a record based on the provided identifier.
        update: Updates an existing record based on the identifier.
        clear: Clears all records from the database table.
        get_all: Retrieves all records from the database.
    """

    table = "verification_db"

    def __init__(self, table_name=None) -> None:
        db_folder = os.path.join(BASE_DIR, "db", "verification_db_account.sqlite3")

        CONNECTION = sqlite3.connect(db_folder, check_same_thread=False)
        CURSOR = CONNECTION.cursor()

        self.connection = CONNECTION
        self.cursor = CURSOR
        return

        if table_name:
            self.table = table_name

        self.cursor.execute(
            f"""
                CREATE TABLE IF NOT EXISTS {self.table} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    identifier VARCHAR(255) NOT NULL,
                    code INTEGER,
                    column_c VARCHAR(255) NULL,
                    expires_at VARCHAR(255) NOT NULL
                ) ;
            """
        )

    def get(self, identifier):
        """
        Retrieve a record from the database based on the provided identifier.

        Args:
            identifier (str): The unique identifier used to fetch the record.

        Returns:
            tuple or None: A tuple representing the fetched record if found,
                        otherwise returns None.
        """
        with self.connection:
            response = self.cursor.execute(
                f"""
                     SELECT * FROM {self.table} WHERE identifier=? ;
                """,
                (identifier,),
            ).fetchone()

            return response

    def insert(self, identifier, code, column_c, expires_at):
        """
        Insert a new record into the database.

        Args:
            identifier (str): The unique identifier for the new record.
            code (str): The code value to be inserted.
            column_c (str): The value for column_c in the new record.
            expires_at (str): The expiration date or time for the new record.

        Returns:
            None
        """
        with self.connection:
            self.cursor.execute(
                f"""
                    INSERT INTO {self.table} (identifier, code, column_c, expires_at)
                    VALUES (?, ?, ?, ?);
                """,
                (identifier, code, column_c, expires_at),
            )

    def delete(self, identifier):
        """
        Delete a record based on the provided identifier.

        Args:
            identifier (str): The identifier used to delete the record.

        Returns:
            None
        """
        with self.connection:
            self.cursor.execute(
                f"""DELETE FROM {self.table} WHERE identifier=?;""", (identifier,)
            )

    def update(self, identifier, new_code, new_column_c, new_expires_at):
        """
        Update an existing record in the database based on the provided identifier.

        Args:
            identifier (str): The unique identifier for the record to be updated.
            new_code (str): The new code value to update in the record.
            new_column_c (str): The new value for column_c in the record.
            new_expires_at (str): The new expiration date or time for the record.

        Returns:
            None
        """
        with self.connection:
            self.cursor.execute(
                f"""
                UPDATE {self.table}
                SET code=?, column_c=?, expires_at=?
                WHERE identifier=?;
                """,
                (new_code, new_column_c, new_expires_at, identifier),
            )

    def clear(self):
        """
        Clear all records from the database table.

        Returns:
            None
        """
        with self.connection:
            self.cursor.execute(f"DELETE FROM {self.table};")
        self.cursor.execute("VACUUM;")
        self.connection.commit()

    def get_all(self):
        """
        Retrieve all records from the database.

        Returns:
            list: A list containing all records from the database.
        """
        with self.connection:
            self.cursor.execute(f"SELECT * FROM {self.table};")
            return self.cursor.fetchall()


class VendorVerificationDB(DB):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate_code(self, vendor):
        identifier = self.generate_identifier(vendor)

        code = str(random.randrange(100000, 999999))

        self.update_code(code, identifier)

        return code

    def generate_identifier(self, vendor):
        user = vendor.user_account

        _id = str(f"u_{user.pk}id_{user.unique_id}v_{vendor.id}")

        return _id

    def update_code(self, code, identifier):
        record = self.get(identifier)

        if record:
            _, _, prev_code, column_c, expires_at = record
            self.update(identifier, code, column_c, expires_at)
        else:
            self.insert(identifier, code, "", str(timezone.now()))
