# AvCheck Python Library

## Overview
A Python library to interact with the AvCheck API. This library provides methods to retrieve service information, get task data, and create new tasks.

## Installation
```sh
pip install avcheck
```

## Usage
```python
from avcheck import AvCheckClient, AvCheckException, InvalidInputException

api_key = "your_api_key"
client = AvCheckClient(api_key)

# Get service information
try:
    service_info = client.get_service_info()
    print(service_info)
except AvCheckException as e:
    print(f"Error: {e}")

# Get task data
try:
    task_data = client.get_task_data("task_id")
    print(task_data)
except InvalidInputException as e:
    print(f"Invalid Input: {e}")
except AvCheckException as e:
    print(f"Error: {e}")

# Create a new task
try:
    task_id = client.create_new_task(file_path="path/to/file")
    print(f"New task created with ID: {task_id}")
except InvalidInputException as e:
    print(f"Invalid Input: {e}")
except AvCheckException as e:
    print(f"Error: {e}")

# Get engines status
try:
    engines_status = client.get_engines_status(task_data)
    print(engines_status)
except AvCheckException as e:
    print(f"Error: {e}")

# Get file detection status
try:
    file_detection_status = client.get_file_detection_status(task_data, "file_name")
    print(file_detection_status)
except AvCheckException as e:
    print(f"Error: {e}")

# Check if a specific engine detected a threat
try:
    detected = client.did_engine_detect(task_data, "engine_name", "file_name")
    print(detected)
except AvCheckException as e:
    print(f"Error: {e}")

# Extract array from data
try:
    array_data = client.extract_array_from_data(task_data, "key")
    print(array_data)
except AvCheckException as e:
    print(f"Error: {e}")

# Get all engines
try:
    all_engines = client.get_all_engines(service_info)
    print(all_engines)
except AvCheckException as e:
    print(f"Error: {e}")

# Get engine by name
try:
    engine_details = client.get_engine_by_name(service_info, "avast")
    print(engine_details)
except AvCheckException as e:
    print(f"Error: {e}")

# Get engines by type
try:
    type_3_engines = client.get_engines_by_type(service_info, 3)
    print(type_3_engines)
except AvCheckException as e:
    print(f"Error: {e}")

# Check if an engine is available
try:
    is_available = client.is_engine_available(service_info, "avast")
    print(is_available)
except AvCheckException as e:
    print(f"Error: {e}")

# Get engine names
try:
    engine_names = client.get_engine_names(service_info)
    print(engine_names['shortname'])
    print(engine_names['longname'])
except AvCheckException as e:
    print(f"Error: {e}")
```

## License
MIT License
```