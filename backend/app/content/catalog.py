import copy
from app.core.config import settings

LEVELS = [
    {"id": "beginner", "name": "Beginner"},
    {"id": "intermediate", "name": "Intermediate"},
    {"id": "advanced", "name": "Advanced"},
]

def _fb(tid: str, sn: int, qi: int, prompt: str, correct: str):
    return {"id": f"{tid}_s{sn}_q{qi}", "type": "fill_blank", "prompt": prompt, "correct": correct.strip().lower()}

def _mcq(tid: str, sn: int, qi: int, prompt: str, correct: str, opts: list[str]):
    return {"id": f"{tid}_s{sn}_q{qi}", "type": "mcq", "prompt": prompt, "options": opts, "correct": correct.strip().lower()}

def _cor(tid: str, sn: int, qi: int, wrong: str, correct: str, decoy: str):
    opts = [correct, decoy, wrong]
    seen = []
    for o in opts:
        if o not in seen:
            seen.append(o)
    return {"id": f"{tid}_s{sn}_q{qi}", "type": "correction", "prompt": f"Pick the right sentence: {wrong}", "options": seen, "correct": correct.strip().lower()}

def _build(tid: str, sn: int, rows: list):
    out = []
    for i, r in enumerate(rows):
        if r[0] == "fb":
            out.append(_fb(tid, sn, i, r[1], r[2]))
        elif r[0] == "mcq":
            out.append(_mcq(tid, sn, i, r[1], r[2], r[3]))
        else:
            out.append(_cor(tid, sn, i, r[1], r[2], r[3]))
    return out

def _alt_sn(tid: str, sn: int, rows0: list, rows1: list):
    return _build(tid, sn, (rows0, rows1)[sn % 2])

def _set_have_has(tid: str, sn: int):
    p = ["a pen", "two cats", "a new job", "many friends", "no money", "a cold", "a red bag", "an old car", "a big house", "a small dog", "three keys", "a good idea", "a question", "a ticket", "a laptop"]
    sg = ["He", "She", "It", "My dad", "Anna", "The shop", "Tom", "This phone", "Maria", "The team"]
    pl = ["I", "We", "They", "You", "The boys", "My parents", "Those kids", "My friends", "These people", "The students"]
    lp = len(p)
    qs = []
    qi = 0
    for i in range(5):
        qs.append(_fb(tid, sn, qi, f"{pl[i]} ___ {p[(i + sn) % lp]}.", "have"))
        qi += 1
    for i in range(5):
        qs.append(_fb(tid, sn, qi, f"{sg[i]} ___ {p[(i + 5 + sn) % lp]}.", "has"))
        qi += 1
    qs.append(_mcq(tid, sn, qi, "We ___ time to talk.", "have", ["have", "has", "is"]))
    qi += 1
    qs.append(_mcq(tid, sn, qi, "She ___ a brother in London.", "has", ["do", "has", "have"]))
    qi += 1
    qs.append(_cor(tid, sn, qi, "I has a bike.", "I have a bike.", "I having a bike."))
    qi += 1
    qs.append(_cor(tid, sn, qi, "They has a car.", "They have a car.", "They are a car."))
    qi += 1
    qs.append(_mcq(tid, sn, qi, "Choose the best line.", "My sister has a dog.", ["My sister have a dog.", "My sister has a dog.", "My sister having a dog."]))
    qi += 1
    qs.append(_fb(tid, sn, qi, f"{'You' if sn % 2 == 0 else 'They'} ___ a nice room.", "have"))
    return qs

def _set_do_does(tid: str, sn: int):
    qs = []
    qi = 0
    acts = ["homework", "the dishes", "yoga", "your best", "a break", "the cleaning", "exercise", "the shopping", "a favor", "work", "the report", "the talking", "the planning", "the driving", "the cooking"]
    la = len(acts)
    sg = ["He", "She", "It", "My boss", "Sam", "The cat", "Lisa", "This app"]
    pl = ["I", "We", "They", "You", "The workers", "My cousins", "Those drivers", "The chefs"]
    for i in range(6):
        qs.append(_fb(tid, sn, qi, f"{pl[i % len(pl)]} ___ {acts[(i + sn) % la]}.", "do"))
        qi += 1
    for i in range(4):
        qs.append(_fb(tid, sn, qi, f"{sg[i]} ___ {acts[(i + 6 + sn) % la]}?", "does"))
        qi += 1
    qs.append(_mcq(tid, sn, qi, "___ she play tennis?", "Does", ["Do", "Does", "Is"]))
    qi += 1
    qs.append(_mcq(tid, sn, qi, "___ you like tea?", "Do", ["Does", "Do", "Are"]))
    qi += 1
    qs.append(_cor(tid, sn, qi, "He don't work here.", "He doesn't work here.", "He doesn't works here."))
    qi += 1
    qs.append(_cor(tid, sn, qi, "She do the report.", "She does the report.", "She is the report."))
    qi += 1
    qs.append(_mcq(tid, sn, qi, "Pick the right question.", "Does it rain often?", ["Do it rains often?", "Does it rain often?", "Is it rain often?"]))
    qi += 1
    qs.append(_fb(tid, sn, qi, f"{'They' if sn % 2 == 0 else 'We'} ___ not want sugar.", "do"))
    return qs

def _set_have_vs_do(tid: str, sn: int):
    pairs0 = [
        ("I ___ a meeting at 3.", "have", ["have", "do", "make"]),
        ("I ___ my work at night.", "do", ["have", "do", "is"]),
        ("She ___ a headache.", "has", ["does", "has", "do"]),
        ("He ___ the talking.", "does", ["has", "does", "is"]),
        ("We ___ dinner now.", "have", ["do", "have", "are"]),
        ("They ___ their jobs well.", "do", ["have", "do", "has"]),
        ("You ___ a nice voice.", "have", ["do", "have", "does"]),
        ("He ___ a shower every day.", "has", ["does", "has", "do"]),
        ("I ___ the laundry on Sunday.", "do", ["have", "do", "has"]),
        ("She ___ a lot of books.", "has", ["does", "has", "do"]),
        ("We ___ fun at the party.", "have", ["do", "have", "make"]),
        ("___ you ___ a minute?", "Do", ["Do", "Have", "Are"]),
    ]
    pairs1 = [
        ("We ___ class at 9.", "have", ["have", "do", "make"]),
        ("She ___ the dishes after lunch.", "does", ["have", "does", "is"]),
        ("He ___ a sore throat.", "has", ["does", "has", "do"]),
        ("She ___ the presentation.", "does", ["has", "does", "is"]),
        ("They ___ lunch together.", "have", ["do", "have", "are"]),
        ("You ___ your best every day.", "do", ["have", "do", "has"]),
        ("I ___ brown eyes.", "have", ["do", "have", "does"]),
        ("She ___ breakfast at 7.", "has", ["does", "has", "do"]),
        ("We ___ the shopping on Friday.", "do", ["have", "do", "has"]),
        ("He ___ two phones.", "has", ["does", "has", "do"]),
        ("You ___ a great time.", "have", ["do", "have", "make"]),
        ("___ she ___ a pet?", "Does", ["Does", "Have", "Is"]),
    ]
    pairs = (pairs0, pairs1)[sn % 2]
    qs = []
    qi = 0
    for i, (pr, ok, opts) in enumerate(pairs[:12]):
        if i == 11:
            qs.append(_mcq(tid, sn, qi, pr, ok.lower(), [o.lower() for o in opts]))
        else:
            qs.append(_mcq(tid, sn, qi, pr, ok.lower(), [o.lower() for o in opts]))
        qi += 1
    qs.append(_cor(tid, sn, qi, "I do a car.", "I have a car.", "I am a car."))
    qi += 1
    qs.append(_cor(tid, sn, qi, "I have my homework.", "I do my homework.", "I make my homework."))
    qi += 1
    if sn % 2 == 0:
        qs.append(_fb(tid, sn, qi, "They ___ breakfast together.", "have"))
        qi += 1
        qs.append(_fb(tid, sn, qi, "He ___ not have a bike.", "does"))
    else:
        qs.append(_fb(tid, sn, qi, "We ___ dinner at home.", "have"))
        qi += 1
        qs.append(_fb(tid, sn, qi, "She ___ not have a car.", "does"))
    return qs

