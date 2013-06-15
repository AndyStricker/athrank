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
        self.assign_awards()
        self.assign_final_qualification()

    def calculate_points(self):
        self.db.store.execute(
            'UPDATE Athlete SET ' + ', '.join([
                'sprint_points = 0',
                'longjump_points = 0',
                'highjump_points = 0',
                'shotput_points = 0',
                'ball_points = 0',
            ])
        )
        athletes = self.db.store.find(athrank.db.Athlete)
        for athlete in athletes:
            self.calculate_points_for_athlete(athlete)
        self.db.store.commit()

    def calculate_points_for_athlete(self, athlete):
        total_points = 0
        for discipline in DISCIPLINES:
            value = getattr(athlete, '%s_result' % discipline)
            if (value is None) or (value == 0.0):
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

    def assign_awards(self):
        self.db.store.execute('UPDATE Athlete SET award = NULL')
        for category in self._get_category_list():
            athletes = self.db.store.find(athrank.db.Athlete, category=category)
            athletes.order_by(athrank.db.Athlete.rank)
            if athletes.count() == 0:
                continue
            awards = [u'GOLD', u'SILVER', u'BRONZE']
            candidates = [a for a in athletes]
            while awards and candidates:
                award = awards.pop(0)
                candidates[0].award = award
                if len(candidates) <= 1:
                    break
                while candidates[1].total_points == candidates[0].total_points:
                    candidates.pop(0)
                    candidates[0].award = award
                    if awards:
                        awards.pop()
                    else:
                        break
                    if len(candidates) <= 1:
                        break
                candidates.pop(0)
        self.db.store.commit()

    def assign_final_qualification(self):
        FINAL_PER_CATEGORY = {
            "KJ": { 'percent': 0.35, 'minimum': 2 },
            "MJ": { 'percent': 0.35, 'minimum': 2 },
            "KA": { 'percent': 0.35, 'minimum': 2 },
            "MA": { 'percent': 0.35, 'minimum': 2 },
            "KB": { 'percent': 0.35, 'minimum': 2 },
            "MB": { 'percent': 0.35, 'minimum': 2 },
            "KC": { 'percent': 0.20, 'minimum': 2 },
            "MC": { 'percent': 0.20, 'minimum': 2 },
            "KD": { 'percent': 0.20, 'minimum': 2 },
            "MD": { 'percent': 0.20, 'minimum': 2 },
            "KE": { 'percent': 0.20, 'minimum': 2 },
            "ME": { 'percent': 0.20, 'minimum': 2 },
            "KF": { 'percent': 0.00, 'minimum': 0 },
            "MF": { 'percent': 0.00, 'minimum': 0 },
        }

        self.db.store.execute('UPDATE Athlete SET qualify = FALSE')
        for category in self._get_category_list():
            athletes = self.db.store.find(athrank.db.Athlete, category=category)
            athletes.order_by(storm.expr.Desc(athrank.db.Athlete.total_points))
            count = athletes.count()
            percent = FINAL_PER_CATEGORY[category]['percent']
            minimum = FINAL_PER_CATEGORY[category]['minimum']
            qualified_number = max(int(count * percent) + 0.4, minimum)
            print "category:", category, "count:", count, 'percent:', percent, 'qualified:', qualified_number
            for athlete in athletes:
                if qualified_number < 1:
                    break
                athlete.qualify = True
                qualified_number -= 1
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
            if value >= 21.43: return 1
            return int(7.89305 * (21.8 - value) ** 2.1)
        elif category in ('MB'):       # 80m
            if value >= 17.73: return 1
            return int(11.754907 * (18.03 - value) ** 2.1)
        elif category in ('MC', 'MD'): # 60m
            if value >= 13.93: return 1
            return int(19.742424 * (14.17 - value) ** 2.1)
        elif category in ('ME', 'MF'): # 50m
            if value >= 12.15: return 1
            return int(26.011098 * (12.36 - value) ** 2.1)
        elif category in ('KJ', 'KA'): # 100m
            if value >= 21.11: return 1
            return int(7.080303 * (21.5 - value) ** 2.1)
        elif category in ('KB'):       # 80m
            if value >= 17.46: return 1
            return int(10.54596 * (17.78 - value) ** 2.1)
        elif category in ('KC', 'KD'): # 60m
            if value >= 13.72: return 1
            return int(17.686955 * (13.97 - value) ** 2.1)
        elif category in ('KE', 'KF'): # 50m
            if value >= 11.97: return 1
            return int(23.327251 * (12.19 - value) ** 2.1)
        else:
            raise Exception("Invalid category %s" % category)

    def endurancerun(self, category, value):
        if category in ('MJ', 'MA', 'MB', 'MC'):
            if value > 332.89: return 1
            return int(0.006914 * (341.58 - value) ** 2.3)
        elif category in ('KJ', 'KA', 'KB', 'KC'):
            if value >= 317.07: return 1
            return int(0.0068251 * (325.81 - value) ** 2.3)
        elif category in ('MD', 'ME', 'MF', 'KD', 'KE', 'KF'): # no endurance run
            return 0
        return 0

    def longjump(self, category, value):
        if category in ('MJ', 'MA', 'MB', 'MC', 'MD', 'ME', 'MF'):
            if value <= 1.8: return 1
            return int(220.628792 * (value - 1.8) ** 1.0)
        elif category in ('KJ', 'KA', 'KB', 'KC', 'KD', 'KE', 'KF'):
            if value <= 1.9: return 1
            return int(180.85908 * (value - 1.9) ** 1.0)
        else:
            raise Exception("Invalid category %s" % category)

    def highjump(self, category, value):
        if category in ('MJ', 'MA', 'MB', 'MC'):
            if value <= 0.62: return 1
            return int(855.310049 * (value - 0.62) ** 1.0)
        elif category in ('KJ', 'KA', 'KB', 'KC'):
            if value <= 0.65: return 1
            return int(690.05175 * (value - 0.65) ** 1.0)
        elif category in ('MD', 'ME', 'MF', 'KD', 'KE', 'KF'): # no highjump
            return 0
        else:
            raise Exception("Invalid category %s" % category)

    def shotput(self, category, value):
        if category in ('MJ', 'MA', 'MB'):
            if value <= 1.3: return 1
            return int(83.435373 * (value - 1.3) ** 0.9)
        elif category in ('KJ', 'KA', 'KB', 'KC'):
            if value <= 1.78: return 1
            return int(82.491673 * (value - 1.78) ** 0.9)
        elif category in ('MC', 'MD', 'ME', 'MF', 'KD', 'KE', 'KF'):
            return 0
        else:
            raise Exception("Invalid category %s" % category)

    def ball(self, category, value):
        if category in ('MC', 'MD', 'ME', 'MF'):
            if value <= 5.03: return 1
            return int(22.0 * (value - 5) ** 0.9)
        elif category in ('KD', 'KE', 'KF'):
            if value <= 8.04: return 1
            return int(18.0 * (value - 8) ** 0.9)
        elif category in ('MJ', 'MA', 'MB', 'KJ', 'KA', 'KB', 'KC'): # shotput
            return 0
        else:
            raise Exception("Invalid category %s" % category)

