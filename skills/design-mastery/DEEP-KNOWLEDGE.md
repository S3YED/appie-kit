# Deep Design Knowledge - Het Waarom

Dit is niet wat je moet doen. Dit is WAAROM dingen werken.

---

## De Beste Libraries (en waarom)

### Tier 1: Production-Ready

| Library | Waarom het de beste is | Wanneer gebruiken |
|---------|------------------------|-------------------|
| **shadcn/ui** | Copy-paste ownership. Geen package dependency. Radix primitives = accessibility. Tailwind styling = customizable. JIJ bezit de code. | Alles. Default keuze. |
| **Untitled UI React** | React Aria (Adobe maintained, beter dan Radix). 5000+ components. Figma sync. | Grote projecten, design system nodig |
| **Aceternity UI** | 200+ animated components. Framer Motion. De "wow factor" library. | Landing pages, marketing sites |
| **Magic UI** | Animated sections. Hero's die indruk maken. | Specifieke wow-sections |

### Tier 2: Specifieke Use Cases

| Library | Wanneer |
|---------|---------|
| **Radix UI** | Als je alleen primitives wilt, zelf stylen |
| **React Aria** | Maximum accessibility, enterprise |
| **NextUI** | Next.js projecten, snel en mooi |
| **Mantine** | Als je hooks + components wilt |

### WAAROM shadcn wint:
```
Traditionele library: npm install → dependency hell → wachten op updates → breaking changes
shadcn: copy code → jij bezit het → pas aan wat je wilt → geen externe afhankelijkheid
```

---

## Typography: Diep Begrip

### Het Fundamentele Principe
> **"Typography should be invisible."**
> Als iemand je font keuze opmerkt, heb je gefaald. Goede typography wordt GEVOELD, niet gezien.

### Waarom Bepaalde Fonts Werken

**Sans-serif (Inter, SF Pro, Geist):**
- Modern, clean, digitaal
- Beter leesbaar op schermen
- Voelt: technologie, innovatie, toegankelijk

**Serif (Playfair, Merriweather, Georgia):**
- Traditioneel, betrouwbaar, editorial
- Goed voor lange tekst (leesbaarheid)
- Voelt: autoriteit, luxe, storytelling

**Monospace (JetBrains Mono, Fira Code):**
- Code, technisch, developer
- Voelt: precisie, technical, hacker

### Font Pairing: De Echte Regel
Niet "serif + sans-serif". De echte regel is **CONTRAST met HARMONIE**:

```
Contrast: Verschillende persoonlijkheden
Harmonie: Vergelijkbare x-height, proportions

GOED: Playfair Display (decoratief) + Source Sans (neutraal)
      → Contrast in stijl, harmonie in proportie

SLECHT: Two decoratieve fonts
        → Competitie, chaos, geen hierarchy
```

### De Hierarchy Test
**Als je alle kleur weghaalt, moet de hierarchy nog steeds duidelijk zijn.**

Dat betekent:
- H1 moet DUIDELIJK belangrijker zijn dan H2
- Body text moet DUIDELIJK ondergeschikt zijn
- Dit bereik je met: size, weight, spacing, case

---

## Color Psychology: Waarom Kleuren Werken

### De Wetenschap
Kleuren activeren specifieke emotionele responses. Dit is biologisch, niet cultureel.

| Kleur | Emotie | Gebruikt door | Waarom |
|-------|--------|---------------|--------|
| **Blue** | Trust, calm, professional | Banks, tech, healthcare | Verlaagt hartslag, calmeert |
| **Green** | Growth, health, nature | Finance, eco, wellness | Associatie met natuur, veiligheid |
| **Red** | Urgency, passion, energy | Food, sales, entertainment | Verhoogt hartslag, aandacht |
| **Orange** | Friendly, confident, fun | Tech, food, creative | Warm maar niet agressief |
| **Purple** | Luxury, creativity, wisdom | Beauty, spiritual, premium | Zeldzaam in natuur = exclusief |
| **Black** | Sophistication, power, luxury | Fashion, luxury, tech | Absence = mystery, elegance |
| **White** | Clean, simple, pure | Tech, healthcare, minimal | Space = breathing room |

### De 60-30-10 Regel (Echt Begrijpen)
```
60% - Dominant (achtergrond, base)
30% - Secondary (containers, sections)
10% - Accent (CTA's, highlights)

Dit is niet random. Het creëert RUST met FOCUS.
Te veel accent = chaos
Te weinig accent = saai
```

