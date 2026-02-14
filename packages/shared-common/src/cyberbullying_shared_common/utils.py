# =============================================================================
# UTILITIES MODULE
# =============================================================================
# Purpose: Common utility functions used across all services.
#
# This module provides:
# - UUID generation
# - JSON file operations
# - Directory management
# - Timestamp utilities
# - Data serialization
#
# Author: Cyberbullying Prediction Team
# Version: 1.0.0
# =============================================================================

# =============================================================================
# IMPORTS
# =============================================================================
import json  # JSON encoding/decoding
import uuid  # UUID generation
from datetime import datetime, timezone  # Date/time handling
from pathlib import Path  # Path manipulation
from typing import Any, Dict, Optional, Union  # Type hints

# Third-party imports
import orjson  # Fast JSON library

# =============================================================================
# UUID UTILITIES
# =============================================================================

def generate_uuid() -> str:
    """
    Generate a unique UUID (Universally Unique Identifier).
    
    This function creates a random UUID v4 which is practically unique.
    UUIDs are useful for:
    - Unique identifiers for database records
    - Request IDs for tracing
    - Cache keys
    
    Returns:
        A UUID string in standard format (e.g., '550e8400-e29b-41d4-a716-446655440000')
    
    Example:
        >>> generate_uuid()
        '550e8400-e29b-41d4-a716-446655440000'
        >>> generate_uuid()
        '6ba7b810-9dad-11d1-80b4-00c04fd430c8'
    """
    return str(uuid.uuid4())


def generate_uuid_v5(namespace: str, name: str) -> str:
    """
    Generate a deterministic UUID v5 from a namespace and name.
    
    UUID v5 is generated from a namespace and name using SHA-1 hashing.
    The same namespace + name always produces the same UUID.
    This is useful for:
    - Creating consistent IDs for entities
    - Generating IDs without central coordination
    
    Args:
        namespace: A valid UUID string representing the namespace
                   Common namespaces: URL, DNS, OID, X500
        name: The name within the namespace
    
    Returns:
        A deterministic UUID string
    
    Example:
        >>> generate_uuid_v5(uuid.NAMESPACE_URL, "example.com")
        '2c9ea15c-5d2f-5c23-a8e1-9b1c3d2e4f5a'
    """
    # Convert namespace string to UUID
    ns = uuid.UUID(namespace)
    # Generate name-based UUID
    return str(uuid.uuid5(ns, name))


# =============================================================================
# TIMESTAMP UTILITIES
# =============================================================================

def get_timestamp(
    as_string: bool = True,
    utc: bool = True,
    format: str = "iso",
) -> Union[str, datetime]:
    """
    Get current timestamp.
    
    This function provides a consistent way to get timestamps
    throughout the application.
    
    Args:
        as_string: Whether to return as string or datetime object
                   Default: True (return string)
        utc: Whether to return UTC time or local time
             Default: True (UTC)
        format: Format for string output
                'iso' - ISO 8601 format (2024-01-15T10:30:00.123456Z)
                'date' - Date only (2024-01-15)
                'time' - Time only (10:30:00)
                'unix' - Unix timestamp
    
    Returns:
        Timestamp as string or datetime object
    
    Example:
        >>> get_timestamp()
        '2024-01-15T10:30:00.123456Z'
        >>> get_timestamp(utc=False)
        '2024-01-15T10:30:00.123456+05:30'
        >>> get_timestamp(format='date')
        '2024-01-15'
    """
    # Get current time
    now = datetime.now(timezone.utc) if utc else datetime.now()
    
    # Return based on format
    if as_string:
        if format == "iso":
            return now.isoformat()
        elif format == "date":
            return now.strftime("%Y-%m-%d")
        elif format == "time":
            return now.strftime("%H:%M:%S")
        elif format == "unix":
            return str(int(now.timestamp()))
        else:
            return now.isoformat()
    else:
        return now


def parse_timestamp(timestamp: Union[str, datetime]) -> datetime:
    """
    Parse timestamp from string or datetime.
    
    Args:
        timestamp: Timestamp to parse (ISO string or datetime)
    
    Returns:
        datetime object with timezone info
    
    Example:
        >>> parse_timestamp("2024-01-15T10:30:00Z")
        datetime.datetime(2024, 1, 15, 10, 30, tzinfo=datetime.timezone.utc)
    """
    # If already datetime, return as-is
    if isinstance(timestamp, datetime):
        return timestamp
    
    # Try parsing ISO format
    try:
        # Handle 'Z' suffix
        timestamp = timestamp.replace('Z', '+00:00')
        return datetime.fromisoformat(timestamp)
    except ValueError:
        # Try parsing as Unix timestamp
        try:
            return datetime.fromtimestamp(float(timestamp), tz=timezone.utc)
        except (ValueError, OSError):
            raise ValueError(f"Unable to parse timestamp: {timestamp}")


# =============================================================================
# FILE UTILITIES
# =============================================================================

