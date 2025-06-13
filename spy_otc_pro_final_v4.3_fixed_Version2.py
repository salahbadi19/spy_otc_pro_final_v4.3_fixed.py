import time
import random
from datetime import datetime, timedelta
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.progress import Progress
from rich.table import Table
from tinydb import TinyDB, Query

console = Console()
db = TinyDB('users.json')
keys_db = TinyDB('used_keys.json')

User = Query()
Key = Query()

# --- قاعدة بيانات البلدان ---
COUNTRIES = {
    'EG': {'name': 'مصر', 'timezone': 'Africa/Cairo'},
    'SA': {'name': 'المملكة العربية السعودية', 'timezone': 'Asia/Riyadh'},
    'AE': {'name': 'الإمارات', 'timezone': 'Asia/Dubai'},
    'JO': {'name': 'الأردن', 'timezone': 'Asia/Amman'},
    'LB': {'name': 'لبنان', 'timezone': 'Asia/Beirut'},
    'SY': {'name': 'سوريا', 'timezone': 'Asia/Damascus'},
    'IQ': {'name': 'العراق', 'timezone': 'Asia/Baghdad'},
    'MA': {'name': 'المغرب', 'timezone': 'Africa/Casablanca'},
    'TN': {'name': 'تونس', 'timezone': 'Africa/Tunis'},
    'DZ': {'name': 'الجزائر', 'timezone': 'Africa/Algiers'},
    'SD': {'name': 'السودان', 'timezone': 'Africa/Khartoum'},
    'YE': {'name': 'اليمن', 'timezone': 'Asia/Aden'},
    'QA': {'name': 'قطر', 'timezone': 'Asia/Qatar'},
    'KW': {'name': 'الكويت', 'timezone': 'Asia/Kuwait'},
    'BH': {'name': 'البحرين', 'timezone': 'Asia/Bahrain'},
    'OM': {'name': 'عُمان', 'timezone': 'Asia/Muscat'},
    'PS': {'name': 'فلسطين', 'timezone': 'Asia/Gaza'},
    'LY': {'name': 'ليبيا', 'timezone': 'Africa/Tripoli'}
}

# --- أزواج العملات العشوائية ---
CURRENCY_PAIRS = [
    "AED/CNY OTC", "AUD/CAD OTC", "AUD/CHF OTC", "CAD/CHF OTC", "CAD/JPY OTC",
    "EUR/CHF OTC", "EUR/JPY OTC", "NGN/USD OTC", "SAR/CNY OTC", "UAH/USD OTC",
    "USD/ARS OTC", "USD/COP OTC", "USD/EGP OTC", "USD/RUB OTC", "USD/THB OTC",
    "ZAR/USD OTC", "CHF/NOK OTC", "EUR/HUF OTC", "KES/USD OTC", "EUR/RUB OTC",
    "AUD/USD OTC", "USD/IDR OTC", "QAR/CNY OTC", "USD/CAD OTC", "AUD/JPY OTC",
    "BHD/CNY OTC", "USD/INR OTC", "MAD/USD OTC", "USD/PKR OTC", "USD/CLP OTC",
    "USD/MXN OTC", "USD/JPY OTC", "USD/VND OTC", "EUR/USD OTC", "LBP/USD OTC",
    "YER/USD OTC"
]


# --- المنصات ---
PLATFORMS = ["Quotex", "Kalshi", "Binomo", "CMC Markets", "Pocket Option", "IQ Options"]

# --- مستويات الدقة حسب النوع ---
ACCURACY_LEVELS = {
    "T1": {"name": "بدون مضاعفة", "accuracy": 0.85},
    "Y1": {"name": "مضاعفة x1", "accuracy": 0.60},
    "O1": {"name": "مضاعفة x2", "accuracy": 0.35}
}

# --- الشعار ---
def display_logo():
    logo = r"""                                                                  ,----,                  
            ,-.----.                            ,----..         ,/   .`|                  
  .--.--.   \    /  \                          /   /   \      ,`   .'  : ,----..          
 /  /    '. |   :    \         ,---,          /   .     :   ;    ;     //   /   \         
|  :  /`. / |   |  .\ :       /_ ./|         .   /   ;.  \.'___,/    ,'|   :     :        
;  |  |--`  .   :  |: | ,---, |  ' :        .   ;   /  ` ;|    :     | .   |  ;. /        
|  :  ;_    |   |   \ :/___/ \.  : |        ;   |  ; \ ; |;    |.';  ; .   ; /--`         
 \  \    `. |   : .   / .  \  \ ,' '        |   :  | ; | '`----'  |  | ;   | ;            
  `----.   \;   | |`-'   \  ;  `  ,'        .   |  ' ' ' :    '   :  ; |   : |            
  __ \  \  ||   | ;       \  \    '         '   ;  \; /  |    |   |  ' .   | '___         
 /  /`--'  /:   ' |        '  \   |          \   \  ',  /     '   :  | '   ; : .'|        
'--'.     / :   : :         \  ;  ;           ;   :    /      ;   |.'  '   | '/  :        
  `--'---'  |   | :          :  \  \           \   \ .'       '---'    |   :    /         
            `---'.|           \  ' ;            `---`                   \   \ .'          
              `---`            `--`                                      `---`            
                                                                                         
[+] SPY OTC TERMINAL PRO ULTRA v4.3 [+]
    """
    console.print(f"[bold cyan]{logo}[/bold cyan]")

