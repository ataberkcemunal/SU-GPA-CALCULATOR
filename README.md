# GPA Calculator

A Python tool to calculate GPA based on Sabanci University's grading system. This tool helps students estimate their future GPA by processing their transcript PDF and allowing them to input estimated grades for registered courses.

## Features

- Extracts course information from transcript PDF
- Supports Sabanci University's grading system
- Calculates both term GPA and CGPA
- Handles S/U (Satisfactory/Unsatisfactory) grades
- Supports both SU Credits and ECTS calculations

## Requirements

- Python 3.x
- pdfplumber

## Installation

1. Clone this repository:
```bash
git clone https://github.com/ataberkcemunal/SU-GPA-CALCULATOR.git
cd SU-GPA-CALCULATOR
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your transcript PDF file in the same directory as the script
2. Run the script:
```bash
python gpa_calculator.py
```
3. Follow the prompts to enter estimated grades for your registered courses

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

# GPA Hesaplayıcı

Sabancı Üniversitesi'nin not sistemine göre GPA hesaplayan bir Python aracı. Bu araç, öğrencilerin transkript PDF'lerini işleyerek ve kayıtlı dersler için tahmini notlar girmelerine olanak sağlayarak gelecekteki GPA'lerini tahmin etmelerine yardımcı olur.

## Özellikler

- Transkript PDF'inden ders bilgilerini çıkarır
- Sabancı Üniversitesi'nin not sistemini destekler
- Dönem GPA'si ve CGPA hesaplar
- S/U (Başarılı/Başarısız) notlarını destekler
- SU Kredileri ve ECTS hesaplamalarını destekler

## Gereksinimler

- Python 3.x
- pdfplumber

## Kurulum

1. Bu depoyu klonlayın:
```bash
git clone https://github.com/ataberkcemunal/SU-GPA-CALCULATOR.git
cd SU-GPA-CALCULATOR
```

2. Sanal ortam oluşturun ve aktifleştirin:
```bash
python -m venv venv
source venv/bin/activate  # Windows'ta: venv\Scripts\activate
```

3. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

## Kullanım

1. Transkript PDF dosyanızı script ile aynı dizine yerleştirin
2. Scripti çalıştırın:
```bash
python gpa_calculator.py
```
3. Kayıtlı dersleriniz için tahmini notları girmek üzere yönergeleri takip edin

## Lisans

Bu proje MIT Lisansı altında lisanslanmıştır - detaylar için [LICENSE](LICENSE) dosyasına bakın. 