# -*- coding: utf-8 -*-
# Copyright © 2013 Andreas Stricker <andy@knitter.ch>
# 
# This file is part of Athrank.
# 
# Athrank is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from storm.locals import *
import storm.tracer
import storm.properties
import json
import sys
import errno

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
        self._init_config()


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

    def _init_config(self):
        try:
            with file('config.json', 'r') as f:
                fcfg = json.load(f)
                self._config.update(fcfg)
        except IOError as e:
            if e.errno != errno.ENOENT:
                raise

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

CATEGORIES = {'U8', 'U10', 'U12', 'U14', 'U16', 'U18', 'U20'}
AWARDS = {'GOLD', 'SILVER', 'BRONZE', 'AWARD'}
SEXES = {'female', 'male'}

class Section(object):
    __storm_table__ = 'section'
    id_section = Int(primary=True)
    name = Unicode()
    canton = Unicode()

class Sexes(object):
    __storm_table__ = 'sexes'
    sex = Unicode(primary=True)

class Categories(object):
    __storm_table__ = 'categories'
    category = Unicode(primary=True)

class Awards(object):
    __storm_table__ = 'awards'
    award = Unicode(primary=True)

class Category(object):
    __storm_table__ = 'category'
    __storm_primary__ = ('category', 'sex')
    category = Enum(map=dict((x, x) for x in CATEGORIES))
    sex = Unicode()
    sprint_distance = Int()
    has_longjump = Bool()
    has_highjump = Bool()
    has_shotput = Bool()
    has_ball = Bool()
    has_endurance_run = Bool()
    r_category = Reference(category, Categories.category)
    r_sex = Reference(sex, Sexes.sex)

class AgeCategory(object):
    __storm_table__ = 'agecategory'
    __storm_primary__ = ('age_cohort', 'sex')
    age_cohort = Int()
    sex = Unicode()
    category = Unicode()
    age = Int()
    r_category = ReferenceSet((category, sex), (Category.category, Category.sex))
    r_sex = Reference(sex, Sexes.sex)
    r_category = Reference(category, Categories.category)

class Athlete(object):
    __storm_table__ = 'athlete'
    id_athlete = Int(primary=True)
    number = Int()
    firstname = Unicode()
    lastname = Unicode()
    id_section = Int()
    age_cohort = Int()
    sex = Unicode()
    category = Unicode()
    sprint_result = Decimal()
    longjump_result = Decimal()
    highjump_result = Decimal()
    shotput_result = Decimal()
    ball_result = Decimal()
    endurance_run_result = Decimal()
    sprint_points = Int()
    longjump_points = Int()
    highjump_points = Int()
    shotput_points = Int()
    ball_points = Int()
    endurance_run_points = Int()
    total_points = Int()
    rank = Int()
    award = Unicode()
    qualified = Bool()
    verified = Bool()
    r_section = Reference(id_section, Section.id_section)
    r_category_sex = Reference((category, sex), (Category.category, Category.sex))
    r_age_cohort_sex = Reference((age_cohort, sex), (AgeCategory.age_cohort, AgeCategory.sex))
    r_category = Reference(category, Categories.category)
    r_sex = Reference(sex, Sexes.sex)
    r_award = Reference(award, Awards.award)

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

