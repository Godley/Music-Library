def extendJoinQuery(query_len, extender, operand, init_string=''):
    query = ''
    for i in range(query_len):
        if i == 0:
            query += init_string
        query += extender
        if i != query_len - 1:
            query += operand
    if query_len > 0:
        query += ')'
    return query

def do_online_offline_query(query, piece_id_field, online=False):
    new_query = query
    if online:
        new_query += ' AND EXISTS '
    else:
        new_query += ' AND NOT EXISTS '
    new_query += '(SELECT * FROM sources WHERE piece_id = '+piece_id_field+')'
    return new_query