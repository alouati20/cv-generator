def extract_certifications(content):
  cleaned_text = content.split("Certifications")[1].split("Formation")[0]
  data = cleaned_text.split(',')
  cleaned_array = []
  for el in data:
        if(el.strip() != "'" and el.strip() != "''"):
            cleaned_array.append(el.strip())
  result = []

  for i in range(0, len(cleaned_array), 2):
        date = cleaned_array[i].strip("' :")
        name = cleaned_array[i+1].strip("'")
        result.append({"date": date, "name": name})


  return result
  # certification_date = cleaned_text.split(':')[0].strip()
  # certification_name = cleaned_text.split(':')[1]

  # # Format the certification data as per the JSON schema
  # certification = {
  #     "date": certification_date,
  #     "name": certification_name.strip(", '")
  # }
  # return [certification]