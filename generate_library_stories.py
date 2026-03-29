import argparse
import json
from pathlib import Path

BASE_PROTAGONISTS = [
    "Aarav", "Mila", "Kabir", "Tara", "Noah", "Ira", "Vihaan", "Lina", "Reyansh", "Maya",
    "Arjun", "Nia", "Dev", "Sana", "Rohan", "Anya", "Ishaan", "Pihu", "Kian", "Meera",
    "Adi", "Zoya", "Yuvan", "Ria", "Neel", "Aisha", "Om", "Gia", "Avi", "Diya",
    "Pari", "Rudra", "Myra", "Sam", "Elina", "Vik", "Kiara", "Manu", "Nora", "Veer"
]

VARIANTS = {
    "classic": {
        "protagonists": BASE_PROTAGONISTS,
        "companions": [
            "a chatty squirrel", "a shy rabbit", "a tiny dragon", "a sleepy moonbird", "a giggling fox",
            "a bright blue fish", "a careful turtle", "a striped cat", "a humming bee", "a brave deer",
            "a cloud puppy", "a singing robin", "a little robot", "a gentle bear", "a silver firefly"
        ],
        "places": [
            "Whispering Forest", "Rainbow Village", "Moonbeam Meadow", "Pebblebrook", "Starlight Hill",
            "Cinnamon Harbor", "Golden Orchard", "Willow Lane", "Sunny Hollow", "Cloudberry Cottage",
            "Fern Valley", "Merry Market", "Silver Lake", "Bumble Bridge", "Rosebud Woods",
            "Little Lighthouse Bay", "Pinecone Path", "Honeydew Farm", "Dandelion Square", "Twinkle Town"
        ],
        "objects": [
            "glowing lantern", "singing pebble", "silver key", "paper kite", "golden acorn",
            "whistling teacup", "soft blue feather", "star-shaped bell", "pocket compass", "moon umbrella",
            "tiny drum", "sunny scarf", "sparkle jar", "rainbow map", "wishing seed"
        ],
        "problems": [
            "a path that had forgotten where to go", "a sleepy garden that would not bloom", "a bridge that had lost its courage",
            "a hill covered in quiet fog", "a pond with no songs left in it", "a windy lane where hats kept flying away",
            "a picnic basket that had rolled downhill", "a shy star that would not sparkle", "a bakery clock that had stopped smiling",
            "a library shelf that had lost its labels"
        ],
        "subtitle_hooks": [
            "A little wonder can change a whole day.", "A tiny adventure with a warm surprise.", "One gentle choice lights the way.",
            "A cozy journey full of heart.", "Where courage arrives in quiet steps.", "A cheerful tale of wonder and friendship."
        ],
    },
    "cozy": {
        "protagonists": [
            "Elsie", "Ben", "Suri", "Finn", "Lulu", "Theo", "Anvi", "Momo", "Rafi", "Nell",
            "Poppy", "Hari", "Juno", "Miki", "Tobin", "Ayla", "Luca", "Miri", "Ollie", "Tia"
        ],
        "companions": [
            "a polite hedgehog", "a sleepy kitten", "a waddling duck", "a kind badger", "a woolly lamb",
            "a humming teapot sprite", "a paper-winged owl", "a jam-loving mouse", "a broomstick sparrow", "a button-eyed bear"
        ],
        "places": [
            "Bramble Cottage", "Buttercup Lane", "Hazelbrook Farm", "Mossy Mill", "Bluebell Green",
            "Clover Corner", "Puddingstone Village", "Applecart Hollow", "Thistle Hill", "Wren Cottage Row",
            "Primrose Wharf", "Honeysuckle Square", "Lantern End", "Maple Nook", "Daisyford"
        ],
        "objects": [
            "honey jar", "patchwork blanket", "copper bell", "blue teacup", "star pillow",
            "ribbon kite", "acorn lantern", "cookie tin", "feather pen", "pocket mitten"
        ],
        "problems": [
            "a bakery shelf that had gone quiet", "a bedtime train that missed its yawn", "a meadow where butterflies felt shy",
            "a pond that wanted a lullaby", "a raincoat line tangled by wind", "a family picnic hidden by mist",
            "a garden gate that would not creak kindly", "a sleepy scarecrow who forgot its smile", "a lamp post with no glow at dusk",
            "a market basket that needed finding"
        ],
        "subtitle_hooks": [
            "A warm little tale for rainy afternoons.", "A soft adventure with cookies and courage.", "A cozy surprise waits at the end.",
            "Tiny kindness, big magic.", "A bedtime-bright story full of smiles.", "A gentle journey in a lovely little world."
        ],
    },
    "wonder": {
        "protagonists": [
            "Ari", "Bella", "Cian", "Dara", "Emi", "Farah", "Glen", "Hana", "Indu", "Jasper",
            "Kavi", "Lola", "Milan", "Niko", "Orla", "Pia", "Quin", "Rumi", "Seth", "Tula"
        ],
        "companions": [
            "a moonlit fawn", "a velvet fox", "a pocket phoenix", "a honeybee captain", "a ribbon-tailed rabbit",
            "a peppermint dragon", "a lantern owl", "a puddle whale", "a cinnamon squirrel", "a silver kitten"
        ],
        "places": [
            "Starapple Grove", "Velvet Glen", "Moonpetal Moor", "Sunberry Wharf", "Glimmergate",
            "Dawnfern Village", "Larkspur Hollow", "Amberbrook", "Mistletoe Crossing", "Skylantern Field",
            "Saffron Steps", "Tinselmere", "Juniper Harbor", "Willowglass Bay", "Hearthlight Hill"
        ],
        "objects": [
            "amber lantern", "sugar-star key", "echo shell", "golden spool", "firefly cape",
            "crystal marble", "wish ribbon", "moon-map", "sun pocket watch", "glowberry basket"
        ],
        "problems": [
            "a sleepy orchard that forgot its colors", "a river path that had hidden its stepping stones", "a clock tower waiting for a cheerful chime",
            "a cloud garden with drooping blossoms", "a windy square that had misplaced its songs", "a family porch missing its evening glow",
            "a story gate that would not open kindly", "a meadow where laughter had become too quiet", "a row of lanterns that had lost their sparkle",
            "a little harbor asking for a brave helper"
        ],
        "subtitle_hooks": [
            "A bright-hearted story full of wonder.", "Where small miracles walk beside brave children.", "A sparkling journey with a tender ending.",
            "The kind of story that glows after bedtime.", "A magical adventure wrapped in warmth.", "A wondrous tale for smiling hearts."
        ],
    },
}

