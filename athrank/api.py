""" RESTful Athrank webservice API """

import sys
import os
sys.path.append(os.getcwd())
import web
import web.webapi
import json
import athrank.db

from web.contrib.template import render_cheetah
import Cheetah.Template

PREFIX = '/api/v1'
urls = (
    '/', 'Index',
    PREFIX + '/athletes(/)?', 'Athletes',
    PREFIX + '/athlete(/)?', 'Athletes',
    PREFIX + '/athlete/(\d+)', 'Athlete',
    PREFIX + '/athlete/number/(\d+)', 'AthleteStartNumber',
    PREFIX + '/categories', 'Categories',
    PREFIX + '/category/(\w+)', 'Category',
    PREFIX + '/sections', 'Sections',
)

def _create_api_path(resource, rid):
    return '{0}/{1}/{2}'.format(PREFIX, resource, rid)

class Index:
    def GET(self):
        render = render_cheetah('reports/api')
        return render.index(title='Athrank', statistics={ 'total_athletes': 42 })

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

        personal_data = web.input('firstname', 'lastname', 'section', 'year_of_birth', 'sex')

        db = athrank.db.DB()
        section = db.store.find(athrank.db.Section, name=personal_data.section)
        if section.is_empty():
            raise web.badrequest(
                message='Section "{0}" not found'.format(personal_data.section)
            )
        section = section.one()

        year_of_birth = int(personal_data.year_of_birth)
        category = db.store.find(
            athrank.db.Category,
            age_cohort=year_of_birth,
            sex=personal_data.sex
        )
        if category.is_empty():
            raise web.badrequest(
                message='Category for year "{0}" and sex "{1}" not found'.format(
                    personal_data.year_of_birth,
                    personal_data.sex
                )
            )
        category = category.one()

        athlete = athrank.db.Athlete(
            firstname=personal_data.firstname,
            lastname=personal_data.lastname,
            year_of_birth=year_of_birth,
            sex=personal_data.sex,
            section=section.id_section,
            category=category.category,
            category_code=category.category_code
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

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
