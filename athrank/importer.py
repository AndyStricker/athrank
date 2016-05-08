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

import csv
import codecs
import decimal
import athrank.db

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class RFC4180:
    delimiter = ','
    quotechar = '"'
    doublequote = True
    escapechar = None
    skipinitialspace = False
    lineterminator = '\n'
    quoting = csv.QUOTE_MINIMAL

class CSVImporter(object):
    """
    CSV import base class

    Setup field lookup table and queries db to build section
    lookup table
    """
    def __init__(self, db):
        self._db = db
        self._sections = None
        self._fields = None

    @property
    def db(self):
        return self._db

    @property
    def sections(self):
        if not self._sections:
            self._sections = self._create_section_lookup_table()
        return self._sections

    @property
    def fields(self):
        if not self._fields:
            self._fields = self._create_fields_lookup_table()
        return self._fields

    def _create_section_lookup_table(self):
        table = {}
        for section in self.db.store.find(athrank.db.Section):
            table[section.name] = section.id_section
        return table

    def _section_to_id(self, name):
        return self.sections[name]

    def _create_fields_lookup_table(self):
        table = {}
        for idx, field in enumerate(self.HEADER):
            table[field] = idx
        return table

    def _check_header(self, header):
        for n in xrange(0, self.CHECK_HEADER_MAX):
            expected = self.HEADER[n]
            value = header[n]
            if expected != value:
                raise Exception('Expected header field %d is "%s" but got "%s"' % (n, expected, value))
    def _category_from_age_and_sex(self, age_cohort, sex):
        AgeCategory = athrank.db.AgeCategory
        print 'XXX {!r} {!r}'.format(age_cohort, sex)
        age_category = self.db.store.find(AgeCategory,
            (AgeCategory.age_cohort == age_cohort) & (AgeCategory.sex == sex)).one()
        if age_category is None:
            print "XXX category not found {} {}".format(age_cohort, sex)
            return None
        return age_category.category


class CSVAthleteImporter(CSVImporter):
    """
    Importer for batch import of athletes from CSV file.
    """
    CHECK_HEADER_MAX = 6
    HEADER = (
        u"Sektion",
        u"Name",
        u"Vorname",
        u"Jahrgang",
        u"G",
        u"Kategorie",
        u"Poulet",
        u"k1",
        u"k2"
    )
    IMPORT_FIELDS = {
        u"Sektion": 'section',
        u"Name": 'lastname',
        u"Vorname": 'firstname',
        u"Jahrgang": 'age_cohort',
        u"G": 'sex',
        u"Kategorie": 'category',
    }

    def __init__(self, db, add_to_year=0):
        super(CSVAthleteImporter, self).__init__(db)
        self._add_to_year = add_to_year

    def read(self, filename):
        reader = UnicodeReader(open(filename, 'rb'), RFC4180)
        header = reader.next()
        self._check_header(header)
        n = 0
        for record in reader:
            self._insert(record)
            n += 1
        self.db.store.commit()
        return n

    def _insert(self, record):
        data = self.record_to_dict(record)
        athlete = self.db.create('athlete')

        athlete.firstname = data['firstname']
        athlete.lastname = data['lastname']
        athlete.age_cohort = int(data['age_cohort']) + self._add_to_year
        athlete.sex = self._convert_sex(data['sex'])
        athlete.id_section = self._section_to_id(data['section'])
        athlete.category = self._category_from_age_and_sex(athlete.age_cohort, athlete.sex)

        self.db.store.add(athlete)

    def _get_record_field(self, record, name):
        return record[self.fields[name]]

    def _convert_sex(self, v):
        return {'k':'male', 'm': 'female'}[v.lower()].decode('utf-8')

    def record_to_dict(self, record):
        d = {}
        for csvfield, fieldname in self.IMPORT_FIELDS.iteritems():
            d[fieldname] = record[self.fields[csvfield]]
        return d

