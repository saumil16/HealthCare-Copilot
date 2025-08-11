# HealthCare-Copilot

## Setup & Run Instructions

### 1. Prerequisites
- Python 3.x installed
- MongoDB up and running (local or remote)
- Access to an OpenAI API key

---

### 2. Clone the Repository
```bash
git clone https://github.com/saumil16/HealthCare-Copilot.git
cd HealthCare-Copilot
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create a .env File
In the project root, create a file named .env and define your environment variables like this:
```bash
dbName=""
collectionName=""
mongo_url=""
OPENAI_API_KEY=""
```
Replace the empty strings with your actual values:
- dbName: Name of the MongoDB database to use
- collectionName: Target collection name for storing PDFs
- mongo_url: Your MongoDB connection URL
- OPENAI_API_KEY: Your OpenAI API key

  
### 5. Load Data (PDFs to MongoDB)
Run the data importer to process PDFs and store them in MongoDB:
```bash
python data_loader.py
```
This script reads the PDFs (from the dataset/ folder) and inserts them into your specified MongoDB collection.

### 6. Run the Main Application
Once data loading is complete, start the main application:
```bash
python main.py
```
