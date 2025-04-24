ip="https://192.168.1.11:3000"

base_ssl=r"D:/gradProject/ssl11"

cert_loc=fr"{base_ssl}/certificate.crt"
key_loc=fr"{base_ssl}/private.key"


base_arabic_ai = r"D:\gradProject\Ai\ArabicAi"
base_english_ai = r"D:\gradProject\Ai\EnglishAi"
base_recommendation = r"D:\gradProject\Ai\Recommendation\English"
base_arabic_recommendation = r"D:\gradProject\Ai\Recommendation\Arabic"

MapDataLocationAr = fr"{base_arabic_ai}\MapData.json"
arabic_word = fr"{base_arabic_ai}\arabic_words.txt"
ResponseDataLocationAr = fr"{base_arabic_ai}\response.json"
NamesinCorrectArabic = fr"{base_arabic_ai}\arabic_names.txt"
subjectNameLocation = fr"{base_arabic_ai}\subject_names.txt"
CourseNameArabic = fr"{base_arabic_ai}\اسماء المواد.txt"



MapDataLocationEn = fr"{base_english_ai}\map.json"
ResponseDataLocationEn = fr"{base_english_ai}\response.json"
Bigrams = fr"{base_english_ai}\bigrams.txt"
NamesinCorrectEnglish = fr"{base_english_ai}\Names.txt"
courseLocation = fr"{base_english_ai}\courses.txt"
MapData2LocationEn = fr"{base_english_ai}\Newmap.json"

ResponseDataLocationRE = fr"{base_recommendation}\responseExamReco.json"
MapDataLocationRE = fr"{base_recommendation}\mapR.json"
RecomLocation = fr"{base_recommendation}\courses.json"

ArResponseDataLocationRE = fr"{base_arabic_recommendation}\AraResponseEx.json"
