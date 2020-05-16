from neomodel import db, StructuredNode, StringProperty
from metrics import metrics_query_latency, metrics_query_in_progress, metrics_query_count


class User(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    password = StringProperty()

    @classmethod
    @metrics_query_latency.time()
    @metrics_query_in_progress.track_inprogress()
    def find_by_name(cls, name=None):
        metrics_query_count.labels(object=type(cls).__name__, method='find_by_name').inc()
        return cls.nodes.first_or_none(name=name)

    @classmethod
    def is_admin(cls):
        return False

    @db.transaction
    @metrics_query_latency.time()
    @metrics_query_in_progress.track_inprogress()
    def save_to_db(self):
        metrics_query_count.labels(object=type(self).__name__, method='save_to_db').inc()
        self.save()

    @db.transaction
    @metrics_query_latency.time()
    @metrics_query_in_progress.track_inprogress()
    def delete_from_db(self):
        metrics_query_count.labels(object=type(self).__name__, method='delete_from_db').inc()
        self.delete()

    @metrics_query_latency.time()
    @metrics_query_in_progress.track_inprogress()
    def json(self):
        metrics_query_count.labels(object=type(self).__name__, method='json').inc()
        return {'name': self.name}

    @metrics_query_latency.time()
    @metrics_query_in_progress.track_inprogress()
    def json_full(self):
        metrics_query_count.labels(object=type(self).__name__, method='json').inc()
        return {'name': self.name, 'password': self.password}


class Administrator(User):
    @classmethod
    def is_admin(cls):
        return True
