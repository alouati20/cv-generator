def extract_formation(content):
    list = ["Compétences", "Skills", "Connaissances"]
    result = []

    for item in list:
        if item in content:
            formation_data = content.split("Formation")[1].split(item)[0]
            data = formation_data.split(',')
            cleaned_array = []
            for el in data:
                if(el.strip() != "'" and el.strip() != "''"):
                    cleaned_array.append(el.strip())

            for i in range(0, len(cleaned_array), 2):
                date = cleaned_array[i].strip("' :")
                title = cleaned_array[i+1].strip("'")
                result.append({"date": date, "title": title})

    return result