from typing import cast

import werkzeug
from flask_admin import expose
from flask_login import current_user
from wtforms import ValidationError

from overhave import db
from overhave.admin.views.base import ModelViewConfigured
from overhave.admin.views.formatters import result_report_formatter


class TestRunView(ModelViewConfigured):
    list_template = 'test_run_list.html'
    details_template = 'test_run_detail.html'
    can_edit = False
    column_exclude_list = ('scenario', 'traceback', 'report', 'created_at')  # type: ignore
    column_searchable_list = (
        'name',
        'executed_by',
    )
    column_filters = ('name', 'start', 'executed_by', 'status')

    column_formatters = dict(status=result_report_formatter,)

    def on_model_delete(self, model: db.TestRun) -> None:
        if not (current_user.login == model.executed_by or current_user.role == db.Role.admin):
            raise ValidationError('Only test run initiator could delete test run result!')

    @expose('/details/', methods=('GET', 'POST'))
    def details_view(self) -> werkzeug.Response:
        return cast(werkzeug.Response, super().details_view())