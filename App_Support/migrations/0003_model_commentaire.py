# Generated by Django 2.1 on 2021-09-08 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App_Configuration', '0003_auto_20210707_1409'),
        ('App_Support', '0002_model_reclamation_transfert'),
    ]

    operations = [
        migrations.CreateModel(
            name='Model_Commentaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentaire', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now=True)),
                ('auteur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='auteurs_comm', to='App_Configuration.Model_Personne')),
                ('reclamation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentaire_recl', to='App_Support.Model_Reclamation')),
            ],
        ),
    ]
