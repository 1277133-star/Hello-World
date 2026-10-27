import html
import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hello World Motion Lab", page_icon="✨", layout="wide")

st.title("✨ Hello World Motion Lab")
st.caption("Type a name, choose its style, and add a looping motion effect.")

with st.sidebar:
    st.header("Customize your app")
    name = st.text_input("Enter your name", value="Hello World", max_chars=80)
    font_family = st.selectbox(
        "Font type",
        ["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana",
         "Trebuchet MS", "Impact", "Comic Sans MS", "monospace", "sans-serif"],
    )
    font_size = st.slider("Font size", min_value=20, max_value=100, value=48, step=2)
    background = st.selectbox(
        "Background",
        ["Light", "Dark", "Ocean", "Sunset", "Forest", "Lavender", "Midnight"],
    )
    name_mode = st.selectbox("Name display mode", ["Centered", "Ticker Tape", "Repeated"])
    effect = st.selectbox(
        "Dynamic action",
        ["None", "Rain", "Snow", "Hail", "Wind gust", "Confetti", "Tornado"],
    )
    speed = st.slider(
        "Animation speed", min_value=1, max_value=10, value=5,
        help="Higher values make the animation move faster.",
    )

backgrounds = {
    "Light": ("#f8fafc", "#172033"),
    "Dark": ("#10131a", "#f8fafc"),
    "Ocean": ("linear-gradient(135deg, #0f766e, #0c4a6e)", "#ffffff"),
    "Sunset": ("linear-gradient(135deg, #ffedd5, #fda4af, #c4b5fd)", "#40213a"),
    "Forest": ("linear-gradient(135deg, #14532d, #365314)", "#f0fdf4"),
    "Lavender": ("linear-gradient(135deg, #ede9fe, #f5d0fe)", "#3b245f"),
    "Midnight": ("radial-gradient(circle at top, #263b73, #080b18 75%)", "#ffffff"),
}
bg_css, text_color = backgrounds[background]
safe_name = html.escape(name or "Hello World")
# Prevent user-controlled font strings from being interpreted as arbitrary CSS.
font_css = font_family.replace("\\", "").replace(";", "").replace("{", "").replace("}", "")
animation_duration = round(11 - speed, 2)

# Build a decorative particle layer. CSS animates it continuously without rerunning
# the whole Streamlit script, keeping the motion smooth and resource-friendly.
particles = []
particle_count = 44 if effect != "None" else 0
symbols = {
    "Rain": ["💧", "│"],
    "Snow": ["❄", "❅", "✳"],
    "Hail": ["●", "🧊"],
    "Wind gust": ["〰", "➝", "﹏"],
    "Confetti": ["🎉", "◆", "●", "■", "✦"],
    "Tornado": ["〰", "🌀", "·"],
}
for i in range(particle_count):
    symbol = random.choice(symbols.get(effect, [""]))
    left = random.randint(0, 98)
    delay = random.uniform(-animation_duration, 0)
    duration = random.uniform(animation_duration * 0.65, animation_duration * 1.5)
    size = random.randint(12, 25)
    drift = random.randint(-100, 100)
    particles.append(
        f'<span class="particle p-{effect.replace(" ", "-").lower()}" '
        f'style="left:{left}%; animation-delay:{delay:.2f}s; '
        f'animation-duration:{duration:.2f}s; font-size:{size}px; '
        f'--drift:{drift}px;">{html.escape(symbol)}</span>'
    )
particle_html = "".join(particles)

if name_mode == "Ticker Tape":
    name_html = f'<div class="ticker"><span>{safe_name}</span><span aria-hidden="true">{safe_name}</span></div>'
elif name_mode == "Repeated":
    name_html = '<div class="repeated">' + "".join(
        f'<div>{safe_name}</div>' for _ in range(6)
    ) + "</div>"
else:
    name_html = f'<div class="center-name">{safe_name}</div>'

effect_class = "effect-" + effect.replace(" ", "-").lower()
html_doc = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; }}
.stage {{
    position: relative; isolation: isolate; overflow: hidden;
    height: 68vh; min-height: 360px; width: 100%;
    border-radius: 18px; background: {bg_css}; color: {text_color};
    font-family: "{font_css}", sans-serif;
}}
.particles {{ position: absolute; inset: 0; overflow: hidden; pointer-events: none; z-index: 1; }}
.particle {{ position: absolute; top: -50px; opacity: .82; user-select: none;
    animation-name: fall; animation-timing-function: linear; animation-iteration-count: infinite; }}
@keyframes fall {{
    0% {{ transform: translate3d(0, -50px, 0) rotate(0deg); opacity: 0; }}
    10% {{ opacity: .9; }}
    100% {{ transform: translate3d(var(--drift), 80vh, 0) rotate(360deg); opacity: .15; }}
}}
.effect-rain .particle {{ color: #38bdf8; }}
.effect-rain .particle {{ transform: scaleX(.7); }}
.effect-hail .particle {{ color: #bae6fd; text-shadow: 0 1px 3px #64748b; }}
.effect-wind-gust .particle {{ animation-name: gust; top: auto; }}
@keyframes gust {{
    0% {{ transform: translateX(-15vw) rotate(0deg); opacity: 0; }}
    15% {{ opacity: .8; }}
    100% {{ transform: translateX(115vw) rotate(180deg); opacity: 0; }}
}}
.effect-confetti .particle {{ animation-name: confetti; }}
@keyframes confetti {{
    0% {{ transform: translate3d(0,-40px,0) rotate(0deg); opacity: 0; }}
    10% {{ opacity: 1; }}
    100% {{ transform: translate3d(var(--drift),75vh,0) rotate(900deg); opacity: .2; }}
}}
.effect-tornado .particle {{ animation-name: tornado; left: 50%; }}
@keyframes tornado {{
    0% {{ transform: translate3d(-50px,-30px,0) rotate(0deg) scale(.5); opacity: 0; }}
    15% {{ opacity: .8; }}
    100% {{ transform: translate3d(160px,75vh,0) rotate(1080deg) scale(1.5); opacity: 0; }}
}}
.name-layer {{ position: absolute; inset: 0; z-index: 2; display: flex;
    align-items: center; justify-content: center; padding: 24px; overflow: hidden; }}
.name-text {{ font-size: {font_size}px; font-weight: 700; line-height: 1.2;
    overflow-wrap: anywhere; text-align: center; text-shadow: 0 2px 14px rgba(0,0,0,.12); }}
.ticker {{ display: flex; align-items: center; width: max-content; gap: 8vw;
    white-space: nowrap; animation: marquee {max(8, animation_duration * 1.5):.2f}s linear infinite; }}
.ticker span {{ font-size: {font_size}px; font-weight: 700; }}
@keyframes marquee {{ from {{ transform: translateX(100vw); }} to {{ transform: translateX(-100%); }} }}
.repeated {{ display: flex; flex-direction: column; gap: 8px; width: 100%;
    text-align: center; font-size: {font_size}px; font-weight: 700; line-height: 1.12; }}
.repeated div:nth-child(even) {{ opacity: .7; transform: translateX(12px); }}
@media (prefers-reduced-motion: reduce) {{
    .particle, .ticker {{ animation-duration: 30s !important; }}
}}
</style>
</head>
<body>
<div class="stage {effect_class}">
  <div class="particles" aria-hidden="true">{particle_html}</div>
  <div class="name-layer">
    <div class="name-text">{name_html}</div>
  </div>
</div>
</body>
</html>
"""

components.html(html_doc, height=500, scrolling=False)
st.info("Tip: change the font, background, or action in the sidebar. The selected effect loops continuously inside the preview.")
