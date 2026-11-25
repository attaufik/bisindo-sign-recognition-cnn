import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report, confusion_matrix
import argparse

def evaluate(model_path, val_dir):
    print(f"Memuat model {model_path}...")
    model = tf.keras.models.load_model(model_path)
    
    # Diagnosis #8: Val generator harus murni TANPA augmentasi & shuffle=False
    val_datagen = ImageDataGenerator(rescale=1./255)
    val_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=(224, 224),   # sesuai model CNN terbaru (224x224)
        batch_size=32,
        class_mode='categorical',
        shuffle=False
    )
    
    print("Mengevaluasi model pada dataset validasi bersih...")
    predictions = model.predict(val_generator)
    y_pred = np.argmax(predictions, axis=1)
    y_true = val_generator.classes
    class_names = list(val_generator.class_indices.keys())
    
    print("\n=== CLASSIFICATION REPORT (Akurasi Asli) ===")
    print(classification_report(y_true, y_pred, target_names=class_names))
    
    # Diagnosis #6: Identifikasi pasangan huruf yang paling sering tertukar
    cm = confusion_matrix(y_true, y_pred)
    print("\n=== TOP CONFUSIONS (Huruf yang Sering Tertukar) ===")
    np.fill_diagonal(cm, 0) # Sembunyikan tebakan yang benar agar fokus ke error
    ditemukan_error = False
    for i in range(len(class_names)):
        for j in range(len(class_names)):
            if cm[i, j] > 3: # Tampilkan jika salah tebak lebih dari 3 kali
                print(f"Huruf {class_names[i]} malah ditebak sebagai {class_names[j]}: {cm[i,j]} kali")
                ditemukan_error = True
                
    if not ditemukan_error:
         print("Model cukup solid, tidak ada salah tebak dominan.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default='model_bisindo_cnn.h5')
    parser.add_argument('--dir', type=str, default='images/val')
    args = parser.parse_args()
    evaluate(args.model, args.dir)