# Newsletter Project 
# AWS EC2 Setup Guide

## 1-create AWS Account
1.Go to https://aws.amazon.com

2.Sign up for a free-tier account

3.Add billing and verify identity

4.Choose Basic support plan 

## 2-Launch Amazon Linux 2 EC2 Instance
1.Go to the EC2 Dashboard

1.Click Launch Instance

### Configure:

1.Name: newsletter-ec2

2.AMI: Amazon Linux 2 AMI (HVM), SSD Volume Type

3.Instance Type: t2.micro (Free Tier)

4.Key pair: Create new, download .pem file

### Security group:

1.Add rule: SSH (port 22)

2.Add rule: HTTP (port 80) if needed

3.Click Launch

## 3-Connect via SSH
Move .pem file to your ~/.ssh folder:
(in vs code terminal)

mv ~/Downloads/your-key.pem ~/.ssh/ (change according to you)

chmod 400 ~/.ssh/your-key.pem

SSH into your EC2 instance:
ssh -i ~/.ssh/your-key.pem ec2-user@your-ec2-public-ip (change according to your public ip)

## 4-Install Python, Git, and Pip
### Amazon Linux 2 doesn't have Python 3.10+ by default, so install it manually:
sudo yum update -y
sudo yum install -y git
sudo amazon-linux-extras enable python3.8
sudo yum install -y python3.8 python3.8-devel

### Set python3 and pip3 aliases:
sudo alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
sudo alternatives --install /usr/bin/pip3 pip3 /usr/bin/pip3.8 1

## 5-Clone GitHub Repository
git clone https://github.com/Moazam-Alii/Newsletter-.git

cd Newsletter-

## 6-Create Virtual Environment (Optional)
python3 -m venv venv
source venv/bin/activate

## 7-Install Dependencies
pip3 install --upgrade pip
pip3 install -r requirements.txt

## 8-Set OpenAI Key
nano .env
OPENAI_API_KEY=your-openai-api-key (add your key in the file)
Save and exit (Ctrl + X, Y, Enter)

## 9-Install Playwright on Amazon Linux 2
pip3 install playwright
playwright install
### Install dependencies for Chromium:
sudo yum install -y libXcomposite libXcursor libXdamage libXrandr libXScrnSaver libXtst alsa-lib \
  atk cups-libs gtk3 libdrm libxkbcommon libxshmfence mesa-libEGL mesa-libGL \
  pango xorg-x11-fonts-Type1 xorg-x11-fonts-misc

## 10-Run with nohup (Background Execution)
nohup python3 app.py > output.log 2>&1 & 

### To check the logs:
tail -f output.log

### To stop the app:
ps aux | grep python (enter this command and check the process ID)
kill (process_id)

### your app will be running on your http://your-publicIP:5000 (port)











