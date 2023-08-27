import re
import json

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

towns_type = {"поселок":"поселок", "посёлок":"поселок", 
"город":"город", "г.":"город", "г":"город"}

city_names = {"спб", "санкт", "петербург", "питер", "санкт-петербург", "г.санкт-петербург"}

house_names = {"дом":"дом", "д":"дом", "д.":"дом"}
corp_names = {"корпус":"корпус", "корп.":"корпус", "корп":"корпус", "к.":"корпус", "к":"корпус"}
build_names = {"строение":"строение", "стр.":"строение", "стр":"строение"}
liter = {"литера":"литера"}

with open("./fullstack_django/backend_api/src/parse_good_adr.json", "r", encoding="utf-8") as file:
    parse_good_adr = json.load(file)
parse_good_adr = eval(parse_good_adr)

types_by_towns = dict()
with open("./fullstack_django/backend_api/src/types_by_towns.json", "r", encoding="utf-8") as file:
    types_by_towns = json.load(file)

def parsing(good_addresses, id):
    good_addresses = list(good_addresses)
    id = list(id)
    parse_good_adr = []
    adr_idx_by_street = dict()
    types_by_street = dict()
    for i in range(len(good_addresses)):
        adr1 = good_addresses[i].lower().split(", ")
        adr = adr1.copy()
        tmp_town = "undefined"
        tmp_subtown = "undefined"
        tmp_street = "undefined"
        tmp_street_type = "undefined"
        tmp_corp = "undefined"
        tmp_build = "undefined"
        tmp_liter = "undefined"
        short_name = []
        town_find = False
        street_find = False
        house_find = False
        corp_find = False
        build_find = False
        liter_find = False
        for part in adr1:
            if part in city_names:
                adr.remove(part)
                continue
            words0 = part.split(" ")
            short_name.extend(words0)
            words = words0
            tmp_type_town = "undefined"
            for w in words:
                if not town_find and w in towns_type.keys():
                    words.remove(w)
                    tmp_type_town = towns_type[w]
                    town_find = True
                    tmp_town = ""
                    for w in words:
                        tmp_town += w
                    types_by_towns[tmp_town] = tmp_type_town
                    adr.remove(part)
                    break
                if not street_find and w in street_types.keys():
                    if w != 'линия':
                        words.remove(w)
                    tmp_street_type = street_types[w]
                    tmp_street = ""
                    for w in words:
                        tmp_street += " " + w
                    if tmp_street in street_types0.keys():
                        words.append(w)
                        continue
                    if tmp_street in types_by_street.keys():
                        types_by_street[tmp_street].update({tmp_street_type})
                        adr_idx_by_street[tmp_street].append(i)
                    else:
                        types_by_street[tmp_street] = {tmp_street_type}
                        adr_idx_by_street[tmp_street] = [i]
                    adr.remove(part)
                    street_find = True
                    break
                if not house_find and w in house_names.keys():
                    house_find = True
                    words.remove(w)
                    if re.match(r'^(?=.*[а-я])(?=.*\d).+$', words[0]):
                        words[0] = re.findall(r'\d+', words[0])
                    if "/" in words[0]:
                        tmp_house = words[0].split("/")[0]
                        corp_find = True
                        tmp_corp = words[0].split("/")[1]
                    else:
                        tmp_house = words[0]
                    adr.remove(part)
                    break
                if not corp_find and w in corp_names.keys():
                    corp_find = True
                    words.remove(w)
                    tmp_corp = words[0]
                    adr.remove(part)
                    break
                if not build_find and w in build_names.keys():
                    build_find = True
                    words.remove(w)
                    tmp_build = words[0]
                    adr.remove(part)
                    break
                if not liter_find and w in liter.keys():
                    liter_find = True
                    words.remove(w)
                    tmp_liter = words[0]
                    adr.remove(part)
                    break
            if town_find and not street_find and tmp_town not in part:
                tmp_subtown = part
                if part in adr:
                    adr.remove(part)
        

        parse_good_adr.append(dict({"town":tmp_town, "subtown":tmp_subtown,
        "street":tmp_street, "street_type":tmp_street_type, "house":tmp_house,
        "corp":tmp_corp, "build":tmp_build, "liter":tmp_liter, "full_name":good_addresses[i], 
        "short_name": set(short_name), "target_building_id":id[i]}))

    json_data = json.dumps(str(parse_good_adr))
    with open("./fullstack_django/backend_api/src/parse_good_adr.json", "w") as file:
        file.write(json_data)
    json_data = json.dumps(types_by_towns)
    with open("./fullstack_django/backend_api/src/types_by_towns.json", "w") as file:
        file.write(json_data)