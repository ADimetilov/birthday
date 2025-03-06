import psycopg2

class Database:
    def __init__(self):
        conn = psycopg2.connect(dbname = "birthday",user = "postgres", password = "123qweR%", host = "localhost", port = "5432")
        self.cursor = conn.cursor()
    
    def language(self,user_id:int,lang:str):
        try:
            self.cursor.execute(f'''BEGIN TRANSACTION;
                                    UPDATE public."setting" Set "language" = '{lang}' where "user_id"='{user_id}';
                                    COMMIT;''')
            return True
        except Exception as error:
            print(error)
            self.cursor.execute("ROLLBACK")
            return False

    def get_language(self,user_id):
        try:
            self.cursor.execute(f'''BEGIN TRANSACTION;
                                    SELECT "language" from public."setting" where "user_id"='{user_id}';''')
            return str(self.cursor.fetchone()[0]).strip()
        except Exception as error:
            print(error)
            self.cursor.execute("ROLLBACK")
            return False

    def user(self,user_id:int,chat_id:int):
        try:
            self.cursor.execute(f'''BEGIN TRANSACTION;
                                SELECT "id" FROM public."user" WHERE "id" = '{user_id}';''')
            check = self.cursor.fetchone()
            if check:
                return True
            else:
                self.cursor.execute(f'''BEGIN TRANSACTION;
                                    INSERT INTO public."user"("id","chat_id") VALUES('{user_id}','{chat_id}');
                                    INSERT INTO public."setting" ("user_id","language","interactive") VALUES('{user_id}','Ru','True');
                                    COMMIT;''')
                return True
        except Exception as error:
            print(error)
            self.cursor.execute("ROLLBACK;")
            return False
    
    def check_notifi(self,user_id:int)->bool:
        try:
            self.cursor.execute(f'''BEGIN TRANSACTION;
                                SELECT "interactive" from public."setting" where "user_id"='{user_id}';''')
            return self.cursor.fetchone()[0]
        except Exception as error:
            print(error)
            self.cursor.execute("ROLLBACK;")

    def notifi_on(self,user_id:int)->bool:
        try:
            self.cursor.execute(f'''BEGIN TRANSACTION;
                                    UPDATE public."setting" Set "interactive" = '{True}' where "user_id"='{user_id}';
                                    COMMIT;''')
            return True
        except Exception as error:
            print(error)
            self.cursor.execute("ROLLBACK")
            return False

    def notifi_off(self,user_id:int)->bool:
        try:
            self.cursor.execute(f'''BEGIN TRANSACTION;
                                    UPDATE public."setting" Set "interactive" = '{False}' where "user_id"='{user_id}';
                                    COMMIT;''')
            return True
        except Exception as error:
            print(error)
            self.cursor.execute("ROLLBACK")
            return False

    def delete_birthday(self,id:int):
        try:
            self.cursor.execute(f'''BEGIN TRANSACTION;
                                DELETE FROM public."birthdays" where "id" = '{id}';
                                COMMIT;''')
            return True
        except Exception as error:
            print(error)
            self.cursor.execute("ROLLBACK;")
            return False

    def get_all_users(self):
        try:
            self.cursor.execute('''BEGIN TRANSACTION;
                                SELECT "id" from public."user";''')
            user_list = self.cursor.fetchall()
            return user_list
        except Exception as error:
            print(error)
            self.cursor.execute("ROLLBACK;")
            return False


    def get_all_birthdays(self,user_id:int):
        try:
            self.cursor.execute(f'''BEGIN TRANSACTION;
                                SELECT * from public."birthdays" WHERE "user_id" = '{user_id}';''')
            birthdays = self.cursor.fetchall()
            return birthdays
        except Exception as error:
            print(error)
            self.cursor.execute("ROLLBACK;")
            return False

    def insert_birthday(self,user_id:int,data:dict):
        try:
            name = data['Name'] 
            date = str(data['Day'])+"."+str(data['Month'])
            self.cursor.execute(f'''BEGIN TRANSACTION;
                                INSERT INTO public."birthdays" ("user_id","day","name") VALUES ('{user_id}','{date}','{name}');
                                COMMIT;''')
            return True
        except Exception as error:
            print(error)
            self.cursor.execute("ROLLBACK;")
            return False