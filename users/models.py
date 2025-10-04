from django.contrib.auth.models import AbstractUser
from django.db import models
import cloudinary.uploader

class User(AbstractUser):
    avatar_url = models.URLField(blank=True, null=True)
    following = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        related_name='followers',
        blank=True
    )

    def __str__(self):
        return self.username

    def set_avatar(self, image_file):
        """
        Faz upload do avatar no Cloudinary e salva a URL no campo avatar_url.
        Usa um public_id único baseado no ID do usuário para sobrescrever o avatar antigo.
        """
        if image_file:
            result = cloudinary.uploader.upload(
                image_file,
                folder="avatars",
                public_id=f"user_{self.id}",
                overwrite=True,
                resource_type="image"
            )
            self.avatar_url = result.get("secure_url")
            self.save()

    @property
    def avatar(self):
        """
        Retorna a URL do avatar, ou uma URL de avatar padrão se não existir.
        Isso facilita usar `user.avatar` diretamente nas templates.
        """
        if self.avatar_url:
            return self.avatar_url
        return "https://res.cloudinary.com/seu_cloud_name/image/upload/v1234567890/avatars/default-avatar.png"