### Waarom "Max 3 Kleuren" Werkt
Cognitieve load. Mensen kunnen ~3-4 dingen tegelijk in werkgeheugen houden.
Meer kleuren = meer processing = verwarring.

---

## Copywriting: De Frameworks Die Converteren

### AIDA (Attention → Interest → Desire → Action)
```
ATTENTION: "Stop losing 40% of your leads"
INTEREST: "Most businesses respond to inquiries in 24 hours. Winners respond in 5 minutes."
DESIRE: "Imagine automatically qualifying every lead the moment they come in."
ACTION: "Start your free trial"
```

### PAS (Problem → Agitate → Solution)
```
PROBLEM: "Your website looks dated."
AGITATE: "Every day, potential customers land on your site and leave because it doesn't feel trustworthy. That's money walking out the door."
SOLUTION: "We rebuild websites that convert visitors into customers."
```

### The 4 U's (voor Headlines)
- **Useful** — Wat krijg ik eruit?
- **Urgent** — Waarom nu?
- **Unique** — Waarom jij?
- **Ultra-specific** — Geen vage beloftes

```
SLECHT: "Grow Your Business"
GOED: "Add $10K MRR in 90 Days (Or Your Money Back)"
```

### Copywriting Truths
1. **Benefits > Features** — Niemand wil een drill, ze willen een gat
2. **Specifiek > Vaag** — "347 happy customers" > "Many satisfied clients"
3. **You > We** — Praat over de klant, niet over jezelf
4. **One CTA** — Verwar mensen niet met keuzes

---

## Branding: Waarom Merken Voelen

### Een Merk Is Een Gevoel
Nike verkoopt geen schoenen. Ze verkopen "overwinning over jezelf."
Apple verkoopt geen computers. Ze verkopen "creativiteit en status."
Tesla verkoopt geen auto's. Ze verkopen "de toekomst."

### De Brand Elements (en hun functie)

| Element | Functie |
|---------|---------|
| **Logo** | Herkenning in <1 seconde |
| **Kleuren** | Emotionele associatie |
| **Typography** | Persoonlijkheid/stem |
| **Imagery style** | Wereld waarin merk leeft |
| **Voice/Tone** | Hoe het merk "praat" |

### Brand Consistency Regel
> **Elke touchpoint moet voelen alsof dezelfde persoon het maakte.**

Website, social, email, packaging — allemaal één stem.

---

## Design Decisions: Mijn Framework

Wanneer ik een design keuze maak, vraag ik:

1. **Wat is het DOEL van dit element?**
   - Informeren? → Clarity first
   - Converteren? → CTA prominence
   - Entertaninen? → Delight allowed

2. **Wie is de GEBRUIKER?**
   - Tech-savvy? → Kan complexity aan
   - General public? → Simplify everything
   - Luxury buyer? → White space, restraint

3. **Wat is de EMOTIE die ik wil?**
   - Trust? → Blue, serif, testimonials
   - Excitement? → Bold colors, motion
   - Calm? → White space, soft colors

4. **Werkt het ZONDER dit element?**
   - Als ja → verwijder het
   - Als nee → het is essentieel

---

## Anti-Patterns (Wat Slecht Design Slecht Maakt)

| Anti-pattern | Waarom het faalt |
|--------------|------------------|
| **Te veel fonts** | Chaos, geen hierarchy |
| **Random spacing** | Voelt "off" zonder te weten waarom |
| **Weak contrast** | Accessibility fail, moeilijk lezen |
| **Decoration without purpose** | Voegt noise toe, geen signal |
| **Inconsistent styling** | Voelt onprofessioneel, onbetrouwbaar |
| **Copy-first design** | Lange tekst = niet gelezen |
| **No visual hierarchy** | Gebruiker weet niet waar te kijken |

---

## Mijn Studie Lijst

### Sites om DAGELIJKS te analyseren:
1. **Linear.app** — Information density met clarity
2. **Vercel.com** — Gradients, motion, dark mode
3. **Stripe.com** — Typography, documentation
4. **Raycast.com** — Glow effects, premium dark
5. **Notion.so** — Simplicity, whitespace
6. **Framer.com** — Motion, playfulness

### Vragen bij elke site:
- Wat voel ik als ik land?
- Waar kijk ik EERST?
- Welke fonts? Waarom?
- Welke kleuren? Waarom?
- Wat is de CTA? Hoe prominent?
- Wat zou ik NIET doen?

---

*Dit document groeit. Elke keer dat ik iets leer over WAAROM design werkt, voeg ik het toe.*
