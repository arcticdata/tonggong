import unittest

from tonggong.crontab import CronTab


class CrontabTestCase(unittest.TestCase):
    def test_crontab(self):
        test_cases = ["* * * * *", "1 * 2 * *", "*/3 * * * *", "* */2 * * 1-7", "5 4 */2 * 3"]
        for case in test_cases:
            CronTab(case)

        wrong_case = ["61 * * * *", "58 26 * * *", "0.1 * * * *", "*//2 * * * *", "1-4 * * * 9", "1", "* * * *"]
        length = len(wrong_case)
        for case in wrong_case:
            try:
                CronTab(case)
            except Exception:
                length -= 1
        self.assertFalse(length)
