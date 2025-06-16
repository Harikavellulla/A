import streamlit as st
from tensorflow.keras.applications import (
    VGG16,VGG19, ResNet50, InceptionV3, Xception, MobileNetV2, DenseNet121
)
from tensorflow.keras.applications.imagenet_utils import decode_predictions, preprocess_input
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import time

# Dictionary of Keras application models
MODELS = {
    "VGG16": VGG16,
    "VGG19":VGG19,
    "ResNet50": ResNet50,
    "InceptionV3": InceptionV3,
    "Xception": Xception,
    "MobileNetV2": MobileNetV2,
    "DenseNet121": DenseNet121
}

# Streamlit app UI
st.title("🧠 Keras Pretrained Model Image Classifier")
st.sidebar.title("Settings")

# Select model
model_name = st.sidebar.selectbox("Choose a Model", list(MODELS.keys()))
model = MODELS[model_name](weights='imagenet')

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    img = Image.open(uploaded_file).convert('RGB')
    st.image(img, caption="Uploaded Image", use_column_width=True)

    # Preprocess image
    img_resized = img.resize((224, 224))  # Some models need 299x299 like Xception/Inception
    if model_name in ["Xception", "InceptionV3"]:
        img_resized = img.resize((299, 299))

    img_array = image.img_to_array(img_resized)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # Predict
    st.write("⏳ Predicting...")
    start = time.time()
    preds = model.predict(img_array)
    end = time.time()

    # Decode and show predictions
    top_preds = decode_predictions(preds, top=3)[0]
    st.success(f"✅ Prediction completed in {end - start:.2f} seconds")
    st.subheader("🔍 Top Predictions:")
    for i, pred in enumerate(top_preds):
        st.write(f"{i+1}. **{pred[1]}** ({pred[2]*100:.2f}%)")

else:
    st.info("Please upload an image to begin.")

