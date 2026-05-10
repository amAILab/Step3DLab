from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]

BASE_CSS = """
:root{--bg:#f5f5f2;--surface:#fff;--soft:#efefec;--ink:#101010;--muted:#5e5e59;--line:#ddd;--radius:28px;--max:1120px}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;line-height:1.55;letter-spacing:-.015em}a{color:inherit;text-decoration:none}.container{width:min(100% - 40px,var(--max));margin:0 auto}.header{position:sticky;top:0;background:rgba(245,245,242,.9);backdrop-filter:blur(16px);border-bottom:1px solid var(--line);z-index:10}.head{min-height:72px;display:flex;align-items:center;justify-content:space-between;gap:18px}.brand{font-weight:900;font-size:1.25rem}.nav{display:flex;gap:10px;flex-wrap:wrap}.btn{display:inline-flex;align-items:center;justify-content:center;border-radius:999px;padding:12px 16px;border:1px solid var(--ink);font-weight:800}.btn.primary{background:var(--ink);color:white}.btn.ghost{background:transparent}.hero{padding:86px 0 52px}.eyebrow{text-transform:uppercase;font-weight:900;letter-spacing:.13em;font-size:.78rem;color:var(--muted);margin:0 0 10px}h1{font-size:clamp(2.4rem,6vw,5.6rem);line-height:.92;letter-spacing:-.075em;margin:0 0 22px;max-width:920px}h2{font-size:clamp(1.7rem,3vw,3.2rem);line-height:1;letter-spacing:-.055em;margin:0 0 16px}h3{font-size:1.25rem;margin:0 0 8px}.lead{font-size:clamp(1.08rem,2vw,1.35rem);color:var(--muted);max-width:790px;margin:0 0 28px}.section{padding:44px 0}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:24px}.card p,.muted{color:var(--muted);margin:0}.list{padding:0;margin:14px 0 0;list-style:none;display:grid;gap:10px}.list li{display:flex;gap:9px;color:var(--muted)}.list li:before{content:'→';font-weight:900;color:var(--ink)}.trust-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.trust-card{background:var(--soft);border:1px solid var(--line);border-radius:22px;padding:18px}.trust-card strong{display:block;margin-bottom:6px}.trust-card p{color:var(--muted);margin:0}.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.step{background:var(--soft);border:1px solid var(--line);border-radius:22px;padding:18px}.step strong{display:block;font-size:1.7rem;letter-spacing:-.06em;margin-bottom:8px}@media(max-width:860px){.steps,.trust-grid{grid-template-columns:1fr 1fr}}@media(max-width:560px){.steps,.trust-grid{grid-template-columns:1fr}}.split{display:grid;grid-template-columns:1.05fr .95fr;gap:18px;align-items:start}.image{border-radius:var(--radius);overflow:hidden;border:1px solid var(--line);background:var(--soft)}.image img{width:100%;display:block}.cta{background:var(--ink);color:#fff;border-radius:34px;padding:32px;display:grid;grid-template-columns:1fr auto;gap:20px;align-items:center}.cta p{color:#ddd;margin:0}.footer{padding:52px 0 36px;color:var(--muted);background:#eeeeea;border-top:1px solid var(--line)}.footer-map{display:grid;grid-template-columns:1.35fr repeat(4,minmax(0,1fr));gap:26px;align-items:start}.footer-brand strong{display:block;color:var(--ink);font-size:1.18rem;margin-bottom:8px}.footer-brand p{margin:0;max-width:300px}.footer-col h3{margin:0 0 12px;color:var(--ink);font-size:.95rem}.footer-col ul{list-style:none;margin:0;padding:0;display:grid;gap:9px}.footer-col a{color:var(--muted)}.footer-col a:hover{color:var(--ink);text-decoration:underline}.footer-bottom{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;border-top:1px solid var(--line);margin-top:32px;padding-top:20px}@media(max-width:860px){.grid,.split,.cta{grid-template-columns:1fr}.footer-map{grid-template-columns:1fr 1fr}.footer-brand{grid-column:1/-1}.hero{padding-top:56px}.nav{display:none}h1{font-size:3rem}}@media(max-width:560px){.footer-map{grid-template-columns:1fr}.footer-brand{grid-column:auto}.footer-bottom{display:grid}}
"""

