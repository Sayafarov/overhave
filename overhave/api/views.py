import logging
from http import HTTPStatus
from typing import Optional

import fastapi

from overhave.api.deps import get_test_user_storage
from overhave.entities.converters import TestUserModel, TestUserSpecification
from overhave.storage import ITestUserStorage, TestUserDoesNotExistError

logger = logging.getLogger(__name__)


def _test_user_id_handler(user_id: int, test_user_storage: ITestUserStorage) -> TestUserModel:
    logger.info("Getting %s with user_id=%s...", TestUserModel.__name__, user_id)
    test_user = test_user_storage.get_test_user_by_id(user_id)
    if test_user is None:
        raise fastapi.HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"User with id={user_id} does not exist")
    return test_user


def _test_user_name_handler(user_name: str, test_user_storage: ITestUserStorage) -> TestUserModel:
    logger.info("Getting %s with user_name='%s'...", TestUserModel.__name__, user_name)
    test_user = test_user_storage.get_test_user_by_name(user_name)
    if test_user is None:
        raise fastapi.HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=f"User with name='{user_name}' does not exist"
        )
    return test_user


def test_user_handler(
    user_id: Optional[int] = None,
    user_name: Optional[str] = None,
    test_user_storage: ITestUserStorage = fastapi.Depends(get_test_user_storage),
) -> TestUserModel:
    if user_id is not None:
        return _test_user_id_handler(user_id=user_id, test_user_storage=test_user_storage)
    if user_name is not None:
        return _test_user_name_handler(user_name=user_name, test_user_storage=test_user_storage)
    raise fastapi.HTTPException(
        status_code=HTTPStatus.BAD_REQUEST, detail="'user_id' or 'user_name' query parameter should be set"
    )


def test_user_get_spec_handler(
    user_id: int, test_user_storage: ITestUserStorage = fastapi.Depends(get_test_user_storage)
) -> TestUserSpecification:
    test_user = _test_user_id_handler(user_id=user_id, test_user_storage=test_user_storage)
    return test_user.specification


def test_user_put_spec_handler(
    user_id: int,
    specification: TestUserSpecification,
    test_user_storage: ITestUserStorage = fastapi.Depends(get_test_user_storage),
) -> None:
    logger.info("Updating %s for user_id=%s...", TestUserSpecification.__name__, user_id)
    try:
        test_user_storage.update_test_user_specification(user_id=user_id, specification=specification)
    except TestUserDoesNotExistError:
        raise fastapi.HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"User with id={user_id} does not exist")
    logger.info("%s for user_id=%s was successfully updated", TestUserSpecification.__name__, user_id)