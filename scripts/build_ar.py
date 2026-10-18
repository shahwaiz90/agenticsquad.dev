import sys, json, re, html as H
# Builds ar/index.html from index.html: Arabic text, RTL styles, Arabic SEO tags.
# Run after editing index.html:  python3 scripts/build_ar.py index.html ar/index.html
# It fails loudly if an English string it translates has changed; update the pair here.
src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, (c, old[:120])
    s = s.replace(old, new)

URL = 'https://agenticsquad.dev/ar/'
TITLE = 'AgenticSquad.dev – فريق وكلاء ذكاء اصطناعي لـ Claude Code وCodex وGemini'
DESC = 'شغّل سكرم ماستر وقائدًا تقنيًا ومطوّرًا ومختبِر جودة كوكلاء ذكاء اصطناعي. يحوّل AgenticSquad.dev طلبًا واحدًا إلى بطاقات كانبان ويعرض كل تسليم مباشرة. مجاني ومحلي وبأمر npm واحد.'

# ---------- head ----------
rep('<html lang="en">', '<html lang="ar" dir="rtl">')
s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{DESC}">', s, count=1)
s = re.sub(r'<title>[^<]*</title>', f'<title>{TITLE}</title>', s, count=1)
rep('<link rel="canonical" href="https://agenticsquad.dev/">', f'<link rel="canonical" href="{URL}">')
s = re.sub(r'<meta property="og:(title|description)" content="[^"]*">', lambda m: f'<meta property="og:{m.group(1)}" content="{TITLE if m.group(1)=="title" else DESC}">', s)
s = re.sub(r'<meta name="twitter:(title|description)" content="[^"]*">', lambda m: f'<meta name="twitter:{m.group(1)}" content="{TITLE if m.group(1)=="title" else DESC}">', s)
rep('<meta property="og:url" content="https://agenticsquad.dev/">', f'<meta property="og:url" content="{URL}">')
rep('<meta property="og:locale" content="en_US">', '<meta property="og:locale" content="ar_AR">\n<meta property="og:locale:alternate" content="en_US">')
rep("page_title: 'AgenticSquad.dev landing'", "page_title: 'AgenticSquad.dev landing (ar)'")
# fonts
rep('family=JetBrains+Mono:wght@400;500&display=swap', 'family=JetBrains+Mono:wght@400;500&family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap')

FAQ = [
 ("ما هو AgenticSquad.dev؟",
  "يمنح AgenticSquad.dev مساعد البرمجة بالذكاء الاصطناعي فريقًا كاملًا: سكرم ماستر، ومعه قائد تقني ومطوّر ومختبِر جودة لكل منصة (الويب وأندرويد وiOS). تتحدث إلى السكرم ماستر فيضع العمل على لوحة كانبان على شكل بطاقات، ويتولى بقية الوكلاء البطاقات وينجزونها. وتعرض بوابة محلية كل تسليم مباشرة على مخطط مكتب وعلى اللوحة."),
 ("كيف أثبّته؟",
  "تحتاج إلى Node.js. افتح الطرفية، وانتقل إلى مجلد مشروعك باستخدام <code>cd</code>، ثم شغّل <code>npx agenticsquad</code>. لا حاجة إلى تثبيت أي شيء على مستوى النظام، ويستغرق الأمر أقل من 5 ثوانٍ. تفتح البوابة في متصفحك وتكتشف وكلاءك، أو تساعدك على اختيار فريق للويب أو أندرويد أو iOS."),
 ("ما أدوات البرمجة بالذكاء الاصطناعي التي يعمل معها؟",
  "Claude Code وOpenAI Codex وGoogle Gemini وAntigravity وOpenCode، بما في ذلك النماذج المحلية عبر OpenCode. تعرّف الفريق مرة واحدة، ثم يكتبه الأمر <code>npx -p agenticsquad agents sync</code> في ملفات CLAUDE.md وAGENTS.md وGEMINI.md وملفات الوكلاء الخاصة بكل أداة."),
 ("هل تغادر شيفرتي جهازي؟",
  "لا. تعمل البوابة على 127.0.0.1 وتقرأ سجل جلسات كل أداة من قرصك. لا تُرسَل الشيفرة ولا مسارات الملفات ولا نصوص البطاقات ولا الرموز (tokens) إلى أي مكان. ترسل البوابة إحصاءات استخدام مجهولة الهوية، ويمكنك إيقافها من الإعدادات أو بتشغيلها مع <code>VO_ANALYTICS=off</code>."),
 ("هل هو مجاني؟",
  "نعم. AgenticSquad.dev مجاني ومرخّص برخصة MIT."),
 ("هل يمكنني تعديل الوكلاء ومهاراتهم وقواعدهم؟",
  "نعم. عدّلهم من Team Studio داخل البوابة، أو عدّل ملفات Markdown في <code>.agents/definitions/</code> مباشرة. يمكنك تحديد الأدوار والأسماء والأدوات المسموح بها والمهارات والقواعد والصور الرمزية، ثم تشغيل <code>npx -p agenticsquad agents sync</code>."),
 ("ما الفرق بين التغييرات الصغيرة والكبيرة؟",
  "يقدّر السكرم ماستر حجم كل طلب. التغيير الصغير (من ملف إلى ثلاثة ملفات، دون تغيير نوع مشترك أو واجهة API أو بيانات مخزّنة) يذهب مباشرة إلى مطوّر المنصة، ويراجعه القائد التقني. أما التغيير الأكبر فيذهب إلى القائد التقني، الذي يكتب عقودًا تقنية للمطوّر ويسلّم الاختبار لمختبِر الجودة."),
 ("هل يمكنني تشغيله على منفذ آخر أو لمجلد آخر؟",
  "نعم. استخدم <code>npx agenticsquad --port 3001</code> لمنفذ آخر، أو <code>npx agenticsquad --dir /path/to/project</code> لمتابعة مشروع مختلف. ويمكن تشغيل عدة مشاريع معًا على منافذ مختلفة."),
]
strip = lambda t: H.unescape(re.sub(r'<[^>]+>', '', t))
# JSON-LD: replace FAQ and app description
m = re.search(r'<script type="application/ld\+json">(\{"@context": "https://schema.org", "@type": "FAQPage".*?)</script>', s)
faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": "ar",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in FAQ]}
s = s.replace(m.group(1), json.dumps(faq_ld, ensure_ascii=False))
m = re.search(r'<script type="application/ld\+json">(\[.*?\])</script>', s)
ld = json.loads(m.group(1))
ld[0]['description'] = DESC; ld[0]['url'] = URL; ld[0]['inLanguage'] = 'ar'
ld[1]['url'] = URL; ld[1]['inLanguage'] = 'ar'
s = s.replace(m.group(1), json.dumps(ld, ensure_ascii=False))