def _set_is_am_are(tid: str, sn: int):
    return _alt_sn(tid, sn, [
        ("fb", "I ___ happy today.", "am"),
        ("fb", "She ___ a teacher.", "is"),
        ("fb", "We ___ ready.", "are"),
        ("fb", "They ___ at home.", "are"),
        ("fb", "He ___ late.", "is"),
        ("mcq", "___ you okay?", "Are", ["Am", "Is", "Are"]),
        ("mcq", "___ I late?", "Am", ["Are", "Am", "Is"]),
        ("cor", "I is fine.", "I am fine.", "I are fine."),
        ("cor", "We is friends.", "We are friends.", "We am friends."),
        ("fb", "The keys ___ on the table.", "are"),
        ("fb", "This cake ___ sweet.", "is"),
        ("fb", "My brother and I ___ tall.", "are"),
        ("mcq", "The weather ___ nice.", "is", ["are", "is", "am"]),
        ("fb", "You ___ kind.", "are"),
        ("mcq", "___ it cold outside?", "Is", ["Are", "Am", "Is"]),
    ], [
        ("fb", "You ___ right about that.", "are"),
        ("fb", "Tom ___ a driver.", "is"),
        ("fb", "The girls ___ outside.", "are"),
        ("fb", "My parents ___ away.", "are"),
        ("fb", "Anna ___ busy.", "is"),
        ("mcq", "___ we ready to go?", "Are", ["Is", "Am", "Are"]),
        ("mcq", "___ this your coat?", "Is", ["Are", "Am", "Is"]),
        ("cor", "You is late.", "You are late.", "You am late."),
        ("cor", "He are tall.", "He is tall.", "He am tall."),
        ("fb", "The cups ___ in the sink.", "are"),
        ("fb", "This soup ___ hot.", "is"),
        ("fb", "My sister and he ___ cousins.", "are"),
        ("mcq", "The pizza ___ ready.", "is", ["are", "is", "am"]),
        ("fb", "We ___ glad to help.", "are"),
        ("mcq", "___ you at school now?", "Are", ["Is", "Am", "Are"]),
    ])

def _set_present_simple(tid: str, sn: int):
    verbs = [("work", "works"), ("live", "lives"), ("play", "plays"), ("study", "studies"), ("watch", "watches"), ("go", "goes"), ("eat", "eats"), ("read", "reads"), ("speak", "speaks"), ("help", "helps"), ("clean", "cleans"), ("walk", "walks"), ("talk", "talks"), ("listen", "listens"), ("open", "opens")]
    qs = []
    qi = 0
    a, b = verbs[sn % 15], verbs[(sn + 7) % 15]
    qs.append(_fb(tid, sn, qi, f"{'I' if sn % 2 == 0 else 'They'} ___ to work by bus.", a[0])); qi += 1
    qs.append(_fb(tid, sn, qi, f"{'She' if sn % 2 == 0 else 'He'} ___ math after school.", b[1])); qi += 1
    if sn % 2 == 0:
        qs.append(_mcq(tid, sn, qi, "They ___ football on Sundays.", "play", ["plays", "play", "playing"])); qi += 1
        qs.append(_mcq(tid, sn, qi, "He ___ TV in the evening.", "watches", ["watch", "watches", "watching"])); qi += 1
        qs.append(_fb(tid, sn, qi, "We ___ dinner at 7.", "eat")); qi += 1
        qs.append(_fb(tid, sn, qi, "It ___ a lot in winter.", "rains")); qi += 1
        qs.append(_cor(tid, sn, qi, "She go to school.", "She goes to school.", "She going to school.")); qi += 1
        qs.append(_cor(tid, sn, qi, "I works here.", "I work here.", "I working here.")); qi += 1
        qs.append(_mcq(tid, sn, qi, "___ he like coffee?", "Does", ["Do", "Does", "Is"])); qi += 1
        qs.append(_mcq(tid, sn, qi, "I ___ not understand.", "do", ["does", "do", "am"])); qi += 1
        qs.append(_fb(tid, sn, qi, "My dad ___ the news.", "reads")); qi += 1
        qs.append(_fb(tid, sn, qi, "The shop ___ at 9.", "opens")); qi += 1
        qs.append(_fb(tid, sn, qi, "You ___ too fast.", "talk")); qi += 1
        qs.append(_mcq(tid, sn, qi, "We ___ to music.", "listen", ["listens", "listen", "listening"])); qi += 1
        qs.append(_fb(tid, sn, qi, "The kids ___ in the park.", "play")); qi += 1
    else:
        qs.append(_mcq(tid, sn, qi, "The team ___ basketball on Tuesdays.", "plays", ["play", "plays", "playing"])); qi += 1
        qs.append(_mcq(tid, sn, qi, "She ___ films at night.", "watches", ["watch", "watches", "watching"])); qi += 1
        qs.append(_fb(tid, sn, qi, "He ___ lunch at noon.", "eats")); qi += 1
        qs.append(_fb(tid, sn, qi, "It often ___ in spring.", "snows")); qi += 1
        qs.append(_cor(tid, sn, qi, "He walk to work.", "He walks to work.", "He walking to work.")); qi += 1
        qs.append(_cor(tid, sn, qi, "She don't agree.", "She doesn't agree.", "She doesn't agrees.")); qi += 1
        qs.append(_mcq(tid, sn, qi, "___ she play piano?", "Does", ["Do", "Does", "Is"])); qi += 1
        qs.append(_mcq(tid, sn, qi, "We ___ not know.", "do", ["does", "do", "are"])); qi += 1
        qs.append(_fb(tid, sn, qi, "My mom ___ a novel.", "reads")); qi += 1
        qs.append(_fb(tid, sn, qi, "The cafe ___ at 8.", "opens")); qi += 1
        qs.append(_fb(tid, sn, qi, "They ___ too loud.", "talk")); qi += 1
        qs.append(_mcq(tid, sn, qi, "I ___ to podcasts.", "listen", ["listens", "listen", "listening"])); qi += 1
        qs.append(_fb(tid, sn, qi, "The dogs ___ in the yard.", "play")); qi += 1
    return qs

def _set_present_continuous(tid: str, sn: int):
    return _alt_sn(tid, sn, [
        ("fb", "I ___ reading a book.", "am"),
        ("fb", "She ___ cooking now.", "is"),
        ("fb", "They ___ waiting for the bus.", "are"),
        ("fb", "He ___ not listening.", "is"),
        ("mcq", "___ you studying?", "Are", ["Is", "Are", "Am"]),
        ("mcq", "What ___ he doing?", "is", ["are", "is", "do"]),
        ("cor", "I am work now.", "I am working now.", "I working now."),
        ("cor", "She are sleeping.", "She is sleeping.", "She sleeping."),
        ("fb", "We ___ having lunch.", "are"),
        ("fb", "It ___ raining.", "is"),
        ("fb", "The baby ___ crying.", "is"),
        ("mcq", "Look! They ___ run.", "are running", ["run", "are running", "running"]),
        ("fb", "I ___ looking for my keys.", "am"),
        ("fb", "You ___ talking too loud.", "are"),
        ("mcq", "He ___ TV right now.", "is watching", ["watches", "is watching", "watch"]),
    ], [
        ("fb", "We ___ fixing the bike.", "are"),
        ("fb", "He ___ typing an email.", "is"),
        ("fb", "The kids ___ playing outside.", "are"),
        ("fb", "She ___ not paying attention.", "is"),
        ("mcq", "___ they leaving soon?", "Are", ["Is", "Are", "Am"]),
        ("mcq", "What ___ you making?", "are", ["is", "are", "do"]),
        ("cor", "They is coming.", "They are coming.", "They coming."),
        ("cor", "I are thinking.", "I am thinking.", "I thinking."),
        ("fb", "You ___ holding the door.", "are"),
        ("fb", "The dog ___ barking.", "is"),
        ("fb", "My friends ___ chatting online.", "are"),
        ("mcq", "Watch! He ___ slip.", "is slipping", ["slip", "is slipping", "slipping"]),
        ("fb", "She ___ packing her bag.", "is"),
        ("fb", "I ___ not joking.", "am"),
        ("mcq", "She ___ music now.", "is listening to", ["listens", "is listening to", "listen"]),
    ])

def _set_plurals(tid: str, sn: int):
    qs = []
    qi = 0
    data = [
        ("one box / many ___", "boxes"), ("one child / many ___", "children"), ("one tooth / many ___", "teeth"),
        ("one person / two ___", "people"), ("this ___ (more than one)", "these"), ("that ___ (more than one)", "those"),
        ("I have two ___.", "cats"), ("She has three ___.", "books"), ("There are five ___.", "chairs"),
        ("many ___", "students"), ("two ___", "phones"), ("Pick right: There ___ two dogs.", "are"),
        ("Pick right: There ___ a dog.", "is"), ("These ___ my friends.", "are"), ("This ___ my friend.", "is"),
    ]
    if sn % 2 == 1:
        data = [
            ("one city / two ___", "cities"), ("one baby / two ___", "babies"), ("one knife / many ___", "knives"),
            ("one foot / two ___", "feet"), ("one man / two ___", "men"), ("one woman / two ___", "women"),
            ("many ___ on the desk", "papers"), ("two red ___", "cars"), ("Those ___ nice.", "are"),
            ("That ___ nice.", "is"), ("There ___ many cars.", "are"), ("There ___ a car.", "is"),
            ("These ___ not mine.", "are"), ("This ___ not mine.", "is"), ("How many ___?", "apples"),
        ]
    for i, (pr, ans) in enumerate(data):
        if i in (11, 12, 13, 9, 8):
            qs.append(_mcq(tid, sn, qi, pr, ans.lower(), [ans.lower(), "is" if ans == "are" else "are", "am"]))
        elif i in (4, 5):
            qs.append(_mcq(tid, sn, qi, pr, ans.lower(), [ans.lower(), "this", "that"]))
        else:
            qs.append(_fb(tid, sn, qi, pr, ans.lower()))
        qi += 1
    return qs

