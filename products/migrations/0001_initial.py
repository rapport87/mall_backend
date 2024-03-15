# Generated by Django 4.0.10 on 2024-01-02 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.PositiveIntegerField(default=0)),
                ('sale_price', models.PositiveIntegerField(default=0)),
                ('shipping_fee', models.PositiveIntegerField(default=0)),
                ('thumbnail', models.URLField()),
                ('stock', models.PositiveIntegerField(default=0)),
                ('display_status', models.CharField(choices=[('Y', 'Y'), ('N', 'N')], default='N', max_length=1)),
                ('detailed_description', models.TextField(blank=True, null=True)),
                ('categories', models.ManyToManyField(blank=True, related_name='products', to='categories.category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('photo', models.URLField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='product',
            name='product_images',
            field=models.ManyToManyField(related_name='products', to='products.productimage'),
        ),
    ]
