import random


class CardUtil:
    MAXIMUM_PATTERN_NUMBER = 499

    @staticmethod
    def get_random_pattern_number():
        random.seed()
        return random.randint(0, 499)
    
    @staticmethod
    def get_random_float_value():
        random.seed()
        return round(random.uniform(0, 1), 5)
    
    @staticmethod
    def get_float_as_condition(float_value):
        if 0 <= float_value < 0.05:
            return "PSA-10"
        elif 0.05 <= float_value < 0.1:
            return "PSA-9.5"
        elif 0.1 <= float_value < 0.2:
            return "PSA-9"
        elif 0.2 <= float_value <= 0.3:
            return "PSA-8"
        elif 0.3 <= float_value <= 0.4:
            return "PSA-7"
        elif 0.4 <= float_value <= 0.95:
            return "PSA-6"
        elif 0.95 <= float_value <= 1:
            return "WTF"
        else:
            return "Out of Range"


