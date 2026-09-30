"""Create docs/zoo.json from the master mob list.

Refuses to overwrite an existing zoo.json (it holds live catch state) unless --force.
Source of the list + methods: MyWorkshop/wiki/ideas/unity-zoo-mobs.md (Java 26.3).
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "zoo.json"

# Hebrew names: minecraft.wiki Hebrew translation project (יצורים page), fetched 2026-09-30.
# Not on that page (own names): zombie, endermite, copper golem, nautilus, zombie nautilus, camel husk, parched, sulfur cube.
# id, English, Hebrew, tier (1 easy, 2 medium, 3 hard, 4 bonus, 0 impossible), wing, egg base, egg spots, how (Hebrew)
MOBS = [
    ("cow", "Cow", "פרה", 1, "overworld", "#443626", "#a1a1a1", "רצועה או חיטה ביד"),
    ("pig", "Pig", "חזיר", 1, "overworld", "#f0a5a2", "#db635f", "רצועה או גזר ביד"),
    ("sheep", "Sheep", "כבשה", 1, "overworld", "#e7e7e7", "#ffb5b5", "רצועה או חיטה ביד"),
    ("chicken", "Chicken", "תרנגול", 1, "overworld", "#a1a1a1", "#ff0000", "זרעים ביד"),
    ("rabbit", "Rabbit", "ארנב", 1, "overworld", "#995f40", "#734831", "רצועה או גזר ביד"),
    ("horse", "Horse", "סוס", 1, "overworld", "#c09e7d", "#eee500", "לאלף ולרכוב"),
    ("donkey", "Donkey", "חמור", 1, "overworld", "#534539", "#867566", "לאלף ולרכוב"),
    ("mule", "Mule", "פרד", 1, "overworld", "#1b0200", "#51331d", "הכלאה של סוס וחמור"),
    ("llama", "Llama", "למה", 1, "overworld", "#c09e7d", "#995f40", "רצועה"),
    ("camel", "Camel", "גמל", 1, "overworld", "#fcc369", "#cb9337", "לרכוב עליו לגן"),
    ("goat", "Goat", "עז", 1, "overworld", "#a5947c", "#55493e", "רצועה, להיזהר מנגיחות"),
    ("cat", "Cat", "חתול", 1, "overworld", "#efc88e", "#957256", "לאלף עם דג ולהושיב"),
    ("wolf", "Wolf", "זאב", 1, "overworld", "#d7d3d3", "#ceaf96", "לאלף עם עצם ולהושיב"),
    ("fox", "Fox", "שועל", 1, "overworld", "#d5b69f", "#cc6920", "רצועה, או להרביע בגן"),
    ("ocelot", "Ocelot", "חתול ביצות", 1, "overworld", "#efde7d", "#564434", "רצועה מהג'ונגל"),
    ("parrot", "Parrot", "תוכי", 1, "overworld", "#0da70b", "#ff0000", "לאלף עם זרעים ולהושיב"),
    ("bee", "Bee", "דבורה", 1, "overworld", "#edc343", "#43241b", "פרח ביד, או להעביר קן עם Silk Touch"),
    ("frog", "Frog", "צפרדע", 1, "overworld", "#d07444", "#ffc77c", "ראשן בדלי שגדל בגן. צריך תקרה"),
    ("tadpole", "Tadpole", "ראשן", 1, "overworld", "#6d533d", "#160a00", "דלי. להאכיל בשן ארי זהובה שלא יגדל"),
    ("axolotl", "Axolotl", "אקסולוטל", 1, "overworld", "#fbc1e3", "#a62d74", "דלי מהמערות השופעות"),
    ("cod", "Cod", "בקלה", 1, "overworld", "#c1a76a", "#e5c48b", "דלי"),
    ("salmon", "Salmon", "סלמון", 1, "overworld", "#a00f10", "#0e8474", "דלי"),
    ("tropical_fish", "Tropical Fish", "דג טרופי", 1, "overworld", "#ef6915", "#fff9ef", "דלי"),
    ("pufferfish", "Pufferfish", "אבו נפחא", 1, "overworld", "#f6b201", "#37c3f2", "דלי. מרעיל"),
    ("squid", "Squid", "דיונון", 1, "overworld", "#223b4d", "#708899", "רצועה או תעלת מים. תג שם"),
    ("glow_squid", "Glow Squid", "דיונון זוהר", 1, "overworld", "#095656", "#85f1bc", "רצועה או תעלת מים. תג שם"),
    ("dolphin", "Dolphin", "דולפין", 1, "overworld", "#223b4d", "#f9f9f9", "רצועה או תעלת מים"),
    ("turtle", "Turtle", "צב", 1, "overworld", "#e7e7e7", "#00afaf", "להרביע ולבקוע ביצים בגן"),
    ("villager", "Villager", "כפרי", 1, "overworld", "#563c33", "#bd8b72", "סירה או עגלה"),
    ("iron_golem", "Iron Golem", "גולם ברזל", 1, "overworld", "#dbcdc2", "#74a332", "לבנות בגן"),
    ("snow_golem", "Snow Golem", "גולם שלג", 1, "overworld", "#d9f2f2", "#81a4a4", "לבנות בגן"),
    ("copper_golem", "Copper Golem", "גולם נחושת", 1, "overworld", "#c15a36", "#6fa38e", "לבנות בגן ולשעוות, אחרת יהפוך לפסל"),
    ("zombie", "Zombie", "זומבי", 1, "overworld", "#00afaf", "#799c65", "בור או סירה, תג שם, תקרה"),
    ("skeleton", "Skeleton", "שלד", 1, "overworld", "#c1c1c1", "#494949", "בור או סירה, תג שם, תקרה"),
    ("spider", "Spider", "עכביש", 1, "overworld", "#342d27", "#a80e0e", "בור או סירה, תג שם"),
    ("cave_spider", "Cave Spider", "עכביש מערות", 1, "overworld", "#0c424e", "#a80e0e", "ממכרה נטוש, סירה, תג שם"),
    ("creeper", "Creeper", "קריפר", 1, "overworld", "#0da70b", "#000000", "סירה. לא להתקרב"),
    ("slime", "Slime", "רפש", 1, "overworld", "#51a03e", "#7ebf6e", "ביצה או צ'אנק סליים, לפתות"),
    ("witch", "Witch", "מכשפה", 1, "overworld", "#340000", "#51a03e", "טבעת עגלות או סירה"),
    ("husk", "Husk", "האסק", 1, "overworld", "#797061", "#e6cc94", "מדבר, בור או סירה, תג שם"),
    ("stray", "Stray", "תועה", 1, "overworld", "#617677", "#dde4e4", "להקפיא שלד בשלג אבקה"),
    ("bogged", "Bogged", "שקוע", 1, "overworld", "#8a9b76", "#314d1b", "ביצות או תאי ניסיון, כמו שלד"),
    ("drowned", "Drowned", "טבוע", 1, "overworld", "#8ff1d7", "#799c65", "כמו זומבי, צריך מים בעומק 2"),
    ("pillager", "Pillager", "שודד כפרים", 1, "overworld", "#532f36", "#959b9b", "סירה ליד מאחז"),
    ("vindicator", "Vindicator", "מרטש", 1, "overworld", "#959b9b", "#275e61", "סירה או טבעת עגלות"),
    ("evoker", "Evoker", "מעורר", 1, "overworld", "#959b9b", "#1e1c1a", "סירה או טבעת עגלות"),
    ("mooshroom", "Mooshroom", "מושרום", 2, "overworld", "#a00f10", "#b7b7b7", "רצועה מאי הפטריות הרחוק"),
    ("polar_bear", "Polar Bear", "דוב קוטב", 2, "overworld", "#f2f2f2", "#959590", "רצועה, בלי גורים לידו"),
    ("panda", "Panda", "פנדה", 2, "overworld", "#e7e7e7", "#1b1b22", "במבוק ביד או רצועה"),
    ("armadillo", "Armadillo", "ארמדיל", 2, "overworld", "#ad716d", "#824848", "רצועה מהסוואנה"),
    ("sniffer", "Sniffer", "רחרחן", 2, "overworld", "#871e09", "#25ab70", "ביצה מחול חשוד בחורבות אוקיינוס חמות"),
    ("allay", "Allay", "אלאיי", 2, "overworld", "#00daff", "#00adff", "לשחרר מהכלוב ולתת לו חפץ"),
    ("happy_ghast", "Happy Ghast", "גאסט שמח", 2, "overworld", "#f9f9f9", "#bcbcbc", "גאסט מיובש במים, צריך תקרה"),
    ("strider", "Strider", "סטריידר", 2, "nether", "#9c3436", "#4d494d", "פטריית וורפד על מקל, לבה בגן"),
    ("magma_cube", "Magma Cube", "קוביית מאגמה", 2, "nether", "#340000", "#fcfc00", "לפתות כמו סליים"),
    ("nautilus", "Nautilus", "נאוטילוס", 2, "overworld", "#d9c8a8", "#8a5a3b", "לאלף עם אבו נפחא, אוכף, לשחות לגן"),
    ("zombie_nautilus", "Zombie Nautilus", "נאוטילוס זומבי", 2, "overworld", "#6b8a73", "#3d4f43", "כמו נאוטילוס, צריך תקרה"),
    ("camel_husk", "Camel Husk", "גמל האסק", 2, "overworld", "#b59a6a", "#6f5a3a", "במדבר, להרוג את הרוכב"),
    ("parched", "Parched", "פארצ'ד", 2, "overworld", "#d8c49a", "#8f7a55", "שלד מדבר, כמו שלד"),
    ("zombie_horse", "Zombie Horse", "סוס זומבי", 2, "overworld", "#315234", "#97c284", "נשרף בשמש, לעבוד בלילה"),
    ("skeleton_horse", "Skeleton Horse", "שלד סוס", 2, "overworld", "#68684f", "#e5e5d8", "מלכודת שלדים בסופת ברקים"),
    ("zombie_villager", "Zombie Villager", "זומבי כפרי", 2, "overworld", "#563c33", "#799c65", "כפרי + זומבי על Hard"),
    ("zombified_piglin", "Zombified Piglin", "פיגלין זומבי", 2, "overworld", "#ea9393", "#4c7129", "להביא פיגלין לעולם העליון"),
    ("zoglin", "Zoglin", "זוגלין", 2, "overworld", "#c66e55", "#e6e6e6", "להביא הוגלין דרך פורטל"),
    ("enderman", "Enderman", "אנדרמן", 2, "overworld", "#161616", "#000000", "בסירה, לא לשבור אותה. תקרה"),
    ("endermite", "Endermite", "אנדרמייט", 2, "overworld", "#161616", "#6e6e6e", "לזרוק פנינים בגן, תג שם תוך 2 דקות"),
    ("silverfish", "Silverfish", "דג כסף", 2, "overworld", "#6e6e6e", "#303030", "מבלוק נגוע במבצר"),
    ("bat", "Bat", "עטלף", 2, "overworld", "#4c3e30", "#0f0f0f", "קופסה חשוכה מתחת ל-Y 63"),
    ("trader_llama", "Trader Llama", "למה של סוחר", 2, "overworld", "#eaa430", "#456296", "רצועה ולאלף, תג שם לא מספיק"),
    ("sulfur_cube", "Sulfur Cube", "קוביית גופרית", 2, "overworld", "#d6c94a", "#8a7f1e", "דלי ריק על קובייה גדולה"),
    ("wither_skeleton", "Wither Skeleton", "שלד וויד'ר", 2, "nether", "#141414", "#474d4d", "מבצר נת'ר, בור או סירה"),
    ("blaze", "Blaze", "להבון", 2, "nether", "#f6b201", "#fff87e", "סירות ועגלות מסביב לספאונר"),
    ("piglin", "Piglin", "פיגלין", 2, "nether", "#995f40", "#f9f3a4", "זהב ביד. רק באגף הנת'ר"),
    ("piglin_brute", "Piglin Brute", "פיגלין פראי", 2, "nether", "#592a10", "#f9f3a4", "מהבאסטיון. רק באגף הנת'ר"),
    ("hoglin", "Hoglin", "הוגלין", 2, "nether", "#c66e55", "#5f6464", "לפתות, להתרחק מפטריות וורפד. רק באגף הנת'ר"),
    ("ravager", "Ravager", "הרסן", 2, "overworld", "#757470", "#5b5049", "טבעת עגלות בפשיטה. גן גדול"),
    ("guardian", "Guardian", "שומר", 2, "overworld", "#5a8272", "#f17d30", "סירות מעל המקדש"),
    ("warden", "Warden", "וורדן", 3, "overworld", "#0f4649", "#39d6e0", "כדורי שלג, שביל צמר, מכונת רעש, תג שם"),
    ("ghast", "Ghast", "גאסט", 3, "nether", "#f9f9f9", "#bcbcbc", "עגלה בנת'ר ודרך הפורטל"),
    ("breeze", "Breeze", "בריזה", 3, "overworld", "#af94df", "#9166df", "חדר קטן בתא ניסיון, עגלה החוצה"),
    ("phantom", "Phantom", "פאנטום", 3, "overworld", "#43518a", "#88ff00", "3 לילות בלי שינה, לעמוד בתוך הגן"),
    ("elder_guardian", "Elder Guardian", "שומר בכיר", 3, "overworld", "#ceccba", "#747693", "לייבש חדר, פורטל בפנים, עגלה בנת'ר"),
    ("shulker", "Shulker", "שולקר", 3, "overworld", "#946794", "#4d3852", "עגלה מעיר האנד לפורטל היציאה"),
    ("creaking", "Creaking", "החורק", 3, "overworld", "#5f5f5f", "#fc7812", "לב קריקינג בין 2 בולי אלון חיוור בגן"),
    ("wither", "Wither", "וויד'ר", 4, "overworld", "#141414", "#4d72a0", "בונוס: גולם ברזל, עמוד בועות, כלוב"),
    ("wandering_trader", "Wandering Trader", "סוחר נודד", 4, "overworld", "#456296", "#eaa430", "בונוס: תערוכה זמנית, נעלם תמיד"),
    ("ender_dragon", "Ender Dragon", "דרקון אנדר", 0, "end", "#1c1c1c", "#e079fa", "אי אפשר לכלוא מחוץ לאנד"),
    ("vex", "Vex", "ווקס", 0, "overworld", "#7a90a4", "#e8edf1", "עובר דרך קירות ומת אחרי זמן קצר"),
]


def main():
    if OUT.exists() and "--force" not in sys.argv:
        raise SystemExit(f"{OUT} exists (live catch state). Use --force to reset.")
    ids = [m[0] for m in MOBS]
    assert len(ids) == len(set(ids)), "duplicate id"
    data = {
        "title": "גן החיות של יוניטי",
        "site_url": "",
        "channel_url": "https://www.youtube.com/@livourmana",
        "updated": None,
        "last_caught": None,
        "mobs": [
            {"id": i, "en": en, "he": he, "tier": t, "wing": w, "egg": [a, b],
             "how": how, "caught": False, "caught_at": None}
            for i, en, he, t, w, a, b, how in MOBS
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    goal = sum(1 for m in MOBS if m[3] in (1, 2, 3))
    print(f"Wrote {OUT} — {len(MOBS)} mobs, goal {goal}")


if __name__ == "__main__":
    main()
