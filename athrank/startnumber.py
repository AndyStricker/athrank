import athrank.db

def assign_start_number_from_id(db):
    db.store.execute('UPDATE Athlete SET number = id_athlete')
    db.store.commit()

def assign_start_number_sequential(db, start=0, skip_assigned=True):
    if skip_assigned:
        result = db.store.execute('SELECT MAX(number) FROM Athlete')
        start = max(result.get_one()[0], start)
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
