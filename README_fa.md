![Example Image](holderbotcover.png)

<p align="center">
  <a href="./README.md">
	English
	</a>
	|
	<a href="./README_ru.md">
	Русский
	</a>
 |
	<a href="./README_fa.md">
	فارسی
	</a>

</p>

# هولدر بات چیست ؟ #

هولدر بات یک ربات سریع و ساده است که طراحی شده است تا به مشکل عدم وجود گزینه شروع تایمر پس از اولیین اتصال در رابط کاربری "پنل مرزبان" پاسخ دهد. با استفاده از رابط‌های برنامه‌نویسی پنل مرزبان، هولدر بات به کاربران امکان استفاده آسان از این ویژگی را در تلگرام فراهم کرده است. با ارتقاء به نسخه ۳.۰، هولدر بات قابلیت‌های خود را با معرفی ویژگی‌های ویژه ارتقا داده و در نسخه‌های بعدی به اوج خود رسیده است. اکنون، هولدر بات به عنوان یک دستیار حرفه‌ای برای کاربران پنل مرزبان خدمت می‌کند. برای کسب اطلاعات بیشتر، می‌توانید به بخش به‌روزرسانی‌ها مراجعه کنید یا به کانال تلگرام ما بپیوندید.

> [!IMPORTANT]
> شما می‌توانید با دادن یک ستاره به این پروژه در GitHub، حمایت خود را نشان دهید. 
> ما یک کانال تلگرام برای اعلانات، نظرسنجی‌ها و تعامل با کاربران ایجاد کرده‌ایم. می‌توانید با @ErfjabHolderbot به ما بپیوندید. [@ErfjabHolderbot](https://t.me/erfjabholderbot).

# چرا هولدر بات؟

- قابلیت پیکربندی خودکار پس از رسیدن به حداکثر حجم یا زمان.
- قابلیت مدیریت مدیران پنل (تغییر رمز عبور یا سودو)
- قابلیت افزودن یا حذف مدیران برای پنل
- قابلیت تعیین ضریب مصرف گره
- قابلیت مدیریت گره‌ها (غیرفعال‌سازی/فعال‌سازی/اتصال مجدد)
- قابلیت نظارت و دریافت اعلان‌های قطع اتصال گره
- قابلیت غیرفعال‌سازی/فعال‌سازی نظارت
- قابلیت تغییر تایمر نظارت برای گره‌ها
- قابلیت ایجاد کاربران به صورت عمده/تکی (در حال نگهداری)
- قابلیت ایجاد کاربران از طریق قالب‌ها
- قابلیت ایجاد قالب‌ها (حجم، زمان، ورودی)
- قابلیت دریافت زمان آخرین آنلاین بودن، بروزرسانی زیرکاربر (تکی)
- قابلیت مستقیم دریافت بارکد و متن لینک زیریا حذف کاربر
- قابلیت دریافت نرم‌افزار استفاده شده توسط کاربر
- قابلیت دریافت بارکد برای لینک ارسال شده مورد نظر
- قابلیت جستجو و دریافت کاربران مشابه (مانند Did you Mean گوگل)
- قابلیت دریافت لیست کاربران آنلاین/آفلاین (از ۱ دقیقه تا آخرین ۶۰ روز به صورت جدول و PDF)
- قابلیت دریافت لیست زیرکاربران بروزرسانی/غیربروزرسانی (از ۱ دقیقه تا آخرین ۶۰ روز به صورت جدول و PDF)
- رابط کاربری جدید، زیبا و ساده


> [!NOTE]
> ما به ‌طور مداوم در حال کار بر روی بروزرسانی‌های جدید هستیم. آیا ایده‌ها یا پیشنهاداتی دارید؟ لطفاً آن‌ها را به عنوان مسایل مطرح کنید، ما در بروزرسانی‌های آینده ، آنها را در نظر خواهیم گرفت.

# چگونه Holderbot نصب کنیم؟ #

برای استفاده از هولدر بات، شما به اطلاعات زیر نیاز دارید:
۱- نام : می‌توانید هر نامی که ترجیح می‌دهید وارد کنید.
۲- شما میتوانید چت آیدی را از @chatIDrobot بدست آورید.
۳- شما میتوانید بات توکن را از @botfather بدست آورید.
۴- نام کاربری پنل: نام کاربری ادمین سودو پنل خود را وارد کنید.
۵- رمز عبور پنل: رمز عبور ادمین سودو پنل خود را وارد کنید.
۶- دامنه پنل: دامنه پنل خود را به این شکل وارد کنید (sub.domain.com:port).


> [!WARNING]
> لطفاً توجه داشته باشید که هولدر بات در حال حاضر تنها برای نصب و استفاده بر روی سرورهای اوبونتو پشتیبانی می‌شود، و هرگونه مسئولیتی در مورد راه‌اندازی‌های دیگر با شما خواهد بود.

لطفاً برای نصب روی سرور خود از دستور زیر استفاده کنید

```
cd && cd .. && rm -f holderbot.sh* || true && sudo apt install && sudo apt-get install libjpeg-dev && wget https://raw.githubusercontent.com/erfjab/holderbot/main/holderbot.sh && chmod +x holderbot.sh && ./holderbot.sh
```

# چگونه از ربات استفاده کنیم؟ # 

تمام توضیحات کامل و واضح است، اما اگر هنوز نقص یا کوتاهی‌هایی در توضیحات مشاهده می‌کنید، لطفاً یک مشکل ایجاد کنید و ما آن را برطرف خواهیم کرد. از همکاری شما متشکریم.

> [!WARNING]
> این آموزش‌ها به صورت اختصاصی برای نسخه 4 می‌باشند. نسخه‌های قبلی دیگر پشتیبانی نمی‌شوند.

## 🏛 صفحه اصلی

درباره صفحه اصلی، شما تمام دستورات لازم را لیست شده مشاهده خواهید کرد، همراه با توضیحات دقیقی که در پایین صفحه ارائه شده‌اند. در اینجا، علاوه بر وارد کردن دستورات، می‌توانید نام کاربری یا لینک اشتراک خود را نیز ارسال کنید. اگر کاربر وجود داشته باشد، آمار آن‌ها را دریافت خواهید کرد و اگر وجود نداشته باشد، می‌توانید با ویژگی جستجوی Holder Bot یک لیست از کاربران مشابه دریافت کنید.

وقتی آمار کاربر به شما ارسال می‌شود، سه گزینه مشاهده می‌کنید: "به‌روزرسانی"، "بارکد" و "حذف". برای به‌روزرسانی آمار کاربر، از دکمه "به‌روزرسانی" استفاده کنید. برای دریافت بارکد لینک اشتراک کاربر، از دکمه "بارکد" استفاده کنید. و برای حذف کاربر، از دکمه "حذف" استفاده کنید. 

> [!NOTE]
>نگران نباشید، قبل از انجام عملیات حذف، از شما درخواست تأیید خواهد شد.

## 🚀 ایجاد کاربر

شما دو گزینه برای ایجاد کاربر دارید: از طریق الگوها یا به صورت دستی. شما می‌توانید الگوهای آماده را با مراجعه به بخش 'الگوها' در این آموزش ایجاد کنید. وقتی کاربری ایجاد می‌کنید، اگر روی یکی از الگوهای خود کلیک کنید، ورودی، حجم و زمان پیش‌فرض انتخاب می‌شوند و از شما نام کاربری و تعداد مورد نظر خواسته خواهد شد. ربات به صورت خودکار نام‌های کاربری را شماره‌گذاری کرده و کاربران را ایجاد می‌کند.

اگر می‌خواهید این کار را به صورت دستی انجام دهید، از شما ورودی، حجم و زمان خواسته خواهد شد که برای موارد خاص مناسب‌تر است. الگوها کارتان را سریع‌تر انجام می‌دهند و به شما امکان ایجاد صدها کاربر در یک دهم ثانیه را می‌دهند.

## 🎖 اطلاع

به بخش پیام‌ها خوش آمدید! این ویژگی با حمایت مجموعه [Gray](https://t.me/GrayServer) اضافه شده است. ❤️  شما می‌توانید به کانال و ربات Gray collection برای خرید سرورها به صورت ساعتی و ماهانه، با تنوع گسترده‌ای از مکان‌ها و مشخصات، همراه با IP‌های تمیز با کمترین قیمت‌ها مراجعه کنید. قبل از فعال کردن اعلان، شما باید یک ورودی(Inbound) Shadowsocks با نام "Holderbot" در داخل پنل ایجاد کنید:

```
{
  "tag": "Holderbot",
  "listen": "0.0.0.0",
  "port": 2222,
  "protocol": "shadowsocks",
  "settings": {
    "clients": [],
    "network": "tcp,udp"
  }
}
```
Then, inside the host settings of the inbound, we put our desired messages. After applying the changes, inside the Holderbot, we click on the "Change Status" option in the Notice section, and this feature becomes active. Holderbot checks users every 5 seconds and activates the messages for completed users, notifying you accordingly.

## 👤 Users

In the Users section, you receive general statistics of your panel. The number of users "all," "activated," "disabled," "on_hold," "limited," and "expired," along with the count of users who were online or offline in the last 24 hours, and whether their links have been updated or not, are provided.

Below, you'll find options where clicking on them will provide you with a list of user names in PDF format. If you click on the last two options, you'll be prompted for your desired timeframe, and based on that, you'll receive the statistics.

> [!TIP]
> If you have a specific timeframe in mind, you can enter it based on the pattern 'time min/hour/day'.

## 👨🏻‍💻 Admins

You can fully manage the panel admins in this section. You can add admins, remove admins, change admin passwords, and modify admin permissions. Just note that for removing sudo admins, it can only be done from the master server using the CLI command. APIs do not allow us access to this capability.

## 🎗 Nodes

You can also manage your servers here, reconnect, deactivate, activate, or set the consumption coefficient for your desired server. For monitoring and receiving server disconnection notifications, refer to the monitoring section on this page.

## 🗃 Templates

By creating templates, you can easily manage repetitive tasks, such as specifying volume, duration, and inbounds. In the templates section, you can create a new template or delete existing ones. To create a new template, simply click on "➕ Add new template." In the first step, enter the name without spaces, numbers, or icons. Then enter the volume (in gigabytes) and duration (in days), and finally select the inbounds. Each selected inbound marked with ➕ is included, while those marked with ➖ are not. After completing your selection, click "✅ finish" to save the template. To delete a template, simply click on it, and you'll be asked for confirmation. Once confirmed, it will be deleted.

> [!NOTE]
> You add/remove templates in this section, but you only use them in the "🚀 Create User" section.

## 🎛 Monitoring

Monitoring for your servers is enabled by default during the installation of HolderBot. You can enable/disable it from this section. You can also set the server check interval for monitoring and specify the waiting time for the next check when receiving a server disconnection notification.

## 🔍 Search

Sometimes you may not remember the username completely but want to input a few letters for the bot to find it easily and tell you. Is this what you mean? This capability is specifically designed for searches of this nature, where the bot can list the usernames similar to your input and send them to you.

> [!NOTE]
> This section is not for receiving user statistics. For that purpose, you can refer to the homepage tutorial.

## 💬 Help

A guide on solving problems, requesting assistance, reporting bugs, contacting the developer, and similar matters will be sent to you. Additionally, a file containing Holder Bot logs will be sent to you, which you can share with the developer if needed for debugging and problem-solving.

## 🖼 QR Code

You can receive its barcode by sending any link or text. This feature is not exclusive to v2ray links, and it can provide you with its barcode in code form for any received link. It's quick and simple!

> [!TIP]
> You can modify the barcode color in the "qr.py" file in the "Function" folder using line 8 (fill_color) with options like red, pink, blue, yellow.
<p align="center">
  <a target="_blank" href="https://t.me/ErfjabHolderbot">
    <img alt="Telegram Badge" src="https://img.shields.io/badge/holderbotchanel-Telegramlink?style=for-the-badge&logo=telegram&logoColor=white&color=blue&link=https%3A%2F%2Ft.me%2FErfjabHolderbot&link=https%3A%2F%2Ft.me%2FErfjabHolderbot">
  </a>
</p>

