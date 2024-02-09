
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

  return []