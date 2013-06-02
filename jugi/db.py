import mysql.connector

class DB(object):
    def __init__(self):
        self._config = {
            'user':'jugiuser',
            'database': 'jugi'
        }
        self._connection = None

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    @property
    def connection(self):
        if not self._connection:
            self._connection = mysql.connector.connect(**self.config)
        return self._connection

    def create_cursor(self):
        return self.connection.cursor()

    def commit(self):
        if self._connection:
            self._connection.commit()

    def close(self):
        if self._connection:
            self.commit()
            self._connection.close()
            self._connection = None

    def create(self, relation):
        """ Factory for relation objects """
        if relation.lower() == 'athlete':
            return Athlete(self)
        elif relation.lower() == 'section':
            return Section(self)
        else:
            raise DBError("Relation %s not known" % relation)

class DBError(Exception):
    pass

class DBObjectBase(dict):
    def __init__(self, db, **kwargs):
        self._db = db
        for k, v in kwargs.iteritems():
            self[k] = v

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, super(DBObjectBase, self).__repr__())

    @property
    def db(self):
        return self._db

    @property
    def name(self):
        return self.NAME

    @property
    def id_field(self):
        return self.ID_FIELD

    @property
    def fields(self):
        return self.FIELDS

    def _encode(self, v):
        if isinstance(v, unicode):
            return v.encode('utf-8')
        else:
            return v

    def _decode(self, v):
        if isinstance(v, str):
            return v.decode('utf-8')
        else:
            return v

    def sql_fetch_where(self, where=None):
        fields = ', '.join(["`%s`" % n for n in self.fields])
        sql = 'SELECT %s FROM `%s`' % (fields, self.name)
        if where:
            sql += ' WHERE %s' % where
        return sql

    def sql_insert(self, fields=None):
        if fields:
            field_list = filter(lambda x: x in fields, self.fields)
        else:
            field_list = self.fields
        fields_sql = ["`%s`" % n for n in field_list]
        values_sql = ["%s" for n in field_list]
        sql = 'INSERT INTO `%s` (%s) VALUES (%s)' % (
            self.name,
            ', '.join(fields_sql),
            ', '.join(values_sql))
        return sql

    def sql_update(self, where, fields=None):
        if fields:
            update_fields = filter(lambda x: x in fields, self.fields)
        else:
            update_fields = self.fields
        sql_fields = ', '.join(["%s = %%s" % n for n in update_fields])
        sql = 'UPDATE `%s` SET (%s)' % (self.name, sql_fields)
        if where:
            sql += ' WHERE %s' % where

    def fetch_id(self, itemid):
        sql = self.sql_fetch_where('%s = %%s' % self.id_field)
        cursor = self.db.create_cursor()
        try:
            cursor.execute(sql, itemid)
            item = cursor.next()
            for k, v in zip(self.fields, item):
                self[k] = self._decode(v)
        finally:
            cursor.close()

    def fetch_all(self):
        sql = self.sql_fetch_where()
        cursor = self.db.create_cursor()
        try:
            cursor.execute(sql)
            for item in cursor:
                values = {}
                for k, v in zip(self.fields, item):
                    values[k] = v
                yield self.__class__(self.db, **values)
        finally:
            cursor.close()

    def insert(self, fields=None):
        if fields:
            field_list = filter(lambda x: x in fields, self.fields)
        else:
            field_list = self.fields
        values = [(self._encode(self[f]) if self.has_key(f) else None) for f in field_list]
        sql = self.sql_insert(fields)
        print repr(sql)
        print repr(values)
        c = self.db.create_cursor()
        try:
            c.execute(sql, values)
        finally:
            c.close()

    def update(self, fields=None):
        where = '%s = %%s' % self.id_field
        if fields:
            update_fields = filter(lambda x: x in fields), 
            sql = self.sql_update(where, update_fields), 
        else:
            update_fields = self.fields
            sql = self.sql_update(where), 
        values = [self._encode(self[f]) for f in update_fields]

        c = self.db.create_cursor()
        try:
            c.execute(sql, values)
        finally:
            c.close()
            

class Athlete(DBObjectBase):
    NAME = 'Athlete'
    ID_FIELD = 'id_athlete'
    FIELDS = (
        'id_athlete',
        'number',
        'firstname',
        'lastname',
        'section',
        'year_of_birth',
        'sex',
        'category',
        'category_code',
        'sprint_result',
        'longjump_result',
        'highjump_result',
        'shotput_result',
        'ball_result',
        'sprint_points',
        'longjump_points',
        'highjump_points',
        'ball_points',
        'total_points',
        'award',
        'qualify',
    )
    def __init__(self, db, **kwargs):
        super(Athlete, self).__init__(db, **kwargs)

class Section(DBObjectBase):
    NAME = 'Section'
    ID_FIELD = 'id_section'
    FIELDS = (
        'id_section',
        'name',
        'canton',
    )
    def __init__(self, db, **kwargs):
        super(Section, self).__init__(db, **kwargs)

