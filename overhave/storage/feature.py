import abc
from typing import cast

from overhave import db
from overhave.db.converters import FeatureTypeModel


class IFeatureTypeStorage(abc.ABC):
    @abc.abstractmethod
    def get_default_feature_type(self) -> FeatureTypeModel:
        pass


class FeatureTypeStorage(IFeatureTypeStorage):
    def get_default_feature_type(self) -> FeatureTypeModel:
        with db.create_session() as session:
            feature_type: db.FeatureType = session.query(db.FeatureType).order_by(db.FeatureType.id.asc()).first()
            return cast(FeatureTypeModel, FeatureTypeModel.from_orm(feature_type))