# ---------- RTL / Arabic typography ----------
RTL_CSS = '''
/* Arabic: font, no tight tracking, right-to-left fixes. The portal replay, code and the sync diagram stay left-to-right. */
:root { --f-display: "IBM Plex Sans Arabic", "Bricolage Grotesque", system-ui, sans-serif; --f-body: "IBM Plex Sans Arabic", "Instrument Sans", system-ui, sans-serif; }
h1, h2, h3, .hero h1, .eyebrow { letter-spacing: 0; }
.hero h1 { line-height: 1.2; font-size: clamp(2.4rem, 6vw, 4.8rem); }
.hero h1 .lit { white-space: normal; }
.diff, .diff-h, .diff-body, .bar-row span:first-child { direction: ltr; text-align: left; }
.step .s-w, .msg small, .rp small, .meter .st, .view-foot, .panel-h, .tour-banner, .rp-bar .tag { font-family: var(--f-body); letter-spacing: 0; }
h2 { line-height: 1.25; }
.eyebrow { font-family: var(--f-body); font-weight: 600; font-size: .85rem; }
code, pre, .cmd, .term, .stage, .sync, .diff-body, .num-cell b { direction: ltr; unicode-bidi: isolate; }
.stage, .term, .sync { text-align: left; }
.sync h3 { text-align: right; direction: rtl; }
[dir="rtl"] .step .bar { transform-origin: right; }
[dir="rtl"] .bar-row .fl { transform-origin: right; }
'''
rep('</style>', RTL_CSS + '</style>', 1) if s.count('</style>') == 1 else None
if RTL_CSS not in s:
    i = s.index('</style>'); s = s[:i] + RTL_CSS + s[i:]

