import Levenshtein
import re
import json
import pickle

all_types = {"ул.": "улица", "у.": "улица", "улица": "улица", "ул": "улица", "у": "улица",
                "шоссе":"шоссе", "ш.":"шоссе", "ш":"шоссе",
                "переулок":"переулок", "пер.":"переулок", "пер":"переулок",
                "проезд": "проезд", "пр.":"проспект", "пр":"проспект",
                "проспект":"проспект", "просп.":"проспект", "пр-кт":"проспект", "просп":"проспект",
                "набережная":"набережная", "наб.":"набережная", "наб":"набережная", 
                "площадь":"площадь", "пл.":"площадь", "пл":"площадь", 
                "бул.":"бульвар", "бул":"бульвар", "б-р":"бульвар", "бульвар":"бульвар", "бульв.":"бульвар",
                "аллея":"аллея", "ал.":"аллея", "ал":"аллея", 
                "парк":"парк", "км":"км", "слобода":"слобода",
                "вал":"вал", "гавань":"гавань", "линия":"линия",
                "коса":"коса", "канал":"канал", "кольцо":"кольцо", "спуск":"спуск",
                "дорога":"дорога", "дорожка":"дорожка", "дор.":"дорога",
                "тупик":"тупик", "остров":"остров", "переезд":"переезд",
                "поселок":"поселок", "посёлок":"поселок", 
                "город":"город", "г.":"город", "г":"город",
                "дом":"дом", "д":"дом", "д.":"дом",
                "корпус":"корпус", "корп.":"корпус", "корп":"корпус", "к.":"корпус", "к":"корпус",
                "строение":"строение", "стр.":"строение", "стр":"строение"}

towns_type = {"поселок":"поселок", "посёлок":"поселок", 
"город":"город", "г.":"город", "г":"город"}

street_types0 = {"ул.": "улица", "у.": "улица", "улица": "улица", "ул": "улица", "у": "улица"}
street_types = {"ул.": "улица", "у.": "улица", "улица": "улица", "ул": "улица", "у": "улица",
                "шоссе":"шоссе", "ш.":"шоссе", "ш":"шоссе",
                "переулок":"переулок", "пер.":"переулок", "пер":"переулок",
                "проезд": "проезд", 
                "проспект":"проспект", "просп.":"проспект", "пр-кт":"проспект", "просп":"проспект",
                "набережная":"набережная", "наб.":"набережная", "наб":"набережная", 
                "площадь":"площадь", "пл.":"площадь", "пл":"площадь", 
                "бул.":"бульвар", "бул":"бульвар", "б-р":"бульвар", "бульвар":"бульвар", "бульв.":"бульвар",
                "аллея":"аллея", "ал.":"аллея", "ал":"аллея", 
                "парк":"парк", "км":"км", "слобода":"слобода",
                "вал":"вал", "гавань":"гавань", "линия":"линия",
                "коса":"коса", "канал":"канал", "кольцо":"кольцо", "спуск":"спуск",
                "дорога":"дорога", "дорожка":"дорожка", "дор.":"дорога",
                "тупик":"тупик", "остров":"остров", "переезд":"переезд"}


city_names = {"спб", "санкт", "петербург", "питер", "санкт-петербург", "г.санкт-петербург"}

house_names = {"дом":"дом", "д":"дом", "д.":"дом"}
corp_names = {"корпус":"корпус", "корп.":"корпус", "корп":"корпус", "к.":"корпус", "к":"корпус"}
build_names = {"строение":"строение", "стр.":"строение", "стр":"строение"}
liter = {"литера":"литера"}

with open("./fullstack_django/backend_api/src/parse_good_adr.bin", "rb") as f:
    parse_good_adr = pickle.load(f)

with open("./fullstack_django/backend_api/src/adr_idx_by_streets.bin", "rb") as f:
    adr_idx_by_streets = pickle.load(f)

with open("./fullstack_django/backend_api/src/types_by_streets.bin", "rb") as f:
    types_by_street = pickle.load(f)
def expand_reduction(address):
    translation_table = str.maketrans("ё().", "е   ")
    tmp_adr = address.translate(translation_table).replace(",", " , ")
    res_adr = ""
    words = tmp_adr.split(" ")
    for w in words:
        if w == " ":
            continue
        if w.lower() in all_types.keys():
            res_adr += " " + all_types[w.lower()]
        else:
            res_adr += " " + w
    return res_adr

def find_letters_after_digits(string):
    pattern = r'\d([a-zA-Z])'
    matches = re.findall(pattern, string)

    return matches

def count_matching_letters(words):
    count = 0
    for chars in zip(*words):
        # Check if all characters in the group are the same
        if all(char == chars[0] for char in chars):
            count += 1
    return count


translation_table = str.maketrans("ё().,/", "е    -")

