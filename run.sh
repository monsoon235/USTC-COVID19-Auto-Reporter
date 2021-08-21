sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
apt update
apt install -y tesseract-ocr tesseract-ocr-eng locales
sed -i 's/# zh_CN.UTF-8 UTF-8/zh_CN.UTF-8 UTF-8/g' /etc/locale.gen
locale-gen
export LANG=zh_CN.UTF-8

pip install -r requirements.txt

while true; do
  date
  python3 reporter.py
  sleep 3600
done
