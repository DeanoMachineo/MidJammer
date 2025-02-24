from flask import Flask, request, render_template
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        prompt = request.form['prompt']
        sref_count = int(request.form['sref_count'])
        aspect_ratio = request.form['aspect_ratio']
        results = generate_images(prompt, sref_count, aspect_ratio)
        return render_template('results.html', results=results)
    return render_template('home.html')

def generate_images(prompt, sref_count, aspect_ratio):
    chrome_options = Options()
    profile_dir = os.path.join(os.getcwd(), "chrome_profile")
    os.makedirs(profile_dir, exist_ok=True)
    chrome_options.add_argument(f"user-data-dir={profile_dir}")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.get("https://discord.com/channels/1136719932407681200/1136719933347221587")
    time.sleep(10)
    print("Page loaded")
    driver.refresh()
    time.sleep(5)
    print("Page refreshed")

    def get_input_box():
        return WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-slate-node='element']"))
        )

    results = []

    # Send base prompt
    input_box = get_input_box()
    input_box.click()
    base_prompt = f"/imagine prompt: {prompt} --ar {aspect_ratio}"
    input_box.send_keys(base_prompt)
    print("Base prompt typed")
    time.sleep(1)
    input_box = get_input_box()
    input_box.send_keys(Keys.ENTER)
    print("Base prompt sent")
    time.sleep(2)
    results.append(f"Base: {prompt} --ar {aspect_ratio}")

    # Send random sref prompts
    for i in range(sref_count):
        input_box = get_input_box()
        input_box.click()
        styled_prompt = f"/imagine prompt: {prompt} --sref random --ar {aspect_ratio}"
        input_box.send_keys(styled_prompt)
        print(f"Run {i+1} typed")
        time.sleep(1)
        input_box = get_input_box()
        input_box.send_keys(Keys.ENTER)
        print(f"Run {i+1} sent")
        time.sleep(2)
        results.append(f"Run {i+1}: {styled_prompt}")

    driver.quit()
    return results

if __name__ == '__main__':
    app.run(debug=True)