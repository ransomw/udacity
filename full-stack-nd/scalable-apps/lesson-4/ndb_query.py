
### query by kind
q = Conference.query()

q.order(Conference.name)

q.filter(Conference.month == 2)

q.get() # one results
q.fetch() # all results
q.fetch(n) # n results

for result in q:
    pass

### query by ancestor
q = Conference.query(ancestor=ndb.Key(Profile, user_id))

### query with filters

# basic
q = Conference.query(Conference.city == "London")

# advanced
q = Conference.query()
field = "city"
operator = "=="
value = "London"
f = ndb.query.FilterNode(field, operator, value)
q = q.filter(f)
