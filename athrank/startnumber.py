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

import athrank.db

def assign_start_number_from_id(db):
    db.store.execute('UPDATE Athlete SET number = id_athlete')
    db.store.commit()

def assign_start_number_sequential(db, start=0, skip_assigned=True):
    if skip_assigned:
        result = db.store.execute('SELECT MAX(number) FROM Athlete')
        start = max(result.get_one()[0] + 1, start)
    else:
        db.store.execute('UPDATE Athlete SET number = NULL')
    n = start
    athletes = db.store.find(athrank.db.Athlete)
    # order by category to improve manual lookup by number
    athletes.order_by(athrank.db.Athlete.category)
    for athlete in athletes:
        if skip_assigned and (athlete.number > 0):
            continue
        athlete.number = n
        n += 1
    db.store.commit()
