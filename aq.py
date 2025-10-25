import serial
import time
import threading
from flask import Flask, render_template_string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import redirect
import datetime

app = Flask(__name__)

current_data = {
    'ph': 7.25,
    'turbidity': 280,
    'is_dirty': False,
    'status': 'NORMAL',
    'last_email_sent': None,
    'alert_count': 0
}

# Email Configuration
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'harshpreet4799.se24@chitkara.edu.in',
    'sender_password': 'tujpdnhfxkvkcmrt',
    'receiver_email': 'harshpreet98143@gmail.com'
}

def can_send_email():
    """Check if we can send email (prevent spam)"""
    if current_data['last_email_sent'] is None:
        return True
    
    # Wait at least 10 minutes between emails
    time_since_last = (datetime.datetime.now() - current_data['last_email_sent']).total_seconds()
    return time_since_last > 600  # 10 minutes

def send_email_alert(ph, turbidity, status, reason):
    """Send email alert when water quality is bad"""
    try:
        # Check if we can send email
        if not can_send_email():
            print("⏳ Too soon to send another email")
            return False
        
        # Create message
        message = MIMEMultipart()
        message['From'] = EMAIL_CONFIG['sender_email']
        message['To'] = EMAIL_CONFIG['receiver_email']
        message['Subject'] = f'🚨 AQUARIUM ALERT - {status}'
        
        # Email body
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background: #fff0f0; padding: 20px;">
            <div style="background: white; padding: 30px; border-radius: 10px; border-left: 10px solid #ff4444;">
                <h1 style="color: #ff4444;">🚨 WATER QUALITY ALERT!</h1>
                <h2>Immediate Action Required</h2>
                
                <div style="background: #fff3cd; padding: 15px; border-radius: 5px; margin: 15px 0;">
                    <h3>🔍 ALERT DETAILS:</h3>
                    <p><strong>pH Level:</strong> <span style="color: {'#ff4444' if ph < 6.5 else '#28a745'}">{ph:.2f}</span> {'🚨 (TOO ACIDIC!)' if ph < 6.5 else '✅ (Normal)'}</p>
                    <p><strong>Turbidity:</strong> <span style="color: {'#ff4444' if turbidity < 200 else '#28a745'}">{turbidity}</span> {'🚨 (DIRTY WATER!)' if turbidity < 200 else '✅ (Clean)'}</p>
                    <p><strong>Status:</strong> <span style="color: #ff4444; font-weight: bold;">{status}</span></p>
                    <p><strong>Reason:</strong> {reason}</p>
                    <p><strong>Time:</strong> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                
                <div style="background: #ffebee; padding: 15px; border-radius: 5px;">
                    <h3>🎯 REQUIRED ACTION:</h3>
                    <p><strong>CHANGE WATER IMMEDIATELY!</strong></p>
                    <p>• Check fish health</p>
                    <p>• Perform 25-50% water change</p>
                    <p>• Test water parameters after change</p>
                </div>
                
                <p style="margin-top: 20px; color: #666; font-size: 12px;">
                    Alert #{current_data['alert_count'] + 1} from Smart Aquarium Monitoring System
                </p>
            </div>
        </body>
        </html>
        """
        
        message.attach(MIMEText(body, 'html'))
        
        # Send email with timeout
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'], timeout=30)
        server.starttls()
        server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
        server.send_message(message)
        server.quit()
        
        current_data['last_email_sent'] = datetime.datetime.now()
        current_data['alert_count'] += 1
        print(f"✅ Email alert #{current_data['alert_count']} sent successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False

def read_arduino_data():
    while True:
        try:
            ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
            time.sleep(2)
            print("✅ Connected to Arduino")
            
            while True:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    print(f"📨 {line}")
                    
                    if "PH:" in line:
                        try:
                            parts = line.split(',')
                            data = {}
                            for part in parts:
                                if ':' in part:
                                    key, value = part.split(':', 1)
                                    data[key] = value
                            
                            # Store old values to detect changes
                            old_status = current_data['status']
                            
                            # Update current values
                            current_data['ph'] = float(data.get('PH', 7.0))
                            current_data['turbidity'] = int(data.get('TURB', 280))
                            current_data['is_dirty'] = (current_data['turbidity'] < 200)
                            
                            # Update status
                            ph = current_data['ph']
                            dirty = current_data['is_dirty']
                            
                            if ph < 6.5 and dirty:
                                current_data['status'] = 'CRITICAL'
                                reason = 'pH too acidic AND water dirty'
                                # Send email only when status changes to CRITICAL
                                if old_status != 'CRITICAL':
                                    send_email_alert(ph, current_data['turbidity'], 'CRITICAL', reason)
                            elif ph < 6.5:
                                current_data['status'] = 'WARNING'
                                reason = 'pH too acidic'
                                if old_status != 'WARNING':
                                    send_email_alert(ph, current_data['turbidity'], 'WARNING', reason)
                            elif dirty:
                                current_data['status'] = 'WARNING'
                                reason = 'Water dirty'
                                if old_status != 'WARNING':
                                    send_email_alert(ph, current_data['turbidity'], 'WARNING', reason)
                            else:
                                current_data['status'] = 'NORMAL'
                                
                        except Exception as e:
                            print(f"Error: {e}")
                
                time.sleep(0.1)
                
        except Exception as e:
            print(f"Connection error: {e}")
            time.sleep(5)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Aquarium Monitor</title>
    <meta http-equiv="refresh" content="3">
    <style>
        body { font-family: Arial; margin: 20px; background: #f5f5f5; }
        .container { max-width: 500px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 10px; text-align: center; }
        .status { padding: 20px; margin: 15px 0; border-radius: 10px; text-align: center; font-size: 20px; font-weight: bold; }
        .normal { background: #d4edda; color: #155724; }
        .warning { background: #fff3cd; color: #856404; }
        .critical { background: #f8d7da; color: #721c24; }
        .data { font-size: 18px; margin: 10px 0; padding: 10px; background: #f8f9fa; border-radius: 5px; }
        .email-info { background: #e7f3ff; padding: 10px; border-radius: 5px; margin: 10px 0; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐠 Aquarium Monitor</h1>
            <p>Email Alerts - Reliable Mode</p>
        </div>
        
        <div class="email-info">
            📧 Emails: {{ alert_count }} sent | 
            {% if last_email_sent %}
                Last: {{ last_email_sent.strftime('%H:%M') }}
            {% else %}
                No emails sent yet
            {% endif %}
        </div>
        
        <div class="status {{ status.lower() }}">
            {% if status == 'NORMAL' %}✅ Water SAFE
            {% elif status == 'WARNING' %}⚠️ CHANGE WATER SOON!
            {% else %}🚨 CHANGE WATER IMMEDIATELY!{% endif %}
        </div>
        
        <div class="data">
            <div>pH: <strong>{{ "%.2f"|format(ph) }}</strong></div>
            <div>Turbidity: <strong>{{ turbidity }}</strong></div>
            <div>Water: <strong>{{ "DIRTY" if is_dirty else "CLEAN" }}</strong></div>
        </div>
        
        <div style="text-align: center;">
            <a href="/test-email"><button style="background: #28a745; color: white; border: none; padding: 10px 20px; margin: 10px; border-radius: 5px; cursor: pointer;">📧 Test Email Now</button></a>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def dashboard():
    return render_template_string(HTML, **current_data)

@app.route('/test-email')
def test_email():
    send_email_alert(5.50, 120, 'TEST', 'Manual test email')
    return redirect('/')

if __name__ == '__main__':
    thread = threading.Thread(target=read_arduino_data)
    thread.daemon = True
    thread.start()
    print("🚀 Dashboard running: http://192.168.1.114:5000")
    print("📧 Email system: RELIABLE MODE (10 min cooldown)")
    app.run(host='0.0.0.0', port=5000, debug=False)