# ---------- body text ----------
T = [
 ('<nav class="nav" aria-label="Page">', '<nav class="nav" aria-label="الصفحة">'),
 ('<a href="#flow">How it works</a>', '<a href="#flow">كيف يعمل</a>'),
 ('<a href="#views">What you see</a>', '<a href="#views">ما الذي تراه</a>'),
 ('<a href="#tools">Any AI tool</a>', '<a href="#tools">أي أداة ذكاء اصطناعي</a>'),
 ('<a href="#build">Progress</a>', '<a href="#build">التقدّم</a>'),
 ('<a href="#start">Get started</a>', '<a href="#start">ابدأ الآن</a>'),
 ('<a href="#faq">FAQ</a>', '<a href="#faq">الأسئلة الشائعة</a>'),
 ('<a class="lang" href="/ar/" hreflang="ar" lang="ar">العربية</a>', '<a class="lang" href="/" hreflang="en" lang="en">English</a>'),
 ('aria-label="Switch to dark theme"', 'aria-label="التبديل إلى الوضع الداكن"'),
 ('<h1>Talk to one routine. The team <span class="lit">finishes&nbsp;it.</span></h1>', '<h1>تحدّث إلى وكيل واحد. <span class="lit">والفريق يُنجز&nbsp;العمل.</span></h1>'),
 ('<p class="lede">You describe the work once, to the Scrum Master. It sizes the request and puts it on a Kanban board as cards. The Tech Lead, Developer and QA pick those cards up and finish them, and you watch each handoff in a live office and on the board.</p>',
  '<p class="lede">تصف العمل مرة واحدة للسكرم ماستر، فيقدّر حجم الطلب ويضعه على لوحة كانبان على شكل بطاقات. يتولى القائد التقني والمطوّر ومختبِر الجودة هذه البطاقات وينجزونها، وتتابع أنت كل تسليم في مكتب حيّ وعلى اللوحة.</p>'),
 ('See a request move <span aria-hidden="true">→</span>', 'شاهد مسار الطلب <span aria-hidden="true">←</span>'),
 ('aria-label="Copy the install command"', 'aria-label="نسخ أمر التثبيت"', 2),
 ('<span class="copy">copy</span>', '<span class="copy">نسخ</span>'),
 ('<span class="copy" style="border:0;padding:0">copy</span>', '<span class="copy" style="border:0;padding:0">نسخ</span>'),
 ('<p class="cmd-hint">First <code>cd</code> into your project folder, then run <code>npx agenticsquad</code>. Setup takes under 5 seconds.</p>',
  '<p class="cmd-hint">انتقل أولًا إلى مجلد مشروعك باستخدام <code>cd</code>، ثم شغّل <code>npx agenticsquad</code>. يستغرق الإعداد أقل من 5 ثوانٍ.</p>'),
 ('aria-label="Animated replay of the AgenticSquad.dev portal: four agents at desks walk over to hand cards to each other while a Kanban board and activity log update."',
  'aria-label="إعادة عرض متحركة لبوابة AgenticSquad.dev: أربعة وكلاء على مكاتبهم يتنقلون لتسليم البطاقات لبعضهم بينما تتحدّث لوحة كانبان وسجل النشاط."'),
 ('<span>Replay of a typical run, shortened</span>', '<span dir="rtl">إعادة عرض مختصرة لتشغيل نموذجي</span>'),
 ('<div class="eyebrow">Why</div>', '<div class="eyebrow">لماذا</div>'),
 ('<p class="big">You should not have to run a team of agents by hand. <em>Talk to one routine and the team finishes the task.</em></p>',
  '<p class="big">لا ينبغي أن تدير فريقًا من الوكلاء يدويًا. <em>تحدّث إلى وكيل واحد، والفريق يُنجز المهمة.</em></p>'),
 ("<p class=\"lede\">Your session hands the request to the Scrum Master and only dispatches from there. It picks the platform team (Web, Android or iOS). A small change goes straight to that team's Developer with its Tech Lead reviewing; a bigger one goes to the Tech Lead, who writes the contract and brings in QA. Instructions, decisions and results live on the cards, so no one works from a pasted prompt.</p>",
  '<p class="lede">تسلّم جلستك الطلب إلى السكرم ماستر، ومن بعدها تكتفي بتوزيع العمل. يختار السكرم ماستر فريق المنصة (الويب أو أندرويد أو iOS). التغيير الصغير يذهب مباشرة إلى مطوّر ذلك الفريق ويراجعه قائده التقني، والتغيير الأكبر يذهب إلى القائد التقني الذي يكتب العقد ويُشرك مختبِر الجودة. التعليمات والقرارات والنتائج كلها على البطاقات، فلا أحد يعمل من موجّه منسوخ ولصق.</p>'),
 ('<p class="lede">Usually all of that is a scrolling terminal. AgenticSquad.dev reads the sessions your tools already record and shows who is working, on which card, what they handed off and why.</p>',
  '<p class="lede">عادةً يضيع كل ذلك في طرفية تتمرّر بلا توقف. يقرأ AgenticSquad.dev الجلسات التي تسجّلها أدواتك أصلًا، ويعرض من يعمل، وعلى أي بطاقة، وماذا سلّم ولماذا.</p>'),
 ('<div class="eyebrow">How one request moves</div>', '<div class="eyebrow">مسار الطلب الواحد</div>'),
 ('<h2>How the AI agent team turns a sentence into a finished card.</h2>', '<h2>كيف يحوّل فريق وكلاء الذكاء الاصطناعي جملة واحدة إلى بطاقة منجزة.</h2>'),
 ('aria-label="Stages of a request"', 'aria-label="مراحل الطلب"'),
 ('<div class="eyebrow">Small change? Fast path.</div>', '<div class="eyebrow">تغيير صغير؟ المسار السريع.</div>'),
 ("<p>When the Scrum Master sizes a request as small (one to three files, no change to a shared type, API, payload or stored data), it skips the contract. One card goes straight to the platform's Developer (<code>web-dev</code>, <code>android-dev</code> or <code>ios-dev</code>), who maps the impact first, and that platform's Tech Lead reviews it.</p>",
  '<p>عندما يقدّر السكرم ماستر أن الطلب صغير (من ملف إلى ثلاثة ملفات، دون تغيير نوع مشترك أو واجهة API أو حمولة أو بيانات مخزّنة)، يتجاوز مرحلة العقد. تذهب بطاقة واحدة مباشرة إلى مطوّر المنصة (<code>web-dev</code> أو <code>android-dev</code> أو <code>ios-dev</code>)، الذي يحدّد نطاق التأثير أولًا، ثم يراجعها القائد التقني لتلك المنصة.</p>'),
 ('aria-label="Fast path: you, Scrum Master, Developer, then Tech Lead review"', 'aria-label="المسار السريع: أنت، ثم السكرم ماستر، ثم المطوّر، ثم مراجعة القائد التقني"'),
 ('<span class="hop"><span class="you">you</span>You</span>', '<span class="hop"><span class="you">أنت</span>أنت</span>'),
 ('<span class="arr" aria-hidden="true">→</span>', '<span class="arr" aria-hidden="true">←</span>', 3),
 ('src="/img/projectmanager.webp">Scrum Master</span>', 'src="/img/projectmanager.webp">السكرم ماستر</span>'),
 ('src="/img/developer.webp">Developer</span>', 'src="/img/developer.webp">المطوّر</span>'),
 ('src="/img/techlead.webp">Tech Lead reviews</span>', 'src="/img/techlead.webp">مراجعة القائد التقني</span>'),
 ('<div class="eyebrow">What you see</div>', '<div class="eyebrow">ما الذي تراه</div>'),
 ('<h2>Every angle on your AI agents&#39; work, all from real sessions.</h2>', '<h2>كل زاوية من عمل وكلائك، وكلها من جلسات حقيقية.</h2>'),
 ('<p class="lede">Next to the floor plan and the board, the portal shows the conversation between agents, the tools they used, the code they changed and the time and tokens each role spent. A finished requirement can be replayed on the floor plan, and first-time users can watch a short demo.</p>',
  '<p class="lede">إلى جانب مخطط المكتب واللوحة، تعرض البوابة المحادثة بين الوكلاء، والأدوات التي استخدموها، والشيفرة التي غيّروها، والوقت والرموز (tokens) التي استهلكها كل دور. ويمكن إعادة عرض أي متطلب منجز على مخطط المكتب، كما يمكن للمستخدمين الجدد مشاهدة عرض توضيحي قصير.</p>'),
 ('<h3>Handoff stream</h3><p>Every delegation with the exact brief that was passed, so you can see why a task moved.</p>', '<h3>سجل التسليمات</h3><p>كل تفويض مع الموجز الدقيق الذي مُرّر، لتعرف لماذا انتقلت المهمة.</p>'),
 ('<div class="view-foot">Example conversation</div>', '<div class="view-foot">محادثة توضيحية</div>'),
 ('<h3>Tool analytics</h3><p>Which tools each agent reached for: terminal commands, MCP tools, handbacks and file writes, counted per call.</p>', '<h3>تحليلات الأدوات</h3><p>الأدوات التي استخدمها كل وكيل: أوامر الطرفية وأدوات MCP والتسليمات الراجعة وكتابة الملفات، محسوبة لكل استدعاء.</p>'),
 ('<div class="view-foot">Tool calls the portal recorded, all agents, measured 17 Oct 2026. Shell commands logged by name (cd, curl, ls…) are counted as Bash; every <code>mcp__</code> tool is counted as MCP; write_to_file as Write.</div>',
  '<div class="view-foot">استدعاءات الأدوات التي سجّلتها البوابة لجميع الوكلاء، قيست في 17 أكتوبر 2026. أوامر الطرفية المسجّلة بأسمائها (cd وcurl وls…) تُحسب ضمن Bash، وكل أداة <code>mcp__</code> تُحسب ضمن MCP، وwrite_to_file ضمن Write.</div>'),
 ('<h3>Code change inspector</h3><p>The diff each agent produced, filed under the card and the role that made it.</p>', '<h3>مستعرض تغييرات الشيفرة</h3><p>الفروق التي أنتجها كل وكيل، مصنّفة تحت البطاقة والدور الذي أجراها.</p>'),
 ('<div class="view-foot">Example diff · web-dev · VO-43</div>', '<div class="view-foot">فروق توضيحية · web-dev · VO-43</div>'),
 ('<h3>Time and tokens</h3><p>Work time is logged per role while it is active, with the token usage your tools recorded.</p>', '<h3>الوقت والرموز</h3><p>يُسجَّل وقت العمل لكل دور أثناء نشاطه، مع استهلاك الرموز (tokens) الذي سجّلته أدواتك.</p>'),
 ('<div class="view-foot">Example figures, counting up</div>', '<div class="view-foot">أرقام توضيحية تتزايد</div>'),
 ('<h3>Replay a requirement</h3><p>A Replay button on a finished requirement plays its handoffs on the floor plan, with decisions, reviews and results as captions. Save as video keeps a recording. Nothing is written to the board.</p>',
  '<h3>إعادة عرض متطلب</h3><p>زر Replay على أي متطلب منجز يعيد عرض تسليماته على مخطط المكتب، مع القرارات والمراجعات والنتائج كتعليقات. وزر Save as video يحفظ تسجيلًا. لا يُكتب أي شيء على اللوحة.</p>'),
 ('<div class="view-foot">Example timeline · VO-41</div>', '<div class="view-foot">خط زمني توضيحي · VO-41</div>'),
 ('<h3>Watch demo</h3><p>New to the office? A Watch demo button on the floor plan walks a scripted request through your own team, from the Scrum Master to the people who build and test it and back. It runs in the browser and saves nothing.</p>',
  '<h3>عرض توضيحي</h3><p>جديد على المكتب؟ زر Watch demo على مخطط المكتب يمرّر طلبًا مُعدًّا مسبقًا عبر فريقك أنت، من السكرم ماستر إلى من يبنيه ويختبره ثم العودة. يعمل في المتصفح ولا يحفظ شيئًا.</p>'),
 ('<div class="view-foot">Built from the roster you saved in Team Studio</div>', '<div class="view-foot">مبني من قائمة الفريق التي حفظتها في Team Studio</div>'),
 ('<div class="eyebrow">Works with your AI tool</div>', '<div class="eyebrow">يعمل مع أداة الذكاء الاصطناعي لديك</div>'),
 ('<h2>Define the agent team once. Claude Code, Codex, Gemini and OpenCode get the same roles.</h2>', '<h2>عرّف فريق الوكلاء مرة واحدة، فتحصل Claude Code وCodex وGemini وOpenCode على الأدوار نفسها.</h2>'),
 ('<p class="lede">Roles, skills and rules live as plain Markdown and YAML in your repository, and Team Studio in the portal edits the same files. One command writes them out in the format each AI tool reads, including the rule that the main session only dispatches, so nothing drifts between tools.</p>',
  '<p class="lede">الأدوار والمهارات والقواعد محفوظة كملفات Markdown وYAML عادية في مستودعك، وTeam Studio في البوابة يعدّل الملفات نفسها. أمر واحد يكتبها بالصيغة التي تقرؤها كل أداة ذكاء اصطناعي، بما في ذلك قاعدة أن الجلسة الرئيسية توزّع العمل فقط، فلا يحدث أي اختلاف بين الأدوات.</p>'),
 ('<h3>Your team, in the repo</h3>', '<h3>فريقك داخل المستودع</h3>'),
 ('<div class="reads"><span>Activity is read from</span><span class="chip">Claude Code transcripts</span><span class="chip">OpenCode database</span><span class="chip">Antigravity sessions</span><span>Nothing to install in the agent tool.</span></div>',
  '<div class="reads"><span>يُقرأ النشاط من</span><span class="chip">سجلات Claude Code</span><span class="chip">قاعدة بيانات OpenCode</span><span class="chip">جلسات Antigravity</span><span>لا حاجة إلى تثبيت أي شيء في أداة الوكلاء.</span></div>'),
 ('<div class="eyebrow">Safe to run on a work laptop</div>', '<div class="eyebrow">آمن للتشغيل على حاسوب العمل</div>'),
 ('<h2>It stays on your machine and shows only what really happened.</h2>', '<h2>يبقى على جهازك، ولا يعرض إلا ما حدث فعلًا.</h2>'),
 ('<h3>Local only</h3>', '<h3>محلي فقط</h3>'),
 ('<p>The server listens on 127.0.0.1 and refuses requests from other websites, so a page you visit cannot read your board.</p>', '<p>يستمع الخادم على 127.0.0.1 ويرفض الطلبات القادمة من مواقع أخرى، فلا تستطيع أي صفحة تزورها قراءة لوحتك.</p>'),
 ('<h3>Tokens stay private</h3>', '<h3>الرموز تبقى خاصة</h3>'),
 ('<p>Jira and Confluence tokens are saved to a gitignored file readable only by you. The portal never displays them.</p>', '<p>تُحفظ رموز Jira وConfluence في ملف مستثنى من git لا يقرؤه أحد سواك، ولا تعرضها البوابة أبدًا.</p>'),
 ('<h3>No made-up numbers</h3>', '<h3>لا أرقام مختلَقة</h3>'),
 ('<p>There is no mock data. Every card, handoff and token count comes from a real session, and 33 test suites guard it in CI. The Watch demo is labelled as a simulation and never touches your board.</p>', '<p>لا توجد بيانات وهمية. كل بطاقة وتسليم وعدد رموز يأتي من جلسة حقيقية، وتحميه 33 مجموعة اختبارات في CI. والعرض التوضيحي موسوم بأنه محاكاة ولا يلمس لوحتك أبدًا.</p>'),
 ('<h3>Changes go through the team</h3>', '<h3>التغييرات تمرّ عبر الفريق</h3>'),
 ('<p>The session you type into only dispatches work. In Claude Code a hook stops it from editing files, so every change, even a one-line fix, goes to the Scrum Master and gets reviewed.</p>', '<p>الجلسة التي تكتب فيها توزّع العمل فقط. في Claude Code يمنعها خطّاف (hook) من تعديل الملفات، فيذهب كل تغيير، حتى إصلاح من سطر واحد، إلى السكرم ماستر ويخضع للمراجعة.</p>'),
 ('<div class="eyebrow">Progress so far</div>', '<div class="eyebrow">التقدّم حتى الآن</div>'),
 ('<h2>Built in four days, shipped as an npm package.</h2>', '<h2>بُني في أربعة أيام، ونُشر كحزمة npm.</h2>'),
 ('<span>days, first commit to today</span>', '<span>أيام من أول commit حتى اليوم</span>'),
 ('<span>commits</span>', '<span>commit</span>'),
 ('<span>pull requests merged</span>', '<span>طلب دمج مدموج</span>'),
 ('<span>skills in the catalog</span>', '<span>مهارة في الكتالوج</span>'),
 ('<span>test suites in CI</span>', '<span>مجموعة اختبارات في CI</span>'),
 ('<span>AI tools supported</span>', '<span>أدوات ذكاء اصطناعي مدعومة</span>'),
 ('<b>14 Oct</b><span><strong>The office opens.</strong> Agent discovery from any folder format, a role-to-role task board, cross-platform support.</span>', '<b>14 أكتوبر</b><span><strong>المكتب يفتح أبوابه.</strong> اكتشاف الوكلاء من أي صيغة مجلدات، ولوحة مهام بين الأدوار، ودعم متعدد المنصات.</span>'),
 ('<b>15 Oct</b><span><strong>Seeing the work.</strong> Workflow screen and video recorder, agent-to-agent prompts captured, file changes tab.</span>', '<b>15 أكتوبر</b><span><strong>رؤية العمل.</strong> شاشة سير العمل ومسجّل الفيديو، والتقاط الموجّهات بين الوكلاء، وتبويب تغييرات الملفات.</span>'),
 ('<b>16 Oct</b><span><strong>One team file.</strong> Universal agent registry, multi-project isolation, project launcher.</span>', '<b>16 أكتوبر</b><span><strong>ملف فريق واحد.</strong> سجل وكلاء موحّد، وعزل بين المشاريع المتعددة، ومشغّل المشاريع.</span>'),
 ('<b>17 Oct</b><span><strong>Ready to share.</strong> Local-only security, Integrations panel, token usage on desks and cards, OpenCode support, v1.2.1.</span>', '<b>17 أكتوبر</b><span><strong>جاهز للمشاركة.</strong> أمان محلي فقط، ولوحة التكاملات، واستهلاك الرموز على المكاتب والبطاقات، ودعم OpenCode، والإصدار v1.2.1.</span>'),
 ("<b>17 Oct</b><span><strong>A team that works like one.</strong> Agents walk to each other's desks on handoffs, a fast path for small tasks, a QA role and Team Studio, Watch demo, a main session that only dispatches, and Replay with Save as video.</span>", '<b>17 أكتوبر</b><span><strong>فريق يعمل كفريق.</strong> الوكلاء يمشون إلى مكاتب بعضهم عند التسليم، ومسار سريع للمهام الصغيرة، ودور مختبِر الجودة وTeam Studio، والعرض التوضيحي، وجلسة رئيسية توزّع العمل فقط، وإعادة العرض مع الحفظ كفيديو.</span>'),
 ('<b>18 Oct</b><span><strong>Leaner and measurable.</strong> Anonymous usage statistics with an opt-out, leaner board calls with about 46% fewer tokens per role, faster agent verification rules, v1.3.0.</span>', '<b>18 أكتوبر</b><span><strong>أخفّ وقابل للقياس.</strong> إحصاءات استخدام مجهولة الهوية مع إمكانية الإيقاف، واستدعاءات أخفّ للوحة بنحو 46% رموز أقل لكل دور، وقواعد تحقق أسرع للوكلاء، والإصدار v1.3.0.</span>'),
 ('<p class="src">Counted from main at 7b64e94 (pull request #23) on 17 Oct 2026, 17:30: commits from git log, merged pull requests, SKILL.md files in .agents/skills, suites in npm test, tool adapters in server/adapters.</p>', '<p class="src">محسوبة من الفرع main عند 7b64e94 (طلب الدمج رقم 23) في 17 أكتوبر 2026 الساعة 17:30: الـ commits من git log، وطلبات الدمج المدموجة، وملفات SKILL.md في .agents/skills، ومجموعات npm test، ومحوّلات الأدوات في server/adapters.</p>'),
 ('<div class="eyebrow">Get started</div>', '<div class="eyebrow">ابدأ الآن</div>'),
 ('<h2 style="margin-top:14px">Install the agent team with one command.</h2>', '<h2 style="margin-top:14px">ثبّت فريق الوكلاء بأمر واحد.</h2>'),
 ('<li><span class="i">1</span><p><strong>Open your project folder</strong> in a terminal. New or existing, any stack.</p></li>', '<li><span class="i">1</span><p><strong>افتح مجلد مشروعك</strong> في الطرفية. جديد أو قائم، وبأي تقنية.</p></li>'),
 ('<li><span class="i">2</span><p><strong>Run the command</strong> from inside that folder: <code>cd your-project</code>, then <code>npx agenticsquad</code>. It takes under 5 seconds. The portal finds your agents, or helps you pick an Android, iOS or Web team (Scrum Master, Tech Lead, Developer and QA), or all three with the Scrum Master routing by platform, that you can adjust in Team Studio.</p></li>',
  '<li><span class="i">2</span><p><strong>شغّل الأمر</strong> من داخل ذلك المجلد: <code>cd your-project</code>، ثم <code>npx agenticsquad</code>. يستغرق أقل من 5 ثوانٍ. تكتشف البوابة وكلاءك، أو تساعدك على اختيار فريق لأندرويد أو iOS أو الويب (سكرم ماستر وقائد تقني ومطوّر ومختبِر جودة)، أو الفرق الثلاثة معًا مع توجيه السكرم ماستر حسب المنصة، ويمكنك تعديلها في Team Studio.</p></li>'),
 ('<li><span class="i">3</span><p><strong>Ask as usual</strong> in Claude Code, Codex, Gemini or OpenCode. Your session hands the request to the Scrum Master, and the office fills in as your agents work.</p></li>', '<li><span class="i">3</span><p><strong>اطلب كالمعتاد</strong> في Claude Code أو Codex أو Gemini أو OpenCode. تسلّم جلستك الطلب إلى السكرم ماستر، ويمتلئ المكتب بالحركة بينما يعمل وكلاؤك.</p></li>'),
 ('<div class="eyebrow">FAQ</div>', '<div class="eyebrow">الأسئلة الشائعة</div>'),
 ('<h2>Questions about the AI agent team.</h2>', '<h2>أسئلة عن فريق وكلاء الذكاء الاصطناعي.</h2>'),
 ('<p class="lede">New to it? Read the <a href="/claude-code-multi-agent-team/">guide to running a multi-agent team in Claude Code</a>.</p>', '<p class="lede">جديد عليه؟ اقرأ <a href="/claude-code-multi-agent-team/" hreflang="en">دليل تشغيل فريق متعدد الوكلاء في Claude Code</a> (بالإنجليزية).</p>'),
 ('<span>AgenticSquad.dev · MIT licence · by <a', '<span>AgenticSquad.dev · رخصة MIT · من إعداد <a'),
 ('>Syed Ahmad Shahwaiz</a></span>', '>سيد أحمد شهويز</a></span>'),
 ('<span><a href="/sitemap/">Sitemap</a> · <a href="/llms.txt">llms.txt</a></span>', '<span><a href="/sitemap/">خريطة الموقع</a> · <a href="/llms.txt">llms.txt</a></span>'),
 # script strings
 ("say('Copied: ' + txt)", "say('تم النسخ: ' + txt)"),
 ("say('Select and copy: ' + txt)", "say('حدّد وانسخ: ' + txt)"),
 ("isDark() ? 'Switch to light theme' : 'Switch to dark theme'", "isDark() ? 'التبديل إلى الوضع الفاتح' : 'التبديل إلى الوضع الداكن'"),
 ("{ t: 'Request', who: 'you', w: 'You', body: 'You describe the goal in plain words, in whichever AI tool you already use. That session only dispatches: it passes the request to the Scrum Master and starts each next role from the HANDOFF lines they return. In Claude Code a hook stops it from editing files itself.',",
  "{ t: 'الطلب', who: 'you', w: 'أنت', body: 'تصف الهدف بكلمات بسيطة، في أي أداة ذكاء اصطناعي تستخدمها أصلًا. تلك الجلسة توزّع العمل فقط: تمرّر الطلب إلى السكرم ماستر وتشغّل كل دور تالٍ من أسطر HANDOFF التي يعيدها. وفي Claude Code يمنعها خطّاف (hook) من تعديل الملفات بنفسها.',"),
 ("{ t: 'Plan', who: 'tech-pm', w: 'Scrum Master', body: 'The Scrum Master sizes the request with a quick look and posts the size on the requirement. A small change takes the fast path below. Anything bigger becomes a card for the Tech Lead with a brief, acceptance criteria and context. It never writes application code.',",
  "{ t: 'التخطيط', who: 'tech-pm', w: 'السكرم ماستر', body: 'يقدّر السكرم ماستر حجم الطلب بنظرة سريعة ويسجّل الحجم على المتطلب. التغيير الصغير يسلك المسار السريع أدناه، وأي شيء أكبر يصبح بطاقة للقائد التقني مع موجز ومعايير قبول وسياق. ولا يكتب السكرم ماستر شيفرة التطبيق أبدًا.',"),
 ("{ t: 'Contract', who: 'web-tech-lead', w: 'Tech Lead', body: 'The Tech Lead writes a short contract for the Developer, about 40 lines at most. It starts with an impact map: the files to change, the files affected, the files checked and left alone, and the risks. When a change needs real testing, it also opens a card for QA.',",
  "{ t: 'العقد', who: 'web-tech-lead', w: 'القائد التقني', body: 'يكتب القائد التقني عقدًا قصيرًا للمطوّر، في حدود 40 سطرًا. يبدأ بخريطة التأثير: الملفات التي ستتغير، والملفات المتأثرة، والملفات التي فُحصت وتُركت كما هي، والمخاطر. وعندما يحتاج التغيير إلى اختبار حقيقي، يفتح أيضًا بطاقة لمختبِر الجودة.',"),
 ("{ t: 'Build', who: 'web-dev', w: 'Developer', body: 'The Developer implements one card at a time, checks every acceptance criterion, writes the result and deliverable on the card and moves it to review.',",
  "{ t: 'البناء', who: 'web-dev', w: 'المطوّر', body: 'ينفّذ المطوّر بطاقة واحدة في كل مرة، ويتحقق من كل معيار قبول، ويكتب النتيجة والمُخرَج على البطاقة وينقلها إلى المراجعة.',"),
 ("{ t: 'Test and review', who: 'web-tech-lead', w: 'QA · Tech Lead', body: 'QA tests the change against the criteria and records pass or fail for each one. The Tech Lead reviews against the contract. When every task is done, the requirement closes itself and a summary goes on its thread.',",
  "{ t: 'الاختبار والمراجعة', who: 'web-tech-lead', w: 'مختبِر الجودة · القائد التقني', body: 'يختبر مختبِر الجودة التغيير وفق المعايير ويسجّل النجاح أو الإخفاق لكل منها، ويراجع القائد التقني العمل وفق العقد. وعندما تكتمل كل المهام، يُغلق المتطلب نفسه ويُضاف ملخص إلى سجله.',"),
 ("s.who === 'you' ? '<span class=\"you\">you</span>'", "s.who === 'you' ? '<span class=\"you\">أنت</span>'"),
 ("['tech-pm', 'Scrum Master → Tech Lead', 'Sized as full: it adds an API route. Please write the contract for <span class=\"hk\">VO-42</span>. Titles with commas must survive the export.', false],",
  "['tech-pm', 'السكرم ماستر ← القائد التقني', 'الحجم كبير: يضيف مسار API جديدًا. اكتب العقد من فضلك لـ <span class=\"hk\">VO-42</span>. يجب أن تبقى العناوين التي تحتوي على فواصل سليمة عند التصدير.', false],"),
 ("['web-tech-lead', 'Tech Lead → Developer', 'Impact map and contract are on <span class=\"hk\">VO-43</span>: two files, three checks. QA tests it after you.', true],",
  "['web-tech-lead', 'القائد التقني ← المطوّر', 'خريطة التأثير والعقد على <span class=\"hk\">VO-43</span>: ملفان وثلاثة فحوص. ويختبره مختبِر الجودة بعدك.', true],"),
 ("['web-dev', 'Developer → Tech Lead', 'Done. All 33 suites pass and every criterion is checked on the card. Moved to review.', false],",
  "['web-dev', 'المطوّر ← القائد التقني', 'تم. نجحت المجموعات الـ 33 كلها، وكل معيار محقَّق على البطاقة. نُقلت إلى المراجعة.', false],"),
 ("['tech-pm', 'handoff · Scrum Master → Tech Lead', 'VO-42 Contract for CSV export'],", "['tech-pm', 'تسليم · السكرم ماستر ← القائد التقني', 'VO-42 عقد تصدير CSV'],"),
 ("['web-tech-lead', 'decision', 'Escape quotes on the server, not in the browser'],", "['web-tech-lead', 'قرار', 'معالجة علامات الاقتباس على الخادم، لا في المتصفح'],"),
 ("['web-dev', 'result', 'VO-43 built, 33 suites pass'],", "['web-dev', 'نتيجة', 'VO-43 بُنيت، ونجحت 33 مجموعة اختبارات'],"),
 ("['web-tester', 'review · QA', 'VO-44 3/3 criteria pass'],", "['web-tester', 'مراجعة · مختبِر الجودة', 'VO-44 نجاح 3 من 3 معايير'],"),
 ("['web-tech-lead', 'review · Tech Lead', 'VO-43 approved, VO-41 done'],", "['web-tech-lead', 'مراجعة · القائد التقني', 'VO-43 معتمدة، وVO-41 منجزة'],"),
 ("['tech-pm', 'Scrum Master → Tech Lead', 'The Scrum Master hands the request to the Tech Lead.'],", "['tech-pm', 'السكرم ماستر ← القائد التقني', 'يسلّم السكرم ماستر الطلب إلى القائد التقني.'],"),
 ("['web-tech-lead', 'Tech Lead → Developer', 'The Tech Lead hands the build to the Developer.'],", "['web-tech-lead', 'القائد التقني ← المطوّر', 'يسلّم القائد التقني البناء إلى المطوّر.'],"),
 ("['web-dev', 'Developer → Tech Lead', 'The Developer builds it and hands it back for review.'],", "['web-dev', 'المطوّر ← القائد التقني', 'يبنيه المطوّر ويعيده للمراجعة.'],"),
 ("['web-tester', 'QA → Tech Lead', 'QA tests it and reports the results back.'],", "['web-tester', 'مختبِر الجودة ← القائد التقني', 'يختبره مختبِر الجودة ويُبلغ بالنتائج.'],"),
 ("['web-tech-lead', 'Tech Lead → Scrum Master', 'The Tech Lead reports back to the Scrum Master.'],", "['web-tech-lead', 'القائد التقني ← السكرم ماستر', 'يرفع القائد التقني التقرير إلى السكرم ماستر.'],"),
 ("<span class=\"tag\">▶ Replay</span>", "<span class=\"tag\">▶ إعادة العرض</span>"),
 ("<span class=\"tag\">Save as video</span>", "<span class=\"tag\">حفظ كفيديو</span>"),
 ("<b>Demo</b> · Simulated walkthrough. Nothing is saved to your board.", "<b>عرض توضيحي</b> · جولة محاكاة. لا يُحفظ أي شيء على لوحتك."),
 ("['tech-pm', 'sizing, 2 cards',", "['tech-pm', 'تقدير الحجم، بطاقتان',"),
 ("['web-tech-lead', 'contract + review',", "['web-tech-lead', 'العقد + المراجعة',"),
 ("['web-dev', 'building VO-43',", "['web-dev', 'بناء VO-43',"),
 ("['web-tester', 'testing VO-44',", "['web-tester', 'اختبار VO-44',"),
 ("aria-label=\"Commits per day: ${DAYS.map(([d, v]) => v + ' on ' + d).join(', ')}\"", "aria-label=\"عدد الـ commits يوميًا: ${DAYS.map(([d, v]) => v + ' في ' + d).join('، ')}\""),
 ("const DAYS = [['14 Oct', 14], ['15 Oct', 4], ['16 Oct', 10], ['17 Oct', 71]];", "const DAYS = [['14 أكتوبر', 14], ['15 أكتوبر', 4], ['16 أكتوبر', 10], ['17 أكتوبر', 71]];"),
]
for t in T:
    old, new = t[0], t[1]; n = t[2] if len(t) > 2 else 1
    rep(old, new, n)
