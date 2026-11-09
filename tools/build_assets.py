#!/usr/bin/env python3
"""Genera TODAS las imágenes SVG del perfil (claras y oscuras) y el README.md.

    python tools/build_assets.py

Escribe:
  assets/*.svg, assets/projects/*.svg        -> variante clara (marfil)
  assets/dark/*.svg, assets/dark/projects/*  -> variante oscura (tinta cálida)
  README.md                                  -> enlaza cada imagen con <picture>

Estilo: sobrio, tipo blog de Anthropic. Fondo marfil #faf9f5, tinta #141413, líneas finas de 1 px en gris cálido
#a3a095, un único acento naranja #d97757, títulos en serif, interfaz en sans, esquinas rectas, sin sombras ni
degradados. GitHub no carga fuentes externas dentro de un <img>, así que se usan pilas del sistema.

Escala tipográfica única (px del viewBox): 64 hero · 32 títulos y cifras · 20 destacados · 16 cuerpo · 14 interfaz.

Distribución: todos los paneles miden 1000 de ancho (margen 48) y se muestran al 100 %, de modo que forman una sola
columna continua. Las filas de proyecto y la tira de enlaces se reparten el 100 % sin huecos (anchos que suman 99.99 %).

Movimiento (solo CSS dentro del SVG, funciona en un <img> de GitHub): entradas escalonadas al cargar y, para que se note
también más abajo en la página, pequeños movimientos continuos (destello naranja sobre las líneas, puntos que pulsan,
guiones que avanzan). Todo se apaga con prefers-reduced-motion y, si el navegador no anima, el contenido queda visible.

Para cambiar contenido o enlaces edita los datos de este archivo y vuelve a ejecutarlo: no edites los SVG a mano.
Solo usa la biblioteca estándar.
"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

# ───────────────────────────── paleta ─────────────────────────────
THEMES = {
    "light": dict(bg="#faf9f5", ink="#141413", text="#2b2a27", muted="#5e5d59", soft="#87867f",
                  rule="#a3a095", track="#e6e3d8", accent="#d97757", accent_t="#b9532f"),
    "dark": dict(bg="#141413", ink="#faf9f5", text="#e8e6dc", muted="#b0aea5", soft="#87867f",
                 rule="#5e5d59", track="#2b2a27", accent="#d97757", accent_t="#e8896a"),
}

SERIF = "Georgia,'Times New Roman',serif"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"

MX = 48           # margen lateral
RX = 952          # borde derecho del contenido (1000 - 48)

# Anchos (en %) que suman 99.99: la fila de proyecto y sus dos celdas, y las cuatro celdas de enlaces.
W_ROW, W_CELL, W_LINK = "73.79%", "13.1%", "24.99%"
VB_ROW, VB_CELL, VB_LINK = 738, 131, 250   # viewBox con la misma proporción (1000 en total)


def css(c):
    """Estilos del SVG. Las animaciones usan fill-mode 'backwards': si no se reproducen, el contenido sigue visible."""
    return (
        f".serif{{font-family:{SERIF}}}.sans{{font-family:{SANS}}}"
        ".t64{font-size:64px;letter-spacing:-1px}.t32{font-size:32px;letter-spacing:-.3px}"
        ".t20{font-size:20px}.t16{font-size:16px}.t14{font-size:14px}.b{font-weight:600}.i{font-style:italic}"
        f".ink{{fill:{c['ink']}}}.tx{{fill:{c['text']}}}.mu{{fill:{c['muted']}}}.so{{fill:{c['soft']}}}"
        f".ac{{fill:{c['accent']}}}.at{{fill:{c['accent_t']}}}"
        f".ul{{text-decoration:underline;text-underline-offset:3px;text-decoration-color:{c['rule']}}}"
        # entradas
        ".rise{animation:rise .9s cubic-bezier(.2,.7,.2,1) backwards}"
        ".pop{animation:pop .7s cubic-bezier(.2,.7,.2,1) backwards}"
        ".fade{animation:fade .9s ease backwards}"
        ".draw{stroke-dasharray:1;animation:draw 1.3s cubic-bezier(.6,0,.2,1) backwards}"
        ".grow{transform-box:fill-box;transform-origin:left center;animation:grow 1.1s cubic-bezier(.2,.7,.2,1) backwards}"
        "@keyframes rise{from{opacity:0;transform:translateY(10px)}}"
        "@keyframes pop{from{opacity:0;transform:translateY(12px)}}"
        "@keyframes fade{from{opacity:0}}"
        "@keyframes draw{from{stroke-dashoffset:1}}"
        "@keyframes grow{from{transform:scaleX(0)}}"
        # movimiento continuo
        ".pulse{animation:pulse 2.8s ease-in-out infinite}"
        ".ping{transform-box:fill-box;transform-origin:center;animation:ping 2.8s ease-out infinite}"
        ".glint{stroke-dasharray:60 1000;animation:glint 8s ease-in-out infinite}"
        ".march{stroke-dasharray:3 7;animation:march 1.8s linear infinite}"
        ".travel{animation:travel 7s linear infinite}"
        ".nudge{animation:nudge 3.2s ease-in-out infinite}"
        ".scan{animation:scan 9s steps(1,end) infinite}"
        ".slide{animation:slide 9s linear infinite}"
        ".trace{animation:trace 10s linear infinite}"
        "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}"
        "@keyframes ping{0%{transform:scale(.5);opacity:.8}80%,100%{transform:scale(2.8);opacity:0}}"
        "@keyframes glint{0%{stroke-dashoffset:60}65%,100%{stroke-dashoffset:-1000}}"
        "@keyframes march{to{stroke-dashoffset:-10}}"
        "@keyframes travel{0%{transform:translateY(0);opacity:0}8%{opacity:1}92%{opacity:1}100%{transform:translateY(var(--d));opacity:0}}"
        "@keyframes nudge{0%,55%,100%{transform:translate(0,0)}70%{transform:translate(2px,-2px)}85%{transform:translate(0,0)}}"
        "@keyframes scan{0%{opacity:1}11.1%,100%{opacity:0}}"
        "@keyframes slide{0%{transform:translateX(0);opacity:0}6%{opacity:1}72%{opacity:1}80%,100%{transform:translateX(var(--d));opacity:0}}"
        "@keyframes trace{0%{offset-distance:0%;opacity:0}5%{opacity:1}68%{offset-distance:100%;opacity:1}75%,100%{offset-distance:100%;opacity:0}}"
        "@media (prefers-reduced-motion:reduce){"
        ".rise,.pop,.fade,.draw,.grow,.pulse,.ping,.glint,.march,.travel,.nudge,.scan,.slide,.trace{animation:none}"
        ".glint,.ping,.travel,.scan,.slide,.trace{opacity:0}}"
    )


def svg(w, h, body, label, c, size=False):
    dims = f' width="{w}" height="{h}"' if size else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"{dims} role="img" '
        f'aria-label="{escape(label, quote=True)}">'
        f"<style>{css(c)}</style>"
        f'<rect width="{w}" height="{h}" fill="{c["bg"]}"/>'
        f"{body}</svg>\n"
    )


def st(delay=0.0, extra=""):
    """Atributo style con retardo de animación (y variables extra)."""
    parts = []
    if delay:
        parts.append(f"animation-delay:{delay}s")
    if extra:
        parts.append(extra)
    return f' style="{";".join(parts)}"' if parts else ""


def T(x, y, text, cls, anchor=None, anim=None, delay=0.0):
    a = f' text-anchor="{anchor}"' if anchor else ""
    k = f"{cls} {anim}" if anim else cls
    return f'<text x="{x}" y="{y}" class="{k}"{a}{st(delay if anim else 0)}>{escape(text, quote=False)}</text>'


def G(inner, anim, delay=0.0):
    return f'<g class="{anim}"{st(delay)}>{inner}</g>'


def hline(c, x1, x2, y, op=0.7, draw=None):
    cls = ' class="draw" pathLength="1"' if draw is not None else ""
    return (f'<line{cls} x1="{x1}" y1="{y + .5}" x2="{x2}" y2="{y + .5}" stroke="{c["rule"]}" stroke-width="1" '
            f'stroke-opacity="{op}"{st(draw or 0)}/>')


def vline(c, x, y1, y2, op=0.7, draw=None):
    cls = ' class="draw" pathLength="1"' if draw is not None else ""
    return (f'<line{cls} x1="{x + .5}" y1="{y1}" x2="{x + .5}" y2="{y2}" stroke="{c["rule"]}" stroke-width="1" '
            f'stroke-opacity="{op}"{st(draw or 0)}/>')


def glint(c, x1, x2, y, delay=0.0, horizontal=True):
    """Destello naranja que recorre una línea fina."""
    if horizontal:
        return (f'<line class="glint" pathLength="1000" x1="{x1}" y1="{y + .5}" x2="{x2}" y2="{y + .5}" '
                f'stroke="{c["accent"]}" stroke-width="1"{st(delay)}/>')
    return (f'<line class="glint" pathLength="1000" x1="{y + .5}" y1="{x1}" x2="{y + .5}" y2="{x2}" '
            f'stroke="{c["accent"]}" stroke-width="1"{st(delay)}/>')


def box(c, x, y, w, h, op=0.8, fill="none"):
    return (f'<rect x="{x + .5}" y="{y + .5}" width="{w - 1}" height="{h - 1}" fill="{fill}" '
            f'stroke="{c["rule"]}" stroke-width="1" stroke-opacity="{op}"/>')


def square(c, x, y, s=8, pulse=True, delay=0.0):
    k = ' class="pulse"' if pulse else ""
    return f'<rect{k} x="{x}" y="{y}" width="{s}" height="{s}" fill="{c["accent"]}"{st(delay if pulse else 0)}/>'


def dot(c, cx, cy, r=4, delay=0.0, ring=True):
    s = (f'<circle class="ping" cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c["accent"]}"{st(delay)}/>' if ring else "")
    return s + f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c["accent"]}"/>'


# ───────────────────────────── datos ─────────────────────────────
GH = "https://github.com/GustavoAdolfoNavarroPacheco"
PRIVATE = "private"

PROJECTS = [
    dict(name="CRM Campuslands",
         desc=["Internal CRM for Campuslands S.A.S.: companies, clients, projects, billing, receivables,",
               "plus forecasting, per-area modules (IA Academy, Tech Leap, Hubux) and a virtual assistant."],
         tech=["TypeScript", "React", "Vite", "Tailwind", "shadcn/ui", "Firebase", "Firestore"],
         live="https://fullservices-crm.web.app/", repo=PRIVATE),
    dict(name="Waylo.ai",
         desc=["Conversational patient navigator: spots red-flag symptoms, asks plain-language questions",
               "and routes to Emergency, Priority or General care. Orients, never diagnoses."],
         tech=["TypeScript", "Next.js", "Vercel AI SDK", "PostgreSQL (Neon)", "Tailwind", "Vitest"],
         live="https://waylo-ai.vercel.app/", repo=f"{GH}/waylo.ai"),
    dict(name="Conect.ia",
         desc=["AI social media suite: generates copy, images and vertical video with Gemini, then schedules",
               "and auto-publishes to LinkedIn, Facebook, Instagram and TikTok (Make / n8n ready)."],
         tech=["TypeScript", "React", "Vite", "Auth.js", "PostgreSQL (Neon)", "Gemini", "Vercel"],
         live="https://conectia-campuslands.vercel.app/", repo=f"{GH}/conect.ia"),
    dict(name="FullService Agents",
         desc=["Monorepo of 6 AI agents for the Campuslands sales cycle: prospecting, LinkedIn outreach,",
               "branded decks, scope quotes, tender analysis and contract drafting, end to end."],
         tech=["AI agents", "Claude Code", "Perplexity", "Python", "MD", "HTML", "CSS"],
         live=None, repo=f"{GH}/fullservice-agents"),
    dict(name="Casablanca Hub",
         desc=["Talent hub for Carnes Casablanca: vacancies, job profiles and a candidate pipeline, with",
               "an AI agent that pre-screens and scores applicants on WhatsApp, plus live human takeover."],
         tech=["TypeScript", "Next.js", "React", "Prisma", "PostgreSQL", "DeepSeek", "WhatsApp API"],
         live="https://carnescasablanca.vercel.app/", repo=PRIVATE),
    dict(name="Portfolio",
         desc=["Personal portfolio in vanilla HTML, CSS and JS: scroll-driven cinematic hero, ES/EN/PT i18n,",
               "light/dark themes, interactive terminal, optimized assets and keyboard accessibility."],
         tech=["JS", "HTML", "CSS", "Vercel"],
         live="https://gustavoadolfonavarropacheco.vercel.app/", repo=PRIVATE),
    dict(name="LMS Portal",
         desc=["Web learning platform for students, teachers and admins: course catalog, user profiles,",
               "progress tracking and assignments, consuming a REST API with LocalStorage for session data."],
         tech=["JS", "HTML", "CSS"],
         live="https://gustavoadolfonavarropacheco.github.io/LMS_Portal/", repo=f"{GH}/LMS_Portal"),
    dict(name="TecnoStore",
         desc=["Java console app for a phone store (MVC, JDBC, MySQL): brands, phones, customers and sales,",
               "plus analytics like low-stock alerts, top-3 sellers and monthly revenue."],
         tech=["Java", "MySQL", "XML"],
         live=None, repo=f"{GH}/TecnoStore"),
    dict(name="LogiTrack",
         desc=["Warehouse management REST API on Spring Boot 3 / Java 21: products, multiple warehouses and",
               "inventory movements with real-time stock, audit log, JWT security and Swagger docs."],
         tech=["Java", "CSS", "JS", "HTML", "SpringBoot", "Lombok", "JWT", "Swagger"],
         live="https://gustavoadolfonavarropacheco.github.io/Logitrack/frontend/", repo=f"{GH}/LogiTrack"),
    dict(name="KarioMedia",
         desc=["Static, responsive KPI dashboard for Kario Media: login, user profile and screens to view,",
               "add, delete and report indicators. Designed in Figma, built with HTML and CSS."],
         tech=["HTML", "CSS"],
         live="https://gustavoadolfonavarropacheco.github.io/KarioMedia/", repo=f"{GH}/KarioMedia"),
    dict(name="Sora",
         desc=["AI-driven recruitment platform as a single zero-dependency web app: KPI dashboard, Kanban",
               "vacancies, calendar and a WhatsApp chat copilot where recruiters can take over from the AI."],
         tech=["JS", "HTML", "CSS"],
         live="https://gustavoadolfonavarropacheco.github.io/Sora/", repo=f"{GH}/Sora"),
    dict(name="Topping",
         desc=["Relational database for a pizzeria in MySQL: customers, pizzas, ingredients, orders and",
               "delivery drivers, automated with triggers and functions for totals, stock and price audits."],
         tech=["MySQL"],
         live=None, repo=f"{GH}/Topping"),
    dict(name="Spendify",
         desc=["Python expense tracker: create, record and manage daily expenses from the terminal,",
               "with clean table reports rendered through tabulate."],
         tech=["Python"],
         live=None, repo=f"{GH}/Spendify"),
    dict(name="ViraAI",
         desc=["Multi-agent marketing system for Campuslands AI Academy: plans editorial calendars,",
               "writes posts, edits video, creates visual assets and validates brand rules, with memory."],
         tech=["Python", "MD"],
         live=None, repo=f"{GH}/ViraAI-Agents"),
]

ECOSYSTEM = [
    ("Sistemas de negocio", [
        ("CRM Campuslands", "Internal Company CRM"),
        ("Casablanca Hub", "Recruitment · AI + WhatsApp"),
        ("TecnoStore", "Enterprise Management"),
        ("Logitrack", "Warehouse Management"),
        ("Topping", "Pizzeria Management")]),
    ("IA y automatización", [
        ("Waylo.ai", "Patient Triage Navigator"),
        ("Conect.ia", "Social Media Automation"),
        ("FullService Agents", "Sales Agents Pipeline"),
        ("ViraAI", "Marketing Multi-Agent"),
        ("Sora", "Smart Recruitment")]),
    ("Web y datos", [
        ("LMS Portal", "LMS Web Platform"),
        ("KarioMedia", "Metrics Dashboard"),
        ("Portfolio", "Personal Site"),
        ("Spendify", "Expense Simulator")]),
]

STACK = [
    ("Lenguajes", "TypeScript · Java · JavaScript · Python · HTML · CSS"),
    ("Backend", "SpringBoot · Node.js · Express · Serverless · Cloud Functions"),
    ("Frontend", "React · Next.js · Vite · Tailwind · shadcn/ui"),
    ("Bases de datos", "MySQL · PostgreSQL (Neon) · Firestore · Prisma"),
    ("IA", "Gemini · DeepSeek · Vercel AI SDK · Claude Code · WhatsApp API"),
    ("Arquitectura", "Monolith · REST APIs · MVC · Microservices"),
    ("Terminal", "TUI / CLI · bash workflows"),
    ("Herramientas", "Git · GitHub Actions · Vitest · Postman · Swagger · Maven · Lombok"),
    ("Despliegue", "Vercel · Firebase Hosting"),
]

TIMELINE = [  # (fecha, hito) — el actual va resaltado
    ("Apr 2025", "Started coding"),
    ("Jul 2025", "Solvo Internship"),
    ("Feb 2026", "LogiTrack"),
    ("Apr 2026", "Finished Campuslands Course"),
    ("May 2026", "Campuslands Internship"),
    ("Jul 2026", "Full Service Team"),
    ("Dec 2026", "Graduation"),
]
CURRENT = 5

EXPERIENCE = [
    ("1yr 4mo", "Campuslands", "Software Developer · Internship"),
    ("1yr 1mo", "Solvo", "Software Developer · Internship"),
]

LANGS_BYTES = [("TypeScript", 60, 270), ("HTML", 16, 72), ("CSS", 11, 50), ("JavaScript", 11, 50),
               ("Python", 2, 9), ("Java", 1, 4)]

GH_STATS = [("Estrellas totales", "30"), ("Commits en 2026", "678"), ("Pull requests totales", "83"),
            ("Issues totales", "0"), ("Repositorios contribuidos", "9")]
GH_LANGS = [("JavaScript", 270), ("CSS", 255), ("TypeScript", 195), ("HTML", 180), ("Python", 60)]  # sobre 270

ACTIVITY_PTS = ("52.0,236.0 69.2,236.0 86.5,234.0 103.7,236.0 120.9,236.0 138.2,234.0 155.4,235.0 172.6,236.0 "
                "189.8,236.0 207.1,236.0 224.3,236.0 241.5,233.0 258.8,236.0 276.0,228.1 293.2,226.1 310.5,218.1 "
                "327.7,229.1 344.9,229.1 362.2,230.0 379.4,228.1 396.6,221.1 413.8,227.1 431.1,229.1 448.3,229.1 "
                "465.5,229.1 482.8,229.1 500.0,229.1 517.2,229.1 534.5,229.1 551.7,229.1 568.9,229.1 586.2,229.1 "
                "603.4,229.1 620.6,222.1 637.8,220.1 655.1,223.1 672.3,216.2 689.5,217.2 706.8,215.2 724.0,208.2 "
                "741.2,218.1 758.5,167.6 775.7,226.1 792.9,224.1 810.2,227.1 827.4,192.4 844.6,222.1 861.8,204.3 "
                "879.1,112.0 896.3,217.2 913.5,179.5 930.8,184.4 948.0,229.1")
ACTIVITY_MONTHS = [(52.0, "Oct"), (155.4, "Dec"), (224.3, "Jan"), (293.2, "Feb"), (362.2, "Mar"), (448.3, "Apr"),
                   (517.2, "May"), (603.4, "Jun"), (672.3, "Jul"), (741.2, "Aug"), (827.4, "Sep"), (896.3, "Oct")]

SECTIONS = [  # (archivo, título)
    ("s01", "Sobre mí"), ("s02", "Ecosistema de proyectos"), ("s03", "Proyectos"),
    ("s04", "Actividad"), ("s05", "Trayectoria"), ("s06", "Stack técnico"),
]

LINKS = [  # (archivo, etiqueta, url, alt)
    ("link-portfolio", "Portafolio", "https://gustavoadolfonavarropacheco.vercel.app/", "Portafolio"),
    ("link-resume", "Currículum", "https://gustavoadolfonavarropacheco.vercel.app/Gustavo_Navarro_CV.pdf", "Currículum (PDF)"),
    ("link-linkedin", "LinkedIn", "https://www.linkedin.com/in/gustavo-adolfo-navarro-pacheco-876b06356/", "LinkedIn"),
    ("link-email", "Correo", "mailto:adolfonavarro0212@gmail.com", "Correo electrónico"),
]


# ───────────────────────────── imágenes ─────────────────────────────
def header(c):
    b = [G(square(c, MX, 56, 10, pulse=False), "fade", .1), T(MX + 22, 66, "Portafolio", "sans t14 mu", anim="fade", delay=.1),
         T(RX, 66, "Campuslands S.A.S", "sans t14 mu", "end", anim="fade", delay=.2),
         T(MX - 3, 172, "Gustavo Navarro", "serif t64 ink", anim="rise", delay=.25),
         T(MX, 216, "Full-Stack Developer · Functional QA · Automation & AI — Girón, Colombia.", "serif t20 mu", anim="rise", delay=.5),
         hline(c, MX, RX, 256, draw=.7), glint(c, MX, RX, 256, 1.5)]
    return svg(1000, 284, "".join(b), "Gustavo Navarro — Full-Stack Developer, Functional QA, Automation & AI en Girón, Colombia", c)


def link_button(label, idx):
    def f(c):
        b = [hline(c, 0, VB_LINK, 0, 0.9), hline(c, 0, VB_LINK, 55, 0.9), vline(c, VB_LINK - 1, 0, 56, 0.9),
             glint(c, 0, VB_LINK, 55, 1.0 + idx * 1.6)]
        if idx == 0:
            b.append(vline(c, 0, 0, 56, 0.9))
        b.append(f'<text x="{VB_LINK / 2}" y="33" class="sans t14 b ink" text-anchor="middle">{escape(label)} '
                 f'<tspan class="at">↗</tspan></text>')
        return svg(VB_LINK, 56, "".join(b), label, c)
    return f


def section(title, idx):
    def f(c):
        b = [T(MX, 52, title, "serif t32 ink", anim="rise"), hline(c, MX, RX, 68, draw=.2),
             glint(c, MX, RX, 68, 1.0 + idx * 1.3)]
        return svg(1000, 84, "".join(b), title, c)
    return f


def whoami(c):
    d = 600   # columna derecha
    b = [T(MX, 52, "Graduated from Campuslands S.A.S", "serif t20 mu", anim="rise", delay=.05),
         T(MX - 1, 100, "Full-Stack Developer", "serif t32 ink", anim="rise", delay=.15),
         T(MX, 134, "Java · TypeScript · React · Next.js · Node.js", "sans t16 tx", anim="rise", delay=.25),
         T(MX, 184, "Drawn to projects where design meets data.", "serif t20 mu", anim="rise", delay=.35),
         T(MX, 212, "Clean architecture and user experience in equal measure.", "serif t20 mu", anim="rise", delay=.45),
         vline(c, d - 24, 32, 232, 0.6, draw=.3),
         T(d, 52, "Enfoque", "sans t14 mu", anim="rise", delay=.3),
         T(d, 82, "Mobile · Full-Stack Systems", "sans t16 ink", anim="rise", delay=.35),
         T(d, 106, "Terminal UI / CLI", "sans t16 ink", anim="rise", delay=.4),
         T(d, 130, "Functional QA · Automation & AI", "sans t16 ink", anim="rise", delay=.45),
         T(d, 172, "Estado", "sans t14 mu", anim="rise", delay=.5),
         G(square(c, d, 190, 8), "rise", .55),
         T(d + 18, 199, "Open to internships ·", "sans t16 ink", anim="rise", delay=.55),
         T(d + 18, 223, "freelance · collaboration", "sans t16 ink", anim="rise", delay=.6)]
    return svg(1000, 260, "".join(b), "Sobre Gustavo: Full-Stack Developer graduado de Campuslands, abierto a pasantías, freelance y colaboración", c)


def ecosystem(c):
    cw, ch, pitch = 264, 62, 76
    xs = [48, 368, 688]
    centers = [int(x + cw / 2) for x in xs]
    top, nmax = 184, 5
    bottom = top + (nmax - 1) * pitch + ch          # 550
    b = [G(box(c, 400, 24, 200, 56, 0.9, c["bg"]) + T(500, 50, "Gustavo Navarro", "serif t20 ink", "middle")
           + T(500, 69, "One-person build pipeline", "sans t14 mu", "middle"), "pop", .05),
         vline(c, 500, 80, 104, draw=.3), hline(c, centers[0], centers[2], 104, draw=.4)]
    # columnas: guiones que avanzan y un punto que viaja, por detrás de las tarjetas
    for k, cx in enumerate(centers):
        b.append(vline(c, cx, 104, 132, draw=.5))
        b.append(f'<line class="march" x1="{cx + .5}" y1="132" x2="{cx + .5}" y2="{bottom}" stroke="{c["rule"]}" stroke-opacity=".7"/>')
        b.append(f'<circle class="travel" cx="{cx + .5}" cy="132" r="3" fill="{c["accent"]}" style="--d:{bottom - 132}px;animation-delay:{k * 2.3}s"/>')
    n = 0
    for k, (x, cx, (head, nodes)) in enumerate(zip(xs, centers, ECOSYSTEM)):
        b.append(T(cx, 156, head, "sans t14 b ink", "middle", anim="fade", delay=.5 + k * .1))
        off = (nmax - len(nodes)) * pitch // 2          # centra verticalmente las columnas con menos tarjetas
        for i, (name, sub) in enumerate(nodes):
            y = top + off + i * pitch
            n += 1
            b.append(G(box(c, x, y, cw, ch, 0.8, c["bg"]) + T(x + 20, y + 27, name, "sans t16 b ink")
                       + T(x + 20, y + 48, sub, "sans t14 mu"), "pop", .6 + n * .06))
    b += [hline(c, MX, RX, 576, draw=1.0), T(MX, 602, "Everything from one pipeline.", "serif t14 i mu", anim="fade", delay=1.2)]
    return svg(1000, 624, "".join(b), "Mapa del ecosistema: sistemas de negocio, IA y automatización, y web y datos, todo desde un mismo flujo de trabajo", c)


def project_row(p, idx):
    def f(c):
        d = idx * .07
        b = [T(MX, 34, p["name"], "serif t20 ink", anim="rise", delay=d),
             T(MX, 60, p["desc"][0], "sans t14 tx", anim="rise", delay=d + .08),
             T(MX, 80, p["desc"][1], "sans t14 tx", anim="rise", delay=d + .12),
             T(MX, 104, " · ".join(p["tech"]), "sans t14 mu", anim="rise", delay=d + .16),
             hline(c, MX, VB_ROW, 118, 0.55, draw=d + .2), glint(c, MX, VB_ROW, 118, idx * .5 + .5)]
        return svg(VB_ROW, 124, "".join(b), p["name"], c)
    return f


def cell(kind):
    """Celdas de enlace: mismo ancho de texto (x=34) y misma columna de icono (x=20) en las cuatro variantes."""
    label = {"live": "Sitio en vivo", "live-none": "Sin sitio", "repo": "Repositorio", "repo-private": "Repositorio privado"}[kind]
    txt = {"live": "Sitio ↗", "live-none": "Sin sitio", "repo": "Código ↗", "repo-private": "Privado"}[kind]

    def f(c):
        active = kind in ("live", "repo")
        if kind == "live":
            icon = dot(c, 20, 29, 3.5)
        elif kind == "repo":
            icon = f'<circle cx="20" cy="29" r="3.5" fill="{c["ink"]}"/>'
        else:
            icon = f'<circle cx="20" cy="29" r="3" fill="none" stroke="{c["soft"]}" stroke-width="1"/>'
        x2 = VB_CELL - 48 if kind.startswith("repo") else VB_CELL
        b = [icon, T(34, 34, txt, "sans t14 b ink ul" if active else "sans t14 so"), hline(c, 0, x2, 118, 0.55)]
        return svg(VB_CELL, 124, "".join(b), label, c)
    return f


def telemetry(c):
    b = [vline(c, 360, 20, 300, 0.45, draw=.2), vline(c, 676, 20, 300, 0.45, draw=.3)]
    b.append(T(MX, 38, "Lenguajes · por bytes", "sans t14 mu", anim="fade"))
    for i, (lang, pct, w) in enumerate(LANGS_BYTES):
        y = 78 + i * 40
        fill = c["accent"] if i == 0 else c["soft"]
        b += [T(MX, y, lang, "sans t14 ink", anim="rise", delay=i * .08),
              f'<rect class="grow" x="{MX}" y="{y + 8}" width="{w}" height="8" fill="{fill}"{st(.2 + i * .1)}/>',
              T(MX + w + 10, y + 16, f"{pct}%", "sans t14 mu", anim="fade", delay=.5 + i * .1)]
    b.append(T(392, 38, "Ritmo de entrega · 2025 → 2026", "sans t14 mu", anim="fade"))
    b += [hline(c, 392, 656, 212),
          f'<polyline class="draw" pathLength="1" points="392,200 440,192 488,170 536,148 584,108 622,72 656,52" fill="none" '
          f'stroke="{c["ink"]}" stroke-width="1.5" stroke-linejoin="round"{st(.4)}/>']
    for k, (px, py) in enumerate([(440, 192), (488, 170), (536, 148), (584, 108)]):
        b.append(f'<circle class="fade" cx="{px}" cy="{py}" r="2.5" fill="{c["ink"]}"{st(.9 + k * .15)}/>')
    b.append(G(dot(c, 622, 72, 4.5), "fade", 1.5))
    b += [T(392, 236, "Apr '25", "sans t14 mu"), T(500, 236, "Feb '26", "sans t14 mu"), T(612, 236, "Oct '26", "sans t14 mu"),
          T(392, 272, "Tendencia: acelerando", "sans t14 ink", anim="fade", delay=1.2)]
    counters = [("27", "Repositorios", False), ("14", "Proyectos documentados", False),
                ("3", "Web · API · AI agents", False), ("∞", "Pestañas de terminal abiertas", True)]
    b.append(T(708, 38, "Perfil en cifras", "sans t14 mu", anim="fade"))
    for i, (n, label, hl) in enumerate(counters):
        y = 84 + i * 62
        b += [T(708, y, n, "serif t32 " + ("at pulse" if hl else "ink"), anim=None if hl else "rise", delay=.2 + i * .12)
              if not hl else f'<text x="708" y="{y}" class="serif t32 at pulse">{n}</text>',
              T(708, y + 21, label, "sans t14 mu", anim="fade", delay=.3 + i * .12)]
    return svg(1000, 312, "".join(b), "Lenguajes por bytes, ritmo de entrega 2025-2026 y cifras del perfil: 27 repositorios, 14 proyectos y 3 plataformas", c)


def github_stats(c):
    b = [vline(c, 500, 24, 296, 0.45, draw=.2),
         T(MX, 44, "Estadísticas de GitHub", "serif t20 ink", anim="rise"),
         T(532, 44, "Lenguajes por repositorio", "serif t20 ink", anim="rise", delay=.1)]
    for i, (label, val) in enumerate(GH_STATS):
        y = 96 + i * 46
        b += [T(MX, y, label, "sans t14 tx", anim="rise", delay=.1 + i * .08),
              T(452, y + 1, val, "serif t20 ink", "end", anim="rise", delay=.15 + i * .08),
              hline(c, MX, 452, y + 14, 0.45, draw=.2 + i * .08)]
    for i, (lang, w) in enumerate(GH_LANGS):
        y = 96 + i * 46
        fw = round(312 * w / 270, 1)
        b += [T(532, y, lang, "sans t14 tx", anim="rise", delay=.1 + i * .08),
              f'<rect x="640" y="{y - 9}" width="312" height="8" fill="{c["track"]}"/>',
              f'<rect class="grow" x="640" y="{y - 9}" width="{fw}" height="8" fill="{c["ink"]}"{st(.3 + i * .12)}/>',
              f'<rect class="pulse" x="{640 + fw - 3}" y="{y - 9}" width="3" height="8" fill="{c["accent"]}"{st(i * .45)}/>',
              hline(c, 532, RX, y + 14, 0.45, draw=.2 + i * .08)]
    return svg(1000, 312, "".join(b), "Estadísticas de GitHub y lenguajes por repositorio", c)


def activity(c):
    area = f"{ACTIVITY_PTS} 948.0,236.0 52.0,236.0"
    path = "M" + ACTIVITY_PTS.replace(" ", " L")
    b = [T(MX, 44, "Actividad de contribuciones", "serif t20 ink", anim="rise"),
         T(RX, 44, "772 contribuciones · últimos 12 meses", "sans t14 mu", "end", anim="fade", delay=.2)]
    for k, gy in enumerate((194.7, 153.3, 112.0)):
        b.append(f'<line class="fade" x1="{MX}" y1="{gy}" x2="{RX}" y2="{gy}" stroke="{c["rule"]}" stroke-opacity=".45" '
                 f'stroke-dasharray="2 4"{st(.2 + k * .1)}/>')
    b += [f'<polygon class="fade" points="{area}" fill="{c["ink"]}" fill-opacity=".06"{st(1.2)}/>',
          hline(c, MX, RX, 236),
          f'<polyline class="draw" pathLength="1" points="{ACTIVITY_PTS}" fill="none" stroke="{c["ink"]}" stroke-width="1.5" '
          f'stroke-linejoin="round" style="animation-duration:2.4s;animation-delay:.3s"/>',
          G(dot(c, 879.1, 112, 4), "fade", 1.6),
          T(867, 117, "Pico: 125 por semana", "sans t14 at", "end", anim="fade", delay=1.7),
          f'<circle cx="948" cy="229.1" r="3" fill="{c["ink"]}"/>',
          # punto que recorre la curva
          f'<circle class="trace" cx="0" cy="0" r="3.5" fill="{c["accent"]}" style="offset-path:path(\'{path}\');animation-delay:2.5s"/>']
    for x, m in ACTIVITY_MONTHS:
        b.append(T(x, 266, m, "sans t14 mu", "middle" if 52 < x < 940 else ("start" if x < 100 else "end"), anim="fade", delay=.3))
    return svg(1000, 288, "".join(b), "Contribuciones en GitHub: 772 en los últimos 12 meses, actividad semanal", c)


def timeline(c):
    ax, y0 = [90 + i * 140 for i in range(len(TIMELINE))], 130
    b = [hline(c, MX, RX, y0, draw=.2),
         f'<circle class="slide" cx="{MX}" cy="{y0 + .5}" r="3" fill="{c["accent"]}" style="--d:{RX - MX}px;animation-delay:2s"/>']
    for i, (x, (date, label)) in enumerate(zip(ax, TIMELINE)):
        cur = i == CURRENT
        up = i % 2 == 0
        d = .35 + i * .15
        dc = "sans t14 " + ("at" if cur else "mu")
        if up:
            b += [vline(c, x, 98, y0 - 6, 0.9, draw=d), T(x, 62, date, dc, "middle", anim="rise", delay=d),
                  T(x, 86, label, "sans t16 ink", "middle", anim="rise", delay=d + .05)]
        else:
            b += [vline(c, x, y0 + 6, y0 + 34, 0.9, draw=d), T(x, 188, date, dc, "middle", anim="rise", delay=d),
                  T(x, 212, label, "sans t16 ink", "middle", anim="rise", delay=d + .05)]
        if cur:
            b.append(G(dot(c, x, y0 + .5, 6), "pop", d))
        else:
            b.append(f'<circle class="pop" cx="{x}" cy="{y0 + .5}" r="5" fill="{c["bg"]}" stroke="{c["ink"]}" stroke-width="1.5"{st(d)}/>')
    return svg(1000, 240, "".join(b), "Trayectoria: " + "; ".join(f"{d} {t}" for d, t in TIMELINE), c)


def experience(c):
    cols = [MX, 548]
    b = [vline(c, 500, 8, 120, 0.6, draw=.2)]
    for i, (dur, company, role) in enumerate(EXPERIENCE):
        x, d = cols[i], .15 + i * .15
        b += [T(x, 40, dur, "sans t14 mu", anim="rise", delay=d), T(x, 74, company, "serif t32 ink", anim="rise", delay=d + .05),
              T(x, 100, role, "sans t14 tx", anim="rise", delay=d + .1)]
    return svg(1000, 128, "".join(b), "Experiencia: " + "; ".join(f"{co}, {r} ({d})" for d, co, r in EXPERIENCE), c)


def stack(c):
    b = []
    n = len(STACK)
    for i, (label, value) in enumerate(STACK):
        y = 34 + i * 40
        b += [T(MX, y, label, "sans t14 mu", anim="rise", delay=i * .06), T(200, y, value, "sans t16 ink", anim="rise", delay=.05 + i * .06),
              hline(c, MX, RX, y + 18, 0.55, draw=.1 + i * .06),
              # marcador naranja que recorre las filas, una a una
              f'<rect class="scan" x="{MX - 14}" y="{y - 13}" width="2" height="18" fill="{c["accent"]}" '
              f'style="animation-duration:{n * 1.2}s;animation-delay:{i * 1.2}s;opacity:0"/>']
    return svg(1000, 34 + 40 * n - 8, "".join(b), "Stack técnico: lenguajes, backend, frontend, bases de datos, IA, arquitectura, herramientas y despliegue", c)


def footer(c):
    b = [dot(c, MX + 6, 55, 5), T(MX + 26, 62, "Estado · En construcción", "sans t16 ink", anim="fade"),
         T(MX + 26, 90, "probably in a terminal, probably past midnight", "serif t14 i mu", anim="fade", delay=.2),
         T(RX, 90, "Gustavo Navarro  ·  Girón, CO  ·  © 2026", "sans t14 mu", "end", anim="fade", delay=.3)]
    return svg(1000, 116, "".join(b), "Estado: construyendo. Girón, Colombia.", c)


# ───────────────────────────── escritura ─────────────────────────────
def build_all():
    files = {"header-v1": header, "whoami": whoami, "ecosystem": ecosystem, "telemetry": telemetry,
             "github-stats": github_stats, "activity": activity, "timeline": timeline,
             "experience": experience, "stack": stack, "footer": footer}
    for i, (name, title) in enumerate(SECTIONS):
        files[name] = section(title, i)
    for i, (key, label, _, _) in enumerate(LINKS):
        files[key] = link_button(label, i)
    for i, p in enumerate(PROJECTS, 1):
        files[f"projects/{i:02d}"] = project_row(p, i - 1)
    for kind in ("live", "live-none", "repo", "repo-private"):
        files[f"projects/{kind}"] = cell(kind)

    for theme, folder in (("light", ASSETS), ("dark", ASSETS / "dark")):
        c = THEMES[theme]
        for name, fn in files.items():
            path = folder / f"{name}.svg"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(fn(c), encoding="utf-8", newline="\n")
    return len(files)


def pic(name, alt, width=None):
    """<picture> sin hueco vertical: align="top" evita el espacio de línea bajo las imágenes en línea."""
    w = f' width="{width}"' if width else ""
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="assets/dark/{name}.svg"/>'
            f'<img src="assets/{name}.svg"{w} align="top" alt="{escape(alt, quote=True)}"/></picture>')


def build_readme():
    # Todo en un único párrafo (sin líneas en blanco ni <div>), para que GitHub no añada márgenes entre paneles.
    L = [pic("header-v1", "Gustavo Navarro — Full-Stack Developer · Functional QA · Automation & AI"),
         "".join(f'<a href="{url}">{pic(key, alt, W_LINK)}</a>' for key, _, url, alt in LINKS)]
    titles = dict(SECTIONS)
    L += [pic("s01", titles["s01"]), pic("whoami", "Sobre Gustavo"),
          pic("s02", titles["s02"]), pic("ecosystem", "Mapa del ecosistema de proyectos"),
          pic("s03", titles["s03"])]
    for i, p in enumerate(PROJECTS, 1):
        row = pic(f"projects/{i:02d}", p["name"], W_ROW)
        if p["live"]:
            row += f'<a href="{p["live"]}">{pic("projects/live", p["name"] + " — sitio en vivo", W_CELL)}</a>'
        else:
            row += pic("projects/live-none", "Sin sitio en vivo", W_CELL)
        if p["repo"] == PRIVATE:
            row += pic("projects/repo-private", "Repositorio privado", W_CELL)
        else:
            row += f'<a href="{p["repo"]}">{pic("projects/repo", p["name"] + " — repositorio", W_CELL)}</a>'
        L.append(row)
    L += [pic("s04", titles["s04"]), pic("telemetry", "Lenguajes, ritmo de entrega y cifras del perfil"),
          pic("github-stats", "Estadísticas de GitHub y lenguajes por repositorio"),
          pic("activity", "Actividad de contribuciones en GitHub"),
          pic("s05", titles["s05"]), pic("timeline", "Línea de tiempo"), pic("experience", "Experiencia profesional"),
          pic("s06", titles["s06"]), pic("stack", "Stack técnico"), pic("footer", "Estado actual")]
    text = "\n".join(L) + "\n\n<!-- Generado con tools/build_assets.py: edita los datos allí y vuelve a ejecutarlo. -->\n"
    (ROOT / "README.md").write_text(text, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    n = build_all()
    build_readme()
    print(f"{n} imagenes x 2 temas + README.md")
