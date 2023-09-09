class Mydb2Router:
    def db_for_read(model, **hints):
        if model._meta.app_label == 'chat':
            return 'mydb2'
        return None

    def db_for_write(model, **hints):
        if model._meta.app_label == 'chat':
            return 'mydb2'
        return None

    def allow_relation(obj1, obj2, **hints):
        if obj1._meta.app_label == 'chat' or \
           obj2._meta.app_label == 'chat':
           return True
        return None

    def allow_migrate(db, app_label, model_name=None, **hints):
        if app_label == 'chat':
            return db == 'mydb2'
        elif db == 'mydb2':
            return False
        return None