# --- رسالة الترحيب ---
def welcome_message():
    display_logo()
    console.print(Panel("[green]👋 مرحبًا بك في أداة تداول الخيارات الثنائية المتطورة![/green]", expand=False))

# --- اختيار البلد في عمودين ---
def choose_country():
    codes = list(COUNTRIES.keys())
    table = Table(title="🌍 اختر بلدك")
    table.add_column("الرمز", justify="center")
    table.add_column("الاسم", justify="center")
    table.add_column("الرمز", justify="center")
    table.add_column("الاسم", justify="center")

    for i in range(0, len(codes), 2):
        if i + 1 < len(codes):
            code1, code2 = codes[i], codes[i+1]
            table.add_row(code1, COUNTRIES[code1]['name'], code2, COUNTRIES[code2]['name'])
        else:
            table.add_row(codes[i], COUNTRIES[codes[i]]['name'], "", "")

    console.clear()
    welcome_message()
    console.print(table)
    choice = Prompt.ask("[green]🔢 أدخل رمز البلد[/green]", default="EG").upper()
    return choice

# --- التحقق من صحة المفتاح ---
def validate_license_key(key):
    if keys_db.contains(Key.key == key):
        return {"valid": False, "reason": "🚫 هذا المفتاح تم استخدامه بالفعل"}
    if len(key) != 10:
        return {"valid": False, "reason": "🚫 طول المفتاح غير صحيح"}
    prefix = key[:2]
    if prefix not in ACCURACY_LEVELS:
        return {"valid": False, "reason": "🚫 نوع الحساب غير مدعوم"}
    try:
        trades_part = ''.join(filter(str.isdigit, key[2:5]))
        trades = int(trades_part)
    except:
        return {"valid": False, "reason": "🚫 عدد الصفقات غير صالح"}

    return {
        "valid": True,
        "multiplier": prefix,
        "trades": trades,
        "key": key
    }

# --- تسجيل دخول أو إنشاء حساب ---
def login_or_register():
    console.clear()
    welcome_message()
    console.print("[yellow]🔐 هل لديك حساب؟[/yellow]")
    console.print("[cyan]1. نعم، سجل دخولي[/cyan]")
    console.print("[cyan]2. لا، أنشئ حسابًا جديدًا[/cyan]")
    choice = Prompt.ask("[green]📌 اختر خيارًا[/green]", default="2")

    if choice == "1":
        username = Prompt.ask("[green]👤 اسم المستخدم[/green]")
        password = Prompt.ask("[green]🔒 كلمة المرور[/green]", password=True)
        user = db.get((User.username == username) & (User.password == password))
        if user:
            console.print(f"[green]✅ مرحبًا {username}![/green]")
            return user
        else:
            console.print("[red]❌ بيانات الدخول غير صحيحة[/red]")
            time.sleep(2)
            return login_or_register()
    else:
        while True:
            username = Prompt.ask("[green]👤 أدخل اسم المستخدم[/green]")
            password = Prompt.ask("[green]🔒 أدخل كلمة مرور قوية[/green]", password=True)
            confirm = Prompt.ask("[green]🔁 أكد كلمة المرور[/green]", password=True)
            if password == confirm:
                break
            else:
                console.print("[red]❌ كلمات المرور غير متطابقة.[/red]")
        db.insert({'username': username, 'password': password})
        console.print(f"[green]✅ تم إنشاء الحساب بنجاح، {username}![/green]")
        time.sleep(1)
        return db.get(User.username == username)

# --- إدخال مفتاح الترخيص ---
def enter_license_key():
    console.clear()
    welcome_message()
    license_key = Prompt.ask("[green]🔑 أدخل مفتاح الترخيص[/green]")
    key_data = validate_license_key(license_key)

    if not key_data or not key_data["valid"]:
        console.print(f"[red]❌ {key_data['reason'] if key_data else 'مفتاح غير صحيح'}[/red]")
        console.print("[blue]📩 يجب عليك التواصل مع @tatin34 للحصول على مفتاح ترخيص.[/blue]")
        input("\n🔚 اضغط Enter للمحاولة مرة أخرى...")
        return enter_license_key()
    else:
        keys_db.insert({'key': key_data['key'], 'used': False})
        console.print(f"[green]✅ تم التحقق من المفتاح بنجاح![/green]")
        time.sleep(1)
        return {
            "license_key": license_key,
            "multiplier": key_data.get("multiplier", "T1"),
            "trades_remaining": key_data.get("trades", 1)
        }

