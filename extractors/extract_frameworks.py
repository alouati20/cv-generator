def extract_frameworks(content):
  return content.split("Frameworks")[1].split("SGBD")[0] + content.split("SGBD")[1].split("IDE")[0]