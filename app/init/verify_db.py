from app.core.database import engine
from sqlalchemy import inspect

def verify_tables():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print("=== TABLAS ENCONTRADAS ===")
    for table in tables:
        print(f"\n📊 Tabla: {table}")
        columns = inspector.get_columns(table)
        for column in columns:
            print(f"  - {column['name']}: {column['type']} (Nullable: {column['nullable']})")
    
    if not tables:
        print("❌ No se encontraron tablas")
    else:
        print(f"\n✅ Se encontraron {len(tables)} tabla(s)")

if __name__ == '__main__':
    verify_tables()