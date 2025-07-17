import os
import hashlib
import json

def calculate_sha1(file_path):
    sha1 = hashlib.sha1()
    with open(file_path, "rb") as f:
        while True:
            data = f.read(65536)  # читаємо блоками по 64кб
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()

def generate_manifest(game_version, mods_dir="mods", versions_dir="versions"):
    manifest = {
        "game_version": game_version,
        "versions": [],
        "mods": []
    }

    # Обробка папки versions
    if os.path.exists(versions_dir):
        for folder_name in os.listdir(versions_dir):
            folder_path = os.path.join(versions_dir, folder_name)
            if os.path.isdir(folder_path):
                # Припускаємо, що в кожній папці versions є один файл installer.jar (або інший)
                for file_name in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, file_name)
                    if os.path.isfile(file_path):
                        sha1_hash = calculate_sha1(file_path)
                        manifest["versions"].append({
                            "folder": folder_name,
                            "file": file_name,
                            "sha1": sha1_hash
                        })
                        break  # беремо перший файл у папці і виходимо
    else:
        print(f"Папка '{versions_dir}' не знайдена!")

    # Обробка папки mods
    if os.path.exists(mods_dir):
        for file_name in os.listdir(mods_dir):
            file_path = os.path.join(mods_dir, file_name)
            if os.path.isfile(file_path):
                sha1_hash = calculate_sha1(file_path)
                manifest["mods"].append({
                    "file": file_name,
                    "sha1": sha1_hash
                })
    else:
        print(f"Папка '{mods_dir}' не знайдена!")

    # Запис у файл manifest.json
    with open("manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4, ensure_ascii=False)

    print("Manifest saved to manifest.json")

if __name__ == "__main__":
    # Вкажи тут потрібну версію гри
    game_version = "1.20.1-forge-47.4.0"
    generate_manifest(game_version)
