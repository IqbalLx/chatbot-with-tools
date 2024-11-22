import pypika as pk  # type: ignore
from psycopg2 import ProgrammingError

class User:
     def __init__(
            self,
            id: str,
            nik: str,
            name: str,
            sex: str,
            place_of_birth: str,
            date_of_birth: str,
            profession: str,
            address: str,
            religion: str,
    ):
        self.id = id
        self.nik = nik
        self.name = name
        self.sex = sex
        self.place_of_birth = place_of_birth
        self.date_of_birth = date_of_birth
        self.profession = profession
        self.address = address
        self.religion = religion


def get_user(db, nik: str) -> User:
        users = pk.Table('users')

        query = (
            pk.PostgreSQLQuery.from_(users)
            .select(
                "id",
                "nik",
                "name",
                "sex",
                "place_of_birth",
                "date_of_birth",
                "profession",
                "address",
                "religion",
            )
            .where(users.nik == pk.Parameter("%s"))
            .limit(1)
        )

        cursor = db.cursor()
        cursor.execute(
            str(query), (nik,)
        )

        try:
            result = cursor.fetchone()
        except ProgrammingError:
            result = None
        finally:
            cursor.close()

        if result is None:
             return None
        
        return User(*result)