def _set_articles(tid: str, sn: int):
    qs = []
    qi = 0
    rows = [
        ("___ apple", "an"), ("___ university", "a"), ("___ hour", "an"), ("___ honest person", "an"),
        ("___ book", "a"), ("___ umbrella", "an"), ("___ European trip", "a"), ("___ egg", "an"),
        ("___ sun is bright.", "The"), ("___ water is cold.", "The"), ("___ cats are cute.", "The"),
        ("I need ___ pen.", "a"), ("She is ___ teacher.", "a"), ("It is ___ useful tool.", "a"), ("___ moon tonight", "The"),
    ]
    if sn % 2 == 1:
        rows = [
            ("___ orange", "an"), ("___ one-way street", "a"), ("___ ice cream", "an"), ("___ big idea", "a"),
            ("___ old man", "an"), ("___ young boy", "a"), ("___ elephant", "an"), ("___ car", "a"),
            ("___ Earth is round.", "The"), ("___ sky is blue.", "The"), ("___ information is free.", "The"),
            ("Can I have ___ coffee?", "a"), ("He is ___ engineer.", "an"), ("It was ___ accident.", "an"), ("___ best day", "The"),
        ]
    for pr, ans in rows:
        if ans in ("a", "an"):
            other = "an" if ans == "a" else "a"
            qs.append(_mcq(tid, sn, qi, pr, ans, [ans, other, "the"]))
        else:
            qs.append(_mcq(tid, sn, qi, pr, ans, [ans, "a", "an"]))
        qi += 1
    return qs

def _set_past_simple(tid: str, sn: int):
    return _alt_sn(tid, sn, [
        ("fb", "I ___ to the store yesterday.", "went"),
        ("fb", "She ___ her friend last night.", "called"),
        ("fb", "They ___ pizza for dinner.", "ordered"),
        ("mcq", "He ___ TV after work.", "watched", ["watch", "watched", "watching"]),
        ("mcq", "We ___ late.", "arrived", ["arrive", "arrived", "arriving"]),
        ("cor", "I goed home.", "I went home.", "I gone home."),
        ("cor", "She buyed a coat.", "She bought a coat.", "She buy a coat."),
        ("fb", "Did you ___ the email?", "send"),
        ("fb", "I did not ___ the answer.", "know"),
        ("mcq", "___ you see him?", "Did", ["Do", "Did", "Was"]),
        ("fb", "It ___ a good day.", "was"),
        ("fb", "They ___ not happy.", "were"),
        ("fb", "He ___ his keys.", "lost"),
        ("mcq", "She ___ early.", "left", ["leave", "left", "leaved"]),
        ("fb", "We ___ a movie.", "saw"),
    ], [
        ("fb", "She ___ to Paris last month.", "flew"),
        ("fb", "We ___ them at the cafe.", "met"),
        ("fb", "He ___ his leg playing football.", "hurt"),
        ("mcq", "They ___ the bill.", "paid", ["pay", "paid", "payed"]),
        ("mcq", "I ___ asleep on the bus.", "fell", ["fall", "fell", "falled"]),
        ("cor", "He teached English.", "He taught English.", "He teach English."),
        ("cor", "I thinked about it.", "I thought about it.", "I think about it."),
        ("fb", "Did she ___ the door?", "lock"),
        ("fb", "We did not ___ the noise.", "hear"),
        ("mcq", "___ he finish on time?", "Did", ["Do", "Did", "Was"]),
        ("fb", "The test ___ hard.", "was"),
        ("fb", "You ___ right.", "were"),
        ("fb", "They ___ the game.", "won"),
        ("mcq", "He ___ his phone.", "broke", ["break", "broke", "broken"]),
        ("fb", "I ___ a sandwich.", "ate"),
    ])

def _set_future_will(tid: str, sn: int):
    return _alt_sn(tid, sn, [
        ("fb", "I ___ help you.", "will"),
        ("fb", "She ___ not come.", "will"),
        ("mcq", "___ it rain tomorrow?", "Will", ["Do", "Will", "Is"]),
        ("mcq", "We ___ travel next week.", "will", ["will", "are", "do"]),
        ("fb", "They ___ call later.", "will"),
        ("cor", "I will to go.", "I will go.", "I will going."),
        ("fb", "He ___ be here soon.", "will"),
        ("fb", "I am going to ___ a cake.", "make"),
        ("mcq", "I ___ going to study.", "am", ["is", "am", "are"]),
        ("fb", "It ___ going to snow.", "is"),
        ("fb", "We ___ going to leave.", "are"),
        ("mcq", "___ you going to call?", "Are", ["Is", "Are", "Do"]),
        ("fb", "She ___ visit her mom.", "will"),
        ("cor", "They will comes.", "They will come.", "They will coming."),
        ("mcq", "Pick the best plan line.", "I will send it today.", ["I will to send it today.", "I will send it today.", "I sending it today."]),
    ], [
        ("fb", "We ___ pick you up.", "will"),
        ("fb", "He ___ not agree.", "will"),
        ("mcq", "___ you join us?", "Will", ["Do", "Will", "Are"]),
        ("mcq", "They ___ move in June.", "will", ["will", "are", "do"]),
        ("fb", "I ___ text you later.", "will"),
        ("cor", "She will to call.", "She will call.", "She will calling."),
        ("fb", "It ___ be fine.", "will"),
        ("fb", "She is going to ___ a speech.", "give"),
        ("mcq", "He ___ going to drive.", "is", ["am", "is", "are"]),
        ("fb", "They ___ going to wait.", "are"),
        ("fb", "The sky ___ going to clear.", "is"),
        ("mcq", "___ we taking the train?", "Are", ["Is", "Are", "Do"]),
        ("fb", "I ___ book the tickets.", "will"),
        ("cor", "He will goes alone.", "He will go alone.", "He will going alone."),
        ("mcq", "Pick the best line.", "We are going to try again.", ["We will to try again.", "We are going to try again.", "We going to try again."]),
    ])

def _set_modals(tid: str, sn: int):
    return _alt_sn(tid, sn, [
        ("fb", "I ___ swim.", "can"),
        ("fb", "You ___ be quiet.", "must"),
        ("fb", "She ___ speak three languages.", "can"),
        ("mcq", "___ I borrow this?", "May", ["May", "Do", "Is"]),
        ("mcq", "We ___ leave early.", "should", ["should", "shoulds", "musted"]),
        ("fb", "He ___ not enter.", "must"),
        ("cor", "I must to go.", "I must go.", "I must going."),
        ("cor", "She cans drive.", "She can drive.", "She can drives."),
        ("fb", "You ___ try this app.", "should"),
        ("fb", "I ___ help tomorrow.", "could"),
        ("mcq", "___ you open the door?", "Could", ["Should", "Could", "Woulds"]),
        ("fb", "Kids ___ not run here.", "must"),
        ("fb", "We ___ not smoke inside.", "must"),
        ("mcq", "I ___ like some water.", "would", ["will", "would", "can"]),
        ("fb", "He ___ be lost.", "might"),
    ], [
        ("fb", "They ___ play guitar.", "can"),
        ("fb", "Drivers ___ wear belts.", "must"),
        ("fb", "He ___ lift heavy boxes.", "can"),
        ("mcq", "___ I ask a question?", "May", ["May", "Do", "Is"]),
        ("mcq", "You ___ see a doctor.", "should", ["should", "shoulds", "musted"]),
        ("fb", "Visitors ___ not feed the animals.", "must"),
        ("cor", "You must to wait.", "You must wait.", "You must waiting."),
        ("cor", "He can runs fast.", "He can run fast.", "He can runs fastly."),
        ("fb", "We ___ leave now.", "should"),
        ("fb", "She ___ join us later.", "could"),
        ("mcq", "___ I sit here?", "May", ["Should", "May", "Woulds"]),
        ("fb", "You ___ not use phones here.", "must"),
        ("fb", "He ___ not be late again.", "must"),
        ("mcq", "___ you mind waiting?", "Would", ["will", "would", "can"]),
        ("fb", "It ___ rain later.", "might"),
    ])

