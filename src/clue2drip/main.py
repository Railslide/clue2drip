import csv
import json

ROW_STRUCTURE = {
    "date": "",
    "temperature.value": "",
    "temperature.exclude": "",
    "temperature.time": "",
    "temperature.note": "",
    "bleeding.value": "",
    "bleeding.exclude": "",
    "mucus.feeling": "",
    "mucus.texture": "",
    "mucus.value": "",
    "mucus.exclude": "",
    "cervix.opening": "",
    "cervix.firmness": "",
    "cervix.position": "",
    "cervix.exclude": "",
    "note.value": "",
    "desire.value": "",
    "sex.solo": "",
    "sex.partner": "",
    "sex.condom": "",
    "sex.pill": "",
    "sex.iud": "",
    "sex.patch": "",
    "sex.ring": "",
    "sex.implant": "",
    "sex.diaphragm": "",
    "sex.none": "",
    "sex.other": "",
    "sex.note": "",
    "pain.cramps": "",
    "pain.ovulationPain": "",
    "pain.headache": "",
    "pain.backache": "",
    "pain.nausea": "",
    "pain.tenderBreasts": "",
    "pain.migraine": "",
    "pain.other": "",
    "pain.note": "",
    "mood.happy": "",
    "mood.sad": "",
    "mood.stressed": "",
    "mood.balanced": "",
    "mood.fine": "",
    "mood.anxious": "",
    "mood.energetic": "",
    "mood.fatigue": "",
    "mood.angry": "",
    "mood.other": "",
    "mood.note": "",
}


def get_bleeding_value(bleeding_string: str) -> int:
    """Convert Clue bleeding value to its numeric Drip counterpart"""

    bleeding_mapping = {
        "spotting": 0,
        "light": 1,
        "medium": 2,
        "heavy": 3,
    }
    try:
        return bleeding_mapping[bleeding_string]
    except KeyError:
        raise RuntimeError("Unknown string value for bleeding")


def convert(clue_file: str) -> None:
    """Takes a clue file and converts it in Drip compatible csv"""
    with open(clue_file, encoding="utf-8") as fh:
        clue_data = json.load(fh)

    output = []
    for entry in clue_data["data"]:
        # TODO use dataclass perhaps?
        row = dict(ROW_STRUCTURE)  # make sure we don't edit the base dict
        row["date"] = entry["day"][:10]  # This is ugly, but will do for now
        if entry.get("period"):
            row["bleeding.value"] = get_bleeding_value(entry["period"])
            row["bleeding.exclude"] = False
            output.append(row)

    with open("output.csv", "w", encoding="utf-8") as csvfile:
        field_names = ROW_STRUCTURE.keys()
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(output)


if __name__ == "__main__":
    convert("../../test_data/cluebackup.cluedata")
