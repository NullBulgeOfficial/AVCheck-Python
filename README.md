# AvCheck Python Library

## Overview
A Python library to interact with the AvCheck API. This library provides methods to retrieve service information, get task data, and create new tasks.

## Installation
```sh
pip install avcheck
```

## Usage
```python
from avcheck import AvCheckClient, AvCheckException

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
except AvCheckException as e:
    print(f"Error: {e}")

# Create a new task
try:
    task_id = client.create_new_task(file_path="path/to/file")
    print(f"New task created with ID: {task_id}")
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
```

## License
MIT License
```

The `README.md` file is updated to include documentation for the new methods.

### Final Step
Compile the package into a `.whl` file for distribution.

Run the following command to build the wheel file:
```sh
python setup.py bdist_wheel
```