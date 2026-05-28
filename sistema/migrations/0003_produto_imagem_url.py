

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0002_compra'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='imagem_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
