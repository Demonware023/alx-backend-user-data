#!/usr/bin/env python3
"""
This module provides a filtered logger and database connection
handling, including secure access to a MySQL database using environment
variables.
"""

import os
import mysql.connector
import logging
from typing import List
import re


# Define the PII fields to be redacted
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Filter values in incoming log records using filter_datum.
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Returns the log message obfuscated.

    Args:
        fields: a list of strings representing all fields to obfuscate
        redaction: a string representing by what the field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is separating
                   all fields in the log line (message)
    """
    for field in fields:
        message = re.sub(f'{field}=[^{separator}]*',
                         f'{field}={redaction}', message)
    return message


def get_logger() -> logging.Logger:
    """
    Returns a logging.Logger object configured with a RedactingFormatter.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a MySQL database connection object using environment
    variables for credentials.
    """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.getenv('PERSONAL_DATA_DB_NAME')

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )


def main():
    """
    Retrieves and displays rows from the 'users' table with filtered output.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()

    for row in cursor:
        msg = f"name={row[0]}; email={row[1]}; phone={row[2]}; " \
              f"ssn={row[3]}; password={row[4]}; ip={row[5]}; " \
              f"last_login={row[6]}; user_agent={row[7]};"
        logger.info(msg)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