TRUST_SECTION = """<section class="section" aria-labelledby="trust-title"><div class="container"><p class="eyebrow">Почему можно доверять</p><h2 id="trust-title">Перед запуском предупреждаем о рисках</h2><div class="trust-grid"><div class="trust-card"><strong>Проверяем геометрию</strong><p>Смотрим толщины, посадки, масштаб и слабые места до печати.</p></div><div class="trust-card"><strong>Подбираем технологию</strong><p>Не обещаем одну кнопку: выбираем материал и метод под задачу.</p></div><div class="trust-card"><strong>Работаем с файлами</strong><p>Принимаем STL, STEP, 3MF, OBJ, фото, эскиз или физическую деталь.</p></div><div class="trust-card"><strong>Фиксируем вводные</strong><p>Срок, количество, внешний вид и прочность уточняем до запуска.</p></div></div></div></section>"""

LOCAL_SECTION = """<section class="section" aria-labelledby="local-title"><div class="container"><p class="eyebrow">Локально</p><h2 id="local-title">3D-печать и прототипирование в Москве</h2><div class="grid"><article class="card"><h3>Москва и область</h3><p>Можно начать с онлайн-оценки по фото, эскизу, STL/STEP или описанию задачи. Для первичного расчёта достаточно размеров, срока и назначения детали.</p><ul class="list"><li><a href="../#brief">заявка на расчёт</a></li><li><a href="../3d-printing/">3D-печать деталей</a></li></ul></article><article class="card"><h3>Вузы, технопарки и команды</h3><p>Помогаем с прототипами, демонстрационными макетами, проектными занятиями и образовательными форматами по цифровому производству.</p><ul class="list"><li><a href="../workshops/">мастер-классы и обучение</a></li><li><a href="../services/">все услуги Step3D</a></li></ul></article><article class="card"><h3>События, сцена и кейсы</h3><p>Делаем награды, бутафорию, арт-объекты и презентационные модели к конкретной дате — с учётом веса, внешнего вида и сборки.</p><ul class="list"><li><a href="../cases/">посмотреть кейсы</a></li><li><a href="../reverse-engineering/">реверс-инжиниринг</a></li></ul></article></div></div></section>"""