# --- تحليل البيانات ---
def analyze_data(country_code):
    console.clear()
    welcome_message()
    console.print(Panel("[yellow]🔍 جارٍ تحليل البيانات...[/yellow]", expand=False))
    with Progress() as progress:
        task = progress.add_task("[cyan]⏳ التحميل...", total=100)
        while not progress.finished:
            progress.update(task, advance=random.randint(5, 15))
            time.sleep(0.2)
    console.print("[green]✅ تحليل البيانات اكتمل![/green]")
    time.sleep(1)

# --- اختيار المنصة ---
def choose_platform():
    console.clear()
    welcome_message()
    console.print(Panel("[yellow]🌐 اختر المنصة[/yellow]", expand=False))
    for i, p in enumerate(PLATFORMS, start=1):
        console.print(f"[cyan]{i}. {p}[/cyan]")
    choice = IntPrompt.ask("[green]📌 أدخل رقم المنصة[/green]", default=1)
    return PLATFORMS[choice - 1]

# --- اختيار مدة الصفقة عشوائيًا ---
def choose_duration_randomly():
    durations = [i * 60 for i in range(1, 11)]  # من 1 إلى 10 دقائق
    return random.choice(durations)

# --- عرض تحليل الصفقة ---
def show_analysis(pair, action, accuracy, country_tz, user_trades):
    console.clear()
    welcome_message()
    console.print(Panel(
        f"[bold green]PAIR:[/bold green] {pair}\n"
        f"[bold blue]ACTION:[/bold blue] {action}\n"
        f"[bold yellow]ENTRY TIME:[/bold yellow] {datetime.now(tz=country_tz).strftime('%H:%M:%S')}\n"
        f"[bold magenta]ACCURACY:[/bold magenta] {int(accuracy * 100)}%\n"
        f"[bold red]REMAINING TRADES:[/bold red] {user_trades}"
    ))

# --- مؤقت الدخول قبل الصفقة ---
def entry_timer(seconds=60):
    console.print(Panel(f"[yellow]⏰ ستبدأ الصفقة بعد {seconds // 60} دقيقة[/yellow]", expand=False))
    with Progress() as progress:
        task = progress.add_task("[cyan]⏳ الانتظار حتى وقت الدخول...", total=seconds)
        while not progress.finished:
            progress.update(task, advance=1)
            time.sleep(1)

# --- بدء الصفقة ---
def start_trade(platform, duration, user, country_tz):
    pair = random.choice(CURRENCY_PAIRS)
    action = random.choice(["📈 شراء", "📉 بيع"])
    accuracy = ACCURACY_LEVELS[user["multiplier"]]["accuracy"]
    user_trades = user["trades_remaining"]

    console.clear()
    welcome_message()
    console.print(Panel(f"[yellow]⏰ جارٍ الاستعداد للصفقة...[/yellow]", expand=False))

    # عرض تحليل الصفقة
    show_analysis(pair, action, accuracy, country_tz, user_trades)

    # مؤقت الدخول
    entry_timer(60)

    # المؤقت الحقيقي للصفقة
    with Progress() as progress:
        task = progress.add_task("[cyan]⏳ المؤقت...", total=duration)
        while not progress.finished:
            progress.update(task, advance=1)
            time.sleep(1)

    result = "🎉 فوز" if random.random() < accuracy else "💥 خسارة"
    color = "[green]" if result == "فوز" else "[red]"
    console.print(f"\n{color}📊 نتيجة الصفقة: {result}[/]")

    user["trades_remaining"] -= 1
    again = Prompt.ask("[yellow]🔄 اضغط Enter للصفقة الجديدة أو q للخروج[/yellow]", default="")
    return again.lower() != "q"

# --- لوحة التحكم ---
def dashboard(user, country_code):
    from pytz import timezone
    country_tz = timezone(COUNTRIES[country_code]['timezone'])

    console.print(f"[blue]👋 مرحبًا {user['username']}![/blue]")
    while True:
        platform = choose_platform()
        duration = choose_duration_randomly()
        analyze_data(country_code)

        if user["trades_remaining"] <= 0:
            console.print("[red]🔚 لقد انتهت صلاحية مفتاحك. يجب الحصول على مفتاح جديد.[/red]")
            console.print("[blue]🔗 اضغط Enter للتواصل مع @tatin34[/blue]")
            input()
            continue

        keep_going = start_trade(platform, duration, user, country_tz)
        if not keep_going:
            console.print("[green]🔚 تم إنهاء الجلسة[/green]")
            time.sleep(1)
            break

# --- الدالة الرئيسية ---
def main():
    console.clear()
    welcome_message()
    country_code = choose_country()
    user_data = enter_license_key()
    user = {
        "username": user_data['license_key'],
        "license_key": user_data['license_key'],
        "multiplier": user_data['multiplier'],
        "trades_remaining": user_data['trades_remaining']
    }
    dashboard(user, country_code)

if __name__ == "__main__":
    main()