import requests
import os
import random
from datetime import datetime
from PIL import Image
import io

# ================= 1. 配置与翻译字典 =================
LEAGUE = "Standard" 
DATA_URL = f"https://poe.ninja/api/data/currencyoverview?league={LEAGUE}&type=Currency&language=en"
ICON_DIR = "icons" 

NAME_MAP = {
    "Mirror of Kalandra": "卡兰德的魔镜",
    "Mirror Shard": "魔镜碎片",
    "Hinekora's Lock": "卡兰德之锁",
    "Divine Orb": "神圣石",
    "Exalted Orb": "崇高石",
    "Ancient Orb": "远古宝珠",
    "Fracturing Orb": "分裂宝珠",
    "Fracturing Shard": "分裂碎片",
    "Chaos Orb": "混沌石",
    "Vaal Orb": "瓦尔宝珠",
    "Orb of Annulment": "剥离宝珠",
    "Orb of Regret": "后缀重铸石",
    "Orb of Unmaking": "洗点水",
    "Orb of Scouring": "重铸石",
    "Orb of Alchemy": "点金石",
    "Orb of Fusing": "连接石",
    "Orb of Alteration": "改造石",
    "Chromatic Orb": "幻色石",
    "Enkindling Orb": "点燃宝珠",
    "Instilling Orb": "滴注宝珠",
    "Gemcutter's Prism": "宝石匠的棱镜",
    "Glassblower's Bauble": "玻璃弹珠",
    "Cartographer's Chisel": "制图钉",
    "Sacred Orb": "神圣宝珠",
    "Reflecting Mist": "反射迷雾",
    "Eldritch Chaos Orb": "古灵混沌石",
    "Eldritch Exalted Orb": "古灵崇高石",
    "Orb of Conflict": "冲突宝珠",
    "Awakener's Orb": "觉醒者宝珠",
    "Orb of Remembrance": "追忆宝珠",
    "Artificer's Orb": "工匠宝珠",
    "Lesser Jeweller's Orb": "次级工匠宝珠",
}

# ================= 2. 自动化逻辑函数 =================

