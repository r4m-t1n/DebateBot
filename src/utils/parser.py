from utils.redis_utils import get_raw_subjects

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

def check_triggers(text: str, triggers: list[str]):
    for trigger in triggers:
        if trigger.lower() in text.lower():
            return True
    return False

def parse_subjects(subjects: list[list]):
    unique_subjects = set()

    for level_class in subjects:
        for subject in level_class:
            if subject:
                unique_subjects.add(subject)
    if not unique_subjects:
            return "No subjects registered."

    subjects_text = str()
    for subject in unique_subjects:
        subjects_text += f"- {subject}\n"

    return subjects_text

async def export_subjects():
    subjects = list()

    crtiticisms = await get_raw_subjects("criticism")
    defendants = await get_raw_subjects("defendant")

    for level in range(1, 6):
        for subject in crtiticisms[level-1]:
            subjects.append(
                "- Subject: {} | Mode: criticism | Level: {}".format(
                    subject, level
                )
            )
    
        for subject in defendants[level-1]:
            subjects.append(
                "- Subject: {} | Mode: defendant | Level: {}".format(
                    subject, level
                )
            )
    return subjects