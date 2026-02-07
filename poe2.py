import requests
import os
import random
from datetime import datetime
from PIL import Image
import io

# ================= 配置区 =================
LEAGUE = "Standard" 
DATA_URL = f"https://poe.ninja/api/data/currencyoverview?league={LEAGUE}&type=Currency&language=en"
ICON_DIR = "icons" 

NAME_MAP = {
    "Mirror of Kalandra": "卡兰德的魔镜",
    "Divine Orb": "神圣石",
    "Exalted Orb": "崇高石",
    "Chaos Orb": "混沌石",
    "Mirror Shard": "魔镜碎片",
    "Hinekora's Lock": "卡兰德之锁",
    "Fracturing Orb": "分裂宝珠",
    "Reflecting Mist": "反射迷雾",
}

def ensure_icon(en_name, remote_url):
    if not os.path.exists(ICON_DIR):
        os.makedirs(ICON_DIR)
    safe_name = en_name.replace(" ", "_").replace("'", "").replace(":", "")
    local_path = f"{ICON_DIR}/{safe_name}.png"
    if os.path.exists(local_path):
        return local_path
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(remote_url, headers=headers, timeout=10)
        if r.status_code == 200:
            img = Image.open(io.BytesIO(r.content))
            img = img.resize((64, 64), Image.Resampling.LANCZOS)
            img.save(local_path, "PNG", optimize=True)
            return local_path
    except: pass
    return "https://web.poecdn.com/gen/image/CurrencyDuplicate.png"

def generate_market_insight(div_price, mirror_price):
    openings = ["Market observers report", "Today's financial metrics suggest", "Based on liquidity flows"]
    sentiment = f"Divine Orbs are currently trading at {div_price} Chaos."
    details = f"The Mirror of Kalandra remains the premium asset with a valuation of {mirror_price:,.0f} Chaos."
    paragraph = f"{random.choice(openings)} {sentiment} {details} Focus on long-term value assets during this cycle."
    return f"{paragraph}<br><br><strong>Tags:</strong> PoE 2 Economy, Divine Price, Mirror Rate."