PAGES = {
    'services/index.html': {
        'project_param': '3D-модель / промышленный дизайн',
        'title': 'Услуги Step3D — 3D-печать, моделирование, сканирование и обучение',
        'description': 'Основные услуги Step3D: 3D-печать, CAD-моделирование, 3D-сканирование, реверс-инжиниринг, прототипирование, малые серии и образовательные проекты.',
        'h1': 'Услуги Step3D',
        'lead': 'Помогаем пройти путь от идеи, фото или сломанной детали до готового объекта, прототипа, модели или малой серии.',
        'image': '../assets/img/hero-production.webp',
        'blocks': [
            ('3D-печать', 'Детали, макеты, корпуса, декоративные и сценические объекты. Подходит, когда есть STL/STEP/3MF или понятная форма изделия.', ['подбор технологии FDM/SLA', 'подготовка модели к печати', 'базовая постобработка и проверка']),
            ('3D-моделирование', 'Создаём модель по эскизу, фото, размерам или референсам. Сразу учитываем ограничения печати и сборки.', ['модель под производство', 'итерации и уточнение формы', 'подготовка файлов для печати']),
            ('3D-сканирование и реверс-инжиниринг', 'Восстанавливаем геометрию детали или объекта, когда нужно повторить форму, посадки или сложную поверхность.', ['сканирование объекта', 'восстановление CAD-логики', 'модель для печати или производства']),
            ('Прототипы и малые серии', 'Сначала проверяем форму и материал на прототипе, затем считаем повторяемую партию.', ['тестовый образец', 'доработка после проверки', 'расчёт малой серии']),
            ('Образовательные проекты', 'Мастер-классы и проектные занятия по 3D-печати, CAD, сканированию и цифровому производству.', ['формат под возраст участников', 'практический результат занятия', 'методическая и проектная логика']),
            ('Объекты для событий', 'Награды, бутафория, декорации, арт-объекты и презентационные макеты к конкретной дате.', ['визуальная задача', 'контроль сроков', 'подготовка к показу или сцене']),
        ]
    },
    'reverse-engineering/index.html': {
        'project_param': 'Реверсивный инжиниринг / сканирование',
        'title': 'Реверс-инжиниринг и 3D-сканирование — Step3D',
        'description': '3D-сканирование и реверс-инжиниринг деталей: восстановление геометрии, подготовка CAD-модели и файлов для печати или производства.',
        'h1': 'Реверс-инжиниринг и 3D-сканирование',
        'lead': 'Когда нет чертежа или 3D-модели, но есть физическая деталь, мы помогаем перевести её в цифровую геометрию и подготовить к производству.',
        'image': '../assets/img/case-kawasaki.webp',
        'blocks': [
            ('Когда нужно', 'Подходит для восстановления сломанной детали, повторения формы, доработки посадок или подготовки объекта к изготовлению.', ['деталь снята с производства', 'нужно повторить сложную форму', 'есть объект, но нет CAD-файла']),
            ('Как проходит работа', 'Сначала оцениваем объект, затем сканируем или измеряем критичные зоны, после чего восстанавливаем рабочую модель.', ['осмотр и фото', 'сканирование/измерения', 'CAD-восстановление', 'проверка размеров']),
            ('Что прислать', 'Для первичной оценки достаточно фото, размеров и описания, где деталь используется.', ['3–5 фото с разных сторон', 'общие габариты', 'критичные посадочные размеры']),
        ]
    },
    '3d-printing/index.html': {
        'project_param': '3D-печать детали',
        'title': '3D-печать и прототипирование — Step3D',
        'description': '3D-печать деталей, макетов, корпусов, прототипов и малых серий. Подбор технологии, подготовка модели и базовая постобработка.',
        'h1': '3D-печать и прототипирование',
        'lead': 'Печатаем детали, макеты, корпуса, арт-объекты и прототипы. Если модели нет — поможем подготовить её под печать.',
        'image': '../assets/img/hero-production.webp',
        'blocks': [
            ('Что можно сделать', 'Прототипы, корпуса, крепления, макеты, декоративные элементы, детали для проверки формы и сборки.', ['одиночные детали', 'тестовые образцы', 'малые серии после прототипа']),
            ('Что влияет на цену', 'Размер, материал, сложность модели, плотность заполнения, количество, срочность и постобработка.', ['материал и технология', 'время печати', 'уровень поверхности']),
            ('Срочная замена детали', 'Если сломалась пластиковая деталь оборудования, мебели или корпуса, можно начать с фото и размеров — оценим, получится ли быстро напечатать замену или нужен реверс-инжиниринг.', ['фото поломки и целой зоны', 'габариты и нагрузка', 'желаемый срок замены']),
            ('Какие файлы нужны', 'Лучше всего подходят STL, 3MF, OBJ для печати и STEP для инженерной доработки.', ['STL/3MF/OBJ', 'STEP при доработке', 'фото/эскиз, если файла нет']),
        ]
    },
    'urgent-spare-parts/index.html': {
        'project_param': 'Срочная 3D-печать запчасти по фото',
        'title': 'Срочная 3D-печать запчастей по фото и размерам — Step3D Москва',
        'description': 'Быстрая оценка и изготовление пластиковой запчасти по фото, размерам, сломанной детали или STL/STEP. 3D-печать, реверс-инжиниринг и прототипирование в Москве.',
        'h1': 'Срочная запчасть по фото, размерам или сломанной детали',
        'lead': 'Если пластиковая деталь сломалась, потерялась или снята с производства — начните с фото и габаритов. Быстро скажем, можно ли напечатать замену, нужен ли реверс-инжиниринг и какой будет порядок бюджета.',
        'image': '../assets/img/proof-engineering.webp',
        'blocks': [
            ('Что прислать для расчёта', 'Не нужен идеальный чертёж. Для первого ответа достаточно понятных вводных, чтобы оценить риск и технологию.', ['3–5 фото детали и места установки', 'общие габариты в миллиметрах', 'где работает деталь и какая нагрузка', 'желаемый срок и количество']),
            ('Какие детали подходят', 'Лучше всего заходят корпуса, крышки, крепления, декоративные элементы, держатели, ручки, заглушки и прототипы для проверки формы.', ['пластиковые элементы оборудования', 'детали мебели и корпусов', 'крепления и переходники', 'единичные замены и малые серии']),
            ('Когда предупредим о риске', 'Мы не обещаем магию: если деталь несёт большую нагрузку, работает при температуре или требует точной посадки, заранее скажем, что нужно проверить.', ['нагрузка и износ', 'температура и химия', 'резьбы, защёлки и посадки', 'нужен тестовый прототип']),
            ('Быстрый сценарий', 'Сначала делаем экспресс-оценку. Если задача реалистична — готовим модель, печатаем тест или сразу рабочую деталь.', ['оценка по фото', 'модель или доработка файла', 'печать прототипа', 'повтор после проверки']),
            ('Что получает клиент', 'Понятный ответ: можно/нельзя, чем печатать, что может сломаться, сколько примерно стоит первый образец и что делать дальше.', ['порядок бюджета', 'срок изготовления', 'рекомендация по материалу', 'следующий шаг без лишней переписки']),
            ('Для бизнеса', 'Подходит мастерским, небольшим производствам, лабораториям, вузам, театрам и командам, которым нужно быстро закрыть единичную техническую проблему.', ['быстрая замена', 'проверка гипотезы', 'малые партии после теста', 'файлы для повторного изготовления']),
        ]
    },
    'workshops/index.html': {
        'project_param': 'Мастер-класс / обучение',
        'title': 'Мастер-классы и образовательные проекты — Step3D',
        'description': 'Практические занятия по 3D-печати, CAD, реверс-инжинирингу и цифровому производству для школ, вузов, технопарков и команд.',
        'h1': 'Мастер-классы и образовательные проекты',
        'lead': 'Собираем понятные практические форматы: от знакомства с 3D-печатью до проектной работы с CAD, сканированием и прототипированием.',
        'image': '../assets/img/proof-education.webp',
        'blocks': [
            ('Форматы', 'Мастер-класс, интенсив, проектное занятие, демонстрация оборудования или практикум под событие.', ['для школьников и студентов', 'для технопарков и вузов', 'для мероприятий и проектных смен']),
            ('Что получают участники', 'Понимание полного цикла: идея, цифровая модель, подготовка, печать, проверка результата.', ['практический опыт', 'готовый объект или прототип', 'понимание инженерной логики']),
            ('Что нужно для расчёта', 'Возраст и количество участников, длительность, площадка, желаемый результат и уровень подготовки.', ['возраст группы', 'количество участников', 'длительность и цель занятия']),
        ]
    },
    'cases/index.html': {
        'project_param': 'Объект для события / сцены',
        'title': 'Кейсы Step3D — 3D-печать, сканирование, объекты и обучение',
        'description': 'Кейсы Step3D: награды, реверс-инжиниринг, сценические объекты, арт-прототипы, образовательные проекты и робототехника.',
        'h1': 'Кейсы Step3D',
        'lead': 'Здесь собраны типы задач, по которым проще понять формат работы: входные данные, решение и результат.',
        'image': '../assets/img/case-awards.webp',
        'blocks': [
            ('Награда для премии СТД России', 'Объект для публичного события: дизайн, печать, сборка и подготовка поверхности к конкретной дате.', ['задача: выразительный объект', 'решение: дизайн + печать + сборка', 'результат: готовая награда']),
            ('Kawasaki Puccetti Racing', '3D-сканирование и восстановление сложной геометрии спортивного обвеса.', ['задача: восстановить форму', 'решение: сканирование и reverse engineering', 'результат: цифровая геометрия']),
            ('Фальшсветильники для спектакля', 'Лёгкие сценические объекты для театральной постановки с контролем веса и внешнего вида.', ['задача: сценический эффект', 'решение: печать и подготовка', 'результат: готовые элементы декораций']),
            ('Морские шахматы', 'Предметный арт-объект: идея, 3D-модель, прототип и демонстрационный результат.', ['задача: выразительная форма', 'решение: моделирование и печать', 'результат: прототип для показа']),
        ]
    }
}


