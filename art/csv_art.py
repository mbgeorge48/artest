import csv
from art.arted_ya import Card


def process_csv(csv_path):
    with open(csv_path, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dwarf_id = row["id"]
            name = row["dwarf name"]
            fun_fact = row["fun fact"]
            clue = row["clue"]
            category = row["category"]
            # Stats
            year = row["year"]
            political_alignment = row["political alignment"]
            rizz = row["rizz"]
            stealth = row["stealth"]
            weight = row["weight (kg)"]
            pose = row["pose"]
            pints = row["pints"]
            kebab_sauce = row["kebab sauce"]
            post_night_snack = row["post-night snack"]

            card = Card(
                filename=f"dwarf_{dwarf_id}.png",
                height=2100,
                width=1500,
                number_of_shapes=250,
                cursor_left_margin=70,
                cursor_start_y=50,
            )

            card.add_overlay()
            card.write_heading(heading=name, font_size=128)
            card.insert_spacer()
            card.write_subheading(subheading=category, font_size=98)

            card.insert_spacer(40)
            card.write_subheading(subheading=fun_fact, font_size=56, bold=False)
            card.insert_spacer(40)
            card.insert_image(
                top_image_path=f"input/{dwarf_id}.jpg",
            )
            card.insert_spacer()
            card.write_subheading(subheading=clue, font_size=56, bold=False)
            stats_data = {
                "Year": year,
                "Rizz": rizz,
                "Stealth": stealth,
                "Weight": f"{weight}kg",
                "Pose": pose,
                "Political Alignment": political_alignment,
                "Average Pints a Night": pints,
                "Kebab Sauce": kebab_sauce,
                "Post-Night Snack": post_night_snack,
            }
            card.insert_spacer(60)
            card.write_stats(data=stats_data, font_size=64)

            card.save_image()
