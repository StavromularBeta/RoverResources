import datetime


class ErrorHandling:

    def __init__(self):
        pass

    def checkYearMonthDayFormat(self, year_to_check, month_to_check, day_to_check):
        test_pass = True
        # checks to see if year, month, date can be converted to ints
        try:
            int(year_to_check)
            int(month_to_check)
            int(day_to_check)
        except ValueError:
            test_pass = False
            return test_pass
        # checks to see if the year, month and day are of appropriate length.
        if len(year_to_check) == 4:
            pass
        else:
            test_pass = False
            return test_pass
        if len(month_to_check) <= 2:
            pass
        else:
            test_pass = False
            return test_pass
        if len(day_to_check) <= 2:
            pass
        else:
            test_pass = False
            return test_pass
        # checks to see if the year, month and day are within a reasonable range
        if 1980 <= int(year_to_check) <= int(datetime.date.today().year):
            pass
        else:
            test_pass = False
            return test_pass
        if 1 <= int(month_to_check) <= 12:
            pass
        else:
            test_pass = False
            return test_pass
        if 1 <= int(day_to_check) <= 31:
            pass
        else:
            test_pass = False
            return test_pass
        return test_pass

    def checkNewPrice(self, price_to_check):
        test_pass = True
        if len(str(price_to_check)) == 0:
            test_pass = False
            return test_pass
        try:
            float(price_to_check)
        except ValueError:
            test_pass = False
            return test_pass
        return test_pass

    def checkBlankEntry(self, entry_to_check):
        test_pass = True
        if len(str(entry_to_check)) == 0:
            test_pass = False
        return test_pass
