def extract_titles(markdown):
    if "#" not in markdown:
        raise Exception("No header to remove")
    
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("# ").strip()
    
    raise Exception("No h1 header found")