def _set_comparatives(tid: str, sn: int):
    return _alt_sn(tid, sn, [
        ("fb", "This road is ___ than that one.", "safer"),
        ("fb", "She is ___ than me.", "taller"),
        ("mcq", "This test is ___ than the last.", "easier", ["more easy", "easier", "easyer"]),
        ("mcq", "He runs ___ than her.", "faster", ["more fast", "faster", "fastly"]),
        ("fb", "It is the ___ day this week.", "busiest"),
        ("fb", "This is the ___ cake I ate.", "best"),
        ("cor", "She is more tall.", "She is taller.", "She is tallest."),
        ("cor", "This is goodest.", "This is the best.", "This is the better."),
        ("fb", "London is ___ than my town.", "bigger"),
        ("fb", "I feel ___ today.", "better"),
        ("mcq", "She is ___ student in class.", "the smartest", ["the smart", "the smarter", "the smartest"]),
        ("fb", "This phone is ___ expensive.", "less"),
        ("fb", "He is as ___ as his brother.", "strong"),
        ("mcq", "Pick the right line.", "This room is cleaner.", ["This room is more clean.", "This room is cleaner.", "This room is cleanest."]),
        ("fb", "Winter is the ___ season here.", "coldest"),
    ], [
        ("fb", "This bag is ___ than mine.", "lighter"),
        ("fb", "He is ___ than his dad.", "younger"),
        ("mcq", "Coffee here is ___ than there.", "cheaper", ["more cheap", "cheaper", "cheaply"]),
        ("mcq", "She sings ___ than I do.", "better", ["more good", "better", "gooder"]),
        ("fb", "Monday was my ___ day.", "worst"),
        ("fb", "That was the ___ movie ever.", "funniest"),
        ("cor", "This is more good.", "This is better.", "This is bestest."),
        ("cor", "He is the taller in the team.", "He is the tallest in the team.", "He is the most tall."),
        ("fb", "The river is ___ than before.", "wider"),
        ("fb", "I sleep ___ now.", "longer"),
        ("mcq", "It is ___ place in town.", "the noisiest", ["the noisy", "the noisier", "the noisiest"]),
        ("fb", "This route is ___ crowded.", "less"),
        ("fb", "She is as ___ as a pro.", "fast"),
        ("mcq", "Pick the right line.", "This street is narrower.", ["This street is more narrow.", "This street is narrower.", "This street is narrowest."]),
        ("fb", "Summer feels the ___ here.", "hottest"),
    ])

def _set_conditionals(tid: str, sn: int):
    return _alt_sn(tid, sn, [
        ("fb", "If it rains, I ___ at home.", "will stay"),
        ("fb", "If I ___ you, I would call.", "were"),
        ("mcq", "If you heat ice, it ___.", "melts", ["melt", "melts", "melted"]),
        ("mcq", "If I had time, I ___ travel more.", "would", ["will", "would", "can"]),
        ("fb", "If she studies, she ___ pass.", "will"),
        ("cor", "If I will see him, I tell him.", "If I see him, I will tell him.", "If I see him, I tell him."),
        ("fb", "Unless you hurry, you ___ miss it.", "will"),
        ("fb", "I would help if I ___.", "could"),
        ("mcq", "___ you mind closing the window?", "Would", ["Do", "Would", "Are"]),
        ("fb", "If it ___ sunny, we go out.", "is"),
        ("fb", "If they ___ hard, they win.", "work"),
        ("fb", "I ___ buy it if it is cheap.", "will"),
        ("mcq", "Pick the natural line.", "If I were you, I would rest.", ["If I am you, I would rest.", "If I were you, I would rest.", "If I was you, I will rest."]),
        ("fb", "She would come if she ___.", "could"),
        ("fb", "If he calls, I ___ answer.", "will"),
    ], [
        ("fb", "If it snows, we ___ inside.", "will stay"),
        ("fb", "If he ___ me, I would agree.", "were"),
        ("mcq", "If water freezes, it ___.", "expands", ["expand", "expands", "expanded"]),
        ("mcq", "If I won, I ___ donate half.", "would", ["will", "would", "can"]),
        ("fb", "If he trains, he ___ improve.", "will"),
        ("cor", "If she will come, we start.", "If she comes, we will start.", "If she come, we start."),
        ("fb", "Unless we leave now, we ___ be late.", "will"),
        ("fb", "I could go if I ___ time.", "had"),
        ("mcq", "___ you pass the salt?", "Could", ["Do", "Could", "Are"]),
        ("fb", "If the shop ___ open, we enter.", "is"),
        ("fb", "If she ___ fast, she wins.", "runs"),
        ("fb", "They ___ help if you ask.", "will"),
        ("mcq", "Pick the natural line.", "If I had known, I would have stayed.", ["If I know, I would stay.", "If I had known, I would have stayed.", "If I knew, I will stay."]),
        ("fb", "He would agree if you ___.", "asked"),
        ("fb", "If they agree, we ___ start.", "will"),
    ])

def _set_passive_voice(tid: str, sn: int):
    return _alt_sn(tid, sn, [
        ("fb", "The cake ___ made by Sara.", "was"),
        ("fb", "English ___ in many countries.", "is spoken"),
        ("mcq", "The letter ___ yesterday.", "was sent", ["was send", "was sent", "was sended"]),
        ("mcq", "The work ___ finished soon.", "will be", ["will", "will be", "is be"]),
        ("fb", "The door ___ locked.", "is"),
        ("cor", "The car fixed yesterday.", "The car was fixed yesterday.", "The car was fix yesterday."),
        ("fb", "Mistakes ___ sometimes made.", "are"),
        ("fb", "The report ___ being written.", "is"),
        ("mcq", "Coffee ___ grown in Brazil.", "is", ["are", "is", "be"]),
        ("fb", "He ___ invited to the party.", "was"),
        ("fb", "The bills ___ paid online.", "are"),
        ("fb", "The book ___ read by kids.", "is"),
        ("mcq", "Pick the best passive.", "The house was built in 1990.", ["The house built in 1990.", "The house was built in 1990.", "The house is build in 1990."]),
        ("fb", "The email ___ sent.", "was"),
        ("fb", "Problems ___ solved quickly.", "are"),
    ], [
        ("fb", "The windows ___ cleaned today.", "were"),
        ("fb", "Rice ___ in Asia.", "is grown"),
        ("mcq", "The files ___ last night.", "were uploaded", ["were upload", "were uploaded", "were uploading"]),
        ("mcq", "The bridge ___ repaired next year.", "will be", ["will", "will be", "is"]),
        ("fb", "The gate ___ closed at 6.", "is"),
        ("cor", "The room paint last week.", "The room was painted last week.", "The room was paint last week."),
        ("fb", "Tickets ___ sold online.", "are"),
        ("fb", "Dinner ___ being served.", "is"),
        ("mcq", "Tea ___ grown in India.", "is", ["are", "is", "be"]),
        ("fb", "She ___ hired last month.", "was"),
        ("fb", "Taxes ___ collected yearly.", "are"),
        ("fb", "The story ___ told often.", "is"),
        ("mcq", "Pick the best passive.", "The song was written in 2001.", ["The song wrote in 2001.", "The song was written in 2001.", "The song was wrote in 2001."]),
        ("fb", "The message ___ delivered.", "was"),
        ("fb", "Orders ___ shipped fast.", "are"),
    ])

def _set_reported_speech(tid: str, sn: int):
    return _alt_sn(tid, sn, [
        ("mcq", 'He said, "I am tired." → He said that he ___ tired.', "was", ["is", "was", "were"]),
        ("mcq", 'She said, "I will call." → She said she ___ call.', "would", ["will", "would", "can"]),
        ("fb", 'They said, "We live here." → They said they ___ there.', "lived"),
        ("fb", 'He said, "I like tea." → He said he ___ tea.', "liked"),
        ("mcq", 'She asked, "Do you know?" → She asked if I ___.', "knew", ["know", "knew", "knows"]),
        ("cor", 'He said he is busy yesterday.', "He said he was busy yesterday.", "He said he were busy yesterday."),
        ("fb", 'He told me he ___ help.', "would"),
        ("fb", 'She said she ___ the news.', "had seen"),
        ("mcq", 'He said, "I went home." → He said he ___ home.', "had gone", ["went", "goes", "had gone"]),
        ("fb", 'They said they ___ coming.', "were"),
        ("fb", 'I said I ___ finish later.', "would"),
        ("mcq", 'She asked where I ___.', "was", ["am", "was", "is"]),
        ("fb", 'He claimed he ___ innocent.', "was"),
        ("mcq", "Pick the natural reported line.", "She said she was leaving.", ["She said she is leaving.", "She said she was leaving.", "She said she leaves."]),
        ("fb", 'He asked me ___ I was okay.', "if"),
    ], [
        ("mcq", 'She said, "I am ready." → She said she ___ ready.', "was", ["is", "was", "were"]),
        ("mcq", 'He said, "I will stay." → He said he ___ stay.', "would", ["will", "would", "can"]),
        ("fb", 'We said, "We work nearby." → We said we ___ nearby.', "worked"),
        ("fb", 'She said, "I love jazz." → She said she ___ jazz.', "loved"),
        ("mcq", 'He asked, "Did you go?" → He asked if I ___.', "had gone", ["go", "went", "had gone"]),
        ("cor", 'She said she will come yesterday.', "She said she would come yesterday.", "She said she comes yesterday."),
        ("fb", 'She promised she ___ call back.', "would"),
        ("fb", 'He said he ___ the film before.', "had seen"),
        ("mcq", 'They said, "We left early." → They said they ___ early.', "had left", ["left", "leave", "had left"]),
        ("fb", 'I said I ___ busy.', "was"),
        ("fb", 'He said he ___ arrive soon.', "would"),
        ("mcq", 'He asked what time it ___.', "was", ["is", "was", "is being"]),
        ("fb", 'She insisted she ___ right.', "was"),
        ("mcq", "Pick the natural reported line.", "He said he had forgotten.", ["He said he has forgotten.", "He said he had forgotten.", "He said he forgets."]),
        ("fb", 'She wondered ___ it was true.', "whether"),
    ])