TITLE_SPARKS = [
    "Whisper", "Moon", "Star", "Golden", "Silver", "Sunny", "Velvet", "Merry", "Dancing", "Hidden",
    "Tiny", "Brave", "Gentle", "Wonder", "Cozy", "Bright", "Honey", "Lantern", "Song", "Bloom"
]
TITLE_ENDINGS = [
    "at Daybreak", "under the Blue Sky", "and the Secret Smile", "by Lantern Light", "on the Singing Path",
    "of the Little Valley", "and the Kind Surprise", "under the First Star", "and the Golden Breeze", "at Twilight"
]

LESSONS = [
    ("Kindness", "Kindness makes every place feel warmer."),
    ("Honesty", "Honesty helps hearts trust one another."),
    ("Bravery", "Bravery grows one small step at a time."),
    ("Sharing", "Sharing joy makes it grow."),
    ("Patience", "Good things often bloom slowly."),
    ("Teamwork", "Big problems feel smaller when solved together."),
    ("Confidence", "Believing in yourself helps you begin."),
    ("Gratitude", "Thankfulness turns ordinary days into bright ones."),
    ("Curiosity", "Questions can open wonderful doors."),
    ("Care", "Gentle care can mend more than we think.")
]
OPENERS = [
    "On a bright morning in {place}, {name} found a {obj} near the gate and knew the day would not be ordinary.",
    "In {place}, where the air smelled of bread and flowers, {name} tucked a {obj} into one pocket and stepped outside.",
    "Every child in {place} knew that strange things happened kindly there, and on this day {name} was ready for one of them."
]
MIDDLE_A = [
    "Soon {name} met {companion}, who blinked twice and said, \"I think this belongs to {problem}.\"",
    "At the corner of the lane stood {companion}, who whispered, \"I hoped you would come. Something is wrong with {problem}.\"",
    "Just beyond the fence, {name} heard a soft voice. It was {companion}, and it had news about {problem}."
]
MIDDLE_B = [
    "\"We can fix it,\" said {name}. \"Maybe not quickly, but kindly.\"",
    "\"Let us try together,\" said {companion}. \"One careful idea is better than ten worried ones.\"",
    "{name} took a deep breath. \"All right,\" came the answer. \"We start with one small brave thing.\""
]
ACTIONS = [
    "They followed a winding path under silver leaves and listened for the softest clue.",
    "They carried the {obj} from stone to stone until the air began to glow softly.",
    "They asked the wind, the trees, and even the puddles what they had seen that morning.",
    "They shared crumbs, songs, and patient guesses until the problem loosened like a knot.",
    "They worked slowly, laughing when they slipped, cheering when they managed even a little bit."
]
TURNS = [
    "At first nothing happened. Then the {obj} gave a tiny hum, like a secret saying hello.",
    "For one quiet moment, the world seemed to hold its breath. Then a warm shimmer ran across the ground.",
    "The sky brightened, the breeze changed, and suddenly the answer felt close enough to touch."
]
ENDINGS = [
    "By sunset, {problem} was no longer troubled, and everyone in {place} came out to clap and laugh and share hot snacks.",
    "When the work was done, {place} looked brighter than before, as if the whole town had remembered how to smile.",
    "That evening, lanterns glowed, doors opened, and {name} realized the day had mended more than one small problem."
]
CLOSING_TWISTS = [
    "Just before bed, the {obj} winked once, as if promising another adventure someday.",
    "As the stars came out, {companion} bowed politely and left behind a single shining footprint.",
    "Before the moon climbed high, a tiny note appeared: THANK YOU FOR HELPING THE WORLD FEEL KIND AGAIN.",
    "The next morning, everyone said the place looked ordinary, but {name} could still hear a little song in the air."
]


