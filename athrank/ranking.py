import storm.expr
import athrank.db

DISCIPLINES = [
    'sprint',
    'longjump',
    'highjump',
    'shotput',
    'ball',
]

class Ranking(object):
    def __init__(self, db, score_table):
        self._db = db
        self._score_table = score_table

    @property
    def db(self):
        return self._db

    @property
    def score_table(self):
        return self._score_table

    def rank(self):
        self.calculate_points()
        self.assign_rank()

    def calculate_points(self):
        athletes = self.db.store.find(athrank.db.Athlete)
        for athlete in athletes:
            self.calculate_points_for_athlete(athlete)
        self.db.store.commit()

    def calculate_points_for_athlete(self, athlete):
        total_points = 0
        for discipline in DISCIPLINES:
            value = getattr(athlete, '%s_result' % discipline)
            if value is None:
                points = 0
            else:
                points = self.score_table.calculate_points(
                    discipline,
                    athlete.category,
                    float(value)
                )
            total_points += points
            setattr(athlete, '%s_points' % discipline, points)
        athlete.total_points = total_points

    def assign_rank(self):
        self.db.store.execute('UPDATE Athlete SET rank = NULL')
        for category in self._get_category_list():
            athletes = self.db.store.find(athrank.db.Athlete, category=category)
            athletes.order_by(storm.expr.Desc(athrank.db.Athlete.total_points))
            rank = 1
            for athlete in athletes:
                athlete.rank = rank
                rank += 1
        self.db.store.commit()

    def _get_category_list(self):
        db_categories = self.db.store.find(athrank.db.Category)
        category_set = set()
        for category in db_categories:
            category_set.add(category.category)
        categories = list(category_set)
        categories.sort()
        return categories

class ScoreTable(object):
    def calculate_points(self, discipline, category, value):
        raise Exception("Must be implemented by subclass")

class ScoreTable94(object):
    def calculate_points(self, discipline, category, value):
        method = getattr(self, discipline)
        if method is None:
            raise Exception("No method for discipline %s found" % discipline)
        return method(category, value)

    def sprint(self, category, value):
        if category in ('MJ', 'MA'):   # 100m
            return int(7.89305 * (21.8 - value) ** 2.1)
        elif category in ('MB'):       # 80m
            return int(11.754907 * (18.03 - value) ** 2.1)
        elif category in ('MC', 'MD'): # 60m
            return int(19.742424 * (14.17 - value) ** 2.1)
        elif category in ('ME', 'MF'): # 50m
            return int(26.011098 * (12.36 - value) ** 2.1)
        elif category in ('KJ', 'KA'): # 100m
            return int(7.080303 * (21.5 - value) ** 2.1)
        elif category in ('KB'):       # 80m
            return int(10.54596 * (17.78 - value) ** 2.1)
        elif category in ('KC', 'KD'): # 60m
            return int(17.686955 * (13.97 - value) ** 2.1)
        elif category in ('KE', 'KF'): # 50m
            return int(23.327251 * (12.19 - value) ** 2.1)
        else:
            raise Exception("Invalid category %s" % category)

    def endurancerun(self, category, value):
        if category in ('MJ', 'MA', 'MB', 'MC'):
            return int(0.006914 * (341.58 - value) ** 2.3)
        elif category in ('KJ', 'KA', 'KB', 'KC'):
            return int(0.0068251 * (325.81 - value) ** 2.3)
        elif category in ('MD', 'ME', 'MF', 'KD', 'KE', 'KF'): # no endurance run
            return 0
        return 0

    def longjump(self, category, value):
        if category in ('MJ', 'MA', 'MB', 'MC', 'MD', 'ME', 'MF'):
            return int(220.628792 * (value - 1.8) ** 1.0)
        elif category in ('KJ', 'KA', 'KB', 'KC', 'KD', 'KE', 'KF'):
            return int(180.85908 * (value - 1.9) ** 1.0)
        else:
            raise Exception("Invalid category %s" % category)

    def highjump(self, category, value):
        if category in ('MJ', 'MA', 'MB', 'MC'):
            return int(855.310049 * (value - 0.62) ** 1.0)
        elif category in ('KJ', 'KA', 'KB', 'KC'):
            return int(690.05175 * (value - 0.65) ** 1.0)
        elif category in ('MD', 'ME', 'MF', 'KD', 'KE', 'KF'): # no highjump
            return 0
        else:
            raise Exception("Invalid category %s" % category)

    def shotput(self, category, value):
        if category in ('MJ', 'MA', 'MB'):
            return int(83.435373 * (value - 1.3) ** 0.9)
        elif category in ('KJ', 'KA', 'KB', 'KC'):
            return int(82.491673 * (value - 1.78) ** 0.9)
        elif category in ('MC', 'MD', 'ME', 'MF', 'KD', 'KE', 'KF'):
            return 0
        else:
            raise Exception("Invalid category %s" % category)

    def ball(self, category, value):
        if category in ('MC', 'MD', 'ME', 'MF'):
            return int(22.0 * (value - 5) ** 0.9)
        elif category in ('KD', 'KE', 'KF'):
            return int(18.0 * (value - 8) ** 0.9)
        elif category in ('MJ', 'MA', 'MB', 'KJ', 'KA', 'KB', 'KC'): # shotput
            return 0
        else:
            raise Exception("Invalid category %s" % category)

