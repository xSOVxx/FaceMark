import sys
import os
sys.path.append(os.getcwd())
try:
    import sqlalchemy
    print("SQLAlchemy installed")
    import pymysql
    print("PyMySQL installed")
    from database import engine
    print("Database module imported")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
