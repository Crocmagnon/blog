import os
import re
import shutil
from pathlib import Path

from django.core.management.base import BaseCommand

from attachments.models import Attachment
from articles.models import Article


class Command(BaseCommand):
    def handle(self, *_args, **_options) -> None:
        base_folder="/app/db/posts"
        os.makedirs(base_folder, exist_ok=True)
        for article in Article.objects.all():
            self.stdout.write(f"Processing {article.title}...")
            tags = map(repr, article.tags.all().values_list("name", flat=True))
            date = article.published_at or article.created_at
            lines = [
                "---",
                f'title: "{article.title}"',
                f"tags: [{', '.join(tags)}]",
                f"date: {date.isoformat()}",
                f'aliases: ["/{article.slug}"]',
                "---",
            ]
            folder = f"{base_folder}/{article.slug}"
            os.makedirs(folder, exist_ok=True)
            attachments = set(re.findall(r"/attachments/(\d+)", article.content))
            attachments = Attachment.objects.filter(id__in=attachments)
            content = article.content.replace("\r", "")
            content = re.sub(r"!\[([^]]*)]\(/attachments/(\d+)[^)]*\)", r"![\1](\2.__SUFFIX__)", content)
            content = re.sub(r"\{:[^}]*}", "", content)
            for attachment in attachments:
                src = Path(attachment.original_file.path)
                dst = (Path(folder) / str(attachment.pk)).with_suffix(src.suffix)
                shutil.copy(src, dst)
                self.stdout.write(str(dst))
                content = content.replace(f"{attachment.pk}.__SUFFIX__", f"{attachment.pk}{src.suffix}")
            with open(f"{folder}/index.md", "w") as f:
                f.write("\n".join(lines))
                f.write("\n")
                f.write(content)
                f.write("\n")
        self.stdout.write(self.style.SUCCESS("Successfully wrote all posts."))