def _set_inversion_adv(tid: str, sn: int):
    return _alt_sn(tid, sn, [
        ("fb", "___ had I arrived when it started.", "Hardly"),
        ("fb", "Not only ___ she sing, she dances.", "does"),
        ("mcq", "___ did I know it was a trap.", "Little", ["Little", "Few", "Small"]),
        ("mcq", "Never ___ I seen such a view.", "have", ["have", "has", "had"]),
        ("fb", "Rarely ___ he complain.", "does"),
        ("cor", "I had no sooner arrived it rained.", "No sooner had I arrived than it rained.", "No sooner I arrived than it rained."),
        ("fb", "Not until Monday ___ we know.", "did"),
        ("fb", "___ comes the bus.", "Here"),
        ("mcq", "So tired ___ she that she slept.", "was", ["she was", "was", "is"]),
        ("fb", "Under no circumstances ___ you enter.", "should"),
        ("fb", "Only then ___ I understand.", "did"),
        ("mcq", "Pick the best formal line.", "Seldom do we agree.", ["Seldom we agree.", "Seldom do we agree.", "Seldom does we agree."]),
        ("fb", "Little ___ they expect the result.", "did"),
        ("fb", "___ had the meeting ended than phones rang.", "No sooner"),
        ("fb", "Not a word ___ he say.", "did"),
    ], [
        ("fb", "___ had we left when it began.", "Scarcely"),
        ("fb", "Not only ___ he write, he edits.", "does"),
        ("mcq", "___ did we guess the ending.", "Little", ["Little", "Few", "Small"]),
        ("mcq", "Never ___ she been so calm.", "has", ["have", "has", "had"]),
        ("fb", "Rarely ___ we see snow.", "do"),
        ("cor", "Hardly we sat down the show started.", "Hardly had we sat down when the show started.", "Hardly we had sat down when the show started."),
        ("fb", "Not until evening ___ they reply.", "did"),
        ("fb", "___ she comes!", "There"),
        ("mcq", "So loud ___ the noise that we left.", "was", ["the noise was", "was", "is"]),
        ("fb", "At no time ___ he admit fault.", "did"),
        ("fb", "Only later ___ she agree.", "did"),
        ("mcq", "Pick the best formal line.", "Rarely have I felt safer.", ["Rarely I have felt safer.", "Rarely have I felt safer.", "Rarely has I felt safer."]),
        ("fb", "Little ___ he know the truth.", "did"),
        ("fb", "___ had we spoken than it rang.", "No sooner"),
        ("fb", "Not once ___ she apologize.", "did"),
    ])

def _set_subjunctive(tid: str, sn: int):
    return _alt_sn(tid, sn, [
        ("fb", "I suggest he ___ on time.", "be"),
        ("fb", "It is vital that she ___ the form.", "complete"),
        ("mcq", "I demand that he ___ silent.", "be", ["is", "be", "was"]),
        ("mcq", "If I ___ you, I would wait.", "were", ["was", "were", "am"]),
        ("fb", "It's time we ___ home.", "went"),
        ("cor", "I suggest that he leaves now.", "I suggest that he leave now.", "I suggest that he left now."),
        ("fb", "She insisted that he ___ honest.", "be"),
        ("fb", "I wish I ___ there.", "were"),
        ("mcq", "I'd rather you ___ not smoke here.", "did", ["do", "does", "did"]),
        ("fb", "It's essential that he ___ notified.", "be"),
        ("fb", "He acts as if he ___ the boss.", "were"),
        ("fb", "I recommend she ___ the course.", "take"),
        ("mcq", "Pick the formal correct line.", "It is important that he be informed.", ["It is important that he is informed.", "It is important that he be informed.", "It is important that he was informed."]),
        ("fb", "Suppose he ___ late again.", "be"),
        ("fb", "They requested that the rule ___ changed.", "be"),
    ], [
        ("fb", "I propose she ___ present.", "be"),
        ("fb", "It is crucial that he ___ early.", "arrive"),
        ("mcq", "I require that she ___ ready.", "be", ["is", "be", "was"]),
        ("mcq", "If she ___ here, we would celebrate.", "were", ["was", "were", "is"]),
        ("fb", "It's time he ___ a decision.", "made"),
        ("cor", "I demand that she goes.", "I demand that she go.", "I demand that she went."),
        ("fb", "He demanded that she ___ careful.", "be"),
        ("fb", "I wish this ___ easier.", "were"),
        ("mcq", "I'd rather he ___ not drive.", "did", ["do", "does", "did"]),
        ("fb", "It's necessary that she ___ told.", "be"),
        ("fb", "She talks as if she ___ famous.", "were"),
        ("fb", "I suggest he ___ a break.", "take"),
        ("mcq", "Pick the formal correct line.", "It is vital that the data be secure.", ["It is vital that the data is secure.", "It is vital that the data be secure.", "It is vital that the data was secure."]),
        ("fb", "Suppose she ___ wrong.", "be"),
        ("fb", "They asked that the fee ___ waived.", "be"),
    ])

def _set_prep_place(tid: str, sn: int):
    qs = []
    qi = 0
    r0 = [
        ("The book is ___ the bag.", "in"), ("The phone is ___ the desk.", "on"), ("I am ___ home.", "at"),
        ("She lives ___ London.", "in"), ("Meet me ___ the door.", "at"), ("The picture is ___ the wall.", "on"),
        ("The kids are ___ the garden.", "in"), ("He is ___ work.", "at"), ("The keys are ___ the drawer.", "in"),
        ("Sit ___ the chair.", "on"), ("We wait ___ the bus stop.", "at"), ("The shop is ___ the corner.", "on"),
        ("They swim ___ the pool.", "in"), ("I am ___ the cafe.", "at"), ("The lamp is ___ the ceiling.", "on"),
    ]
    r1 = [
        ("The cat is ___ the sofa.", "on"), ("We are ___ the airport.", "at"), ("Fish live ___ water.", "in"),
        ("The note is ___ the fridge.", "on"), ("She works ___ a bank.", "at"), ("Put it ___ the box.", "in"),
        ("He sits ___ the front row.", "in"), ("Stand ___ the line.", "in"), ("The hotel is ___ Main Street.", "on"),
        ("I study ___ my room.", "in"), ("Call me ___ noon.", "at"), ("The sign is ___ the window.", "on"),
        ("We eat ___ a restaurant.", "at"), ("The shoes are ___ the bed.", "under"), ("The bird is ___ the tree.", "in"),
    ]
    for pr, ans in (r0, r1)[sn % 2]:
        opts = [ans, "on" if ans != "on" else "in", "at" if ans != "at" else "in"]
        if ans == "under":
            opts = ["under", "on", "at"]
        qs.append(_mcq(tid, sn, qi, pr, ans, list(dict.fromkeys(opts))))
        qi += 1
    return qs

def _dup_sets(builder, tid: str, n: int | None = None):
    cnt = settings.question_sets_per_topic if n is None else n
    return [copy.deepcopy(builder(tid, sn)) for sn in range(cnt)]

