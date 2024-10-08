from playwright.sync_api import sync_playwright
import json

authorization = None

def run(playwright):
    global authorization
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    page.on("request", lambda request: handle_request(request))
    page.goto("https://web.telegram.org")
    try:
        with open('cookies.json','rt',encoding='utf-8-sig') as file:
            content = file.read()
            data = json.loads(content)
    except Exception as e:
        print('Cookie file should contain required cookies.')
        exit()

    for k, v in data.items():
        page.evaluate(f"localStorage.setItem('{k}', '{v}');")

    page.goto("https://web.telegram.org/k/#@notpixel")

    try:
        page.wait_for_selector('[class="new-message-bot-commands is-view"]', timeout=100000)
        page.click('[class="new-message-bot-commands is-view"]')

        page.wait_for_selector('.popup-buttons', timeout=100000)
        buttons = page.query_selector_all('button')
        for button in buttons:
            try:
                button_text = button.query_selector("span.i18n").inner_text()
            except Exception as e:
                continue
            if button_text.upper() == 'LAUNCH':
                button.click()

                page.wait_for_timeout(20000)
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    browser.close()

def handle_request(request):
    global authorization
    if "users/me" in request.url:
        headers = request.all_headers()
        authorization = headers['authorization']

def get_authorization():
    with sync_playwright() as playwright:
        run(playwright)
        return authorization
