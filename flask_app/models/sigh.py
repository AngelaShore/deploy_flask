from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Sigh:
    db_name = 'sas'
    def __init__( self , data ):
        self.id = data['id']
        self.location = data['location']
        self.whatHappened = data['whatHappened']
        self.date_of_setting = data['date_of_setting']
        self.of_sasquatches = data['of_sasquatches']
        self.user_id = data['user_id']



    @classmethod
    def create(cls, data):
        query = 'INSERT INTO sighs (location, whatHappened, date_of_setting, of_sasquatches, user_id) VALUES  ( %(location)s, %(whatHappened)s, %(date_of_setting)s, %(of_sasquatches)s, %(user_id)s);'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def getAllSighs(cls):
        query = "SELECT * FROM sighs;"
        results = connectToMySQL(cls.db_name).query_db(query)
        sighs = []
        if results:
            for sigh in results:
                sighs.append(sigh)
        return sighs
    
    @classmethod
    def get_logged_sighs(cls,data):
        query = "SELECT * FROM sighs where user_id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        sighs = []
        if results:
            for sigh in results:
                sighs.append(sigh)
        return sighs
    

    
    
    @classmethod
    def get_sigh_by_id(cls, data):
        query = "SELECT * FROM sighs left join users on sighs.user_id = users.id where sighs.id = %(sigh_id)s;"
        results =  connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    
    @classmethod
    def delete_sigh(cls, data):
        query = "DELETE FROM sighs WHERE id= %(sigh_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    

    @classmethod
    def update_sigh(cls, data):
        query = "UPDATE sighs SET location = %(location)s, whatHappened = %(whatHappened)s, date_of_setting = %(date_of_setting)s, of_sasquatches = %(of_sasquatches)s, WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def delete_users_sigh(cls, data):
        query = "delete from sighs where sighs.user_id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def addSkeptic(cls,data):
        query = "INSERT INTO skeptics (user_id, sigh_id) VALUES (%(id)s, %(sigh_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def believeIt(cls,data):
        query = "DELETE FROM skeptics where sigh_id = %(sigh_id)s and user_id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    
    @classmethod
    def get_skeptics(cls, data):
        query = "SELECT user_id from skeptics where skeptics.sigh_id = %(sigh_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        skeptics = []
        if results:
            for person in results:
                skeptics.append(person['user_id'])
        return skeptics
    
    @classmethod
    def get_skeptics_info(cls, data):
        query = "SELECT * from skeptics left join users on skeptics.user_id = users.id where skeptics.sigh_id = %(sigh_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        skeptics = []
        if results:
            for person in results:
                skeptics.append(person)
        return skeptics



    @classmethod
    def delete_all_skeptics(cls,data):
        query = "DELETE FROM skeptics where sigh_id = %(sigh_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_sigh(data):
        is_valid = True
        # test whether a field matches the pattern
        if len(data['location']) < 3:
            flash("The location is required!", 'location')
            is_valid = False
        if len(data['whatHappened']) < 3:
            flash("The whatHappened is required!", 'whatHappened')
            is_valid = False
        if not data['date_of_setting']:
            flash("The date of setting is required!", 'date_of_setting')
            is_valid = False
        if 'of_sasquatches' in data:
            if int(data['of_sasquatches'])>=1:
                flash("Of sasquatches is required to be min 1!", 'of_sasquatches')
                is_valid = False
            return is_valid
    

       
