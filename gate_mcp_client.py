import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GateMCPClient:
    def __init__(self):
        self.api_url = os.getenv('GATE_MCP_API_URL', 'https://api.gatemcp.ai/mcp')
        self.session = requests.Session()
    
    def send_request(self, endpoint, method='POST', data=None, headers=None):
        """
        Send a request to the Gate MCP API
        """
        url = f"{self.api_url}{endpoint}"
        
        if headers is None:
            headers = {
                'Content-Type': 'application/json'
            }
        
        try:
            if method == 'POST':
                response = self.session.post(url, json=data, headers=headers)
            elif method == 'GET':
                response = self.session.get(url, headers=headers)
            elif method == 'PUT':
                response = self.session.put(url, json=data, headers=headers)
            elif method == 'DELETE':
                response = self.session.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sending request to Gate MCP: {e}")
            return None

# Example usage
if __name__ == "__main__":
    client = GateMCPClient()
    print(f"Gate MCP API URL: {client.api_url}")
    print("Gate MCP client initialized successfully!")