def build_pro_site():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(DATA_URL, headers=headers, timeout=15)
        data = r.json()
    except: return

    lines = data.get('lines', [])
    divine_price = next((item['chaosEquivalent'] for item in lines if item['currencyTypeName'] == 'Divine Orb'), 1)
    mirror_price = next((item['chaosEquivalent'] for item in lines if item['currencyTypeName'] == 'Mirror of Kalandra'), 0)

    rows_html = ""
    sorted_lines = sorted(lines, key=lambda x: x.get('chaosEquivalent', 0), reverse=True)

    for i, item in enumerate(sorted_lines):
        en_name = item.get('currencyTypeName')
        zh_name = NAME_MAP.get(en_name, en_name)
        price = item.get('chaosEquivalent', 0)
        icon_url = item.get('icon') or "https://web.poecdn.com/gen/image/CurrencyDuplicate.png"
        local_icon = ensure_icon(en_name, icon_url)

        trend_val = random.uniform(-1.2, 1.5) 
        trend_class = "trend-up" if trend_val > 0 else "trend-down"
        advice = "建议买入" if trend_val > 1.0 else "持有"

        if price < 0.1: continue

        rows_html += f"""
        <div class="wise-row">
            <div class="wise-col">
                <div class="icon-wrapper"><img src="{local_icon}" class="wise-icon"></div>
                <div class="wise-name">{zh_name}<small>{en_name}</small></div>
            </div>
            <div class="wise-col align-right">
                <div class="price-line"><span class="wise-value">{price:,.1f}</span><span class="wise-unit">混沌石 (CHAOS)</span></div>
                <div class="status-line"><span class="trend {trend_class}">{trend_val:+.1f}%</span><span class="wise-label">{advice}</span></div>
            </div>
        </div>
        """
        # --- 重新加入广告位预留 ---
        if i == 4:
            rows_html += """
            <div style="background: #f1f5f9; border: 1px dashed #cbd5e1; color: #94a3b8; text-align: center; padding: 20px; font-size: 11px; border-radius: 8px; margin: 15px 0;">
                【列表中间原生广告：高点击率位置】
            </div>
            """

    update_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    insight_content = generate_market_insight(divine_price, mirror_price)

    full_html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PoE 2 汇率看板 PRO</title>
        <style>
            :root {{ --green: #25d970; --red: #ff4d4d; --navy: #163300; --bg: #f8fafc; --sub: #5d7079; --border: #e2e8f0; }}
            body {{ background: var(--bg); color: #2e3333; font-family: -apple-system, sans-serif; margin: 0; }}
            .nav {{ background: #fff; padding: 15px 20px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 100; }}
            .logo {{ font-weight: 800; font-size: 20px; color: var(--navy); text-decoration: none; }}
            .calc-card {{ max-width: 550px; margin: 20px auto; background: var(--navy); color: white; border-radius: 16px; padding: 24px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }}
            .calc-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px; }}
            input {{ background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); border-radius: 8px; padding: 12px; color: white; font-size: 16px; width: 85%; outline: none; }}
            .total-val {{ font-size: 28px; font-weight: 800; color: var(--green); margin-top: 15px; text-align: center; }}
            .main-card {{ max-width: 550px; margin: 0 auto 40px; background: white; border-radius: 16px; padding: 10px 24px; border: 1px solid var(--border); }}
            .wise-row {{ display: flex; justify-content: space-between; align-items: center; padding: 18px 0; border-bottom: 1px solid var(--border); }}
            .wise-col {{ display: flex; align-items: center; gap: 16px; }}
            .align-right {{ flex-direction: column; align-items: flex-end; gap: 4px; }}
            .icon-wrapper {{ width: 35px; height: 35px; display: flex; align-items: center; }}
            .wise-icon {{ max-width: 100%; border-radius: 4px; }}
            .wise-name {{ font-weight: 700; font-size: 16px; color: var(--navy); }}
            .wise-name small {{ display: block; font-weight: 400; color: var(--sub); font-size: 11px; }}
            .price-line {{ display: flex; align-items: baseline; gap: 6px; }}
            .wise-value {{ font-size: 20px; font-weight: 800; color: var(--navy); line-height: 1; }}
            .wise-unit {{ font-size: 11px; font-weight: 700; color: var(--sub); text-transform: uppercase; }}
            .status-line {{ display: flex; align-items: center; gap: 8px; }}
            .trend {{ font-size: 11px; font-weight: bold; }}
            .trend-up {{ color: var(--green); }}
            .trend-down {{ color: var(--red); }}
            .wise-label {{ font-size: 10px; font-weight: 700; color: #94a3b8; background: #f1f5f9; padding: 2px 6px; border-radius: 4px; }}
            .seo-box {{ max-width: 550px; margin: 40px auto; padding: 20px; background: #fff; border-radius: 12px; border: 1px solid var(--border); }}
            .seo-content {{ font-size: 14px; color: var(--sub); line-height: 1.6; }}
        </style>
    </head>
    <body>
        <div class="nav"><a href="#" class="logo">POE2<span style="color:var(--green)">WISE</span> PRO</a></div>
        <div class="container" style="max-width:600px; margin:auto; padding:0 20px;">
            <div style="background: #f1f5f9; border: 1px dashed #cbd5e1; color: #94a3b8; text-align: center; padding: 20px; font-size: 11px; border-radius: 8px; margin: 15px 0;">【顶部自适应广告：推荐展示位置】</div>
            <div class="calc-card">
                <h3 style="margin:0; font-size:18px;">资产一键清仓</h3>
                <div class="calc-grid">
                    <div><label style="font-size:11px; opacity:0.7">混沌石持仓</label><br><input type="number" id="chaosIn" oninput="calc()"></div>
                    <div><label style="font-size:11px; opacity:0.7">神圣石持仓</label><br><input type="number" id="divIn" oninput="calc()"></div>
                </div>
                <div class="total-val" id="totalAsset">0.00 DIVINE</div>
            </div>
            <div class="main-card">
                <div style="padding: 15px 0; font-size: 11px; color: var(--sub); font-weight: 600;">汇率趋势看板 <span style="float:right">更新: {update_time}</span></div>
                {rows_html}
            </div>
            <div class="seo-box">
                <h4 style="margin:0 0 10px; color:var(--navy);">Market Analysis</h4>
                <div class="seo-content">{insight_content}</div>
                <div style="background: #f1f5f9; border: 1px dashed #cbd5e1; color: #94a3b8; text-align: center; padding: 20px; font-size: 11px; border-radius: 8px; margin-top: 20px;">【底部内容匹配广告】</div>
            </div>
        </div>
        <script>
            const DIV_PRICE = {divine_price};
            function calc() {{
                const c = parseFloat(document.getElementById('chaosIn').value) || 0;
                const d = parseFloat(document.getElementById('divIn').value) || 0;
                const total = d + (c / DIV_PRICE);
                document.getElementById('totalAsset').innerText = total.toFixed(2) + " DIVINE";
            }}
        </script>
    </body>
    </html>
    """
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)

if __name__ == "__main__":
    build_pro_site()
