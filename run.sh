sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
apt update
apt install -y tesseract-ocr tesseract-ocr-eng
pip install -r requirements.txt

while true; do
    python3 reporter.py
    sleep 3600
done
