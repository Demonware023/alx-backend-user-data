#!/usr/bin/env python3
"""
This module provides a filtered logger for handling and obfuscating
sensitive user data in logs.
"""

import os
import mysql.connector
from mysql.connector import connection
import logging
from typing import List, Tuple

# Define the PII fields to be redacted
PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone_number",
                               "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Obfuscates specified fields in a log message.
    """
    for field in fields:
        pattern = f'{field}=.*?{separator}'
        replace = f'{field}={redaction}{separator}'
        message = re.sub(pattern, replace, message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class for filtering PII fields in logs.
    """

    REDACTION = "***"
    FORMAT = ("[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: "
              "%(message)s")
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter with specific fields to redact.
        """
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record by redacting sensitive information.
        """
        original_message = super().format(record)
        filtered_message = filter_datum(self.fields, self.REDACTION,
                                        original_message, self.SEPARATOR)
        return filtered_message


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger named 'user_data'.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> connection.MySQLConnection:
    """
    Returns a MySQL database connection object using environment
    variables for credentials.

    Environment variables:
        PERSONAL_DATA_DB_USERNAME: Username for the database (default: 'root')
        PERSONAL_DATA_DB_PASSWORD: Password for the database (default: '')
        PERSONAL_DATA_DB_HOST: Hostname of the database (default: 'localhost')
        PERSONAL_DATA_DB_NAME: Name of the database

    Returns:
        MySQLConnection: A connection object to the specified database.
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
