import os, cv2
 
def generate_video(image_folder, video_name, fps):
    images = [
        img
        for img in os.listdir(image_folder)
        if img.endswith(".jpg") or img.endswith(".jpeg") or img.endswith("png")
    ]

    # Array images should only consider
    # the image files ignoring others if any

    images = sorted(images, key=lambda x: int(x.split(".")[0]))

    print(images)

    frame = cv2.imread(os.path.join(image_folder, images[0]))

    # setting the frame width, height width
    # the width, height of first image
    height, width, layers = frame.shape

    video = cv2.VideoWriter(
        video_name, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
    )

    # Appending the images to the video one by one
    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    # Deallocating memories taken for window creation
    cv2.destroyAllWindows()
    video.release()  # releasing the video generated


# Calling the generate_video function
if __name__ == "__main__":
    image_folder = "images"
    video_name = "demo.mp4"
    fps = 20
    generate_video(image_folder, video_name, fps)