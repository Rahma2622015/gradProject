ip="https://192.168.1.5:3000"

base_ssl=r"E:\gradProject"

cert_loc=fr"{base_ssl}/cert.crt"
key_loc=fr"{base_ssl}/private.key"

base_arabic_ai = r"E:\gradProject\Ai\ArabicAi"
base_english_ai = r"E:\gradProject\Ai\EnglishAi"
base_recommendation = r"E:\gradProject\Ai\Recommendation\English"
base_arabic_recommendation = r"E:\gradProject\Ai\Recommendation\Arabic"


MapDataLocationAr = fr"{base_arabic_ai}\MapData.json"
MapData2LocationAr=fr"{base_arabic_ai}\NewMapData.json"
arabic_word = fr"{base_arabic_ai}\arabic_words.txt"
ResponseDataLocationAr = fr"{base_arabic_ai}\response.json"
NamesInCorrectArabic = fr"{base_arabic_ai}\arabic_names.txt"
CourseNameArabic = fr"{base_arabic_ai}\اسماء المواد.txt"


MapDataLocationEn = fr"{base_english_ai}\map.json"
ResponseDataLocationEn = fr"{base_english_ai}\response.json"
Bigrams = fr"{base_english_ai}\\bigram.txt"
NamesinCorrectEnglish = fr"{base_english_ai}\Names.txt"
courseLocation = fr"{base_english_ai}\courses.txt"
MapData2LocationEn = fr"{base_english_ai}\Newmap.json"

ResponseDataLocationRE = fr"{base_recommendation}\responseExamReco.json"
MapDataLocationRE = fr"{base_recommendation}\mapR.json"
RecomLocation = fr"{base_recommendation}\courses.json"

ArResponseDataLocationRE = fr"{base_arabic_recommendation}\AraResponseEx.json"

ResponseDataDocLocation=fr"{base_recommendation}\responseExamDoc.json"

ArResponseDataDocLocationRE = fr"{base_arabic_recommendation}\ArResponseExamDoc.json"