def ensure_dir(path: Union[str, Path]) -> Path:
    """
    Ensure a directory exists, creating it if necessary.
    
    This function creates all intermediate directories in the path.
    
    Args:
        path: Directory path to ensure
    
    Returns:
        Path object for the directory
    
    Example:
        >>> ensure_dir("/data/models/2024")
        PosixPath('/data/models/2024')
        
        # Creates /data/models/ if it doesn't exist
    """
    # Convert to Path if string
    path = Path(path)
    # Create directory and all parents
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_json(
    path: Union[str, Path],
    as_dict: bool = True,
) -> Union[Dict[str, Any], Any]:
    """
    Load JSON file.
    
    This function reads a JSON file and returns its contents.
    It uses orjson for faster JSON parsing.
    
    Args:
        path: Path to JSON file
        as_dict: Whether to return as dictionary
                 Default: True
    
    Returns:
        Parsed JSON data as dict or other type
    
    Example:
        >>> load_json("config.json")
        {'name': 'cyberbullying', 'version': '1.0.0'}
        
        >>> load_json("data.json", as_dict=False)
        [1, 2, 3]
    """
    # Convert to Path if string
    path = Path(path)
    
    # Read file
    with open(path, "rb") as f:
        # Use orjson for faster parsing
        data = orjson.loads(f.read())
    
    # Return as dict or original type
    return dict(data) if as_dict and isinstance(data, dict) else data


def save_json(
    data: Any,
    path: Union[str, Path],
    indent: Optional[int] = 2,
) -> None:
    """
    Save data to JSON file.
    
    This function writes data to a JSON file.
    It uses orjson for faster JSON serialization.
    
    Args:
        data: Data to save (must be JSON serializable)
        path: Path to save JSON file
        indent: Indentation level
               Default: 2 (pretty-printed)
               Set to None for compact output
    
    Example:
        >>> save_json({"name": "cyberbullying"}, "output.json")
        
        # Creates: {"name": "cyberbullying"}
    """
    # Convert to Path if string
    path = Path(path)
    
    # Ensure directory exists
    ensure_dir(path.parent)
    
    # Serialize with orjson
    options = orjson.OPT_INDENT_2 if indent else 0
    json_bytes = orjson.dumps(data, option=options)
    
    # Write to file
    with open(path, "wb") as f:
        f.write(json_bytes)


# =============================================================================
# DATA SERIALIZATION
# =============================================================================

def serialize_to_json(data: Any, pretty: bool = False) -> str:
    """
    Serialize data to JSON string.
    
    Args:
        data: Data to serialize
        pretty: Whether to pretty-print
    
    Returns:
        JSON string
    
    Example:
        >>> serialize_to_json({"key": "value"})
        '{"key": "value"}'
        
        >>> serialize_to_json({"key": "value"}, pretty=True)
        '{\n  "key": "value"\n}'
    """
    if pretty:
        return orjson.dumps(data, option=orjson.OPT_INDENT_2).decode("utf-8")
    return orjson.dumps(data).decode("utf-8")


def deserialize_from_json(json_str: str) -> Any:
    """
    Deserialize JSON string to Python object.
    
    Args:
        json_str: JSON string
    
    Returns:
        Deserialized Python object
    
    Example:
        >>> deserialize_from_json('{"key": "value"}')
        {'key': 'value'}
    """
    return orjson.loads(json_str)


# =============================================================================
# DICTIONARY UTILITIES
# =============================================================================

def flatten_dict(
    d: Dict[str, Any],
    parent_key: str = "",
    sep: str = ".",
) -> Dict[str, Any]:
    """
    Flatten a nested dictionary.
    
    This function converts a nested dictionary to a flat dictionary
    with dot-separated keys.
    
    Args:
        d: Dictionary to flatten
        parent_key: Parent key prefix for nested values
        sep: Separator for nested keys
             Default: '.' (dot)
    
    Returns:
        Flattened dictionary
    
    Example:
        >>> flatten_dict({"a": {"b": {"c": 1}}})
        {'a.b.c': 1}
        
        >>> flatten_dict({"a": 1, "b": {"c": 2}})
        {'a': 1, 'b.c': 2}
    """
    items = []
    
    for k, v in d.items():
        # Create new key with prefix
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        
        if isinstance(v, dict):
            # Recursively flatten nested dictionary
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            # Add leaf value
            items.append((new_key, v))
    
    return dict(items)


def unflatten_dict(
    d: Dict[str, Any],
    sep: str = ".",
) -> Dict[str, Any]:
    """
    Unflatten a dictionary with dot-separated keys.
    
    This is the inverse of flatten_dict.
    
    Args:
        d: Flattened dictionary
        sep: Separator used in keys
             Default: '.' (dot)
    
    Returns:
        Nested dictionary
    
    Example:
        >>> unflatten_dict({'a.b.c': 1})
        {'a': {'b': {'c': 1}}}
    """
    result = {}
    
    for key, value in d.items():
        # Split key by separator
        parts = key.split(sep)
        
        # Navigate/create nested structure
        current = result
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        # Set value at final key
        current[parts[-1]] = value
    
    return result


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # UUID
    "generate_uuid",
    "generate_uuid_v5",
    # Timestamp
    "get_timestamp",
    "parse_timestamp",
    # File
    "ensure_dir",
    "load_json",
    "save_json",
    # Serialization
    "serialize_to_json",
    "deserialize_from_json",
    # Dict utilities
    "flatten_dict",
    "unflatten_dict",
]
