def cutString(text, size, hasDots=True):
    #size is desired size
    if len(text) <= size:
        return text
    if hasDots:
        return (text)[:len(text)-(len(text)-size+3)] + "..."
    return (text)[:len(text)-(len(text)-size)]