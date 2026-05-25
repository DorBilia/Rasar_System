import json
from main import app  # Import your FastAPI app instance

with open("openapi.json", "w") as f:
    json.dump(app.openapi(), f, indent=4)