class CSVJuweImporter(CSVImporter):
    """
    Importer for juwe exports stored as CSV.

    This is basically to import complete data set from old
    ranking lists to rerun and verify the new ranking algorithms.
    """
    CHECK_HEADER_MAX = 30
    HEADER = (
        u"StartNummer",
        u"Name",
        u"Sektion",
        u"Jahrgang",
        u"Gruppe",
        u"Alter",
        u"Geschlecht",
        u"Kategorie",
        u"KatCode",
        u"KatText",
        u"SprintResultat",
        u"SprintPunkte",
        u"WeitResultat",
        u"WeitPunkte",
        u"HochResultat",
        u"HochPunkte",
        u"KugelResultat",
        u"KugelPunkte",
        u"BallResultat",
        u"BallPunkte",
        u"DauerlaufResultat",
        u"Laufzeit",
        u"DauerlaufPunkte",
        u"TotalPunkte",
        u"SpezPunkte",
        u"Auszeichnung",
        u"Qualifikation",
        u"Loschen",
        u"Rang",
        u"Eingabe OK",
        u"Zahl",
    )
    IMPORT_FIELDS = {
        u"StartNummer": 'number',
        u"Name": 'name',
        u"Sektion": 'section',
        u"Jahrgang": 'age_cohort',
        u"Geschlecht": 'sex',
        u"Kategorie": 'category',
        u"SprintResultat": 'sprint_result',
        u"WeitResultat": 'longjump_result',
        u"HochResultat": 'highjump_result',
        u"KugelResultat": 'shotput_result',
        u"BallResultat": 'ball_result',
    }
    CATEGORIES = {
        'MJ': 'U20', 'KJ': 'U20',
        'MA': 'U18', 'KA': 'U18',
        'MB': 'U16', 'KB': 'U16',
        'MC': 'U14', 'KC': 'U14',
        'MD': 'U12', 'KD': 'U12',
        'ME': 'U10', 'KE': 'U10',
        'MF': 'U8',  'KF': 'U8',
    }
    def __init__(self, db, add_to_year=0):
        super(CSVJuweImporter, self).__init__(db)
        self._add_to_year = add_to_year

    def read(self, filename):
        reader = UnicodeReader(open(filename, 'rb'), RFC4180)
        header = reader.next()
        self._check_header(header)
        n = 0
        for record in reader:
            self._insert(record)
            n += 1
        self.db.store.commit()
        return n

    def _insert(self, record):
        data = self.record_to_dict(record)
        if len(data['name']) == 0 and len(data['section']) == 0:
            return      # skip empty records

        athlete = self.db.create('athlete')

        (lastname, firstname) = data['name'].split(' ', 1)
        athlete.firstname = firstname
        athlete.lastname = lastname
        to_year = lambda x: (2000 + x) if x < 50 else (1900 + x)
        athlete.age_cohort = to_year(int(data['age_cohort'])) + self._add_to_year
        athlete.sex = self._convert_sex(data['sex'])
        athlete.category = self._category_from_age_and_sex(athlete.age_cohort, athlete.sex)
        athlete.id_section = self._section_to_id(data['section'])

        to_result = lambda r: decimal.Decimal(r) if len(r) > 0 else None
        athlete.sprint_result = to_result(data['sprint_result'])
        athlete.longjump_result = to_result(data['longjump_result'])
        athlete.highjump_result = to_result(data['highjump_result'])
        athlete.shotput_result = to_result(data['shotput_result'])
        athlete.ball_result = to_result(data['ball_result'])

        self.db.store.add(athlete)

    def record_to_dict(self, record):
        d = {}
        for csvfield, fieldname in self.IMPORT_FIELDS.iteritems():
            d[fieldname] = record[self.fields[csvfield]]
        return d

    def _convert_sex(self, sex):
        return { 'w': 'female', 'm': 'male'}[sex.lower()]

