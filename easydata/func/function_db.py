def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
    
def dictfetchall_pk(cursor, pk_position):
    desc = cursor.description
    dict_pk = {}
    for row in cursor.fetchall():
        dict_pk[row[pk_position]] = dict(zip([col[0] for col in desc], row))
    return dict_pk