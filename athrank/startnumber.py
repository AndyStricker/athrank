import athrank.db

def assign_start_number_from_id(db):
    db.store.execute('UPDATE Athlete SET number = id_athlete')

def assign_start_number_sequential(db, start=0, skip_assigned=True):
    if skip_assigned:
        result = db.store.execute('SELECT MAX(number) FROM Athlete')
        start = max(result.get_one()[0], start)
    n = start
    for athlete in db.store.find(athrank.db.Athlete):
        n += 1
        if skip_assigned and (athlete.number > 0):
            continue
        athlete.number = n
    db.store.commit()
