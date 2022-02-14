from pprint import pprint
import csv
import re


if __name__ == '__main__':
    with open("phonebook_raw.csv") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    my_list = []
    for contacts in contacts_list:
        temp_list = []
        my_str = ','.join(contacts)
        pattern = r"(\+7|8)(\s*|)(\(|)(\d{3})(\)|)(\s*|-)(\d{3})(\s*|-)(\d{2})(\s*|-)(\d{2})"
        subst = r"+7(\4)\7-\9-\11"
        telephone = re.sub(pattern, subst, my_str)

        pattern = r"\(?(доб\.)\s*(\d+)\)?"
        subst = r"\1\2"
        telephone_2 = re.sub(pattern, subst, telephone)

        pattern = r"^([а-яА-Я]+).(\w+)(,| )+((\w+)?)(,| )+((\w+)?)(,| )+([^abd-zA-Z,+]+)?(,| )+" \
                  r"(\+7[^,]+)?(,| )+([a-zA-Z0-9@.]+)?"
        subst = r"\1,\2,\5,\8,\10,\12,\14"
        structure = re.sub(pattern, subst, telephone_2)

        temp_list += structure.split(',')
        my_list.append(temp_list)

    contacts_dict = {}
    for name in my_list:
        k = 0
        if name[0] not in contacts_dict:
            contacts_dict[name[0]] = []
            for record in name:
                contacts_dict[name[0]].append(record)
        else:
            temp_list = []
            for record in contacts_dict[name[0]]:
                if record == '':
                    temp_list.append(k)
                    contacts_dict[name[0]].pop(k)
                    contacts_dict[name[0]].insert(k, name[k])
                    k += 1
                else:
                    k += 1
    new_contacts_list = []
    for i in contacts_dict.values():
        new_contacts_list.append(i)
    pprint(new_contacts_list)

    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(new_contacts_list)
