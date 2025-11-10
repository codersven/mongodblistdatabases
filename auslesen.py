import pymongo
import os.path
import os
import sys

# --- 1. Define Paths and Constants ---

# Path to the mongod executable, depending on the operating system
def get_mongoserver_path():
    if os.name == 'nt':
        # Typical path on Windows. Warning: Version-dependent!
        # A generic check is better here, but it's complex.
        # We'll stick to the Linux path for the function below.
        # For a realistic Windows check, one would have to search PATH.
        return None # We skip the path check on Windows in the function below
    else:
        # Typical path on Linux
        return "/usr/bin/mongod" 

# --- 2. Helper Function: Clear screen ---
def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

clear_screen()
print("--- MongoDB & PyMongo Systemcheck ---")

# --- 3. Function to check the MongoDB Server binary ---
def check_mongodb_binary():
    """Checks if the mongod command/binary exists at the Linux standard path."""
    
    # Since we don't know the exact path on Windows, we only check on POSIX (Linux/macOS)
    if os.name == 'posix':
        path = get_mongoserver_path()
        if os.path.exists(path):
            print("✅ MongoDB Server Binary (mongod) found.")
        else:
            print(f"❌ MongoDB Server Binary (mongod) NOT found at {path}.")
            print("   Please ensure that MongoDB Server is installed.")
    else:
        # On Windows / Mac, we assume it's in the PATH or already running.
        print("✅ MongoDB Server binary check skipped (OS is not Linux).")

# --- 4. Function to check the PyMongo package ---
def check_pymongo_module():
    """Checks if the PyMongo module is importable in Python."""
    try:
        # This import tests if the module exists in the Python path
        import pymongo
        print("✅ PyMongo module is installed and ready.")
    except ImportError:
        print("❌ PyMongo module NOT found.")
        print("   Please install it: pip install pymongo")
        # Exit the script, as the next function will fail
        sys.exit(1) 

# --- 5. Run functions and test connection ---

check_pymongo_module()
check_mongodb_binary()

print("\n--- Database Connection Test ---")
try:
    # Tries to establish a connection
    myclient = pymongo.MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
    
    # Tests the connection (if the server is running)
    myclient.admin.command('ping') 
    
    print("✅ Connection to MongoDB Server (localhost:27017) successful.")
    print("\nAvailable Databases:")
    for db in myclient.list_databases():
        print(f"- {db['name']}")

except pymongo.errors.ServerSelectionError as e:
    print("❌ Connection error:")
    print("   The MongoDB Server is NOT running at localhost:27017.")
    print("   Please start the server.")
    print(f"   Error details: {e}")
except Exception as e:
     print(f"An unexpected error occurred: {e}")

finally:
    print("\n--- Finished ---")