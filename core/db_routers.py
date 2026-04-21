
# Apps whose models live in the vector DB
VECTOR_DB_APPS = {'ml_models'}


class VectorDbRouter:
    """
    Routes all models in apps.ml_models to the 'vector_db' PostgreSQL database.
    This DB has the pgvector extension enabled and stores:
      - Embeddings
      - ML inference results
      - Model registry metadata
    All other apps are ignored (return None) and fall through to ReadReplicaRouter.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label in VECTOR_DB_APPS:
            return 'vector_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in VECTOR_DB_APPS:
            return 'vector_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # Allow relations within the same DB; block cross-DB relations
        db_set = {obj1._meta.app_label in VECTOR_DB_APPS,
                  obj2._meta.app_label in VECTOR_DB_APPS}
        if len(db_set) == 1:
            return True   # Both on same DB
        return False      # Cross-DB relation — not allowed

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in VECTOR_DB_APPS:
            # ml_models migrations run ONLY on vector_db
            return db == 'vector_db'
        if db == 'vector_db':
            # Nothing else migrates into vector_db
            return False
        return None  # Let ReadReplicaRouter decide for everything else


class ReadReplicaRouter:
    """
    Fallback router for all non-vector apps.
    Currently routes everything to 'default'.
    Ready for read-replica scaling: uncomment the 'reader' return
    in db_for_read() and add a 'reader' DB entry in settings.
    """

    def db_for_read(self, model, **hints):
        # return 'reader'  # Uncomment when read replica is available
        return 'default'

    def db_for_write(self, model, **hints):
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # All non-vector migrations go to default only
        return db == 'default'
