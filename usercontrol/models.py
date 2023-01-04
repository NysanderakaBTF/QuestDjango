from django.contrib.auth.base_user import *
from django.contrib.auth.models import PermissionsMixin, User
from django.db import models
from django.contrib.auth import models as auth_models


class ModeratorUser(User):
    class Meta:
        permissions = (
            ("can_edit_any_test", "To edit any test"),
            ("can_delete_any_test", "To delete any test"),
            ("can_create_test", "To create test"),
            ("can_delete_user", "To delete any user"),
            ("can_add_user_to_group", "To add user to group"),
        )


class RegularUser(User):
    class Meta:
        permissions = (
            ("can_edit_his_test", "To edit his test"),
            ("can_delete_his_test", "To delete his test"),
            ("can_create_test", "To create test"),
            ("can_add_user_to_group", "To add user to group"),
        )



