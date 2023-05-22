---
title: "Reduce your page load time with htmx in less than an hour"
tags: ['Django', 'Javascript', 'frontend', 'programming', 'python']
date: 2022-09-26T11:49:45.812120+00:00
aliases: ["/reduce-your-page-load-time-with-htmx-in-less-than-an-hour"]
canonicalURL: "/reduce-your-page-load-time-with-htmx-in-less-than-an-hour"
summary: HTMX is a wonderful piece of technology for backend developers who don't want to write frontend code but still provide nice UX.
---
## Presentation
During DjangoCon EU 2022, a talk reminded me of [htmx](https://htmx.org/). As the authors put it:

> Htmx is a library that allows you to access modern browser features directly from HTML, rather than using javascript.
> 
> \- [htmx docs](https://htmx.org/docs/#introduction)

Since I really don't like javascript that much, this promise is very tempting to me&nbsp;😁

## Context
I'm working on a small cash register web app to help during events and reduce the risk of human error when counting products. If you're curious, you can find it [here](https://git.augendre.info/gaugendre/checkout).

This app also has a reporting section, where I'm generating graphs using matplotlib. Some graphs are heavy to produce, but they're only a portion of the full page. In the screenshot below, I've highlighted them:

{{< img src="42.png" alt="Checkout reports" >}}

Initially, the page took about 6 to 7 seconds to fully load. Before that, nothing was displayed on screen.

|                             | Before htmx | After htmx |
|-----------------------------|-------------|------------|
| [LCP](https://web.dev/lcp/) | 6 seconds   | ?          |

Here's what the template looked like:

```jinja
{% extends "common/base.html" %}
{% load static %}
{% load i18n %}
{% load purchase %}

{% block extrahead %}
    <link rel="stylesheet" href="{% static "purchase/css/reports.css" %}">
{% endblock %}

{% block content %}
    <h1>{% translate "Reports" %}</h1>
    <h2>{% translate "General" %}</h2>
    <ul>
        <li>{% translate "Total turnover:" %} {{ turnover|currency }}</li>
        <li>{% translate "Average basket:" %} {{ average_basket|currency }}</li>
    </ul>

    <h3>{% translate "By day" %}</h3>
    <h4>{% translate "Turnover" %}</h4>
    <ul>
        {% for date, turnover in turnover_by_day.items %}
            <li>{{ date }} : {{ turnover|currency }}</li>
        {% endfor %}
    </ul>
    <h4>{% translate "Average basket" %}</h4>
    <ul>
        {% for date, average in average_basket_by_day.items %}
            <li>{{ date }} : {{ average|currency }}</li>
        {% endfor %}
    </ul>

    {{ by_hour_plot|safe }}

    <h2>{% translate "Products" %}</h2>
    {% include "purchase/snippets/report_products.html" %}
    {{ products_plot|safe }}
    {{ products_sold_pie|safe }}
    {{ products_turnover_pie|safe }}

    <h2>{% translate "Turnover by payment method" %}</h2>
    {% include "purchase/snippets/report_payment_methods.html" %}

    <h2>{% translate "Baskets without payment method" %}</h2>
    {% include "purchase/snippets/report_no_payment_method.html" %}

{% endblock %}
```

## Implementation
Here's how the template looks like with htmx. I've removed the non-relevant parts for brevity.

```jinja {hl_lines="2 8 12 17-20"}
{% extends "common/base.html" %}
{% load static i18n purchase django_htmx %}
{# ... #}

{% block content %}
    {# ... #}

    {% include "purchase/snippets/htmx_plot.html" with url='purchase:by_hour_plot' %}

    <h2>{% translate "Products" %}</h2>
    {% include "purchase/snippets/report_products.html" %}
    {% include "purchase/snippets/htmx_plot.html" with url='purchase:products_plots' %}

    {# ... #}
{% endblock %}

{% block extrascript %}
    <script src="{% static 'vendor/htmx-1.8.0/htmx.min.js' %}" defer></script>
    {% django_htmx_script %}
{% endblock %}
```

```jinja
{% load static %}
<div hx-get="{% url url %}"
    hx-trigger="load"
    hx-swap="outerHTML"
>
    <img class="htmx-indicator" src="{% static 'purchase/spinner.gif' %}" alt="Spinner">
</div>
```

{{< note class="info" title="django-htmx" >}}
The Django htmx part is not mandatory. It's from [django-htmx](https://django-htmx.readthedocs.io/en/latest/index.html), by [Adam Johnson](https://adamj.eu/). It provides a nicer integration between Django and htmx. I encourage you to check out Adam's works, you'll most likely learn a thing or two.
{{< /note >}}

I moved the graph generation part from my main view to two separate views which are called after the DOM is loaded. I didn't have to do much: since I was already rendering everything server-side I only had to render a partial template instead of a complete page.

## Results

The page now renders very fast with all the text reports, and spinners are displayed while the graphs are loaded asynchronously.

It still takes 5-6 seconds for the graphs to load, but the user experience is much nicer since the LCP happens during the first second instead of having to wait for the graphs to load.

|   | Before htmx | After htmx |
|---|-------------|------------|
|LCP| 6 seconds   | 0.17s      |

So performance-wise and UX-wise, I consider it a complete win. I'd also like to point out that it only took me around 30 to 45 minutes to implement this, without prior working knowledge of the library! Another win for free software 🎉

I have a few ideas where this could be useful on projects at ITSF, especially one where we implemented a very similar logic with custom code.
