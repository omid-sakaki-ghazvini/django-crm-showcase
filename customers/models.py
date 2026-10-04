from django.db import models
from django.utils.translation import gettext_lazy as _


# ============================================================
# CUSTOMER — مشتری
# ============================================================

class Customer(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", _("فعال")
        INACTIVE = "inactive", _("غیرفعال")
        VIP = "vip", _("ویژه")

    # اطلاعات شخصی
    first_name = models.CharField(
        max_length=100,
        verbose_name=_("نام"),
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name=_("نام خانوادگی"),
    )
    email = models.EmailField(
        verbose_name=_("ایمیل"),
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_("شماره تماس"),
    )

    # اطلاعات مکانی
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("آدرس"),
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("شهر"),
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="ایران",
        verbose_name=_("کشور"),
    )

    # اطلاعات تجاری
    company = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name=_("شرکت"),
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name=_("وضعیت"),
    )

    # متادیتا
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("یادداشت"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("تاریخ ایجاد"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("آخرین ویرایش"),
    )

    class Meta:
        verbose_name = _("مشتری")
        verbose_name_plural = _("مشتریان")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


# ============================================================
# LEAD — سرنخ (مشتری بالقوه)
# ============================================================

class Lead(models.Model):
    class Source(models.TextChoices):
        WEBSITE = "website", _("وب‌سایت")
        REFERRAL = "referral", _("معرفی")
        SOCIAL = "social", _("شبکه‌های اجتماعی")
        EMAIL = "email", _("ایمیل")
        CALL = "call", _("تماس تلفنی")
        OTHER = "other", _("سایر")

    class Status(models.TextChoices):
        NEW = "new", _("جدید")
        CONTACTED = "contacted", _("تماس گرفته شده")
        QUALIFIED = "qualified", _("واجد شرایط")
        CONVERTED = "converted", _("تبدیل شده")
        LOST = "lost", _("از دست رفته")

    # اطلاعات پایه
    first_name = models.CharField(
        max_length=100,
        verbose_name=_("نام"),
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name=_("نام خانوادگی"),
    )
    email = models.EmailField(
        verbose_name=_("ایمیل"),
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_("شماره تماس"),
    )
    company = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name=_("شرکت"),
    )

    # اطلاعات CRM
    source = models.CharField(
        max_length=20,
        choices=Source.choices,
        default=Source.OTHER,
        verbose_name=_("منبع"),
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name=_("وضعیت"),
    )

    # رابطه: هر سرنخ به یک مشتری تبدیل می‌شود (اختیاری)
    converted_customer = models.OneToOneField(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="source_lead",
        verbose_name=_("مشتری تبدیل‌شده"),
    )

    # متادیتا
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("یادداشت"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("تاریخ ایجاد"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("آخرین ویرایش"),
    )

    class Meta:
        verbose_name = _("سرنخ")
        verbose_name_plural = _("سرنخ‌ها")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["source"]),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_status_display()})"


# ============================================================
# DEAL — معامله / فرصت فروش
# ============================================================

class Deal(models.Model):
    class Stage(models.TextChoices):
        PROSPECTING = "prospecting", _("بررسی اولیه")
        PROPOSAL = "proposal", _("ارائه پیشنهاد")
        NEGOTIATION = "negotiation", _("مذاکره")
        WON = "won", _("برنده شده")
        LOST = "lost", _("از دست رفته")

    # رابطه
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="deals",
        verbose_name=_("مشتری"),
    )

    # اطلاعات معامله
    title = models.CharField(
        max_length=200,
        verbose_name=_("عنوان"),
    )
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name=_("مبلغ (ریال)"),
    )
    stage = models.CharField(
        max_length=20,
        choices=Stage.choices,
        default=Stage.PROSPECTING,
        verbose_name=_("مرحله"),
    )
    probability = models.PositiveIntegerField(
        default=0,
        verbose_name=_("احتمال موفقیت (%)"),
        help_text=_("مقدار بین ۰ تا ۱۰۰"),
    )
    expected_close_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("تاریخ پیش‌بینی بسته شدن"),
    )

    # متادیتا
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("یادداشت"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("تاریخ ایجاد"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("آخرین ویرایش"),
    )

    class Meta:
        verbose_name = _("معامله")
        verbose_name_plural = _("معاملات")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["stage"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.customer.full_name}"


# ============================================================
# TICKET — تیکت پشتیبانی
# ============================================================

class Ticket(models.Model):
    class Priority(models.TextChoices):
        LOW = "low", _("کم")
        MEDIUM = "medium", _("متوسط")
        HIGH = "high", _("بالا")
        URGENT = "urgent", _("فوری")

    class Status(models.TextChoices):
        OPEN = "open", _("باز")
        IN_PROGRESS = "in_progress", _("در حال بررسی")
        RESOLVED = "resolved", _("حل شده")
        CLOSED = "closed", _("بسته شده")

    # رابطه
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name=_("مشتری"),
    )

    # اطلاعات تیکت
    subject = models.CharField(
        max_length=200,
        verbose_name=_("موضوع"),
    )
    description = models.TextField(
        verbose_name=_("توضیحات"),
    )
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        verbose_name=_("اولویت"),
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
        verbose_name=_("وضعیت"),
    )

    # متادیتا
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("تاریخ ایجاد"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("آخرین ویرایش"),
    )
    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("تاریخ حل"),
    )

    class Meta:
        verbose_name = _("تیکت")
        verbose_name_plural = _("تیکت‌ها")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["priority"]),
        ]

    def __str__(self):
        return f"#{self.pk} - {self.subject}"


# ============================================================
# NOTE — یادداشت
# ============================================================

class Note(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="customer_notes",
        verbose_name=_("مشتری"),
        null=True,
        blank=True,
    )
    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name="lead_notes",
        verbose_name=_("سرنخ"),
        null=True,
        blank=True,
    )
    deal = models.ForeignKey(
        Deal,
        on_delete=models.CASCADE,
        related_name="deal_notes",
        verbose_name=_("معامله"),
        null=True,
        blank=True,
    )

    content = models.TextField(
        verbose_name=_("محتوا"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("تاریخ ایجاد"),
    )

    class Meta:
        verbose_name = _("یادداشت")
        verbose_name_plural = _("یادداشت‌ها")
        ordering = ["-created_at"]

    def __str__(self):
        return f"یادداشت #{self.pk}"


# ============================================================
# ACTIVITY — فعالیت (لاگ)
# ============================================================

class Activity(models.Model):
    class ActivityType(models.TextChoices):
        CALL = "call", _("تماس تلفنی")
        EMAIL = "email", _("ایمیل")
        MEETING = "meeting", _("جلسه")
        TASK = "task", _("وظیفه")
        NOTE = "note", _("یادداشت")

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="activities",
        verbose_name=_("مشتری"),
        null=True,
        blank=True,
    )
    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name="activities",
        verbose_name=_("سرنخ"),
        null=True,
        blank=True,
    )

    activity_type = models.CharField(
        max_length=20,
        choices=ActivityType.choices,
        verbose_name=_("نوع فعالیت"),
    )
    subject = models.CharField(
        max_length=200,
        verbose_name=_("موضوع"),
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("توضیحات"),
    )
    due_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("تاریخ سررسید"),
    )
    is_done = models.BooleanField(
        default=False,
        verbose_name=_("انجام شده"),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("تاریخ ایجاد"),
    )

    class Meta:
        verbose_name = _("فعالیت")
        verbose_name_plural = _("فعالیت‌ها")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_activity_type_display()}: {self.subject}"