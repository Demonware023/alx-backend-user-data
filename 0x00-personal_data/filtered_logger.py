#!/usr/bin/env python3
"""
This module contains the function filter_datum which obfuscates 
certain fields in a log message.
"""

import re
from typing import List

def filter_datum(fields: List[str], redaction: str, 
                 message: str, separator: str) -> str:
    """
    Obfuscates certain fields in a log message.
    
    Args:
        fields (List[str]): Fields to obfuscate.
        redaction (str): Replacement string for obfuscation.
        message (str): Log line to obfuscate.
        separator (str): Field separator in the log line.
    
    Returns:
        str: The obfuscated log message.
    """
    for field in fields:
        pattern = f'{field}=[^{separator}]*'
        replacement = f'{field}={redaction}'
        message = re.sub(pattern, replacement, message)
    return message
