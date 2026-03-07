def split_args(text: str):
    args = list()

    word = ''
    big_word = False

    text = text.strip()

    for i in text:
        if i == '"':
            if word == '': #the beginning of the word
                big_word = True
                continue
            else: #the end of the word
                args.append(word)
                word = ''
                big_word = False
                continue

        if big_word:
            word += i
            continue

        if i == ' ':
            if word != '':
                args.append(word)
                word = ''
            continue

        word += i
    
    if word:
        args.append(word)

    return args