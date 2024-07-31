from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from datetime import datetime, timedelta
from num2words import num2words


pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))


def convert_cost_to_lithuanian_words(number):
    words = num2words(number, lang='en')
    translation_dict = {
        "zero": "nulis",
        "one": "vienas",
        "two": "du",
        "three": "trys",
        "four": "keturi",
        "five": "penki",
        "six": "šeši",
        "seven": "septyni",
        "eight": "aštuoni",
        "nine": "devyni",
        "ten": "dešimt",
        "eleven": "vienuolika",
        "twelve": "dvylika",
        "thirteen": "trylika",
        "fourteen": "keturiolika",
        "fifteen": "penkiolika",
        "sixteen": "šešiolika",
        "seventeen": "septyniolika",
        "eighteen": "aštuoniolika",
        "nineteen": "devyniolika",
        "twenty": "dvidešimt",
        "thirty": "trisdešimt",
        "forty": "keturiasdešimt",
        "fifty": "penkiasdešimt",
        "sixty": "šešiasdešimt",
        "seventy": "septyniasdešimt",
        "eighty": "aštuoniasdešimt",
        "ninety": "devyniasdešimt",
        "hundred": "šimtai",
        "thousand": "tūkstantis",
        "million": "milijonas",
        "billion": "milijardas",
        "and": "ir"
    }

    translated_words = []
    for word in words.split():
        if '-' in word:
            parts = word.split('-')
            translated_parts = [translation_dict.get(
                part, part) for part in parts]
            translated_words.append(' '.join(translated_parts))
        else:
            translated_words.append(translation_dict.get(word, word))
    return ' '.join(translated_words)