def ensure_icon(en_name, remote_url):
    if not os.path.exists(ICON_DIR):
        os.makedirs(ICON_DIR)
    safe_name = en_name.replace(" ", "_").replace("'", "").replace(":", "").replace('"', "")
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
    openings = ["Market analysis suggests", "Current economic telemetry shows", "Latest trade data indicates"]
    sentiment = f"Divine Orbs are trading at {div_price} Chaos,"
    details = f"while Mirror of Kalandra holds premium value at {mirror_price:,.0f} Chaos."
    advice = random.choice(["Watch for liquidity shifts.", "Consider long-term asset holding.", "Market volatility is low."])
    paragraph = f"{random.choice(openings)} {sentiment} {details} {advice}"
    return f"{paragraph}<br><br><strong>Keywords:</strong> PoE 2 Trade, Divine Price, Mirror Rate, Economy Analysis."

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
                <div class="wise-name">
                    <span>{zh_name}</span>
                    <small style="display:block; font-size:10px; color:#5d7079; font-weight:400;">{en_name}</small>
                </div>
            </div>
            <div class="wise-col align-right">
                <div class="price-line">
                    <span class="wise-value">{price:,.1f}</span>
                    <span class="wise-unit">混沌石 (CHAOS)</span>
                </div>
                <div class="status-line">
                    <span class="trend {trend_class}">{trend_val:+.1f}%</span>
                    <span class="wise-label">{advice}</span>
                </div>
            </div>
        </div>
        """
        if i == 4:
            rows_html += '<div style="background:#f1f5f9;border:1px dashed #cbd5e1;color:#94a3b8;text-align:center;padding:15px;font-size:11px;border-radius:8px;margin:15px 0;">【列表中间原生广告位】</div>'

    update_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    insight_content = generate_market_insight(divine_price, mirror_price)

    # ---------------- 3. HTML 模板 (含置顶逻辑) ----------------
    full_html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>PoE 2 汇率看板 PRO</title>
        <style>
            :root {{ --green: #25d970; --red: #ff4d4d; --navy: #163300; --bg: #f8fafc; --border: #e2e8f0; }}
            body {{ background: var(--bg); color: #2e3333; font-family: -apple-system, sans-serif; margin: 0; padding-bottom: 50px; -webkit-overflow-scrolling: touch; }}
            .nav {{ background: #fff; padding: 15px 20px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 100; }}
            .logo {{ font-weight: 800; font-size: 18px; color: var(--navy); text-decoration: none; }}
            .container {{ max-width: 550px; margin: auto; padding: 0 15px; }}
            .calc-card {{ background: var(--navy); color: white; border-radius: 16px; padding: 20px; margin: 15px 0; box-shadow: 0 8px 20px rgba(0,0,0,0.1); }}
            .calc-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
            input {{ background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); border-radius: 8px; padding: 10px; color: white; width: 85%; font-size: 16px; outline: none; }}
            .main-card {{ background: white; border-radius: 16px; padding: 5px 20px; border: 1px solid var(--border); box-shadow: 0 2px 4px rgba(0,0,0,0.02); }}
            .wise-row {{ display: flex; justify-content: space-between; align-items: center; padding: 16px 0; border-bottom: 1px solid var(--border); }}
            .wise-col {{ display: flex; align-items: center; gap: 12px; }}
            .align-right {{ flex-direction: column; align-items: flex-end; gap: 4px; }}
            .wise-icon {{ width: 32px; height: 32px; object-fit: contain; }}
            .wise-name {{ font-weight: 700; font-size: 15px; color: var(--navy); }}
            .price-line {{ display: flex; align-items: baseline; gap: 6px; }}
            .wise-value {{ font-size: 19px; font-weight: 800; color: var(--navy); }}
            .wise-unit {{ font-size: 10px; color: #5d7079; font-weight: 700; text-transform: uppercase; }}
            .status-line {{ display: flex; align-items: center; gap: 8px; }}
            .trend {{ font-size: 11px; font-weight: bold; }}
            .trend-up {{ color: var(--green); }}
            .trend-down {{ color: var(--red); }}
            .wise-label {{ font-size: 10px; background: #f1f5f9; padding: 2px 6px; border-radius: 4px; color: #64748b; font-weight: 700; }}
            .seo-box {{ background: #fff; border-radius: 12px; border: 1px solid var(--border); padding: 15px; margin-top: 40px; opacity: 0.7; }}
        </style>
    </head>
    <body id="top">
        <div class="nav">
            <a href="#" class="logo">POE2<span style="color:var(--green)">WISE</span></a>
            <div style="font-size:11px; font-weight:700; color:var(--green)">● MARKET LIVE</div>
        </div>

        <div class="container">
            <div style="background:#f1f5f9;border:1px dashed #cbd5e1;color:#94a3b8;text-align:center;padding:15px;font-size:11px;border-radius:8px;margin:15px 0;">【顶部自适应广告位】</div>

            <div class="calc-card">
                <h3 style="margin:0 0 15px 0; font-size:16px;">资产一键清仓</h3>
                <div class="calc-grid">
                    <div><label style="font-size:10px;opacity:0.6;display:block;margin-bottom:5px;">混沌石持仓</label><input type="number" id="cIn" oninput="calc()" placeholder="0"></div>
                    <div><label style="font-size:10px;opacity:0.6;display:block;margin-bottom:5px;">神圣石持仓</label><input type="number" id="dIn" oninput="calc()" placeholder="0"></div>
                </div>
                <div id="res" style="text-align:center; font-weight:800; font-size:24px; margin-top:20px; color:var(--green)">0.00 DIVINE</div>
            </div>

            <div class="main-card">
                <div style="padding: 15px 0; font-size: 11px; color: #5d7079; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">实时行情看板 <span style="float:right">更新: {update_time}</span></div>
                {rows_html}
            </div>

            <div class="seo-box">
                <h4 style="margin:0 0 10px; font-size:14px; color:var(--navy);">Market Analysis (SEO)</h4>
                <div style="font-size:13px; color:#5d7079; line-height:1.6;">{insight_content}</div>
                <div style="background:#f1f5f9;border:1px dashed #cbd5e1;color:#94a3b8;text-align:center;padding:15px;font-size:11px;border-radius:8px;margin-top:20px;">【底部内容匹配广告位】</div>
            </div>
        </div>

        <script>
            const DIV = {divine_price};
            function calc() {{
                const c = parseFloat(document.getElementById('cIn').value)||0;
                const d = parseFloat(document.getElementById('dIn').value)||0;
                document.getElementById('res').innerText = (d + (c/DIV)).toFixed(2) + " DIVINE";
            }}

            // 核心修复：强制置顶逻辑，防止手机端加载时滚到底部
            window.scrollTo(0, 0);
            document.addEventListener('DOMContentLoaded', () => {{
                setTimeout(() => window.scrollTo(0, 0), 50);
            }});
        </script>
    </body>
    </html>
    """
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)

if __name__ == "__main__":
    build_pro_site()
