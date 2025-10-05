import unittest
from types import SimpleNamespace

from apps.hadmin.views.utils import get_pagination_params


class PaginationParamsTests(unittest.TestCase):

    def test_missing_rows_defaults_to_20(self):
        request = SimpleNamespace(POST={})

        page, rows = get_pagination_params(request, page_default=1, rows_default=20)

        self.assertEqual(page, 1)
        self.assertEqual(rows, 20)


if __name__ == '__main__':
    unittest.main()
