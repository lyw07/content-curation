# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-03-27 21:14
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='extension',
            field=models.CharField(blank=True, choices=[('mp4', b'MP4 Video'), ('vtt', b'VTT Subtitle'), ('srt', b'SRT Subtitle'), ('mp3', b'MP3 Audio'), ('pdf', b'PDF Document'), ('jpg', b'JPG Image'), (
                b'jpeg', b'JPEG Image'), ('png', b'PNG Image'), ('gif', b'GIF Image'), ('json', b'JSON'), ('svg', b'SVG Image'), ('perseus', b'Perseus Exercise'), ('zip', b'HTML5 Zip'), ('epub', b'ePub Document')], max_length=40),
        ),
        migrations.AlterField(
            model_name='file',
            name='preset',
            field=models.CharField(blank=True, choices=[('high_res_video', b'High Resolution'), ('low_res_video', b'Low Resolution'), ('vector_video', b'Vectorized'), ('video_thumbnail', b'Thumbnail'), ('video_subtitle', b'Subtitle'), ('audio', b'Audio'), ('audio_thumbnail', b'Thumbnail'), ('document', b'Document'), ('epub', b'ePub Document'), (
                b'document_thumbnail', b'Thumbnail'), ('exercise', b'Exercise'), ('exercise_thumbnail', b'Thumbnail'), ('exercise_image', b'Exercise Image'), ('exercise_graphie', b'Exercise Graphie'), ('channel_thumbnail', b'Channel Thumbnail'), ('topic_thumbnail', b'Thumbnail'), ('html5_zip', b'HTML5 Zip'), ('html5_thumbnail', b'HTML5 Thumbnail')], max_length=150),
        ),
        migrations.AlterField(
            model_name='localfile',
            name='extension',
            field=models.CharField(blank=True, choices=[('mp4', b'MP4 Video'), ('vtt', b'VTT Subtitle'), ('srt', b'SRT Subtitle'), ('mp3', b'MP3 Audio'), ('pdf', b'PDF Document'), ('jpg', b'JPG Image'), (
                b'jpeg', b'JPEG Image'), ('png', b'PNG Image'), ('gif', b'GIF Image'), ('json', b'JSON'), ('svg', b'SVG Image'), ('perseus', b'Perseus Exercise'), ('zip', b'HTML5 Zip'), ('epub', b'ePub Document')], max_length=40),
        ),
    ]
