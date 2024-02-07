def extract_skills(content):
    list = ["Compétences", "Skills", "Connaissances"]
    competence_content = ""
    result = []
    for item in list:
      if item in content:
          competence_content = content.split(item)[1].split("ExpériencesProfessionnelles")[0]

    #print(competence_content)

    data = competence_content.split("', '")
    cleaned_array = []
    for el in data:
        if(el.strip() != "'" and el.strip() != "''" and el.strip() != ""):
            cleaned_array.append(el.strip())

    #print("====================================================================")
    #print(cleaned_array)


    for i in range(0, len(cleaned_array), 2):
            type = cleaned_array[i].strip("':")
            skills = [skill for skill in cleaned_array[i+1].split("'")]
            result.append({"type": type, "skills": skills})
    
    return result