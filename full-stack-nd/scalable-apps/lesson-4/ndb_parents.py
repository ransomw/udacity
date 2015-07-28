p_key = ndb.Key(Profile, user_id)

c_id = Conference.allocate_ids(size=1, parent=p_key)[0]

c_key = ndb.Key(Conference, c_id, parent=p_key)
