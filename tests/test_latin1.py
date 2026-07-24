# Regression test for non-UTF-8 (latin1) values passed to a pydef.
# EAV table: dispatch on the sibling `fieldname` column via get_row().
import myanon_utils
import hashlib
import hmac

_SENSITIVE = frozenset(('name',))


def anon_fieldvalue(value):
    fieldname = myanon_utils.get_row().get('`fieldname`', '')
    if fieldname in _SENSITIVE:
        secret = myanon_utils.get_secret().encode()
        # surrogateescape: hash the real underlying bytes, never crash
        digest = hmac.new(secret, value.encode('utf-8', 'surrogateescape'),
                          hashlib.sha256).hexdigest()
        return digest[:10]
    if fieldname == 'note':
        # Round-trip through the SQL helpers: they must accept latin1 bytes
        # and hand them back untouched.  Only the quote style is normalised,
        # from mysqldump's \' to the SQL-standard ''.
        return myanon_utils.escape_sql_string(
            myanon_utils.unescape_sql_string(value))
    # non-sensitive keys pass through unchanged (bytes preserved)
    return value
