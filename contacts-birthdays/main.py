import csv
from datetime import datetime

dateTimeObj = datetime.now()
dateTimeStr = f'{dateTimeObj.year}-{dateTimeObj.month}-{dateTimeObj.day}-{dateTimeObj.hour}-{dateTimeObj.minute}'

# variables
eventflag = False
bdayflag = False
totalbdays = 0
bdaydict = {}
birthdate_index = 14
num_first_contact_row = 6
line_count = 0

final_filename = f'{dateTimeStr}_contacts_with_bdays.csv'
calendar_file_path = 'gabbycalendar.csv'
contacts_file_path = 'contacts.csv'


def formatDate(caldate):
    # calendar date format YYYYMMDD
    # contacts date format --MM-DD
    year = caldate[0:4]
    month = caldate[4:6]
    day = caldate[6:8]

    contdate = ' --' + month + '-' + day
    return contdate


def addToBdayDict(person_name, person_bday):
    global totalbdays
    person_name = person_name.lower()
    formatted_bday = formatDate(person_bday)
    if person_name in bdaydict:
        dup_bday = bdaydict[person_name]
        if bool(input(
                f'{person_name} is already added with bday {dup_bday}. Are you trying to add someone different or change bday to {formatted_bday}? Type y or hit enter for no.')):
            person_name = input('What\'s the full name? ')
            bdaydict[person_name] = formatted_bday
            totalbdays += 1
        else:
            # name was already added so don't do anything
            pass
    else:
        bdaydict[person_name] = formatted_bday
        totalbdays += 1


def addBirthdatesToContactList(your_bday_dictionary, your_contact_reader, your_contact_file, your_final_writer):
    global birthdate_index
    global line_count
    num_matches = 0
    subsearch_dict = {}
    missing_contacts_dict = {}

    for key in your_bday_dictionary:
        matchless = True
        print(f'-- searching for {key}')
        for contact_row in your_contact_reader:

            # set up header line of output file
            if line_count < 1:
                your_final_writer.writerow(contact_row)

            full_name = contact_row[0].lower()
            # print(full_name)

            if key in full_name:
                print(f'Found a potential match! {key} with birthday {your_bday_dictionary[key]} and {full_name}')
                if bool(input('Is this a match? Type y or enter to keep searching.')):
                    # add the full row with birthday populated to new file
                    row_to_add = contact_row
                    row_to_add[birthdate_index] = your_bday_dictionary[key]  # add birthdate to the contact entry

                    your_final_writer.writerow(row_to_add)
                    your_contact_file.seek(
                        num_first_contact_row)  # return to beginning of contact file to search for next person
                    matchless = False
                    num_matches += 1

                    break  # match was found, no longer need to search
            line_count += 1

        if matchless:
            alt_name = input(f'Couldn\'t find {key} in your contacts. Type an alternate name or press enter to skip.')
            if alt_name:
                subsearch_dict[alt_name] = your_bday_dictionary[key]
            else:
                missing_contacts_dict[key] = your_bday_dictionary[key]

            your_contact_file.seek(
                num_first_contact_row)  # return to beginning of contact file to search for next person

    if subsearch_dict:
        extra_matches, extra_missing_contacts_dict = addBirthdatesToContactList(subsearch_dict, your_contact_reader,
                                                                                your_contact_file, your_final_writer)
        num_matches = num_matches + extra_matches
        for extra in extra_missing_contacts_dict:
            missing_contacts_dict[extra] = extra_missing_contacts_dict[extra]
    # rerun function on subdict

    return num_matches, missing_contacts_dict


# CSV walking
with open(calendar_file_path, encoding='Latin1') as cal_file:
    cal_reader = csv.reader(cal_file, delimiter=',')

    with open(contacts_file_path, encoding='Latin1') as cont_file:
        contact_reader = csv.reader(cont_file, delimiter=',')
        with open(final_filename, 'w', newline='') as final_file:
            final_writer = csv.writer(final_file)

            for row in cal_reader:
                # print(row)

                c1 = row[0]
                c2 = row[1]
                if c1 == 'BEGIN' and c2 == 'VEVENT':
                    eventflag = True
                elif c1 == 'END' and c2 == 'VEVENT':
                    eventflag = False
                    bdayflag = False

                if eventflag:
                    if c1 == 'DTSTART;VALUE=DATE':
                        date = c2
                    elif c1 == 'RRULE':
                        if 'FREQ=YEARLY' in c2:
                            bdayflag = True
                    elif c1 == 'SUMMARY' and bdayflag:
                        if '\'s birthday' in c2 or '\'s Birthday' in c2:
                            name = c2.split('\'')[0]
                            # print(c2, ' ', name, ' ', date)

                            if ' ' in name or len(
                                    name) < 3:  # entry may have more than one name or is too short to be nicely searchable
                                multibday = input(
                                    f'Is "{name}" more than one person or do you want to rename? Type names separated by commas or hit enter to skip. ')
                                # print(multiname)
                                if multibday:
                                    multibday = multibday.split(',')
                                    for person in multibday:
                                        addToBdayDict(person, date)
                                else:
                                    addToBdayDict(name, date)

                            else:
                                addToBdayDict(name, date)

            # START MATCHING BDAYS TO CONTACT LIST
            print('---------------------------------------------')
            print('Time to add birthdates to your contact list!')
            print('---------------------------------------------')
            num_birthdates_added, not_in_contacts = addBirthdatesToContactList(bdaydict, contact_reader, cont_file,
                                                                               final_writer)

# summary of what was done
print('------------')
print('All done! :)')
print('------------')
print(f'Extracted {len(bdaydict)} birthdates from your calendar.')
print(f'Matched {num_birthdates_added}/{len(bdaydict)} birthdates in your contacts')
print(f'The remaining {len(not_in_contacts)} people weren\'t in your contacts')
for x in not_in_contacts:
    print(x, ' ', not_in_contacts[x])
