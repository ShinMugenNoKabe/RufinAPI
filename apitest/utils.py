def clean_string(string: str) -> str:
    cleaned_string = "".join(char for char in string if char.isalnum())

    return cleaned_string
