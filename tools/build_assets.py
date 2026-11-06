#!/usr/bin/env python3
"""Genera TODAS las imágenes SVG del perfil (claras y oscuras) y el README.md.

    python tools/build_assets.py

Escribe:
  assets/*.svg, assets/projects/*.svg        -> variante clara (marfil)
  assets/dark/*.svg, assets/dark/projects/*  -> variante oscura (tinta cálida)
  README.md                                  -> enlaza cada imagen con <picture>

Estilo: sobrio, tipo blog de Anthropic. Fondo marfil #faf9f5, tinta #141413, líneas finas de 1 px en gris cálido
#a3a095, un único acento naranja #d97757 (usado solo en marcadores y en el dato destacado de cada gráfico),
títulos en serif, interfaz en sans, esquinas rectas, sin sombras ni degradados ni animaciones.
GitHub no carga fuentes externas dentro de un <img>, así que se usan pilas del sistema.

Escala tipográfica única (px del viewBox): 64 hero · 32 títulos y cifras · 20 destacados · 16 cuerpo · 14 interfaz.
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


def css(c):
    return (
        f".serif{{font-family:{SERIF}}}.sans{{font-family:{SANS}}}"
        ".t64{font-size:64px;letter-spacing:-1px}.t32{font-size:32px;letter-spacing:-.3px}"
        ".t20{font-size:20px}.t16{font-size:16px}.t14{font-size:14px}.b{font-weight:600}.i{font-style:italic}"
        f".ink{{fill:{c['ink']}}}.tx{{fill:{c['text']}}}.mu{{fill:{c['muted']}}}.so{{fill:{c['soft']}}}"
        f".ac{{fill:{c['accent']}}}.at{{fill:{c['accent_t']}}}"
        f".ul{{text-decoration:underline;text-underline-offset:3px;text-decoration-color:{c['rule']}}}"
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


def T(x, y, text, cls, anchor=None):
    a = f' text-anchor="{anchor}"' if anchor else ""
    return f'<text x="{x}" y="{y}" class="{cls}"{a}>{escape(text, quote=False)}</text>'


def hline(c, x1, x2, y, op=0.7):
    return f'<line x1="{x1}" y1="{y + .5}" x2="{x2}" y2="{y + .5}" stroke="{c["rule"]}" stroke-width="1" stroke-opacity="{op}"/>'


def vline(c, x, y1, y2, op=0.7):
    return f'<line x1="{x + .5}" y1="{y1}" x2="{x + .5}" y2="{y2}" stroke="{c["rule"]}" stroke-width="1" stroke-opacity="{op}"/>'


def box(c, x, y, w, h, op=0.8):
    return (f'<rect x="{x + .5}" y="{y + .5}" width="{w - 1}" height="{h - 1}" fill="none" '
            f'stroke="{c["rule"]}" stroke-width="1" stroke-opacity="{op}"/>')


def square(c, x, y, s=8):
    return f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{c["accent"]}"/>'


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

LINKS = [  # (archivo, etiqueta, ancho, url, alt)
    ("link-portfolio", "Portafolio", "https://gustavoadolfonavarropacheco.vercel.app/", "Portafolio"),
    ("link-resume", "Currículum", "https://gustavoadolfonavarropacheco.vercel.app/Gustavo_Navarro_CV.pdf", "Currículum (PDF)"),
    ("link-linkedin", "LinkedIn", "https://www.linkedin.com/in/gustavo-adolfo-navarro-pacheco-876b06356/", "LinkedIn"),
    ("link-email", "Correo", "mailto:adolfonavarro0212@gmail.com", "Correo electrónico"),
]


# ───────────────────────────── imágenes ─────────────────────────────
def header(c):
    b = [square(c, MX, 56, 10), T(MX + 22, 66, "Portafolio", "sans t14 mu"),
         T(RX, 66, "Campuslands S.A.S", "sans t14 mu", "end"),
         T(MX - 3, 172, "Gustavo Navarro", "serif t64 ink"),
         T(MX, 216, "Full Stack Developer — Bucaramanga, Santander, Colombia.", "serif t20 mu"),
         hline(c, MX, RX, 262),
         T(MX, 306, "Enfoque", "sans t14 mu"), T(MX + 112, 306, "MySQL · Python · JS · React", "sans t16 ink"),
         T(MX, 340, "Estado", "sans t14 mu"), square(c, MX + 112, 331, 8),
         T(MX + 130, 340, "Open to internships · freelance · collaboration", "sans t16 ink")]
    return svg(1000, 372, "".join(b), "Gustavo Navarro — Full Stack Developer en Bucaramanga, Colombia", c)


def link_button(label):
    def f(c):
        b = [box(c, 0, 0, 168, 44, 0.9), T(84, 27, f"{label} ↗", "sans t14 b ink", "middle")]
        return svg(168, 44, "".join(b), label, c, size=True)
    return f


def section(title):
    def f(c):
        b = [T(MX, 54, title, "serif t32 ink"), hline(c, MX, RX, 70)]
        return svg(1000, 88, "".join(b), title, c)
    return f


def whoami(c):
    b = [T(MX, 48, "Graduated from Campuslands S.A.S", "serif t20 mu"),
         T(MX - 1, 96, "Full Stack Developer", "serif t32 ink"),
         T(MX, 128, "Java · React · SpringBoot · Node.js · HTML & CSS", "sans t16 tx"),
         T(MX, 170, "Drawn to projects where design meets data.", "serif t20 mu"),
         T(MX, 198, "Clean architecture and user experience in equal measure.", "serif t20 mu"),
         hline(c, MX, RX, 230),
         T(MX, 274, "Enfoque", "sans t14 mu"),
         T(MX + 112, 274, "Mobile · Full-Stack Systems · Terminal UI / CLI · AI-integrated architectures", "sans t16 ink"),
         T(MX, 312, "Estado", "sans t14 mu"), square(c, MX + 112, 303, 8),
         T(MX + 130, 312, "Open to internships · freelance · collaboration", "sans t16 ink")]
    return svg(1000, 344, "".join(b), "Sobre Gustavo: Full Stack Developer graduado de Campuslands, abierto a pasantías, freelance y colaboración", c)


def ecosystem(c):
    cw, ch, gap = 264, 62, 14
    xs = [48, 368, 688]
    centers = [x + cw / 2 for x in xs]
    b = [box(c, 400, 24, 200, 56, 0.9),
         T(500, 50, "Gustavo Navarro", "serif t20 ink", "middle"),
         T(500, 69, "One-person build pipeline", "sans t14 mu", "middle"),
         vline(c, 500, 80, 104), hline(c, int(centers[0]), int(centers[2]), 104)]
    for cx in centers:
        b.append(vline(c, int(cx), 104, 132))
    for x, cx, (head, nodes) in zip(xs, centers, ECOSYSTEM):
        b.append(T(int(cx), 156, head, "sans t14 b ink", "middle"))
        for i, (name, sub) in enumerate(nodes):
            y = 176 + i * (ch + gap)
            b += [box(c, x, y, cw, ch), T(x + 20, y + 27, name, "sans t16 b ink"), T(x + 20, y + 48, sub, "sans t14 mu")]
    b += [hline(c, MX, RX, 566), T(MX, 592, "Everything from one pipeline.", "serif t14 i mu")]
    return svg(1000, 612, "".join(b), "Mapa del ecosistema: sistemas de negocio, IA y automatización, y web y datos, todo desde un mismo flujo de trabajo", c)


def project_row(p):
    def f(c):
        b = [T(MX, 34, p["name"], "serif t20 ink"),
             T(MX, 60, p["desc"][0], "sans t14 tx"), T(MX, 80, p["desc"][1], "sans t14 tx"),
             T(MX, 104, " · ".join(p["tech"]), "sans t14 mu"),
             hline(c, MX, 730, 118, 0.55)]
        return svg(730, 124, "".join(b), p["name"], c)
    return f


def cell(kind):
    texts = {"live": ("Sitio ↗", "sans t14 b ink ul"), "live-none": ("Sin sitio", "sans t14 so"),
             "repo": ("Código ↗", "sans t14 b ink ul"), "repo-private": ("Privado", "sans t14 so")}
    label = {"live": "Sitio en vivo", "live-none": "Sin sitio", "repo": "Repositorio", "repo-private": "Repositorio privado"}[kind]

    def f(c):
        x2 = 82 if kind.startswith("repo") else 130
        b = [T(16, 34, texts[kind][0], texts[kind][1]), hline(c, 0, x2, 118, 0.55)]
        return svg(130, 124, "".join(b), label, c)
    return f


def telemetry(c):
    b = [vline(c, 360, 20, 300, 0.45), vline(c, 676, 20, 300, 0.45)]
    # lenguajes por bytes
    b.append(T(MX, 38, "Lenguajes · por bytes", "sans t14 mu"))
    for i, (lang, pct, w) in enumerate(LANGS_BYTES):
        y = 78 + i * 40
        fill = c["accent"] if i == 0 else c["soft"]
        b += [T(MX, y, lang, "sans t14 ink"),
              f'<rect x="{MX}" y="{y + 8}" width="{w}" height="8" fill="{fill}"/>',
              T(MX + w + 10, y + 16, f"{pct}%", "sans t14 mu")]
    # ritmo de entrega
    b.append(T(392, 38, "Ritmo de entrega · 2025 → 2026", "sans t14 mu"))
    b += [hline(c, 392, 656, 212),
          f'<polyline points="392,200 440,192 488,170 536,148 584,108 622,72 656,52" fill="none" stroke="{c["ink"]}" stroke-width="1.5" stroke-linejoin="round"/>']
    for px, py in [(440, 192), (488, 170), (536, 148), (584, 108)]:
        b.append(f'<circle cx="{px}" cy="{py}" r="2.5" fill="{c["ink"]}"/>')
    b.append(f'<circle cx="622" cy="72" r="4.5" fill="{c["accent"]}"/>')
    b += [T(392, 236, "Apr '25", "sans t14 mu"), T(500, 236, "Feb '26", "sans t14 mu"), T(612, 236, "Oct '26", "sans t14 mu"),
          T(392, 272, "Tendencia: acelerando", "sans t14 ink")]
    # contadores
    counters = [("27", "Repositorios", False), ("14", "Proyectos documentados", False),
                ("3", "Web · API · AI agents", False), ("∞", "Pestañas de terminal abiertas", True)]
    b.append(T(708, 38, "Perfil en cifras", "sans t14 mu"))
    for i, (n, label, hl) in enumerate(counters):
        y = 84 + i * 62
        b += [T(708, y, n, "serif t32 " + ("at" if hl else "ink")), T(708, y + 21, label, "sans t14 mu")]
    return svg(1000, 312, "".join(b), "Lenguajes por bytes, ritmo de entrega 2025-2026 y cifras del perfil: 27 repositorios, 14 proyectos y 3 plataformas", c)


def github_stats(c):
    b = [vline(c, 500, 24, 296, 0.45),
         T(MX, 44, "Estadísticas de GitHub", "serif t20 ink"), T(532, 44, "Lenguajes por repositorio", "serif t20 ink")]
    for i, (label, val) in enumerate(GH_STATS):
        y = 96 + i * 46
        b += [T(MX, y, label, "sans t14 tx"), T(452, y + 1, val, "serif t20 ink", "end"), hline(c, MX, 452, y + 14, 0.45)]
    for i, (lang, w) in enumerate(GH_LANGS):
        y = 96 + i * 46
        b += [T(532, y, lang, "sans t14 tx"),
              f'<rect x="640" y="{y - 9}" width="312" height="8" fill="{c["track"]}"/>',
              f'<rect x="640" y="{y - 9}" width="{round(312 * w / 270, 1)}" height="8" fill="{c["ink"]}"/>',
              hline(c, 532, RX, y + 14, 0.45)]
    return svg(1000, 312, "".join(b), "Estadísticas de GitHub y lenguajes por repositorio", c)


def activity(c):
    area = f"{ACTIVITY_PTS} 948.0,236.0 52.0,236.0"
    b = [T(MX, 44, "Actividad de contribuciones", "serif t20 ink"),
         T(RX, 44, "772 contribuciones · últimos 12 meses", "sans t14 mu", "end")]
    for gy in (194.7, 153.3, 112.0):
        b.append(f'<line x1="{MX}" y1="{gy}" x2="{RX}" y2="{gy}" stroke="{c["rule"]}" stroke-opacity=".45" stroke-dasharray="2 4"/>')
    b += [f'<polygon points="{area}" fill="{c["ink"]}" fill-opacity=".06"/>',
          hline(c, MX, RX, 236),
          f'<polyline points="{ACTIVITY_PTS}" fill="none" stroke="{c["ink"]}" stroke-width="1.5" stroke-linejoin="round"/>',
          f'<circle cx="879.1" cy="112" r="4" fill="{c["accent"]}"/>',
          T(867, 117, "Pico: 125 por semana", "sans t14 at", "end"),
          f'<circle cx="948" cy="229.1" r="3" fill="{c["ink"]}"/>']
    for x, m in ACTIVITY_MONTHS:
        b.append(T(x, 266, m, "sans t14 mu", "middle" if 52 < x < 940 else ("start" if x < 100 else "end")))
    return svg(1000, 288, "".join(b), "Contribuciones en GitHub: 772 en los últimos 12 meses, actividad semanal", c)


def timeline(c):
    ax, y0 = [90 + i * 140 for i in range(len(TIMELINE))], 130
    b = [hline(c, MX, RX, y0)]
    for i, (x, (date, label)) in enumerate(zip(ax, TIMELINE)):
        cur = i == CURRENT
        up = i % 2 == 0
        if up:
            b += [vline(c, x, 98, y0 - 6, 0.9), T(x, 62, date, "sans t14 " + ("at" if cur else "mu"), "middle"),
                  T(x, 86, label, "sans t16 ink", "middle")]
        else:
            b += [vline(c, x, y0 + 6, y0 + 34, 0.9), T(x, 188, date, "sans t14 " + ("at" if cur else "mu"), "middle"),
                  T(x, 212, label, "sans t16 ink", "middle")]
        if cur:
            b += [f'<circle cx="{x}" cy="{y0 + .5}" r="11" fill="none" stroke="{c["accent"]}" stroke-opacity=".4"/>',
                  f'<circle cx="{x}" cy="{y0 + .5}" r="6" fill="{c["accent"]}"/>']
        else:
            b.append(f'<circle cx="{x}" cy="{y0 + .5}" r="5" fill="{c["bg"]}" stroke="{c["ink"]}" stroke-width="1.5"/>')
    return svg(1000, 240, "".join(b), "Trayectoria: " + "; ".join(f"{d} {t}" for d, t in TIMELINE), c)


def experience(c):
    b = []
    for i, (dur, company, role) in enumerate(EXPERIENCE):
        y = 44 + i * 88
        b += [T(MX, y, dur, "sans t14 mu"), T(200, y, company, "serif t20 ink"), T(200, y + 25, role, "sans t14 tx"),
              hline(c, MX, RX, y + 44, 0.55)]
    return svg(1000, 8 + 88 * len(EXPERIENCE), "".join(b), "Experiencia: " + "; ".join(f"{co}, {r} ({d})" for d, co, r in EXPERIENCE), c)


def stack(c):
    b = []
    for i, (label, value) in enumerate(STACK):
        y = 34 + i * 40
        b += [T(MX, y, label, "sans t14 mu"), T(200, y, value, "sans t16 ink"), hline(c, MX, RX, y + 18, 0.55)]
    return svg(1000, 34 + 40 * len(STACK) - 8, "".join(b), "Stack técnico: lenguajes, backend, frontend, bases de datos, IA, arquitectura, herramientas y despliegue", c)


def footer(c):
    b = [f'<circle cx="{MX + 6}" cy="55" r="5" fill="{c["accent"]}"/>',
         T(MX + 26, 62, "Estado · En construcción", "sans t16 ink"),
         T(MX + 26, 90, "probably in a terminal, probably past midnight", "serif t14 i mu"),
         T(RX, 90, "Gustavo Navarro  ·  Bucaramanga, CO  ·  © 2026", "sans t14 mu", "end")]
    return svg(1000, 116, "".join(b), "Estado: construyendo. Bucaramanga, Colombia.", c)


# ───────────────────────────── escritura ─────────────────────────────
def build_all():
    files = {"header-v1": header, "whoami": whoami, "ecosystem": ecosystem, "telemetry": telemetry,
             "github-stats": github_stats, "activity": activity, "timeline": timeline,
             "experience": experience, "stack": stack, "footer": footer}
    for name, title in SECTIONS:
        files[name] = section(title)
    for key, label, _, _ in LINKS:
        files[key] = link_button(label)
    for i, p in enumerate(PROJECTS, 1):
        files[f"projects/{i:02d}"] = project_row(p)
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
    w = f' width="{width}"' if width else ""
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="assets/dark/{name}.svg"/>'
            f'<img src="assets/{name}.svg"{w} alt="{escape(alt, quote=True)}"/></picture>')


def build_readme():
    L = ['<div align="center">', "", pic("header-v1", "Gustavo Navarro — Full Stack Developer"), ""]
    L += [f'<a href="{url}">{pic(key, alt)}</a>' for key, _, url, alt in LINKS]
    L += ["", "</div>", ""]
    titles = dict(SECTIONS)
    L += [pic("s01", titles["s01"]), pic("whoami", "Sobre Gustavo"),
          pic("s02", titles["s02"]), pic("ecosystem", "Mapa del ecosistema de proyectos"),
          pic("s03", titles["s03"])]
    for i, p in enumerate(PROJECTS, 1):
        row = pic(f"projects/{i:02d}", p["name"], "73%")
        if p["live"]:
            row += f'<a href="{p["live"]}">{pic("projects/live", p["name"] + " — sitio en vivo", "13%")}</a>'
        else:
            row += pic("projects/live-none", "Sin sitio en vivo", "13%")
        if p["repo"] == PRIVATE:
            row += pic("projects/repo-private", "Repositorio privado", "13%")
        else:
            row += f'<a href="{p["repo"]}">{pic("projects/repo", p["name"] + " — repositorio", "13%")}</a>'
        L.append(row)
    L += [pic("s04", titles["s04"]), pic("telemetry", "Lenguajes, ritmo de entrega y cifras del perfil"), "",
          '<div align="center">', "",
          pic("github-stats", "Estadísticas de GitHub y lenguajes por repositorio", "97%"), "",
          pic("activity", "Actividad de contribuciones en GitHub", "97%"), "", "</div>", "",
          pic("s05", titles["s05"]), pic("timeline", "Línea de tiempo"), pic("experience", "Experiencia profesional"),
          pic("s06", titles["s06"]), pic("stack", "Stack técnico"), pic("footer", "Estado actual"), "",
          "<!-- Generado con tools/build_assets.py: edita los datos allí y vuelve a ejecutarlo. -->", ""]
    (ROOT / "README.md").write_text("\n".join(L), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    n = build_all()
    build_readme()
    print(f"{n} imágenes × 2 temas + README.md")
