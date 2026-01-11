from django.db import models

# 1. KOMPANIYA MA'LUMOTLARI (Sayt egasi o'zi o'zgartira oladigan qism)
class CompanyInfo(models.Model):
    site_name = models.CharField(max_length=100, default="TravelUz", verbose_name="Sayt nomi")
    director_name = models.CharField(max_length=100, verbose_name="Direktor F.I.O")
    director_image = models.ImageField(upload_to='company/', blank=True, null=True, verbose_name="Direktor rasmi")
    
    address_uz = models.CharField(max_length=255, verbose_name="Manzil (UZ)")
    address_ru = models.CharField(max_length=255, verbose_name="Manzil (RU)", blank=True, null=True)
    
    phone = models.CharField(max_length=20, verbose_name="Telefon raqam")
    email = models.EmailField(verbose_name="Email")
    
    # Yuridik ma'lumotlar
    stir = models.CharField(max_length=20, verbose_name="STIR (INN)")
    license_number = models.CharField(max_length=50, default="Jarayonda", verbose_name="Litsenziya raqami")
    
    # Ijtimoiy tarmoqlar
    instagram = models.URLField(blank=True, null=True, verbose_name="Instagram link")
    telegram = models.URLField(blank=True, null=True, verbose_name="Telegram link")
    facebook = models.URLField(blank=True, null=True, verbose_name="Facebook link")

    def __str__(self):
        return "Kompaniya Asosiy Ma'lumotlari"

    class Meta:
        verbose_name = "Kompaniya ma'lumoti"
        verbose_name_plural = "Kompaniya ma'lumotlari"


# 2. SAYOHAT TURLARI (Asosiy mahsulot)
class Tour(models.Model):
    CATEGORY_CHOICES = [
        ('ziyorat', 'Ziyorat'),
        ('europe', 'Yevropa'),
        ('sea', 'Dengiz bo\'yi'),
        ('visa', 'Viza xizmati'),
    ]

    # Asosiy ma'lumotlar
    title_uz = models.CharField(max_length=255, verbose_name="Tur nomi (UZ)")
    title_ru = models.CharField(max_length=255, verbose_name="Tur nomi (RU)", blank=True, null=True)
    
    description_uz = models.TextField(verbose_name="Tavsif (UZ)")
    description_ru = models.TextField(verbose_name="Tavsif (RU)", blank=True, null=True)
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='ziyorat', verbose_name="Kategoriya")
    
    # Narx va Vaqt
    price = models.CharField(max_length=100, help_text="Masalan: $590 yoki 7 mln so'm", verbose_name="Narxi")
    duration_uz = models.CharField(max_length=100, help_text="Masalan: 7 kun / 6 kecha", verbose_name="Davomiyligi (UZ)")
    duration_ru = models.CharField(max_length=100, blank=True, null=True, verbose_name="Davomiyligi (RU)")
    
    # Media
    image = models.ImageField(upload_to='tours/', verbose_name="Asosiy rasm")
    
    # Qo'shimcha
    is_active = models.BooleanField(default=True, verbose_name="Saytda ko'rinsinmi?")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title_uz

    class Meta:
        verbose_name = "Sayohat"
        verbose_name_plural = "Sayohatlar"


# 3. ARIZALAR (Saytdan kelgan murojaatlar)
class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Yangi'),
        ('contacted', 'Bog\'lanildi'),
        ('finished', 'Yakunlandi'),
        ('cancelled', 'Bekor qilindi'),
    ]

    full_name = models.CharField(max_length=100, verbose_name="Ismi")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    message = models.TextField(blank=True, null=True, verbose_name="Xabar")
    
    tour = models.ForeignKey(Tour, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Qaysi tur bo'yicha")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Holati")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Kelib tushgan vaqti")

    def __str__(self):
        return f"{self.full_name} ({self.phone})"

    class Meta:
        verbose_name = "Ariza"
        verbose_name_plural = "Arizalar"