TOPICS_RAW = [
    {"id": "beg_have_has", "level_id": "beginner", "title": "Have / Has", "explanation": "Use 'have' with I, you, we, they. Use 'has' with he, she, it. Both talk about things you own, relationships, or states like having time or a cold.", "examples": ["I have a laptop.", "She has a cat.", "We have a meeting at 10.", "He has a headache today.", "They have two cars."], "question_sets": _dup_sets(_set_have_has, "beg_have_has")},
    {"id": "beg_do_does", "level_id": "beginner", "title": "Do / Does", "explanation": "Use 'do' for actions and questions with I, you, we, they. Use 'does' with he, she, it. Think of chores, habits, and tasks.", "examples": ["I do my homework.", "She does yoga every morning.", "Do you like coffee?", "They do the cleaning on Sunday.", "He does his best at work."], "question_sets": _dup_sets(_set_do_does, "beg_do_does")},
    {"id": "beg_have_vs_do", "level_id": "beginner", "title": "Have vs Do", "explanation": "'Have' often means possession or experience (have a car, have fun). 'Do' often means an action or task (do work, do laundry).", "examples": ["I have a car.", "I do my work.", "She has a question.", "We do the shopping.", "He has lunch at noon."], "question_sets": _dup_sets(_set_have_vs_do, "beg_have_vs_do")},
    {"id": "beg_is_am_are", "level_id": "beginner", "title": "Is / Am / Are", "explanation": "Use 'am' with I. Use 'is' with one person or thing. Use 'are' with you, we, they, or many things.", "examples": ["I am ready.", "She is a doctor.", "We are friends.", "They are late.", "It is cold today."], "question_sets": _dup_sets(_set_is_am_are, "beg_is_am_are")},
    {"id": "beg_present_simple", "level_id": "beginner", "title": "Present Simple", "explanation": "Use it for habits and facts. Add -s for he/she/it on most verbs.", "examples": ["I walk to school.", "He plays football.", "We eat at 7.", "The shop opens at 9.", "They live nearby."], "question_sets": _dup_sets(_set_present_simple, "beg_present_simple")},
    {"id": "beg_present_continuous", "level_id": "beginner", "title": "Present Continuous", "explanation": "Use am/is/are + verb-ing for actions happening now or around now.", "examples": ["I am studying.", "She is cooking.", "They are waiting.", "We are not sleeping.", "He is driving."], "question_sets": _dup_sets(_set_present_continuous, "beg_present_continuous")},
    {"id": "beg_plurals", "level_id": "beginner", "title": "Plurals & This/These", "explanation": "Many plurals add -s. Some words change (children, teeth). Use 'this/that' for one thing and 'these/those' for many.", "examples": ["two books", "three children", "these keys", "those chairs", "many people"], "question_sets": _dup_sets(_set_plurals, "beg_plurals")},
    {"id": "beg_articles", "level_id": "beginner", "title": "Articles: A / An / The", "explanation": "Use 'a' before consonant sounds and 'an' before vowel sounds. Use 'the' when both people know which thing you mean.", "examples": ["a car", "an apple", "the sun", "an hour", "a university"], "question_sets": _dup_sets(_set_articles, "beg_articles")},
    {"id": "beg_prepositions_place", "level_id": "beginner", "title": "Prepositions of Place", "explanation": "Use simple place words: in, on, at. 'At' for a point, 'on' for surfaces, 'in' for inside areas.", "examples": ["The keys are on the table.", "I am at home.", "She is in the kitchen.", "The cat is under the bed.", "We meet at the cafe."], "question_sets": _dup_sets(_set_prep_place, "beg_prepositions_place")},
]

def _set_present_perfect(tid: str, sn: int):
    return _alt_sn(tid, sn, [
        ("fb", "I ___ never been to Japan.", "have"),
        ("fb", "She ___ finished the task.", "has"),
        ("mcq", "___ you seen this film?", "Have", ["Has", "Have", "Did"]),
        ("mcq", "He ___ lost his wallet.", "has", ["have", "has", "is"]),
        ("fb", "We ___ lived here for two years.", "have"),
        ("cor", "I have went there.", "I have gone there.", "I have go there."),
        ("fb", "They ___ just arrived.", "have"),
        ("fb", "It ___ rained a lot this week.", "has"),
        ("mcq", "I ___ not called yet.", "have", ["has", "have", "had"]),
        ("fb", "She ___ already eaten.", "has"),
        ("fb", "___ he ever tried it?", "has"),
        ("mcq", "Pick the natural line.", "I've known her since 2010.", ["I know her since 2010.", "I've known her since 2010.", "I knew her since 2010."]),
        ("fb", "We ___ not decided yet.", "have"),
        ("fb", "He ___ broken his arm.", "has"),
        ("fb", "I ___ read this book twice.", "have"),
    ], [
        ("fb", "She ___ never visited Rome.", "has"),
        ("fb", "He ___ started the report.", "has"),
        ("mcq", "___ they met before?", "Have", ["Has", "Have", "Did"]),
        ("mcq", "She ___ changed her mind.", "has", ["have", "has", "is"]),
        ("fb", "I ___ worked here since May.", "have"),
        ("cor", "We have eat already.", "We have eaten already.", "We have eat already."),
        ("fb", "You ___ just missed him.", "have"),
        ("fb", "It ___ snowed twice today.", "has"),
        ("mcq", "She ___ not replied yet.", "has", ["have", "has", "had"]),
        ("fb", "They ___ already left.", "have"),
        ("fb", "___ you ever sailed?", "have"),
        ("mcq", "Pick the natural line.", "I've lived here for ages.", ["I live here for ages.", "I've lived here for ages.", "I lived here for ages."]),
        ("fb", "He ___ not answered.", "has"),
        ("fb", "We ___ paid the bill.", "have"),
        ("fb", "I ___ seen that show before.", "have"),
    ])

def _set_countable(tid: str, sn: int):
    return _alt_sn(tid, sn, [
        ("mcq", "I don't have ___ time.", "much", ["many", "much", "a lot"]),
        ("mcq", "There are ___ cars.", "many", ["much", "many", "a lot"]),
        ("fb", "Can I have ___ water?", "some"),
        ("fb", "She has ___ friends here.", "few"),
        ("mcq", "I need ___ advice.", "some", ["many", "some", "a few"]),
        ("fb", "How ___ sugar do you want?", "much"),
        ("fb", "How ___ apples are there?", "many"),
        ("cor", "I have many money.", "I have a lot of money.", "I have much money."),
        ("mcq", "Pick the best line.", "I have a lot of friends.", ["I have much friends.", "I have a lot of friends.", "I have many of friends."]),
        ("fb", "There isn't ___ milk.", "much"),
        ("fb", "There aren't ___ chairs.", "many"),
        ("fb", "Give me ___ bread.", "some"),
        ("mcq", "She bought ___ eggs.", "a dozen", ["a dozen", "much dozen", "many dozen"]),
        ("fb", "I only have ___ luggage.", "a little"),
        ("fb", "We need ___ information.", "more"),
    ], [
        ("mcq", "We don't have ___ patience.", "much", ["many", "much", "a lot"]),
        ("mcq", "There are ___ errors.", "many", ["much", "many", "a lot"]),
        ("fb", "Could I get ___ juice?", "some"),
        ("fb", "He has ___ ideas.", "few"),
        ("mcq", "We need ___ help.", "some", ["many", "some", "a few"]),
        ("fb", "How ___ rice should I cook?", "much"),
        ("fb", "How ___ tickets left?", "many"),
        ("cor", "She has much cousins.", "She has many cousins.", "She has a lot of cousins."),
        ("mcq", "Pick the best line.", "There is little time left.", ["There is few time left.", "There is little time left.", "There is a few time left."]),
        ("fb", "There isn't ___ juice.", "much"),
        ("fb", "There aren't ___ tickets.", "many"),
        ("fb", "Pass me ___ butter.", "some"),
        ("mcq", "He ate ___ cookies.", "a few", ["a few", "much few", "a little"]),
        ("fb", "We have ___ homework tonight.", "a little"),
        ("fb", "I need ___ practice.", "more"),
    ])

def _set_gerunds(tid: str, sn: int):
    return _alt_sn(tid, sn, [
        ("fb", "I enjoy ___ movies.", "watching"),
        ("fb", "She avoids ___ late.", "being"),
        ("mcq", "He finished ___ the letter.", "writing", ["write", "to write", "writing"]),
        ("mcq", "We practice ___ English.", "speaking", ["speak", "to speak", "speaking"]),
        ("fb", "They keep ___.", "trying"),
        ("fb", "I want ___ home.", "to go"),
        ("fb", "She decided ___ abroad.", "to study"),
        ("cor", "I enjoy to read.", "I enjoy reading.", "I enjoy read."),
        ("cor", "He wants going.", "He wants to go.", "He wants go."),
        ("mcq", "Pick the right line.", "I hope to see you.", ["I hope seeing you.", "I hope to see you.", "I hope see you."]),
        ("fb", "She agreed ___ help.", "to"),
        ("fb", "He admitted ___ the mistake.", "making"),
        ("fb", "We plan ___ early.", "to leave"),
        ("fb", "I don't mind ___ alone.", "waiting"),
        ("mcq", "She refused ___.", "to answer", ["answer", "answering", "to answer"]),
    ], [
        ("fb", "I love ___ music.", "hearing"),
        ("fb", "He risks ___ everything.", "losing"),
        ("mcq", "She stopped ___ the car.", "driving", ["drive", "to drive", "driving"]),
        ("mcq", "They keep ___ the rules.", "breaking", ["break", "to break", "breaking"]),
        ("fb", "We keep ___.", "practicing"),
        ("fb", "They need ___ soon.", "to rest"),
        ("fb", "He chose ___ silent.", "to stay"),
        ("cor", "She avoids to run.", "She avoids running.", "She avoids run."),
        ("cor", "I enjoy to swim.", "I enjoy swimming.", "I enjoy swim."),
        ("mcq", "Pick the right line.", "She offered to drive.", ["She offered driving.", "She offered to drive.", "She offered drive."]),
        ("fb", "He promised ___ call.", "to"),
        ("fb", "She denied ___ the money.", "taking"),
        ("fb", "I expect ___ on time.", "to arrive"),
        ("fb", "He hates ___ up early.", "getting"),
        ("mcq", "They agreed ___.", "to pay", ["pay", "paying", "to pay"]),
    ])

