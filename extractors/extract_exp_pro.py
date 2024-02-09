import re

def extract_exp_pro(content):
  exp_pro = content.split("ExpériencesProfessionnelles")[1]
  data = exp_pro.split(',')
  cleaned_array = []
  for el in data:
      if(el.strip() != "'" and el.strip() != "''" and el.strip() != '/'):
          cleaned_array.append(el.strip())

  index_adresse = None
  for i, item in enumerate(cleaned_array):
      if '48 rue Jacques Dulud - 92200 Neuilly' in item:
          index_adresse = i
          break

  if index_adresse is not None:
      cleaned_array = cleaned_array[:index_adresse]

  #parse_raw_data(cleaned_array)
  return []


def parse_raw_data(raw_data):
    # print(raw_data)
    experiences = []
    current_experience = {}

    for line in raw_data:
        # print("LINE ===> " + line.strip())
        if re.search('PROJET', line):
            print('HEEEERE')
            if current_experience:
                experiences.append(current_experience)
                print('WHAAAAAT ' + str(re.search(r"'(.*?)'", line)))

            current_experience = {"achievements": {}}
            current_experience["company"] = re.search(r"'(.*?)'", line).group(1)
            date_match = re.search(r"'(\w+ \d{4})", line)
            current_experience["startDate"] = date_match.group(1) if date_match else ""
            date_match = re.search(r'à (aujourd’hui|\w+ \d{4})', line)
            current_experience["endDate"] = date_match.group(1) if date_match else ""
        elif re.search('RÉALISATIONS', line):
            current_experience["missionSummary"] = re.search(r"'(.*?)'", line).group(1)
        elif "'ENVIRONNEMENT '" in line:
            current_experience["ENVIRONNEMENT"] = re.search(r"'(.*?)'", line).group(1)
        elif "'RÉALISATIONS : '" not in line and "'ENVIRONNEMENT '" not in line:
            achievement = re.search(r"'(.*?)'", line)
            # if achievement:
            #     current_experience["achievements"][achievement.group(1)] = ""

    if current_experience:
        experiences.append(current_experience)

    print(experiences)
    return {"experiences": experiences}


