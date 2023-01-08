import json
from sqlalchemy import inspect, func
from datetime import date

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

def row2dict(row,label="null"):
    d = {}
    try:
        inspect(row)
        if(row.__table__.columns):
            for column in row.__table__.columns:
                nonecheck = str(getattr(row, column.name))
                if nonecheck == 'None':
                    nonecheck = ''
                d[column.name] = nonecheck
    except NoInspectionAvailable:
        d[label]=row
    return d

def dict_builder(result):
    dlist = []
    for r in result:
        d={}
        res = r._asdict()
        for key in res:
            d.update(row2dict(res[key],key))
        dlist.append(d)
    return dlist

def sql_to_json(query):
    rows = query.fetchall()
    fields = query.keys()
    object_list = []
    for row in rows:
        json_row = {}
        fields = [f for f in query.keys()]
        for field in fields:
            index = fields.index(field)
            json_row[field] = row[index]
        object_list.append(json_row)
    return jsonify(object_list)