def _set_phrasal_basic(tid: str, sn: int):
    return _alt_sn(tid, sn, [
        ("fb", "Please ___ the TV.", "turn off"),
        ("fb", "I need to ___ early tomorrow.", "wake up"),
        ("mcq", "Can you ___ the light?", "turn on", ["turn on", "turn off", "turn up"]),
        ("mcq", "We need to ___ the truth.", "find out", ["find", "find out", "find in"]),
        ("fb", "She ___ her little brother.", "looks after"),
        ("fb", "Don't ___!", "give up"),
        ("cor", "I wake up it.", "I wake it up.", "I wake up them."),
        ("fb", "He ___ smoking last year.", "gave up"),
        ("fb", "Please ___ your coat.", "take off"),
        ("mcq", "Pick the natural line.", "She turned down the offer.", ["She turned the offer downed.", "She turned down the offer.", "She down turned the offer."]),
        ("fb", "We ___ old photos.", "looked through"),
        ("fb", "The plane ___ late.", "took off"),
        ("fb", "I ___ my friend at the cafe.", "met up with"),
        ("fb", "Could you ___ this form?", "fill out"),
        ("fb", "Let's ___ the bill.", "split"),
    ], [
        ("fb", "___ the radio, please.", "Turn down"),
        ("fb", "I try to ___ every day.", "work out"),
        ("mcq", "___ your shoes before entering.", "Take off", ["Take on", "Take off", "Take in"]),
        ("mcq", "We should ___ the details.", "figure out", ["figure", "figure out", "figure in"]),
        ("fb", "He ___ his parents.", "cares for"),
        ("fb", "Don't ___ the chance!", "pass up"),
        ("cor", "Pick up me at 8.", "Pick me up at 8.", "Pick up I at 8."),
        ("fb", "She ___ junk food.", "cut out"),
        ("fb", "___ your jacket.", "Put on"),
        ("mcq", "Pick the natural line.", "He ran out of time.", ["He ran of time out.", "He ran out of time.", "He ran out time of."]),
        ("fb", "They ___ the names.", "called out"),
        ("fb", "The show ___ on time.", "started"),
        ("fb", "We ___ old classmates.", "caught up with"),
        ("fb", "Please ___ these boxes.", "carry"),
        ("fb", "Let's ___ a taxi.", "call"),
    ])

def _set_participle(tid: str, sn: int):
    return _alt_sn(tid, sn, [
        ("mcq", "___ the work, she went home.", "Having finished", ["Finish", "Having finished", "Finished having"]),
        ("mcq", "___ from the hill, the city looks small.", "Seen", ["Seeing", "Seen", "Saw"]),
        ("fb", "___ tired, he stopped.", "Being"),
        ("fb", "___ the door open, I walked in.", "Seeing"),
        ("cor", "Finishing quickly, the bus left.", "Having finished quickly, she caught the bus.", "Finishing quickly, she caught the bus."),
        ("mcq", "Pick the best line.", "Walking home, I saw a friend.", ["Walk home, I saw a friend.", "Walking home, I saw a friend.", "Walked home, I saw a friend."]),
        ("fb", "___ not invited, he stayed away.", "Not being"),
        ("fb", "___ twice, he didn't repeat it.", "Having been warned"),
        ("mcq", "___ time, we took a taxi.", "Running out of", ["Run out of", "Running out of", "Ran out of"]),
        ("fb", "___ the news, she smiled.", "Hearing"),
        ("fb", "___ carefully, he solved it.", "Thinking"),
        ("fb", "___ in a hurry, we forgot keys.", "Being"),
        ("mcq", "___ the report, I noticed errors.", "While reading", ["While read", "While reading", "While to read"]),
        ("fb", "___ to help, she called.", "Wanting"),
        ("fb", "___ from above, it seems tiny.", "Seen"),
    ], [
        ("mcq", "___ dinner, they watched TV.", "After eating", ["Eat", "After eating", "Eaten"]),
        ("mcq", "___ the map, we took a shortcut.", "Using", ["Use", "Using", "Used"]),
        ("fb", "___ confused, she asked again.", "Feeling"),
        ("fb", "___ the lights on, he entered.", "Seeing"),
        ("cor", "Running fast, the rain started.", "Running fast, she reached the bus.", "Run fast, she reached the bus."),
        ("mcq", "Pick the best line.", "Turning left, we saw the sea.", ["Turn left, we saw the sea.", "Turning left, we saw the sea.", "Turned left, we saw the sea."]),
        ("mcq", "___ the rules once, he obeyed.", "Having read", ["Read", "Having read", "Reading"]),
        ("fb", "___ the bill, she sighed.", "Reading"),
        ("mcq", "___ money, we chose a picnic.", "Lacking", ["Lack", "Lacking", "Lacked"]),
        ("fb", "___ the bell, they stood.", "Hearing"),
        ("fb", "___ slowly, he avoided mistakes.", "Working"),
        ("fb", "___ lost, we asked directions.", "Being"),
        ("mcq", "___ the email, I called him.", "After sending", ["After send", "After sending", "After sent"]),
        ("fb", "___ to rain, we took umbrellas.", "Starting"),
        ("fb", "___ from far, prices look low.", "Seen"),
    ])

def _set_ellipsis(tid: str, sn: int):
    return _alt_sn(tid, sn, [
        ("mcq", "A: Coffee? B: Yes, ___.", "please", ["I please", "please", "pleased"]),
        ("mcq", "A: Going out? B: ___, maybe later.", "Not now", ["Not now", "No now", "Not the now"]),
        ("fb", "A: Hungry? B: ___ bit.", "A"),
        ("mcq", "Pick the natural short reply.", "Sounds good.", ["It sounds good idea.", "Sounds good.", "Sounding good."]),
        ("mcq", "A: See you! B: ___!", "Later", ["Later", "Lately", "Laters"]),
        ("fb", "A: All good? B: ___ good.", "All"),
        ("mcq", "A: Want some water? B: ___, thanks.", "Sure", ["Surely", "Sure", "Suring"]),
        ("fb", "A: Busy? B: ___ busy.", "Kind of"),
        ("mcq", "A: Rain later? B: It ___.", "might", ["might to", "might", "mights"]),
        ("fb", "A: Ready? B: ___ ready.", "Almost"),
        ("mcq", "Pick the best tag.", "Nice day, isn't it?", ["Nice day, isn't it?", "Nice day, is not it?", "Nice day, isn't he?"]),
        ("fb", "A: Thanks! B: ___ problem.", "No"),
        ("fb", "A: Can you help? B: ___.", "Sure"),
        ("mcq", "A: Pizza okay? B: ___.", "Works for me", ["Work for me", "Works for me", "Working for me"]),
        ("fb", "A: Too loud? B: ___ quieter.", "A little"),
    ], [
        ("mcq", "A: Tea? B: Yes, ___.", "thanks", ["thank", "thanks", "thanking"]),
        ("mcq", "A: Movie tonight? B: ___, I'm tired.", "Maybe not", ["Maybe not", "Not maybe", "May not"]),
        ("fb", "A: Cold? B: ___ little.", "A"),
        ("mcq", "Pick the natural short reply.", "Looks fine.", ["It looks fine to me.", "Looks fine.", "Looking fine."]),
        ("mcq", "A: Bye! B: ___ soon!", "See you", ["See you", "Seeing you", "See your"]),
        ("fb", "A: Okay? B: ___ fine.", "Pretty"),
        ("mcq", "A: More soup? B: ___, please.", "No", ["Not", "No", "Nope"]),
        ("fb", "A: Tired? B: ___ exhausted.", "Pretty"),
        ("mcq", "A: Snow tomorrow? B: It ___.", "could", ["could to", "could", "cans"]),
        ("fb", "A: Done? B: ___ done.", "Nearly"),
        ("mcq", "Pick the best tag.", "You're coming, aren't you?", ["You're coming, isn't you?", "You're coming, aren't you?", "You coming, aren't you?"]),
        ("fb", "A: Sorry! B: ___ worries.", "No"),
        ("fb", "A: Need a ride? B: ___.", "Thanks"),
        ("mcq", "A: Thai food? B: ___.", "Sounds great", ["Sound great", "Sounds great", "Sounding great"]),
        ("fb", "A: Too sweet? B: ___ less sugar.", "Way"),
    ])

