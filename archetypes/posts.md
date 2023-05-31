---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: true
tags: []

# Keep them short
description: "Desc Text."
summary: "Post summary"

cover:
  image: "img url"
  relative: true
  alt: "img alt text"
  caption: "img caption"
  hidden: true  # applies only on single view

# showToc: true
# TocOpen: false
---