# FAQ items
items = "\n".join(f'      <details class="qa"{" open" if i == 0 else ""}><summary><h3>{q}</h3></summary><p>{a}</p></details>' for i, (q, a) in enumerate(FAQ))
s = re.sub(r'      <details class="qa" open>.*?</details>\n(?:      <details class="qa">.*?</details>\n)+', items + '\n', s, count=1, flags=re.S)
# meter role names: translate in the meters only
rep("<div class=\"nm\">${ROLE[id]}</div>", "<div class=\"nm\">${ROLE_AR[id]}</div>")
rep("const ROLE = {", "const ROLE_AR = { 'tech-pm': 'السكرم ماستر', 'web-tech-lead': 'القائد التقني', 'web-dev': 'المطوّر', 'web-tester': 'مختبِر الجودة' };\nconst ROLE = {")
open(out, 'w', encoding='utf-8').write(s)
# report leftover English prose outside script/style/code
body = s[s.index('<body>'):s.index('<script>\n(() => {')]
body = re.sub(r'<(script|style|code|pre)[^>]*>.*?</\1>', '', body, flags=re.S)
left = [t.strip() for t in re.findall(r'>([^<]*[A-Za-z]{4,}[^<]*)<', body) if not re.search(r'[؀-ۿ]', t)]
print('\n'.join(sorted(set(left))))
