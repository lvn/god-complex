

# The People object is just a thin wrapper around the database object.
class People:
    def __init__(self, name, world):
        self.name = name
        self.db = world.get_db()

    @staticmethod
    def all_peoples(db, world):
        cursor = db.execute('SELECT name FROM peoples')
        return [People(r[0], world) for r in cursor.fetchall()]

    def get_warlike_factor(self):
        cursor = self.db.execute(
            'SELECT warlike_factor FROM peoples WHERE name = ?', self.name)
        return cursor.fetchone()
