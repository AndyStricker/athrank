import csv, codecs

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


class CSVImporter(object):
    CHECK_HEADER_MAX = 6
    HEADER = (
       u"Sektion",u"Name",u"Vorname",u"Jahrgang",u"G",u"Kategorie",u"Poulet",u"k1",u"k2"
    )
    FIELDS = {
        'section': 0,
        'lastname': 1,
        'firstname' : 2,
        'year_of_birth': 3,
        'sex': 4,
        'category': 5,
    }

    class RFC4180:
        delimiter = ','
        quotechar = '"'
        doublequote = True
        escapechar = None
        skipinitialspace = False
        lineterminator = '\n'
        quoting = csv.QUOTE_MINIMAL
        
    def __init__(self, db):
        self._db = db
        self._sections = self._create_section_lookup_table()

    def _create_section_lookup_table(self):
        table = {}
        section_fetcher = self.db.create('Section')
        for section in section_fetcher.fetch_all():
            table[section['name']] = section['id_section']
        return table

    @property
    def db(self):
        return self._db

    @property
    def sections(self):
        return self._sections

    def read(self, filename):
        reader = UnicodeReader(open(filename, 'rb'), CSVImporter.RFC4180)
        header = reader.next()
        self._check_header(header)
        for record in reader:
            self._insert(record)

    def _check_header(self, header):
        for n in xrange(0, self.CHECK_HEADER_MAX):
            expected = self.HEADER[n]
            value = header[n]
            if expected != value:
                raise Exception('Expected header field %d is "%s" but got "%s"' % (n, expected, value))
        
    def _insert(self, record):
        athlete = self.db.create('athlete')
        for field, idx in self.FIELDS.iteritems():
            athlete[field] = record[idx]
        athlete['section'] = self._section_to_id(athlete['section'])
        athlete['sex'] = self._convert_sex(athlete['sex'])
        athlete['year_of_birth'] = int(athlete['year_of_birth'])
        athlete['category_code'] = athlete['category'][1]
        print repr(athlete)
        athlete.insert(athlete.keys())
        self.db.commit()

    def _section_to_id(self, name):
        return self._sections[name]

    def _convert_sex(self, v):
        return {'k':'m', 'm': 'w'}[v.lower()]
