from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import shutil
import cv2
import numpy as np
from augmentations import *

app = FastAPI()

UPLOAD_FOLDER = "uploads"
AUG_FOLDER = "augmented"
ZIP_NAME = "augmented_images.zip"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUG_FOLDER, exist_ok=True)

templates = Jinja2Templates(directory="templates")

augmentations = {
    "flip": flip_image,
    "rotate": rotate_image,
    "scale": scale_image,
    "translate": translate_image,
    "noise": add_noise,
    "shear": shear_image,
}

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("frontend.html", {"request": request})

@app.post("/generate/")
async def generate_augmented_imgs(
    request: Request,
    files: list[UploadFile] = File(...),
    method: str = Form(...)
):
    if os.path.exists(AUG_FOLDER):
        shutil.rmtree(AUG_FOLDER)
    os.makedirs(AUG_FOLDER, exist_ok=True)

    output_files = []

    for file in files:
        contents = await file.read()
        img = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            continue

        filename = os.path.splitext(file.filename)[0]

        if method.startswith("rotate:"):
            angle = int(method.split(":")[1])
            aug_img = rotate_image(img, angle)
            out_path = os.path.join(AUG_FOLDER, f"{filename}_rotate.jpg")
            cv2.imwrite(out_path, aug_img)
            output_files.append(out_path)

        elif method == "flip":
            aug_img = flip_image(img)
            out_path = os.path.join(AUG_FOLDER, f"{filename}_flip.jpg")
            cv2.imwrite(out_path, aug_img)
            output_files.append(out_path)

        elif method == "scale":
            aug_img = scale_image(img)
            out_path = os.path.join(AUG_FOLDER, f"{filename}_scale.jpg")
            cv2.imwrite(out_path, aug_img)
            output_files.append(out_path)

        elif method == "translate":
            aug_img = translate_image(img)
            out_path = os.path.join(AUG_FOLDER, f"{filename}_translate.jpg")
            cv2.imwrite(out_path, aug_img)
            output_files.append(out_path)

        elif method == "noise":
            aug_img = add_noise(img)
            out_path = os.path.join(AUG_FOLDER, f"{filename}_noise.jpg")
            cv2.imwrite(out_path, aug_img)
            output_files.append(out_path)

        elif method == "shear":
            aug_img = shear_image(img)
            out_path = os.path.join(AUG_FOLDER, f"{filename}_shear.jpg")
            cv2.imwrite(out_path, aug_img)
            output_files.append(out_path)

        elif method == "all":
            for func, suffix in [
                (flip_image, "flip"),
                (lambda img: rotate_image(img, 90), "rotate"),
                (scale_image, "scale"),
                (translate_image, "translate"),
                (add_noise, "noise"),
                (shear_image, "shear"),
            ]:
                aug_img = func(img.copy())
                out_path = os.path.join(AUG_FOLDER, f"{filename}_{suffix}.jpg")
                cv2.imwrite(out_path, aug_img)
                output_files.append(out_path)

        else:
            continue

    if len(output_files) > 1:
        shutil.make_archive("augmented_images", 'zip', AUG_FOLDER)
        return FileResponse(
            "augmented_images.zip",
            filename="augmented_images.zip",
            media_type="application/zip"
        )
    elif len(output_files) == 1:
        return FileResponse(
            output_files[0],
            filename=os.path.basename(output_files[0]),
            media_type="image/jpeg"
        )
    else:
        return JSONResponse({"error": "No valid image processed"}, status_code=400)
