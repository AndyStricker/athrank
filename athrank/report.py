import Cheetah.Template
import os
import athrank.db

class Report(object):
    pass

class RankingReport(Report):
    TITLE = 'Rangliste Jugendriegentag 2013 Satus Neuhausen'

    def __init__(self, db, path='reports/rankings/', filename='rankings.tmpl'):
        self._db = db
        self._path = path
        self._filename = filename

    @property
    def db(self):
        return self._db

    def create(self):
        path = os.path.join(self._path, self._filename)
        tmpl = file(path, 'r').read().decode('utf-8')
        ns = self.get_namespace()
        result = Cheetah.Template.Template(tmpl, searchList=[ns])
        return result

    def get_namespace(self):
        categories = self._get_category_list()
        rank_lists = []
        for category in categories:
            ranks = self.db.store.find(
                athrank.db.Athlete,
                athrank.db.Athlete.total_points > 0,
                category=category
            )
            ranks.order_by(athrank.db.Athlete.rank, athrank.db.Athlete.number)
            if ranks.count() > 0:
                rank_lists.append((category, ranks))
        return {
            'title': self.TITLE,
            'categories': rank_lists,
        }

    def _get_category_list(self):
        db_categories = self.db.store.find(athrank.db.Category)
        category_set = set()
        for category in db_categories:
            category_set.add(category.category)
        categories = list(category_set)
        def category_cmp(a, b):
            s = cmp(a[0], b[0])
            if s != 0:
                return -1 * s
            else:
                return cmp(a[1:], b[1:])
        categories.sort(cmp=category_cmp)
        return categories
