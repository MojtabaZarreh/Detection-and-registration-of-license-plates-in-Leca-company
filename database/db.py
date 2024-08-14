import pymssql
from dotenv import load_dotenv
import os

class SaveDB:
    def __init__(self):
        load_dotenv() 
        self.conn = pymssql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'))

    def insert(self, Date, PlateFull, PlateNo, WeighBridgeName='انتظامات', IOType='خروج', CreateUserName='m.zarreh', CreateDateTime=''):
        try:
            with self.conn.cursor() as cursor:
                insert_query = '''
                INSERT INTO PlateReadIO (Date, PlateFull, PlateNo, WeighBridgeName, IOType, CreateUserName, CreateDateTime)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                '''
                val = (Date, PlateFull, PlateNo, WeighBridgeName, IOType, CreateUserName, CreateDateTime)
                cursor.execute(insert_query, val)
                self.conn.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.conn.close()
            
    def get_status(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute('''SELECT status FROM PlateReadIOStatus WHERE id = 1''')
                status = cursor.fetchone()[0]
                self.conn.commit()
                return status
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.conn.close()
            
    def update_status(self, new_status):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute('''UPDATE PlateReadIOStatus SET status = %s WHERE id = 1''', (new_status,))
                self.conn.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.conn.close()
            
    def delete_all(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute('''DELETE FROM PlateReadIO WHERE id<1000''')
                self.conn.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.conn.close()
            
    def delete_one(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute('''DELETE FROM PlateReadIO WHERE PlateNo = 'د6766' ''')
                self.conn.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.conn.close()         

# SaveDB().insert(Date='1403/02/21', PlateFull='48ل914-99', PlateNo='46969', CreateDateTime='1403/02/20-10:30:30')
# The `SaveDB().delete_all()` method is deleting all records from the `PlateReadIO` table where the
# `id` is less than 1000. This method is used to clear out a subset of data from the table based on
# the specified condition.
# SaveDB().delete_one()
# SaveDB().delete_all()
# print(SaveDB().get_status())


        
        
    
