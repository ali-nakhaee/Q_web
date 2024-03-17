# Generated by Django 4.2.10 on 2024-03-17 12:57

from django.db import migrations

def add_teacher_permissions(apps, schema_migration):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    
    view_quiz = Permission.objects.get(codename='view_quiz')
    add_quiz = Permission.objects.get(codename='add_quiz')
    change_quiz = Permission.objects.get(codename='change_quiz')
    delete_quiz = Permission.objects.get(codename='delete_quiz')

    teachers = Group.objects.get(name='teachers')

    teachers.permissions.add(view_quiz)
    teachers.permissions.add(add_quiz)
    teachers.permissions.add(change_quiz)
    teachers.permissions.add(delete_quiz)
    

class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_alter_user_first_name_alter_user_last_name"),
    ]

    operations = [
        migrations.RunPython(add_teacher_permissions)
    ]