#
def get_serializer_error_message(serializer, default=None):
    _field = None
    _value = None

    try:
        #
        for field, errors in serializer.errors.items():
            for error in errors:
                if "error" not in field:
                    _field = str(field)
                _value = str(error)
                break
    except:
        #
        for errors in serializer.errors:
            for field, error in errors.items():
                if "error" not in field:
                    _field = str(field)
                if isinstance(error, list):
                    _value = str(error[0])
                else:
                    _value = str(error)
                break

    if _value:
        if _field and not _field in _value:
            return f"{_field.capitalize()}: {_value}"
        return _value

    return default or "Error! an intended error has occurred"
