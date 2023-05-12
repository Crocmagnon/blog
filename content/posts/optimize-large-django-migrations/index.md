---
title: "Optimize large Django migrations"
tags: ['Django', 'ITSF', 'python']
date: 2022-03-31T19:50:35.048724+00:00
aliases: ["/optimize-large-django-migrations"]
---
## 📖 Backstory
Today, while working on a project at [ITSF](https://itsf.io), I needed to add a new field to an existing model in a Django project. This field had to initially be computed from other values in the same model, so I couldn't use a constant default value for all the existing objects.

## 🧒🏻 First try
So I sat down, thought about it, and here's the migration I first came up with:

```{ .python .large }
def forwards(apps, schema_editor):
    Model = apps.get_model('app', 'Model')
    db_alias = schema_editor.connection.alias
    instances = Model.objects.using(db_alias).all()
    for instance in instances:
        instance.new_field = compute_new_field(instance)
    Model.objects.using(db_alias).bulk_update(instances, ["new_field"])
```

The `compute_new_field` function takes multiple other fields into account to produce the new value, it's not just a matter of repeating the value of an existing field (which would have been simpler, using [`F` expressions](https://docs.djangoproject.com/en/4.0/ref/models/expressions/#django.db.models.F) and `queryset.update`).

I was quite happy with this migration. I thought it solved my problem in a quite elegant way and only involved two database queries. One to fetch the initial queryset and the second to save the updates in database.

## ✋🏻 Not so fast!
Thankfully, one of my colleagues brought me back to reality:

> *There are 252320 objects in this table.*
>
> \- A very smart coworker

And I just realized that's just in the staging environment! In production we have a whopping 1.7 million of these, and it's growing.

Our migrations run in an environment with limited CPU and RAM. Running this code would have loaded the whole 1.7M objects in memory which would have caused our migration process to crash and some hair scratching to find out what had happened plus the added stress of a production deploy failing. Hopefully we would have caught the issue in staging with the 250k objects but that's not a certainty.

## 😈 Optimizing the queries
Fortunately, Django comes with batteries included and provides a pagination mechanism. It's mostly advertised to facilitate paginating list views, but the [`Paginator`](https://docs.djangoproject.com/en/4.0/ref/paginator/) class can be instantiated manually.

After re-engineering, here's the updated version which will obviously make many more DB queries but will hopefully not send our RAM to a black hole 😁

```{ .python .large hl_lines="5 6 7" }
def forwards(apps, schema_editor):
    Model = apps.get_model('app', 'Model')
    db_alias = schema_editor.connection.alias
    instances = Model.objects.using(db_alias).all()
    pages = Paginator(instances, per_page=1000, orphans=400)
    for page in pages:
        instances = page.object_list
        for instance in instances:
            instance.new_field = compute_new_field(instance)
        Model.objects.using(db_alias).bulk_update(instances, ["new_field"])
```

I could spend time tweaking the page size but I know our migrations job can handle batches of 1000 objects, so I didn't put too much effort into that.

## 📝 Key takeaways

🤓 Choose your optimization metric wisely. We often want to reduce the number of DB queries, but as a matter of fact it's sometimes a good idea to *increase* it, if it means that your process actually finishes 😅

🎉 Django is awesome. Notice how little effort it took me! I only had to add three lines and reindent three other to paginate my queries and be confident that my migration will run and won't break our next deploy.