def new_parse(g_adrs, adr):
    tmp_adr = expand_reduction(adr[0].lower().translate(translation_table))
    words = tmp_adr.split(" ")
    new_words = []
    cntr_one = 0
    for w in words:
        if w in city_names or Levenshtein.distance(w, "россия") < 2 or w in all_types.keys():
            continue
        new_words.append(w)
    new_words = set(new_words) - set({""})
    best_intersect = -1
    best_adr = None
    for g_adr in g_adrs:
        intersec = new_words.intersection(g_adr["short_name"])
        # print(new_words, g_adr["short_name"], len(intersec))
        if len(intersec) > best_intersect:
            best_intersect = len(intersec)
            best_adr = g_adr
    return True, best_adr["full_name"], best_adr['target_building_id']


def double_code(good_adr_comp3, good_adr_comp2, adr):
    if len(good_adr_comp3) == 1:
        return True, good_adr_comp3[0]["full_name"], good_adr_comp3[0]['target_building_id']
    elif len(good_adr_comp3) > 1:
        return new_parse(good_adr_comp3, adr)
    return new_parse(good_adr_comp2, adr)

def find_address(adr):
    tmp_adr = adr.lower().translate(translation_table)
    tmp_adr = re.sub(r'(\d+|\D+)', r'\1 ', tmp_adr)
    words = tmp_adr.split(" ")
    mindist = 100
    good_adr_comp1 = []
    good_adr_comp2_5 = []
    good_adr_comp2 = []
    good_adr_comp3 = []
    fnd_str_types = False
    str_type = ""
    fnd_liter = False
    tmp_liter = ""
    for w in words:
        if w in street_types.keys():
            fnd_str_types = True
            str_type = street_types[w]
        if w in city_names or Levenshtein.distance(w, "россия") < 2 or w in all_types.keys():
            continue
        if w.isalpha() and len(w) < 3:
            tmp_liter = w
            fnd_liter = True
        str_name_set = set()
        for str_name in types_by_street.keys():
            street_lst = str_name.split(" ")
            street_lst = [x for x in street_lst if x != '']
            for street_name in street_lst:
                dist = Levenshtein.distance(w, street_name)
                if dist < 4 and (len(street_name) - dist) / len(street_name) >= 0.75:
                    if fnd_str_types == True:
                        for t in types_by_street[str_name]:
                            if str_type == t:
                                str_name_set.update({str_name})
                    else:
                        str_name_set.update({str_name})
                    if dist < mindist:
                        mindist = dist
        for str_name in str_name_set:
            street_lst = str_name.split(" ")
            street_lst = [x for x in street_lst if x != '']
            if len(street_lst) == 1:
                dist = Levenshtein.distance(w, street_lst[0])
                if dist > mindist:
                    str_name_set = str_name_set - {str_name}
        for str_name in str_name_set:
            for idx in adr_idx_by_street[str_name]:
                good_adr_comp1.append(parse_good_adr[idx])

    if len(good_adr_comp1) == 1:
        return True, good_adr_comp1[0]["full_name"], good_adr_comp1[0]['target_building_id']
    elif len(good_adr_comp1) > 1:
        numbers = re.findall(r'\d+', tmp_adr)
        if len(numbers) == 0:
            return False, "", -1
        for good_adr in good_adr_comp1:
            for num in numbers:
                if good_adr["house"] == num:
                    good_adr_comp2.append(good_adr)
        if len(good_adr_comp2) == 1:
            return True, good_adr_comp2[0]["full_name"], good_adr_comp2[0]['target_building_id']
        elif len(good_adr_comp2) > 1:
            if fnd_liter:
                for good_adr in good_adr_comp2:
                    if good_adr["liter"] == tmp_liter:
                        good_adr_comp2_5.append(good_adr)
                if len(good_adr_comp2_5) == 1:
                    return True, good_adr_comp2_5[0]["full_name"], good_adr_comp2_5[0]['target_building_id']
                elif len(good_adr_comp2_5) > 1:
                    good_adr_comp2 = good_adr_comp2_5
            if len(numbers) > 1:
                for good_adr in good_adr_comp2:
                    for num in numbers:
                        if good_adr["corp"] == num:
                            good_adr_comp3.append(good_adr)
                return double_code(good_adr_comp3, good_adr_comp2, adr)
            # return new_parse(good_adr_comp2, adr)
            for good_adr in good_adr_comp2:
                if good_adr['corp'] == "undefined" or good_adr['corp'] == '1':
                    if fnd_liter:
                        good_adr_comp3.append(good_adr)
                    elif good_adr['liter'] == "undefined" or good_adr['liter'] == 'а':
                        good_adr_comp3.append(good_adr)
            return double_code(good_adr_comp3, good_adr_comp2, adr)
        else:
            return new_parse(good_adr_comp1, adr)
    else:
        return False, "", -1