def render_page(data):
    project_query = quote(data.get('project_param', ''))
    cards = []
    for title, text, items in data['blocks']:
        lis = ''.join(f'<li>{item}</li>' for item in items)
        cards.append(f'<article class="card"><h3>{title}</h3><p>{text}</p><ul class="list">{lis}</ul></article>')
    return f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{data['title']}</title>
<meta name="description" content="{data['description']}">
<meta property="og:type" content="website">
<meta property="og:title" content="{data['title']}">
<meta property="og:description" content="{data['description']}">
<meta property="og:url" content="https://amailab.github.io/Step3D/{data.get('canonical','')}">
<meta property="og:image" content="https://amailab.github.io/Step3D/assets/img/og-step3d.webp">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://amailab.github.io/Step3D/{data.get('canonical','')}">
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>{BASE_CSS}</style>
</head>
<body>
<header class="header"><div class="container head"><a class="brand" href="../">Step3D</a><nav class="nav"><a href="../#cases">Кейсы</a><a href="../#services">Услуги</a><a href="../#project-quiz">Квиз</a><a href="../#brief">Заявка</a></nav><a class="btn primary" href="../?project={project_query}#brief">Рассчитать</a></div></header>
<main>
<section class="hero"><div class="container split"><div><p class="eyebrow">Step3D</p><h1>{data['h1']}</h1><p class="lead">{data['lead']}</p><p><a class="btn primary" href="../?project={project_query}#brief">Оставить заявку</a> <a class="btn ghost" href="../">На главную</a></p></div><div class="image"><img src="{data['image']}" alt="{data['h1']} Step3D" loading="eager"></div></div></section>
<section class="section"><div class="container grid">{''.join(cards)}</div></section>
<section class="section"><div class="container"><p class="eyebrow">Как работаем</p><h2>Понятный цикл без лишней бюрократии</h2><div class="steps"><div class="step"><p class="muted">Получаем фото, размеры, файл или описание задачи.</p></div><div class="step"><p class="muted">Оцениваем технологию, риски, срок и порядок бюджета.</p></div><div class="step"><p class="muted">Делаем модель, сканирование, прототип или печать.</p></div><div class="step"><p class="muted">Проверяем результат и готовим изделие или файлы к передаче.</p></div></div></div></section>
{TRUST_SECTION}
{LOCAL_SECTION}
<section class="section"><div class="container cta"><div><h2>Хотите оценить похожую задачу?</h2><p>Пришлите фото, размеры, срок и короткое описание — подскажем технологию, риски и порядок бюджета.</p></div><a class="btn primary" href="../?project={project_query}#brief">Заполнить заявку</a></div></section>
</main>
<footer class="footer" aria-label="Карта сайта Step3D"><div class="container"><div class="footer-map"><div class="footer-brand"><strong>Step3D</strong><p>Все ключевые разделы сайта — в одном месте: услуги, кейсы, заявка, материалы и контакты.</p></div><nav class="footer-col" aria-label="Услуги"><h3>Услуги</h3><ul><li><a href="../services/">Все услуги</a></li><li><a href="../3d-printing/">3D-печать</a></li><li><a href="../reverse-engineering/">Реверс-инжиниринг</a></li><li><a href="../urgent-spare-parts/">Запчасть по фото</a></li><li><a href="../workshops/">Мастер-классы</a></li></ul></nav><nav class="footer-col" aria-label="Разделы"><h3>Разделы</h3><ul><li><a href="../#process">Как работаем</a></li><li><a href="../#project-quiz">Квиз подбора</a></li><li><a href="../#prices">Стоимость</a></li><li><a href="../#faq">FAQ</a></li></ul></nav><nav class="footer-col" aria-label="Материалы"><h3>Материалы</h3><ul><li><a href="../cases/">Кейсы</a></li><li><a href="../comics/reverse-engineering-part2-egor.pdf">Комикс про реверс</a></li><li><a href="../comics/ai-version/reverse-engineering-part2-ai-illustrated.pdf">AI-версия комикса</a></li><li><a href="../sitemap.xml">Sitemap.xml</a></li></ul></nav><nav class="footer-col" aria-label="Контакты"><h3>Контакты</h3><ul><li><a href="../#brief">Оставить заявку</a></li><li><a href="https://t.me/step_3d_mngr" rel="noopener" target="_blank">Telegram-менеджер</a></li><li><a href="https://t.me/STEP_3D_Lab" rel="noopener" target="_blank">Канал Step3D</a></li><li><a href="mailto:stepgptai@gmail.com">stepgptai@gmail.com</a></li></ul></nav></div><div class="footer-bottom"><span>© Step3D · 3D-печать · моделирование · прототипирование</span><span>GitHub Pages · быстрый расчёт по фото, эскизу или STL/STEP</span></div></div></footer>
</body>
</html>'''

for rel, data in PAGES.items():
    # Keep canonical URLs aligned with sitemap.xml: directory pages should use the
    # clean trailing-slash URL, not /index.html, to avoid duplicate URL signals.
    data['canonical'] = rel[:-10] if rel.endswith('/index.html') else rel
    out = ROOT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_page(data), encoding='utf-8')

print('created', len(PAGES), 'pages')
