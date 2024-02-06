def extract_ide(content):
  return content.split("IDE")[1].split("Outils")[0].strip(', ')