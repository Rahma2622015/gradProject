import re
import variables

class ArabicNormalize:
    def __init__(self):
        with open(variables.CourseNameArabic, "r", encoding="utf-8") as f:
            self.correct_names = set(f.read().splitlines())
            self.preserve_al_words = self.correct_names



        self.replacement_patterns = [
            (r"\bانا\b", "أنا"),
            (r"\bان\b", "أن"),
            (r"\bالى\b", "إلى"),
            (r"\bهوا\b", "هو"),
            (r"\bانتي\b", "أنتِ"),
            (r"\bانت\b", "أنت"),
            (r"\bمش\b", "ليس"),
            (r"\bكويس\b", "جيد"),
            (r"\bحلو\b", "جميل"),
            (r"\bحلوة\b", "جميلة"),
            (r"\نشوي\b", "نشوى"),
            (r"\bعاوز\b", "أريد"),
            (r"\bبدي\b", "أريد"),
            (r"\bلو سمحت\b", "من فضلك"),
            (r"\bشكرا\b", "شكراً"),
            (r"\bاستاذ\b", "أستاذ"),
            (r"\bاستاذة\b", "أستاذ"),
            (r"\الاستاذة\b", "أستاذ"),
            (r"\الاستاذه\b", "أستاذ"),
            (r"\استاذه\b", "أستاذ"),
            (r"\الاستاذ\b", "أستاذ"),
            (r"\الدكتورة\b", "دكتور"),
            (r"\الدكتوره\b", "دكتور"),
            (r"\دكتور\b", "دكتور"),
            (r"\دكتوره\b", "دكتور"),
            (r"\دكتورة\b", "دكتور"),
            (r"\ماده\b", "مادة"),
            (r"\هى\b", "هي"),
            (r"\bمعيد\b", "مدرس مساعد"),
            (r"\bمعيدة\b", "مدرسة مساعدة"),
            (r"\الالي\b"," الالى")
        ]

        self.diacritics = re.compile(r'[\u064B-\u0652]')
        self.non_arabic_symbols = re.compile(r'[^\w\s\u0600-\u06FF]')

    def replace_heh_with_ta(self, word: str) -> str:
        if word.endswith("ه"):
            possible = word[:-1] + "ة"
            if possible in self.correct_names:
                return possible
        return word


    def replace_ending_y_with_alef_maqsura(self, word: str) -> str:
        if word.endswith("ى") and len(word) > 2:
            return word[:-1] + "ي"
        return word

    def remove_diacritics(self, text: str) -> str:
        return self.diacritics.sub('', text)

    def remove_repeated_chars(self, text: str) -> str:
        return re.sub(r'(.)\1{2,}', r'\1', text)

    def remove_non_arabic_symbols(self, text: str) -> str:
        return self.non_arabic_symbols.sub('', text)

    def normalize(self, message: str) -> str:
        message = self.remove_diacritics(message)
        for pattern, replacement in self.replacement_patterns:
            message = re.sub(pattern, replacement, message)
        message = self.remove_repeated_chars(message)
        message = self.remove_non_arabic_symbols(message)
        message = re.sub(r'\s+', ' ', message).strip()

        words = message.split()
        normalized_words = []
        for word in words:
            if word in self.correct_names:
                normalized_words.append(word)
            else:
                word = self.replace_ending_y_with_alef_maqsura(word)
                normalized_words.append(word)

        return " ".join(normalized_words)

