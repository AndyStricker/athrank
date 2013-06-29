# -*- coding: utf-8 -*-
""" RESTful Athrank webservice API """

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

import sys
import os
sys.path.append(os.getcwd())
import web
import web.webapi
import json
import athrank.db
import athrank.ranking
import athrank.report

from web.contrib.template import render_cheetah
import Cheetah.Template

PREFIX = '/v1'
urls = (
    '/', 'Index',
    '/ranking(/)?', 'Ranking',
    PREFIX + '/athletes(/)?', 'Athletes',
    PREFIX + '/athlete(/)?', 'Athletes',
    PREFIX + '/athlete/(\d+)', 'Athlete',
    PREFIX + '/athlete/number/(\d+)', 'AthleteStartNumber',
    PREFIX + '/categories', 'Categories',
    PREFIX + '/category/year/(\d+);([fm])', 'AgeCategory',
    PREFIX + '/category/(\w+)', 'Category',
    PREFIX + '/sections', 'Sections',
)

def _create_api_path(resource, rid):
    return '{0}/{1}/{2}'.format(PREFIX, resource, rid)

class Index:
    def GET(self):
        db = athrank.db.DB()

        total_athletes = db.store.find(athrank.db.Athlete).count()
        count_per_category = db.store.execute(
            'SELECT category, COUNT(id_athlete) FROM Athlete GROUP BY category ORDER BY category'
        ).get_all()

        stats = {
            'total_athletes': total_athletes,
            'count_per_category': count_per_category,
        }

        render = render_cheetah('reports/api')
        return render.index(title='Athrank', statistics=stats)

class Ranking:
    def GET(self, slash):
        if slash:
            raise web.seeother('/ranking')

        db = athrank.db.DB()

        ranking = athrank.ranking.Ranking(db, athrank.ranking.ScoreTable94())
        ranking.rank()

        report = athrank.report.RankingReport(db)
        return report.create()

class AthleteBase(object):
    ATHLETE_ATTRIBUTES = athrank.db.get_relation_fields(athrank.db.Athlete)
    def get_athlete_dict(self, athlete):
        obj = {}
        for name in self.ATHLETE_ATTRIBUTES:
            obj[name] = getattr(athlete, name)
        obj['section'] = athlete.r_section.name
        obj['link'] = {
            'rel': 'self',
            'href': _create_api_path('athlete', obj['id_athlete']),
        }
        obj['category_ref'] = {
            'rel': 'related',
            'href': _create_api_path('category', obj['category']),
        }
        return obj

class Athletes(AthleteBase):
    def GET(self, slash=False):
        if slash:
            raise web.seeother('/athletes')

        params = web.input(_unicode=True)

        db = athrank.db.DB()
        query = []
        if params.has_key('firstname') and len(params['firstname']) > 0:
            query.append(athrank.db.Athlete.firstname == params['firstname'])
        if params.has_key('lastname') and len(params['lastname']) > 0:
            query.append(athrank.db.Athlete.lastname == params['lastname'])
        if params.has_key('category') and len(params['category']) > 0:
            query.append(athrank.db.Athlete.category == params['category'])
        if params.has_key('section') and len(params['section']) > 0:
            query.append(athrank.db.Athlete.r_section == athrank.db.Section.id_section)
            query.append(athrank.db.Section.name == params['section'])
        athletes = db.store.find(athrank.db.Athlete, *tuple(query))
        result = []
        for athlete in athletes:
            result.append(self.get_athlete_dict(athlete))

        web.header('Content-Type', 'application/json')
        return json.dumps({
            'count': len(result),
            'result': result,
        })

    def POST(self, slash=False):
        if slash:
            raise web.seeother('/athletes')

    def POST(self):
        personal_data = web.input(
            'firstname', 'lastname', 'section', 'year_of_birth', 'sex',
            _unicode=True
        )

        db = athrank.db.DB()
        section = db.store.find(athrank.db.Section, name=personal_data.section)
        if section.is_empty():
            raise web.badrequest(
                message='Section "{0}" not found'.format(personal_data.section)
            )
        section = section.one()

        year_of_birth = int(personal_data.year_of_birth)
        agecategory = db.store.find(
            athrank.db.AgeCategory,
            age_cohort=year_of_birth,
            sex=personal_data.sex
        )
        if agecategory.is_empty():
            raise web.badrequest(
                message='Category for year "{0}" and sex "{1}" not found'.format(
                    personal_data.year_of_birth,
                    personal_data.sex
                )
            )
        category = agecategory.one().category

        athlete = athrank.db.Athlete(
            firstname=personal_data.firstname,
            lastname=personal_data.lastname,
            year_of_birth=year_of_birth,
            sex=personal_data.sex,
            section=section.id_section,
            category=category
        )

        db.store.add(athlete)
        db.store.commit()

        web.ctx.status = '201 Created'
        web.header('Location', _create_api_path('athlete', athlete.id_athlete))
        web.header('Content-Type', 'application/json')
        obj = self.get_athlete_dict(athlete)
        return json.dumps(obj)