def generate_contract(details):
    first_name = details["First name"]
    last_name = details["Last name"]
    birth_date = details["Birth date"]
    address = details["Residency Address"]
    phone = details["Phone Number"]
    email = details["Email"]
    date_of_event_str = details["Event date"]
    date_of_event = datetime.strptime(date_of_event_str, "%Y-%m-%d")
    next_day = (date_of_event + timedelta(days=1)).strftime("%Y-%m-%d")
    start_hours = details["Working hours"].split('-')[0]
    end_hours = details["Working hours"].split('-')[1]
    venue = details["Venue"]
    total_cost = details["Total cost"]
    total_cost_words = convert_cost_to_lithuanian_words(total_cost)

    file_name = f"Baro nuomos sutartis {date_of_event_str} {first_name} {last_name}.pdf"
    doc = SimpleDocTemplate(file_name, pagesize=A4)
    styles = getSampleStyleSheet()

    contract_style = ParagraphStyle(
        'Contract',
        fontName='DejaVuSans',
        fontSize=12,
        leading=14,
        spaceAfter=12
    )

    centered_style = ParagraphStyle(
        'Centered',
        fontName='DejaVuSans',
        fontSize=12,
        leading=16,
        alignment=1,
        spaceAfter=14
    )

    elements = []

    title = Paragraph("MOBILAUS BARO NUOMOS SUTARTIS", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    date_location = Paragraph(
        f"{datetime.now().strftime('%Y-%m-%d')}<br/>Kaunas", centered_style)
    elements.append(date_location)
    elements.append(Spacer(1, 12))

    content = [
        f"{first_name} {last_name}, gim. {birth_date}, gyv. {address} (toliau – Nuomininkas) ir Double Vision, MB, įm. k. 306318735, reg. adresas Žeimenos g. 82D-24, Kaunas (toliau – Nuomotojas) sudarė šią sutartį (toliau – Sutartis).",
        "<b>1.Sutarties objektas</b>",
        f"1.1 Nuomotojas už užmokestį įsipareigoja suteikti mobilų barą, barmeno darbo laiką ir baro įrangą į kurią įeina taurės, stiklinės, kokteilių gaminimo įrankiai, termo dėžės. Nuomininkas laikinai jais naudosis nuo {date_of_event_str} {start_hours} iki {next_day} {end_hours}. Nuomininkas įsipareigoja už tai atlyginti 3.1 ir 3.2 sutarties punktuose nustatyto dydžio užmokesčius.",
        " ",
        "<b>2.Sutarties šalių pareigos</b>",
        f"2.1 Nuomotojas įsipareigoja:<br/>2.1.1 Konsultuoti mobilaus baro ir kokteilių klausimais, padėti paruošti gėrimų meniu iki sutartos šventės datos.<br/>2.1.2 Atvykti į nuomininko paskirtą vietą ({venue}) su reikalinga baro įranga ir suteikti barmeno paslaugas nuomininko ir nuomotojo sutartam laiko tarpui.<br/>2.1.3 Suteikti nuomos viršvalandžius už papildomą, prieš tai aptartą, sutartą mokestį.<br/>2.1.3.1 Dirbant dviems barmenams viršvalandžio kaina 100€<br/>2.1.3.2 Dirbant trims barmenams viršvalandžio kaina 150€<br/>2.1.3.4 Dirbant keturiems barmenams viršvalandžio kaina 200€<br/>2.1.4 Nuomininkui atsiųsti kokteilių pasirinkimo katalogą bei Excel failą papildomų gėrimų pasirinkimui.<br/>2.1.5 Paruošti kokteilių ingredientų sąmatą ne vėliau kaip 2 savaitė iki šventės (jei nuomininkas yra išsirinkęs kokteilius savo šventei)<br/>2.1.6 Nuomotojo personalas į šventės vietą atvyksta neanksčiau kaip 2 valandos iki 1.1 punkte nurodyto laiko ir nevėliau kaip 1 valanda iki 1.1 punkte nurodyto laiko. Jei nuominikas reikalauja, kad dėl tam tikrų priežaščių personalas privalo atvykti anksčiau nei 2 valandos iki 1.1 punkte nurodyto laiko už kiekvieną priešlaikinę valandą skaičiuojamas 50€ mokestis.",
        "<b>2.2 Nuomininkas įsipareigoja:</b>",
        "2.2.1 Sumokėti 150 € užstatą per 5 darbo dienas nuo sutarties pasirašymo į nuomotojo sąskaitą:<br/><b>SwedBank<br/>MB DOUBLE VISION<br/>LT557300010180149406</b><br/>2.2.2 150€ užstatas yra neįskaitomas į galutinį mokėjimą. Neatsiradus jokiems 2.2.4 punkte nurodytiems nuostoliams visas užstatas grąžinamas į nuomininko sąskaitą. Atsiradus nuostoliams – atitinkama suma yra išskaičiuojama iš užstato ir grąžinama užstato dalis.<br/>2.2.3 Naudoti suteiktą mobilų barą bei baro įrangą pagal paskirtį.<br/>2.2.4 Esant esminiams mobilaus baro apgadinimams ar baro inventoriaus sulaužymams/pasisavinimams/dingimams dėl nuomininko kaltės nuomos laikotarpiu, kompensuoti žalą. Pasirašydamas šią sutartį nuomininkas patvirtina, jog susipažino su jam/jai nuomojamo inventoriaus kainomis bei žino ir supranta, jog inventoriaus kainos iki nuomos datos gali keistis (priedas nr. 1).<br/>2.2.5 Išsirinkti ir nuomotojui pateikti išsirinktus kokteilius ir gėrimus ne vėliau kaip 1 mėnesis iki nuomos laikotarpio pradžios.<br/>2.2.6 Pasirūpinti personalo maitinimu jei darbas trunka ilgiau nei 5 valandas<br/>2.2.7 Jei šventė toliau kaip 20km nuo Kauno centro apmokėti transportavimo išlaidas kelionei į vieną pusę tarifu 0.3€/km.<br/>2.2.8 Sumokėti Sutarties 3.1 ir 3.2 punktuose numatytus mokesčius.",
        "<b>3.Nuomos mokestis</b>",
        f"3.1 Mobilaus baro vienkartinis mokestis yra <b>{total_cost} EUR</b> (suma žodžiais: {total_cost_words} eurų)<br/>3.2 Mokestis už kokteilių ingredientus ir/ar papildomus gėrimus bus atsiunčiamas atskirame Excel faile, ne vėliau kaip dvi savaitės iki nuomos termino pradžios, kadangi tai kiekvienam nuomininkui subjektyvi suma kuri skaičiuojama pagal nuomininko pageidavimus.<br/>3.3 Nuomininkas įsipareigoja sumokėti Nuomotojui šios sutarties 3.1 ir 3.2 punkte numatytus mokesčius ne vėliau kaip iki nuomos termino pabaigos.",
        "<b>4.Šalių atsakomybė</b>",
        "4.1 Šalys vykdo šią sutartį sąžiningai ir tinkamai. Pažeidus sutartį šalys atsako pagal šią sutartį, LR Civilinį kodeksą ir kitus įstatymus.<br/>4.2 Nuomininkas neatsako už iki sutarties pasirašymo ir ne dėl jų kaltės atsiradusius skolinius įsipareigojimus.<br/>4.3 Nuomotojui nepranešus apie ketinimą nutraukti sutartį arba pranešus vėliau nei 1 sav. iki sutarties vykdymo, šis įsipareigoja atlyginti dėl tokio sutarties nutraukimo Nuomininkui atsiradusius nuostolius.",
        "<b>5.Sutarties nutraukimas</b>",
        "5.1 Sutartis gali būti nutraukta:<br/>5.1.1 šalių susitarimu;<br/>5.1.2 vienašališkai vienos iš šalių prieš 1 sav. apie tai įspėjus kitą šalį.<br/>5.2 Užstato gražinimas dėl sutarties nutraukimo:<br/>5.2.1 jei sutartį nutraukia nuomininkas, tuomet nuomotojas negrąžina 150 € užstato;<br/>5.2.2 jei sutartį nutraukia nuomuotojas, tuomet jis įpareigotas nuomininkui gražinti 150 € užstatą.<br/>5.2.3 jei sutartis nutraukiama dėl Force majeure nuomuotojas įpareigotas nuomininkui grąžinti 150 € užstatą.",
        "<b>6. Baigiamosios nuostatos</b>",
        "6.1 Sutartis abiejų šalių bus pasirašyta naudojant elektroninį parašą „DokoBit“ sistemoje<br/>6.2 Bet kokie sutarties papildymai ar pakeitimai galioja tik tada, kai yra raštu sudaryti abiejų Šalių ar jų įgaliotų atstovų.<br/>6.3 Šioje sutartyje nenumatytos sąlygos nustatomos vadovaujantis Lietuvos Respublikos įstatymais.<br/>6.4 Sutartis sudaryta dviem egzemplioriais - po vieną kiekvienai šaliai.",
        f"Nuomininkas:<br/>{first_name} {last_name}<br/>{phone}<br/>{email}",
        "Nuomotojas:<br/>Viktoras Pčalinas<br/>MB Double Vision<br/>+37065454447"
    ]

    for paragraph in content:
        elements.append(Paragraph(paragraph, contract_style))
        elements.append(Spacer(1, 1))

    doc.build(elements)
    print(f"Contract saved as {file_name}")
    return file_name


if __name__ == "__main__":

    details = {
        "First name": "John",
        "Last name": "Doe",
        "Birth date": "1990-01-01",
        "Residency Address": "123 Main St",
        "Phone Number": "+37012345678",
        "Email": "andrius.pcalinas@gmail.com",
        "Event date": "2024-08-01",
        "Venue": "Kauno g. 5, Kaunas",
        "Number of guests": 50,
        "Number of bartenders": 2,
        "Number of barbacks": 0,
        "Working hours": "17:00-01:00",
        "Overtime hours": 2,
        "Total cost": 899,
        "Base cost": 650,
        "Transport cost": 50,
        "Overtime cost": 100,
    }
    contract_file = generate_contract(details)
