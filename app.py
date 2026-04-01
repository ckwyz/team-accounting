import streamlit as st
from gate_mcp_client import GateMCPClient
import json

# Set page configuration
st.set_page_config(
    page_title="Gate MCP Client",
    page_icon="🔗",
    layout="wide"
)

# Initialize the Gate MCP client
client = GateMCPClient()

# Page header
st.title("Gate MCP Client UI")

# API Configuration section
st.sidebar.header("API Configuration")
st.sidebar.write(f"Current API URL: {client.api_url}")

# Main content
col1, col2 = st.columns(2)

with col1:
    st.header("Request Settings")
    
    # Endpoint input
    endpoint = st.text_input("API Endpoint", value="/", help="Enter the API endpoint path")
    
    # HTTP method selection
    method = st.selectbox("HTTP Method", ["POST", "GET", "PUT", "DELETE"])
    
    # Request data input
    data_input = st.text_area(
        "Request Data (JSON)",
        value="{\n  \"key\": \"value\"\n}",
        help="Enter JSON data for POST, PUT requests"
    )
    
    # Send button
    send_button = st.button("Send Request")

with col2:
    st.header("Response")
    response_placeholder = st.empty()

# Handle request when send button is clicked
if send_button:
    try:
        # Parse JSON data if provided
        data = None
        if data_input and method in ["POST", "PUT"]:
            data = json.loads(data_input)
        
        # Send request
        response = client.send_request(
            endpoint=endpoint,
            method=method,
            data=data
        )
        
        # Display response
        if response:
            response_placeholder.json(response)
        else:
            response_placeholder.error("No response received from the API")
    except json.JSONDecodeError:
        response_placeholder.error("Invalid JSON format in request data")
    except Exception as e:
        response_placeholder.error(f"Error: {str(e)}")

# Example usage section
st.header("Example Usage")
st.markdown("""
### How to use this UI:
1. Enter the API endpoint you want to call (e.g., `/v1/chat/completions`)
2. Select the appropriate HTTP method
3. Enter JSON data for POST or PUT requests
4. Click "Send Request" to make the API call
5. View the response in the Response section

### Example Endpoints:
- `/v1/chat/completions` - For chat completions
- `/v1/models` - To list available models
- `/v1/embeddings` - For text embeddings
""")
