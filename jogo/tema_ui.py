import os
import json

def montar_tema(base_dir):
    tema = {
        "button": {
            "misc": {
                "border_width": "0",
                "shadow_width": "0"
            },
            "colours": {
                "normal_bg": "#00000000",
                "hovered_bg": "#00000000",
                "selected_bg": "#00000000",
                "disabled_bg": "#00000000",
                "normal_border": "#00000000",
                "hovered_border": "#00000000",
                "selected_border": "#00000000",
                "disabled_border": "#00000000",
                "normal_text": "#EFE6F5",
                "hovered_text": "#FFFFFF",
                "selected_text": "#FFFFFF",
                "disabled_text": "#8A8A8A"
            },
            "font": {
                "name": "arial",
                "size": "18",
                "bold": "1"
            }
        }
    }

    caminho_tema = os.path.join(base_dir, "assets", "ui", "tema_gerado.json")
    with open(caminho_tema, "w", encoding="utf-8") as f:
        json.dump(tema, f, ensure_ascii=False, indent=2)

    return caminho_tema