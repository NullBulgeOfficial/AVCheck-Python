import requests
from .exceptions import (
    AvCheckException,
    ApiKeyMissingException,
    InvalidResponseException,
    InvalidInputException,
    TaskNotFoundException,
    EngineNotFoundException
)

class AvCheckClient:
    def __init__(self, api_key, base_url="http://avcheck.net/vhm/api/v1"):
        if not api_key:
            raise ApiKeyMissingException()
        self.api_key = api_key
        self.base_url = base_url

    def _post_request(self, endpoint, data=None, files=None):
        url = f"{self.base_url}/{endpoint}"
        data = data or {}
        data['apikey'] = self.api_key

        try:
            response = requests.post(url, data=data, files=files)
            response.raise_for_status()
        except requests.RequestException as e:
            raise AvCheckException(f"Request failed: {e}")
        
        if response.status_code != 200:
            raise InvalidResponseException(response.status_code, response.text)
        
        return response.json()

    def get_service_info(self):
        response = self._post_request('service/get/')
        return self._process_service_info(response)

    def get_task_data(self, task_id, crc=None):
        if not task_id:
            raise InvalidInputException("Task ID is required")
            
        endpoint = f"check/get/{task_id}/"
        if crc:
            endpoint += f"{crc}/"
        response = self._post_request(endpoint)
        if response['status'] == 404:
            raise TaskNotFoundException(task_id)
        return self._process_task_data(response)

    def create_new_task(self, task_type="file", file_path=None, url=None, engines=None, response_type="on_close"):
        if task_type not in ["file", "domain"]:
            raise InvalidInputException("Invalid task type. Must be 'file' or 'domain'")
        if task_type == "file" and not file_path:
            raise InvalidInputException("File path is required for 'file' task type")
        if task_type == "domain" and not url:
            raise InvalidInputException("URL is required for 'domain' task type")

        data = {
            'task_type': task_type,
            'response_type': response_type
        }
        files = None
        if file_path:
            files = {'file': open(file_path, 'rb')}
        if url:
            data['url'] = url
        if engines:
            data['engines'] = engines

        response = self._post_request('check/new/', data, files)
        return self._process_new_task(response)

    def _process_service_info(self, response):
        # Custom processing logic for service info
        if response['status'] != 1:
            raise InvalidResponseException(response['status'], response['status_t'])
        return response['data']['engines']

    def _process_task_data(self, response):
        # Custom processing logic for task data
        if response['status'] not in [1, 206]:
            raise InvalidResponseException(response['status'], response['status_t'])
        return response['data']

    def _process_new_task(self, response):
        # Custom processing logic for new task
        if response['status'] != 1:
            raise InvalidResponseException(response['status'], response['status_t'])
        return response['data']['task_id']

    # New Methods for Detailed Processing
    def get_engines_status(self, task_data):
        """Extract the status of each engine from task data."""
        if 'results' not in task_data:
            raise AvCheckException("Invalid task data: 'results' key not found")
        
        engines_status = {}
        for engine, data in task_data['results'].items():
            engines_status[engine] = data['status']
        return engines_status

    def get_file_detection_status(self, task_data, file_name):
        """Get detection status for a specific file across all engines."""
        if 'results' not in task_data:
            raise AvCheckException("Invalid task data: 'results' key not found")
        
        file_detection_status = {}
        for engine, data in task_data['results'].items():
            if 'objects' in data and file_name in data['objects']:
                file_detection_status[engine] = {
                    'fast_detect': data['objects'][file_name].get('fast_detect', 0),
                    'slow_detect': data['objects'][file_name].get('slow_detect', 0),
                    'detect_name': data['objects'][file_name].get('detect_name', "")
                }
        return file_detection_status

    def did_engine_detect(self, task_data, engine_name, file_name):
        """Check if a specific engine detected a threat in a specific file."""
        if 'results' not in task_data or engine_name not in task_data['results']:
            raise AvCheckException(f"Invalid task data: 'results' or '{engine_name}' key not found")
        
        engine_data = task_data['results'][engine_name]
        if 'objects' in engine_data and file_name in engine_data['objects']:
            return engine_data['objects'][file_name].get('fast_detect', 0) == 1 or engine_data['objects'][file_name].get('slow_detect', 0) == 1
        return False

    def extract_array_from_data(self, task_data, key):
        """Extract an array from the task data using a specific key."""
        if key not in task_data:
            raise AvCheckException(f"Invalid task data: '{key}' key not found")
        return task_data[key]

    # New Methods for Service Info
    def get_all_engines(self, service_info):
        """Get a list of all engines."""
        return list(service_info.values())

    def get_engine_by_name(self, service_info, engine_name):
        """Get details of an engine by its short name."""
        for engine in service_info.values():
            if engine['short_name'] == engine_name:
                return engine
        raise EngineNotFoundException(engine_name)

    def get_engines_by_type(self, service_info, engine_type):
        """Get a list of engines by their type."""
        return [engine for engine in service_info.values() if engine['type'] == engine_type]

    def is_engine_available(self, service_info, engine_name):
        """Check if a specific engine is available."""
        engine = self.get_engine_by_name(service_info, engine_name)
        return engine['status'] == 1

    def get_engine_names(self, service_info):
        """Get lists of short names and long names of engines."""
        short_names = [engine['short_name'] for engine in service_info.values()]
        long_names = [engine['full_name'] for engine in service_info.values()]
        return {'shortname': short_names, 'longname': long_names}

    # New Method for Detection Check
    def is_detected(self, task_data, total_detections):
        """Check if the total number of detections across all engines is above a given value."""
        if 'results' not in task_data:
            raise AvCheckException("Invalid task data: 'results' key not found")
        
        detection_count = 0
        for engine, data in task_data['results'].items():
            for obj in data['objects'].values():
                if obj.get('fast_detect', 0) == 1 or obj.get('slow_detect', 0) == 1:
                    detection_count += 1
        
        return detection_count > total_detections