class Athlete(AthleteBase):
    def GET(self, id_athlete):
        db = athrank.db.DB()
        athlete = db.store.get(athrank.db.Athlete, int(id_athlete))
        if athlete is None:
            raise web.notfound(message='Athlete with this id not found')
        obj = self.get_athlete_dict(athlete)
        web.header('Content-Type', 'application/json')
        return json.dumps(obj)

    def PUT(self, id_athlete):
        attributes = web.input(_unicode=True)

class AthleteStartNumber(AthleteBase):
    def GET(self, number):
        db = athrank.db.DB()
        athlete = db.store.find(athrank.db.Athlete, number=int(number))
        if athlete.is_empty():
            raise web.notfound(message='No Athlete with this start number found')
        obj = self.get_athlete_dict(athlete.one())
        web.header('Content-Type', 'application/json')
        return json.dumps(obj)

class CategoryBase(object):
    CATEGORY_ATTRIBUTES = athrank.db.get_relation_fields(athrank.db.Category)
    def get_category_dict(self, category): 
        obj = {}
        for name in self.CATEGORY_ATTRIBUTES:
            obj[name] = getattr(category, name)
        obj['link'] = {
            'rel': 'self',
            'href': _create_api_path('category', obj['category']),
        }
        return obj

class Categories(CategoryBase):
    def GET(self):
        db = athrank.db.DB()
        categories = db.store.find(athrank.db.Category)
        result = []
        for category in categories:
            result.append(self.get_category_dict(category))

        web.header('Content-Type', 'application/json')
        return json.dumps({
            'count': len(result),
            'result': result,
        })

class Category(CategoryBase):
    def GET(self, category):
        db = athrank.db.DB()
        try:
            category = db.store.find(athrank.db.Category, category=category)
        except ValueError:
            raise web.notfound(message='Category does not exist')
        category.group_by(athrank.db.Category.category)
        if category.is_empty():
            raise web.notfound(message='Category not found')
        obj = self.get_category_dict(category.one())

        web.header('Content-Type', 'application/json')
        return json.dumps(obj)

class AgeCategory(CategoryBase):
    def GET(self, age_cohort, sex):
        db = athrank.db.DB()
        agecategory = db.store.find(athrank.db.AgeCategory, age_cohort=int(age_cohort), sex=sex)
        if agecategory.is_empty():
            raise web.notfound(
                message='Category for age cohort {0} and sex {1} not found'.format(
                    age_cohort, sex
                )
            )
        category = agecategory.one().r_category
        obj = self.get_category_dict(category)

        web.header('Content-Type', 'application/json')
        return json.dumps(obj)

class Sections:
    SECTION_ATTRIBUTES = athrank.db.get_relation_fields(athrank.db.Section)
    def GET(self):
        db = athrank.db.DB()
        sections = db.store.find(athrank.db.Section)
        result = []
        for section in sections:
            result.append(self.get_section_dict(section))

        web.header('Content-Type', 'application/json')
        return json.dumps({
            'count': len(result),
            'result': result,
        })
    def get_section_dict(self, section): 
        obj = {}
        for name in self.SECTION_ATTRIBUTES:
            obj[name] = getattr(section, name)
        return obj

def get_application():
    return web.application(urls, globals())

if __name__ == '__main__':
    app = get_application()
    app.run()
