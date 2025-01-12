from pathlib import Path

from django.db.models.signals import post_delete, post_save
from django.core.mail import send_mail
from django.dispatch import receiver
from django.conf import settings
from blog.models import BlogPost


@receiver(post_delete, sender=BlogPost)
def delete_post_image(sender: BlogPost, instance: BlogPost, **kwargs) -> None:
    """Удаляет изображение поста при его удалении."""
    image_path = Path(instance.preview.path)
    if image_path.exists():
        image_path.unlink()


@receiver(post_save, sender=BlogPost)
def send_view_count_notification(
    sender: BlogPost, instance: BlogPost, created: bool, **kwargs
) -> None:
    """
    Отправляет уведомление при достижении количества просмотров поста 100.
    """
    if not created and instance.number_views == 100:
        send_mail(
            "Поздравляем!",
            f"Статья {instance.title} набрала 100 просмотров.",
            settings.DEFAULT_FROM_EMAIL,
            ["iv-en-auto@rambler.ru"],
        )
