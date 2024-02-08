def extract_content_without_style(json_content):
    text_styles = []
    def recursive_extract(element):
        if isinstance(element, dict):
            if "textRun" in element:
                text_run = element["textRun"]
                if "content" in text_run and text_run["content"] not in ["\n", " ", "\\x0b"]:
                    text_styles.append(text_run["content"].replace("\\x0b", ""))
            for key, value in element.items():
                recursive_extract(value)
        elif isinstance(element, list):
            for item in element:
                recursive_extract(item)
    recursive_extract(json_content)
    return text_styles