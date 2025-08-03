from flask import Flask, jsonify, Response
import os
import requests
from io import BytesIO
from PIL import Image, ImageDraw

app = Flask(__name__)

@app.route('/api/widget')
def get_icon():
    img_url = f"https://api.mcstatus.io/v2/widget/java/{os.environ['url']}"
    try:
        resp = requests.get(img_url, timeout=5)
        resp.raise_for_status()
        base_img = Image.open(BytesIO(resp.content)).convert("RGBA")
        
        draw = ImageDraw.Draw(base_img)
        
        # Coordinates for the square
        x0, y0 = 739, 205
        x1, y1 = x0 + 111, y0 + 22
        
        # Draw a semi-transparent red rectangle (square)
        draw.rectangle([x0, y0, x1, y1], fill=(35, 35, 35))

        x0, y0 = 228, 86
        x1, y1 = x0 + 352, y0 + 33
        
        # Draw a semi-transparent red rectangle (square)
        draw.rectangle([x0, y0, x1, y1], fill=(35, 35, 35))

        x0, y0 = 229, 126
        width, height = 622, 42
        x1, y1 = x0 + width, y0 + height

        # Crop the rectangle area from the image (copy)
        cropped_region = base_img.crop((x0, y0, x1, y1))

        # Decide where to paste it (example: 50 px right and 50 px down)
        paste_x, paste_y = 228, 80

        # Paste the cropped region back onto the image at new position
        base_img.paste(cropped_region, (paste_x, paste_y))

        x0, y0 = 229, 124
        x1, y1 = x0 + 622, y0 + 89
        
        # Draw a semi-transparent red rectangle (square)
        draw.rectangle([x0, y0, x1, y1], fill=(35, 35, 35))

        x0, y0 = 225, 39
        width, height = 622, 90
        x1, y1 = x0 + width, y0 + height

        # Crop the rectangle area from the image (copy)
        cropped_region = base_img.crop((x0, y0, x1, y1))

        # Decide where to paste it (example: 50 px right and 50 px down)
        paste_x, paste_y = 225, 76

        # Paste the cropped region back onto the image at new position
        base_img.paste(cropped_region, (paste_x, paste_y))

        x0, y0 = 221, 31
        x1, y1 = x0 + 264, y0 + 46
        
        # Draw a semi-transparent red rectangle (square)
        draw.rectangle([x0, y0, x1, y1], fill=(35, 35, 35))

        buf = BytesIO()
        base_img.save(buf, format='PNG')
        buf.seek(0)
        
        return Response(buf.getvalue(), content_type='image/png')
    
    except Exception as e:
        print(f"Error: {e}")
        return Response("Image not found or error", status=404)

@app.route('/api/infoserver')
def get_info():
    url_info = f"https://api.mcstatus.io/v2/status/java/{os.environ['url']}"
    try:
        resp = requests.get(url_info, timeout=5)
        data = resp.json()  # Convert response to JSON dictionary

        out = {
            "online": data["online"],
            "players": data["players"]["online"],
            "maxplayers": data["players"]["max"]
        }
        return jsonify(out)  # Flask handles content type automatically
    except Exception as e:
        print(f"Error: {e}")
        return Response("not found", status=404)

if __name__ == "__main__":
    app.run(port=8080)

