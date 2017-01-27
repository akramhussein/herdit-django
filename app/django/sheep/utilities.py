"""
TestCase mixin that provides extra functionality
"""
import phonenumbers


class TestCaseMixin(object):
    def __init__(self, *args, **kwargs):
        super(TestCaseMixin, self).__init__(*args, **kwargs)

    def assertEqualAPIResponses(self, first, second):
        """
        Wrap assertEqual to print responses comparison easily.
        """
        super(TestCaseMixin, self).assertEqual(
            first,
            second,
            'Expected Response Code {1}, received {0} instead.'.format(first, second))


def formatted_tel(telephone_number):
    p = phonenumbers.parse(telephone_number, "GB")
    return phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.E164)
