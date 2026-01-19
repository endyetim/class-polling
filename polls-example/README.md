# Poll Examples

Example poll file format.

**Your actual polls go in `polls/` directory (gitignored).**

## Setup

1. Copy structure:
```bash
cp -r polls-example/* polls/
```

2. Edit `polls/course-semester/week1.yaml` with your questions

3. Import:
```bash
python src/import_polls.py
```

Poll content stays private.
