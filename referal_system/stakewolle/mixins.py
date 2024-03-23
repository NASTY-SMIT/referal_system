import re

from rest_framework import serializers

import stakewolle.templates as templates


class UsernameValidationMixin:
    def validate_username(self, value: str):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                templates.NAME_NOT_EQUAL_ME_ERROR
            )
        if not re.search(r'^[\w.@+-]+', value):
            raise serializers.ValidationError(
                templates.INVALID_NAME_FORMAT_ERROR
            )
        return value
