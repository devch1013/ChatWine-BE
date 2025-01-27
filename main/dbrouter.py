class MultiDBRouter(object):
    def __init__(self):
        self.model_list = ['default', 'mysql_db']

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'mysql_db':
            return 'mysql_db'

        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'mysql_db':
            return 'mysql_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'mysql_db' or \
           obj2._meta.app_label == 'mysql_db':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'mysql_db':
            return db == 'mysql_db'
        if app_label == 'default':
            return db == 'default'
        return None