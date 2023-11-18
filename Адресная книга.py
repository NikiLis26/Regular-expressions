    
import re
import csv

def normalize_phone(phone):
    # Приведение телефона к формату +7(999)999-99-99 доб.9999
    match = re.match(r"(\+?\d)?\s*[\(\-]?(?P<Code>\d{3})[\)\-]?\s*(?P<First>\d{3})[\-\s]*(?P<Second>\d{2})[\-\s]?(?P<Third>\d{2})\s*доб.?\s*(\d+)?", phone)
    if match:
        return f"+7({match.group('Code')}){match.group('First')}-{match.group('Second')}-{match.group('Third')} доб.{match.group('Fourth') if match.group('Fourth') else ''}"
    else:
        return phone

def main():
    with open("phonebook_raw.csv", "r") as file:
        data = list(csv.reader(file))

    contacts_dict = {}

    for row in data:
        # Помещение фамилии, имени и отчества в соответствующие поля
        lastname, firstname, surname = re.match(r"(.+),\s*(.+)\s+(\w\.?)", row[0]).groups()
        organization = row[1]
        position = row[2]
        phone = normalize_phone(row[5])
        email = row[6]

        key = f"{lastname}_{firstname}_{surname}"

        if key not in contacts_dict:
            contacts_dict[key] = [lastname, firstname, surname, organization, position, phone, email]
        else:
            # Объединение записей о человеке
            contacts_dict[key][3] = contacts_dict[key][3] if contacts_dict[key][3] else organization
            contacts_dict[key][4] = contacts_dict[key][4] if contacts_dict[key][4] else position
            contacts_dict[key][5] = contacts_dict[key][5] if contacts_dict[key][5] else phone
            contacts_dict[key][6] = contacts_dict[key][6] if contacts_dict[key][6] else email

    contacts_list = [contact for contact in contacts_dict.values()]

    with open("phonebook.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(contacts_list)

if __name__ == "__main__":
    main()
