def extract_skills(content):
    return content.split("Langages")[1].split("Frameworks")[0]