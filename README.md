# Document Augmentation API

This project provides a web interface and REST API for uploading images (or entire folder of images) and applying various data augmentation techniques using OpenCV and FastAPI.

## 1. API Endpoint Summary
- Endpoint: `/generate`
- Method: GET
- Description : Loads the HTML frontend for upload

- Endpoint: `/generate`
- Method: POST
- Description: Accepts files & method and return result

## 2. Augmentation Methods
| Method  | Description                        |
|---------|------------------------------------|
| flip    | Horizontally flips the image       |
| scale   | Rescales image by 1.2x             |
| noise   | Adds Gaussian noise (mean=0, std=25px) |
| blur    | Applies a blur filter              |
| sharpen | Sharpens the image                 |
| rotate  | Rotates by custom angle            |
| all     | Applies all above and returns all variants |

## 3. Features
- Upload multiple images or an entire folder
- Choose from the following augmentations:
  - Flip
  - Scale
  - Noise
  - Blur
  - Sharpen
  - Rotate (custom Angle)
  - All augmentations combined
- Download processed files as .zip archive if more than one image is augmented.

## 4. Technologies Used
- FastAPI - backend API framework
- OpenCV (cv2) - image processing
- Jinja2 - templating engine for the frontend
- HTML - static frontend with folder upload support

## 5. Installation & Setup
- Clone the repo:
  git clone <repo_url>

- Create a virtual environment(optional):
  conda create -n image_aug python=3.10
  conda activate image_aug

- Install dependencies:
  pip install fastapi uvicorn opencv-python numpy jinja2

- Run the app:
  uvicorn main:app --reload

- Open your browser and go to:
  http://127.0.0.1:8000

## 6. Usage Instructions
- Upload multiple images or an entire folder
- Select an augmentation method
- If Rotate is selected, specify the angle
- Click Apply Augmentation
- Download the resulting .zip file or single image
