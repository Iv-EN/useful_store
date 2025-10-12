from django.db import models


class BlogPost(models.Model):
    """Описывает запись в блоге."""

    title = models.CharField(max_length=100, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    preview = models.ImageField(upload_to="posts/", verbose_name="Изображение")
    created_at = models.DateTimeField(
        verbose_name="Дата создания записи", auto_now_add=True
    )
    is_published = models.BooleanField(
        verbose_name="Признак публикации", default=False
    )
    number_views = models.IntegerField(
        verbose_name="количество просмотров", default=0
    )

    def __str__(self):
        return (
            f"Запись: {self.title}, количество просмотров: {self.number_views}"
        )

    class Meta:
        verbose_name = "Запись в блоге"
        verbose_name_plural = "Записи в блоге"
