from neomodel import db, StructuredNode, StringProperty


class User(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    password = StringProperty()

    @classmethod
    def find_by_name(cls, name=None):
        return cls.nodes.first_or_none(name=name)

    @classmethod
    def is_admin(cls):
        return False

    @db.transaction
    def save_to_db(self):
        self.save()

    @db.transaction
    def delete_from_db(self):
        self.delete()


class Administrator(User):
    @classmethod
    def is_admin(cls):
        return True

