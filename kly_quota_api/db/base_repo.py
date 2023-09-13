class BaseRepository(object):
    model_class = None

    def count(self, session, **filters):
        """Retrieves a count of entities from the database.

        :param session: A Sql Alchemy database session.
        :param filters: Filters to decide which entities should be retrieved.
        :returns: int
        """
        return session.query(self.model_class).filter_by(**filters).count()

    def create(self, session, **model_kwargs):
        """Base create method for a database entity.

        :param session: A Sql Alchemy database session.
        :param model_kwargs: Attributes of the model to insert.
        :returns: trochilus.db.base_models.TrochilusBase
        """
        with session.begin(subtransactions=True):
            model = self.model_class(**model_kwargs)
            session.add(model)
        return model

    def create_batch(self, session, models_list: list):
        """Batch create method for multiple database entities.

        :param session: A Sql Alchemy database session.
        :param models_list: List of the model to insert.
        :returns: [trochilus.db.base_models.TrochilusBase]
        """
        models = [self.model_class(**m) for m in models_list]
        with session.begin(subtransactions=True):
            session.add_all(models)
        return models

    def update(self, session, id, **model_kwargs):
        """Updates an entity in the database.

        :param session: A Sql Alchemy database session.
        :param model_kwargs: Entity attributes that should be updates.
        :returns: trochilus.db.base_models.TrochilusBase
        """
        with session.begin(subtransactions=True):
            session.query(self.model_class).filter_by(
                id=id).update(model_kwargs)

    def get(self, session, **filters):
        """Retrieves an entity from the database.

        :param session: A Sql Alchemy database session.
        :param filters: Filters to decide which entity should be retrieved.
        :returns: trochilus.db.base_models.TrochilusBase
        """
        return session.query(self.model_class).filter_by(**filters).first()

    def get_all(self, session, args=None, **filters):
        """Retrieves a list of entities from the database.

        :param session: A Sql Alchemy database session.
        :param filters: Filters to decide which entities should be retrieved.
        :returns: [trochilus.db.base_models.TrochilusBase]
        """
        if args:
            return session.query(self.model_class).filter_by(args, **filters)
        return session.query(self.model_class).filter_by(**filters)

    def exists(self, session, id):
        """Determines whether an entity exists in the database by its id.

        :param session: A Sql Alchemy database session.
        :param id: id of entity to check for existence.
        :returns: trochilus.db.base_models.TrochilusBase
        """
        return bool(session.query(self.model_class).filter_by(id=id).first())

