from storm.locals import *
import storm.tracer
import storm.properties
import sys

class DB(object):
    def __init__(self):
        self._config = {
            'database': 'jugi',
            'schema': 'mysql',
            'user': 'jugiuser',
            'password': None,
            'host': 'localhost',
            'port': 3306,
        }
        self._connection = None
        self._store = None

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    @property
    def connection(self):
        if not self._connection:
            self._connection = create_database(self._buildurl())
        return self._connection

    @property
    def store(self):
        if not self._store:
            self._store = Store(self.connection)
        return self._store

    def enable_debug(self):
        storm.tracer.debug(True, stream=sys.stderr)

    def _buildurl(self):
        cfg = self.config.copy()
        cfg['credentials'] = cfg['user']
        if cfg['password']:
            cfg['credentials'] += ':' + cfg['password']
        return "%(schema)s://%(credentials)s@%(host)s:%(port)s/%(database)s" % cfg

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
            return Athlete()
        elif relation.lower() == 'section':
            return Section()
        elif relation.lower() == 'category':
            return Category()
        else:
            raise DBError("Relation %s not known" % relation)

class DBError(Exception): pass

CATEGORIES = {
    u'MJ': u'MJ',
    u'MA': u'MA',
    u'MB': u'MB',
    u'MC': u'MC',
    u'MD': u'MD',
    u'ME': u'ME',
    u'MF': u'MF',
    u'KJ': u'KJ',
    u'KA': u'KA',
    u'KB': u'KB',
    u'KC': u'KC',
    u'KD': u'KD',
    u'KE': u'KE',
    u'KF': u'KF',
}

CATEGORY_CODES = {
    u'J': u'J',
    u'A': u'A',
    u'B': u'B',
    u'C': u'C',
    u'D': u'D',
    u'E': u'E',
    u'F': u'F',
}

AWARDS = {
    u'GOLD': u'GOLD',
    u'SILVER': u'SILVER',
    u'BRONZE': u'BRONZE',
    u'AWARD': u'AWARD',
}

SEXES = {
    u'f': u'f', # feminim
    u'm': u'm', # masculin
}

class Section(object):
    __storm_table__ = 'Section'
    id_section = Int(primary=True)
    name = Unicode()
    canton = Unicode()

class Category(object):
    __storm_table__ = 'Category'
    category = Enum(map=CATEGORIES, primary=True)
    sex = Enum(map=SEXES)

class AgeCategory(object):
    __storm_table__ = 'AgeCategory'
    __storm_primary__ = ('age_cohort', 'sex')
    age_cohort = Enum(map=CATEGORIES)
    sex = Enum(map=SEXES)
    category = Enum(map=CATEGORIES)
    age = Int()

class Athlete(object):
    __storm_table__ = 'Athlete'
    id_athlete = Int(primary=True)
    number = Int()
    firstname = Unicode()
    lastname = Unicode()
    section = Int()
    year_of_birth = Int()
    sex = Enum(map=SEXES)
    category = Enum(map=CATEGORIES)
    sprint_result = Decimal()
    longjump_result = Decimal()
    highjump_result = Decimal()
    shotput_result = Decimal()
    ball_result = Decimal()
    sprint_points = Int()
    longjump_points = Int()
    highjump_points = Int()
    shotput_points = Int()
    ball_points = Int()
    total_points = Int()
    rank = Int()
    award = Unicode()
    qualify = Bool()
    verified = Bool()
    r_section = Reference(section, Section.id_section)
    r_category = Reference(category, Category.category)
    r_age_category = ReferenceSet(
        year_of_birth,
        AgeCategory.age_cohort,
        AgeCategory.sex,
        sex
    )

    def __init__(self, **kwargs):
        for name, value in kwargs.iteritems():
            attribute = getattr(self, name)
            if isinstance(attribute, storm.properties.PropertyColumn):
                raise Exception('Invalid constructor argument {0}'.format(name))
            setattr(self, name, value)

def get_relation_fields(storm_object):
    return filter(
        lambda x: isinstance(
            getattr(storm_object, x), storm.properties.PropertyColumn
        ),
        dir(storm_object)
    )