def age_group_for(index: int) -> str:
    return ["3-5", "6-8", "9-12"][index % 3]


def reading_level_paragraph(name: str, age_group: str, lesson_name: str) -> str:
    if age_group == "3-5":
        return f"{name} used simple steps: look, listen, smile, and try again. That was enough to help everyone feel safe and happy."
    if age_group == "6-8":
        return f"{name} noticed that the best answers were not always loud ones. Sometimes {lesson_name.lower()} worked like a lantern, showing the next small step."
    return f"{name} discovered that real courage often feels quiet at first. It begins with paying attention, asking for help, and keeping a hopeful heart while solving the problem."


def make_story(index: int, variant: str):
    data = VARIANTS[variant]
    name = data["protagonists"][index % len(data["protagonists"])]
    companion = data["companions"][index % len(data["companions"])]
    place = data["places"][index % len(data["places"])]
    obj = data["objects"][index % len(data["objects"])]
    problem = data["problems"][index % len(data["problems"])]
    lesson_name, moral = LESSONS[(index + (0 if variant == 'classic' else 3)) % len(LESSONS)]
    age_group = age_group_for(index)
    subtitle = data["subtitle_hooks"][index % len(data["subtitle_hooks"])]

    spark = TITLE_SPARKS[(index * 3) % len(TITLE_SPARKS)]
    ending = TITLE_ENDINGS[(index * 5) % len(TITLE_ENDINGS)]
    title = f"{name} and the {spark} {obj.title()} of {place}"
    if index % 4 == 1:
        title = f"The {spark} {obj.title()} at {place} {ending}"
    elif index % 4 == 2:
        title = f"{name} in {place} {ending}"
    elif index % 4 == 3:
        title = f"The Day {place} Needed {name} {ending}"

    paragraphs = [
        OPENERS[index % len(OPENERS)].format(name=name, place=place, obj=obj),
        MIDDLE_A[index % len(MIDDLE_A)].format(name=name, companion=companion, problem=problem),
        MIDDLE_B[index % len(MIDDLE_B)].format(name=name, companion=companion),
        ACTIONS[index % len(ACTIONS)].format(obj=obj),
        TURNS[index % len(TURNS)].format(obj=obj),
        reading_level_paragraph(name, age_group, lesson_name),
        ENDINGS[index % len(ENDINGS)].format(problem=problem, place=place, name=name),
        CLOSING_TWISTS[index % len(CLOSING_TWISTS)].format(obj=obj, companion=companion, name=name),
    ]

    story = "\n\n".join(paragraphs)
    return {
        "title": title,
        "subtitle": subtitle,
        "story": story,
        "moral": moral,
        "age_group": age_group,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", choices=sorted(VARIANTS.keys()), default="classic")
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    stories = []
    used_titles = set()
    for i in range(args.count):
        story = make_story(i, args.variant)
        original_title = story["title"]
        if original_title in used_titles:
            story["title"] = f"{original_title} #{i + 1}"
        used_titles.add(story["title"])
        stories.append(story)
    default_name = "library_stories_100.json" if args.variant == "classic" else f"library_stories_100_{args.variant}.json"
    output_path = Path(args.output or default_name)
    output_path.write_text(json.dumps(stories, indent=2, ensure_ascii=False), encoding="utf-8")
    print(output_path)
    print(len(stories))


if __name__ == "__main__":
    main()
