import datetime
import re

TIMESPAN_REGEX = r"^(?:(in) )?(?:(\d+) ?week(?:s)?)? ?(?:(\d+) ?day(?:s)?)? ?(?:(\d+) ?hour(?:s)?)? ?(?:(\d+) ?min(?:ute)?(?:s)?)? ?(?:(\d+) ?sec(:?ond)?(?:s)?)? ?(ago)?$"
LITERAL_REGEX = r"^at (?:(\d+)\:)?(?:(\d+)\:)?(?:(\d+)\:)?(\d+)?$"


def _parse_timespan(string, from_date=None):
    match = re.match(TIMESPAN_REGEX, string.strip(), re.IGNORECASE)
    if match:
        if match.group(1) != "in" and match.group(8) != "ago":
            return None

        result = match.group(2, 3, 4, 5, 6)
        result = map(lambda x: int(x or 0), result)

        if match.group(8) == "ago":
            result = map(lambda x: -x, result)

        r = tuple(result)
        delta = datetime.timedelta(r[1], r[4], 0, 0, r[3], r[2], r[0])

        current_date = from_date
        if not current_date:
            current_date = datetime.datetime.now()

        return current_date + delta

    raise ValueError("Timespan does not match format.")


def _parse_literal(string, from_date=None):
    match = re.match(LITERAL_REGEX, string.strip(), re.IGNORECASE)
    if match:
        result = filter(None, match.group(1, 2, 3, 4))
        result = map(lambda x: int(x or 0), result)

        current_date = from_date
        if not current_date:
            current_date = datetime.datetime.now()

        r = tuple(result)
        if len(r) == 1:
            return current_date.replace(hour=r[0], minute=0, second=0)
        elif len(r) == 2:
            return current_date.replace(hour=r[0], minute=r[1], second=0)
        elif len(r) == 3:
            return current_date.replace(hour=r[0], minute=r[1], second=r[2])
        elif len(r) == 4:
            return current_date.replace(day=r[0], hour=r[1], minute=r[2], second=r[3])

    raise ValueError("Absolute date does not match format.")


def parse(string, from_date=None):
    try:
        return _parse_timespan(string, from_date)
    except ValueError:
        try:
            return _parse_literal(string, from_date)
        except ValueError:
            try:
                return _parse_literal("at {0}".format(string), from_date)
            except ValueError:
                return _parse_timespan("in {0}".format(string), from_date)
