# Poll Organization

## Structure

```
polls/
├── ph3130-sp2026/        # Data Analysis course, Spring 2026
│   ├── week1.yaml
│   ├── week2.yaml
│   └── ...
├── ph3120-sp2026/        # Epidemiology course, Spring 2026
│   ├── week1.yaml
│   └── ...
├── archived/             # Past semesters
│   ├── ph3130-fa2025/
│   └── ph3120-fa2025/
└── README.md
```

## Usage

**Import all polls:**
```bash
python src/import_polls.py
```

**Import specific file:**
```bash
python src/import_polls.py polls/ph3130-sp2026/week1.yaml
```

**Import specific course:**
```bash
python src/import_polls.py polls/ph3130-sp2026/*.yaml
```

## Poll File Format

```yaml
course: "PH3130 Data Analysis"
semester: "Spring 2026"
week: 1

polls:
  poll_id:
    title: "Poll Title"
    question: "Question text?"
    options:
      - "A. Option 1"
      - "B. Option 2"
```

## Naming Convention

**Folders:** `{course}-{semester}/`
- `ph3130-sp2026` = PH3130, Spring 2026
- `ph3120-fa2025` = PH3120, Fall 2025

**Files:** `week{N}.yaml`
- `week1.yaml` = Week 1 polls
- `midterm.yaml` = Midterm review polls

**Poll IDs:** Auto-generated as `{poll_id}_{course}_{week}`
- `anxiety_ph3130_1`
- `epi_definition_ph3120_1`

## Workflow

### Before Semester
1. Create folder: `polls/{course}-{semester}/`
2. Create `week1.yaml` with first week's polls

### Each Week
1. Create `week{N}.yaml` with new polls
2. Run `python src/import_polls.py`
3. Restart Streamlit app

### End of Semester
1. Move folder to `archived/`
2. Export data if needed

## Benefits

✅ Separate polls by course and semester  
✅ Easy to find and edit specific week's polls  
✅ Reuse polls across semesters (copy files)  
✅ Archive old polls without deleting  
✅ Import all or specific files as needed
