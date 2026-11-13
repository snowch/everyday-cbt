# Everyday CBT

A story-led introduction to cognitive behavioural therapy: understand recurring
patterns, choose a small change, and learn from what happens.

**Status: course planning.** The site currently presents the proposed twelve-chapter
curriculum. Lessons, narration, worksheets, and assessments are not yet available.
The course has not had a clinical review or learner pilot.

- [Course site](https://snowch.github.io/everyday-cbt/)
- [Course design and production plan](docs/course-plan.md)

## Build and preview

Python 3.10 or newer is sufficient; no third-party build dependencies are required.

```sh
python3 build.py
python3 -m http.server 8877 --directory dist
```

Open <http://localhost:8877>. The static site has no external fonts, scripts,
analytics, or form submissions.

## Source

- `course.json`: chapter titles, stories, learning goals, and proposed labs.
- `site/template.html`: responsive course overview.
- `site/style.css`: page and print styles.
- `build.py`: validates the curriculum and renders `dist/`.
- `.github/workflows/pages.yml`: builds pull requests; publishes pushes to `main`.

## GitHub Pages

Pages uses **GitHub Actions** as its build source. The workflow builds the site,
uploads `dist/`, and deploys with the official Pages actions. It also supports
manual runs. Pull requests build without deploying.

```sh
gh workflow run pages.yml
gh run list --workflow pages.yml
```

Inspired by the learning format of
[Common Ground](https://github.com/snowch/common-ground-social-psychology): stories,
visual explanations, decisions with feedback, recall, and field practice. This
repository starts with original planning and implementation; it does not copy
Common Ground's course assets.