def _set_linking(tid: str, sn: int):
    return _alt_sn(tid, sn, [
        ("fb", "It was late. ___, we went.", "However"),
        ("fb", "She studied hard. ___, she passed.", "Therefore"),
        ("mcq", "___ it was expensive, we bought it.", "Although", ["Although", "However", "Therefore"]),
        ("mcq", "He was ill. ___, he came.", "Still", ["Therefore", "Still", "Moreover"]),
        ("fb", "___ , the plan needs money.", "Moreover"),
        ("fb", "We left early. ___, we arrived on time.", "Therefore"),
        ("cor", "However it was raining, we went.", "Although it was raining, we went.", "Despite it was raining, we went."),
        ("mcq", "Pick the best connector.", "In addition, we need staff.", ["Additionally to, we need staff.", "In addition, we need staff.", "Additional, we need staff."]),
        ("fb", "___ the traffic, we were late.", "Because of"),
        ("fb", "She tried again. ___, she failed.", "Still"),
        ("fb", "___ speaking, it was fine.", "Honestly"),
        ("mcq", "___ , I disagree.", "On the other hand", ["On other hand", "On the other hand", "In the other hand"]),
        ("fb", "It was cheap. ___, it broke fast.", "However"),
        ("fb", "___ you practice, you improve.", "If"),
        ("fb", "___ , let's start.", "Anyway"),
    ], [
        ("fb", "It rained. ___, we stayed home.", "Therefore"),
        ("fb", "He trained daily. ___, he won.", "Therefore"),
        ("mcq", "___ it was cold, we swam.", "Although", ["Although", "Therefore", "Moreover"]),
        ("mcq", "She was scared. ___, she spoke.", "Still", ["Therefore", "Still", "However"]),
        ("fb", "___ , we need more time.", "Furthermore"),
        ("fb", "We saved money. ___, we could travel.", "Therefore"),
        ("cor", "Although it was dark, but we walked.", "Although it was dark, we walked.", "Despite it was dark, we walked."),
        ("mcq", "Pick the best connector.", "Besides, we need permits.", ["Beside, we need permits.", "Besides, we need permits.", "Besides of, we need permits."]),
        ("fb", "___ the delay, we finished.", "Despite"),
        ("fb", "He called twice. ___, no answer.", "Still"),
        ("fb", "___ , the results were clear.", "Clearly"),
        ("mcq", "___ , costs rose.", "As a result", ["As result", "As a result", "As results"]),
        ("fb", "The plan was bold. ___, it worked.", "Still"),
        ("fb", "___ you rest, you recover.", "If"),
        ("fb", "___ , we should wrap up.", "Otherwise"),
    ])

INTERMEDIATE_TOPICS = [
    {"id": "int_past_simple", "level_id": "intermediate", "title": "Past Simple", "explanation": "Use past simple for finished actions at a time in the past. Many verbs add -ed; some are irregular.", "examples": ["I walked home.", "She went to Paris.", "They didn't call.", "Did you see him?", "We met last year."], "question_sets": _dup_sets(_set_past_simple, "int_past_simple")},
    {"id": "int_future_will", "level_id": "intermediate", "title": "Future: Will / Going to", "explanation": "Use 'will' for quick decisions and offers. Use 'going to' for plans you already thought about.", "examples": ["I will help.", "She is going to travel.", "It will rain.", "We are going to move.", "He won't come."], "question_sets": _dup_sets(_set_future_will, "int_future_will")},
    {"id": "int_modals", "level_id": "intermediate", "title": "Modals: Can, Must, Should", "explanation": "'Can' is ability or permission. 'Must' is strong need or rule. 'Should' is good advice.", "examples": ["I can swim.", "You must wear a seatbelt.", "We should leave early.", "May I sit here?", "He could help tomorrow."], "question_sets": _dup_sets(_set_modals, "int_modals")},
    {"id": "int_comparatives", "level_id": "intermediate", "title": "Comparatives & Superlatives", "explanation": "Compare two things with -er/more. Compare many with the + -est/most.", "examples": ["This is faster.", "She is taller than me.", "It is the best day.", "More expensive", "The easiest test"], "question_sets": _dup_sets(_set_comparatives, "int_comparatives")},
    {"id": "int_present_perfect", "level_id": "intermediate", "title": "Present Perfect Basics", "explanation": "Use have/has + past participle for life experience or a past action with a result now.", "examples": ["I have visited Spain.", "She has lost her keys.", "We have finished.", "Have you eaten?", "He has never tried sushi."], "question_sets": _dup_sets(_set_present_perfect, "int_present_perfect")},
    {"id": "int_countable", "level_id": "intermediate", "title": "Countable / Uncountable", "explanation": "Countable nouns can be counted (two apples). Uncountable nouns use 'much' or measure words (a bottle of water).", "examples": ["many chairs", "much water", "a piece of advice", "few problems", "little time"], "question_sets": _dup_sets(_set_countable, "int_countable")},
    {"id": "int_gerunds", "level_id": "intermediate", "title": "Gerunds after Verbs", "explanation": "After some verbs we use verb+ing (enjoy reading). After others we use 'to' (want to go). Learn common pairs.", "examples": ["I enjoy cooking.", "She avoids driving.", "He finished working.", "We practice speaking.", "They keep trying."], "question_sets": _dup_sets(_set_gerunds, "int_gerunds")},
    {"id": "int_phrasal_basic", "level_id": "intermediate", "title": "Common Phrasal Verbs", "explanation": "Small words like up, off, out change meaning with verbs. Learn whole phrases, not single words.", "examples": ["wake up", "turn off the light", "find out", "give up", "look after"], "question_sets": _dup_sets(_set_phrasal_basic, "int_phrasal_basic")},
]

ADVANCED_TOPICS = [
    {"id": "adv_conditionals", "level_id": "advanced", "title": "Conditionals (0–3)", "explanation": "Zero for facts, first for real futures, second for unreal now, third for unreal past.", "examples": ["If you heat water, it boils.", "If it rains, we will stay.", "If I were you, I would rest.", "If I had known, I would have called."], "question_sets": _dup_sets(_set_conditionals, "adv_conditionals")},
    {"id": "adv_passive", "level_id": "advanced", "title": "Passive Voice", "explanation": "Focus on the action or object: be + past participle. Use when the doer is unknown or not important.", "examples": ["The cake was eaten.", "English is spoken here.", "The work will be done.", "The door is locked.", "Mistakes were made."], "question_sets": _dup_sets(_set_passive_voice, "adv_passive")},
    {"id": "adv_reported", "level_id": "advanced", "title": "Reported Speech", "explanation": "Move tenses back when the reporting verb is past. Change pronouns and time words to fit the new speaker.", "examples": ['He said he was tired.', "She told me she would call.", "They said they lived nearby."], "question_sets": _dup_sets(_set_reported_speech, "adv_reported")},
    {"id": "adv_inversion", "level_id": "advanced", "title": "Inversion (Formal)", "explanation": "After negative adverbs like never, rarely, hardly, the subject and auxiliary swap for emphasis.", "examples": ["Never have I seen this.", "Rarely does he complain.", "Hardly had we arrived when it started."], "question_sets": _dup_sets(_set_inversion_adv, "adv_inversion")},
    {"id": "adv_subjunctive", "level_id": "advanced", "title": "Subjunctive & Formal Verbs", "explanation": "After suggest, demand, vital, use base verb: 'that he be' not 'that he is'.", "examples": ["I suggest he be ready.", "It is important that she know.", "I wish I were there."], "question_sets": _dup_sets(_set_subjunctive, "adv_subjunctive")},
    {"id": "adv_participle", "level_id": "advanced", "title": "Participle Clauses", "explanation": "Use having done, being tired, seen from above to shorten sentences and sound natural.", "examples": ["Having finished, she left.", "Seen from far, it looks small.", "Being tired, I slept early."], "question_sets": _dup_sets(_set_participle, "adv_participle")},
    {"id": "adv_ellipsis", "level_id": "advanced", "title": "Ellipsis in Conversation", "explanation": "Native speakers drop words when meaning is clear: 'Want some?', 'Might rain.', 'See you later.'", "examples": ["Coffee?", "Sounds good.", "Ready?", "Any questions?", "See you!"], "question_sets": _dup_sets(_set_ellipsis, "adv_ellipsis")},
    {"id": "adv_linking", "level_id": "advanced", "title": "Linking & Discourse", "explanation": "Words like however, therefore, although connect ideas in speaking and writing.", "examples": ["However, it rained.", "Therefore, we stayed.", "Although it was late, we went."], "question_sets": _dup_sets(_set_linking, "adv_linking")},
]

TOPICS_LIST = TOPICS_RAW + INTERMEDIATE_TOPICS + ADVANCED_TOPICS
TOPICS_BY_ID = {t["id"]: t for t in TOPICS_LIST}

def normalize_answer(q: dict, ans: str) -> str:
    a = (ans or "").strip().lower()
    c = (q.get("correct") or "").strip().lower()
    if q["type"] == "fill_blank":
        return a
    if q["type"] in ("mcq", "correction"):
        return a
    return a

def grade_answer(q: dict, user_answer: str) -> bool:
    u = (user_answer or "").strip().lower()
    c = (q.get("correct") or "").strip().lower()
    return u == c
