from transformers import MarianMTModel, MarianTokenizer

# ดาวน์โหลดโมเดลและ Tokenizer สำหรับการแปลภาษาไทย -> อังกฤษ
model_name = "Helsinki-NLP/opus-mt-th-en"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

# บันทึกโมเดลและ Tokenizer
model.save_pretrained("./thai_to_english_model")
tokenizer.save_pretrained("./thai_to_english_model")
