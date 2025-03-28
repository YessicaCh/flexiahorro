# Generated by Django 5.1.7 on 2025-03-27 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='savingsgoal',
            name='fixed_amount',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Monto fijo si se selecciona esa opción', max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='savingsgoal',
            name='savings_mode',
            field=models.CharField(choices=[('percentage', 'Porcentaje'), ('round_up', 'Vuelto'), ('fixed_amount', 'Monto Fijo')], default='percentage', max_length=20),
        ),
    ]
