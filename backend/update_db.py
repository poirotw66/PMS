from app.database import engine
from sqlalchemy.sql import text

def update_db_schema():
    with engine.connect() as conn:
        try:
            # 添加 property_assets 表的 current_status 欄位
            conn.execute(text("""
            ALTER TABLE property_assets 
            ADD COLUMN IF NOT EXISTS current_status VARCHAR(255) DEFAULT '良好'
            """))

            # 添加 repair_requests 表的缺少欄位
            conn.execute(text("""
            ALTER TABLE repair_requests 
            ADD COLUMN IF NOT EXISTS repair_vendor VARCHAR(255),
            ADD COLUMN IF NOT EXISTS repair_cost VARCHAR(255),
            ADD COLUMN IF NOT EXISTS cost_bearer VARCHAR(255),
            ADD COLUMN IF NOT EXISTS remarks VARCHAR(255)
            """))
            
            conn.commit()
            print('數據庫結構更新成功！')
        except Exception as e:
            print(f'錯誤: {e}')

if __name__ == "__main__":
    update_db_schema()
