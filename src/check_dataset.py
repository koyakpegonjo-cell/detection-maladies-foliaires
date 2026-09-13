from pathlib import Path
from collections import Counter


# Racine du projet
PROJECT_ROOT = Path(__file__).resolve().parent.parent

IMAGES_DIR = PROJECT_ROOT / "data" / "fieldplant" / "train" / "images"
LABELS_DIR = PROJECT_ROOT / "data" / "fieldplant" / "train" / "labels"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

CLASS_NAMES = [
    "Cassava Bacterial Blight",
    "Cassava Brown Leaf Spot",
    "Cassava Healthy",
    "Cassava Mosaic",
    "Cassava Root Rot",
    "Corn Brown Spots",
    "Corn Charcoal",
    "Corn Chlorotic Leaf Spot",
    "Corn Gray leaf spot",
    "Corn Healthy",
    "Corn Insects Damages",
    "Corn Mildew",
    "Corn Purple Discoloration",
    "Corn Smut",
    "Corn Streak",
    "Corn Stripe",
    "Corn Violet Decoloration",
    "Corn Yellow Spots",
    "Corn Yellowing",
    "Corn leaf blight",
    "Corn rust leaf",
    "Tomato Brown Spots",
    "Tomato bacterial wilt",
    "Tomato blight leaf",
    "Tomato healthy",
    "Tomato leaf mosaic virus",
    "Tomato leaf yellow virus",
]


def get_images():
    return [
        file
        for file in IMAGES_DIR.iterdir()
        if file.is_file()
        and file.suffix.lower() in IMAGE_EXTENSIONS
    ]


def main():

    print("=" * 60)
    print("CONTRÔLE QUALITÉ DU DATASET FIELDPLANT")
    print("=" * 60)

    images = get_images()
    labels = list(LABELS_DIR.glob("*.txt"))

    print(f"\nNombre d'images : {len(images)}")
    print(f"Nombre de labels : {len(labels)}")

    # ---------------------------------------------------------
    # Vérification image -> label
    # ---------------------------------------------------------

    missing_labels = []

    for image in images:
        label_file = LABELS_DIR / f"{image.stem}.txt"

        if not label_file.exists():
            missing_labels.append(image.name)

    print(f"\nImages sans annotation : {len(missing_labels)}")

    # ---------------------------------------------------------
    # Vérification label -> image
    # ---------------------------------------------------------

    image_stems = {image.stem for image in images}

    labels_without_images = [
        label.name
        for label in labels
        if label.stem not in image_stems
    ]

    print(
        f"Annotations sans image : "
        f"{len(labels_without_images)}"
    )

    # ---------------------------------------------------------
    # Vérification des annotations
    # ---------------------------------------------------------

    class_counter = Counter()

    invalid_lines = []
    invalid_class_ids = []
    invalid_coordinates = []

    for label_file in labels:

        with open(label_file, "r", encoding="utf-8") as file:

            for line_number, line in enumerate(file, start=1):

                line = line.strip()

                if not line:
                    continue

                parts = line.split()

                # YOLO doit avoir 5 valeurs
                if len(parts) != 5:

                    invalid_lines.append(
                        f"{label_file.name}: ligne {line_number}"
                    )

                    continue

                try:

                    class_id = int(parts[0])

                    x = float(parts[1])
                    y = float(parts[2])
                    width = float(parts[3])
                    height = float(parts[4])

                except ValueError:

                    invalid_lines.append(
                        f"{label_file.name}: ligne {line_number}"
                    )

                    continue

                # Vérification classe
                if not 0 <= class_id < len(CLASS_NAMES):

                    invalid_class_ids.append(
                        f"{label_file.name}: "
                        f"classe {class_id}"
                    )

                else:

                    class_counter[class_id] += 1

                # Vérification coordonnées
                values = [x, y, width, height]

                if not all(0 <= value <= 1 for value in values):

                    invalid_coordinates.append(
                        f"{label_file.name}: "
                        f"ligne {line_number}"
                    )

    # ---------------------------------------------------------
    # Résultats
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("VALIDITÉ DES ANNOTATIONS")
    print("=" * 60)

    print(
        f"\nLignes YOLO invalides : "
        f"{len(invalid_lines)}"
    )

    print(
        f"Classes invalides : "
        f"{len(invalid_class_ids)}"
    )

    print(
        f"Coordonnées invalides : "
        f"{len(invalid_coordinates)}"
    )

    # ---------------------------------------------------------
    # Distribution des classes
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("DISTRIBUTION DES 27 CLASSES")
    print("=" * 60)

    for class_id, class_name in enumerate(CLASS_NAMES):

        count = class_counter[class_id]

        print(
            f"{class_id:2d} | "
            f"{class_name:<40} | "
            f"{count}"
        )

    # ---------------------------------------------------------
    # Classes absentes
    # ---------------------------------------------------------

    missing_classes = [
        class_id
        for class_id in range(len(CLASS_NAMES))
        if class_counter[class_id] == 0
    ]

    print("\nClasses absentes :")

    if missing_classes:
        for class_id in missing_classes:
            print(
                f"- {class_id}: "
                f"{CLASS_NAMES[class_id]}"
            )
    else:
        print("Aucune classe absente.")

    # ---------------------------------------------------------
    # Conclusion
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("CONCLUSION")
    print("=" * 60)

    if (
        len(images) == len(labels)
        and len(missing_labels) == 0
        and len(labels_without_images) == 0
        and len(invalid_lines) == 0
        and len(invalid_class_ids) == 0
        and len(invalid_coordinates) == 0
        and len(missing_classes) == 0
    ):

        print("\n✓ DATASET VALIDE")
        print("✓ Images et annotations cohérentes")
        print("✓ 27 classes présentes")
        print("✓ Coordonnées YOLO valides")

    else:

        print("\n⚠ DATASET À VÉRIFIER")


if __name__ == "__main__":
    main()